/*! Definition of the text table reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <fstream>
#include <boost/algorithm/string.hpp>
#include "LimitSourceReader.h"
#include "NumericPrimitives.h"
#include "ConfigReader.h"

namespace hh_analysis {

class TextTableReader : public LimitSourceReader {
private:
    struct ColumnDescriptor {
        std::string header;
        bool is_mX;
        bool is_sf;
        bool is_limit;
        bool is_limit_unc;
        LimitType limit_type;

        ColumnDescriptor() : is_mX(false), is_limit(false), is_limit_unc(false) {}

        ColumnDescriptor(const std::string& _header)
            : header(_header)
        {

            is_mX = header == "mX";
            is_sf = header.find("BR") == 0;
            is_limit = analysis::EnumNameMap<LimitType>::GetDefault().TryParse(header, limit_type);
            is_limit_unc = false;
            if(!is_limit) {
                std::stringstream ss;
                ss << LimitType::expected << header;
                is_limit_unc = analysis::EnumNameMap<LimitType>::GetDefault().TryParse(ss.str(), limit_type);
            }
        }

        bool IsInformative() const { return is_mX || is_sf || is_limit || is_limit_unc; }

        bool ExtractValue(const std::string& str, double& value, double expected_limit_value) const
        {
            if(!IsInformative()) return false;
            if(!analysis::TryParse(str, value)) return false;
            if(is_limit_unc)
                value += expected_limit_value;
            return true;
        }
    };

public:
    virtual void Read(LimitDescriptor& desc) override
    {
        std::vector<ColumnDescriptor> column_descs;
        const bool predefined_column_descs = desc.columns.size();
        if(predefined_column_descs)
            column_descs = ParseHeaderColumns(desc.columns);

        for(const auto& path : desc.source_paths) {
            desc.limit_values.StartNewRegion(desc.units);
            std::ifstream f(path);
            if(!f.good())
                throw analysis::exception("File '%1%' not found.") % path;
            f.exceptions(std::ifstream::badbit | std::ifstream::eofbit | std::ifstream::failbit);
            size_t line_number = 0;
            bool at_lease_one_limit_extracted = false;

            try {
                if(predefined_column_descs) {
                    FindHeaderLine(f, line_number, column_descs);
                } else {
                    const std::string header_line = ReadLine(f, line_number);
                    column_descs = ParseHeaderColumns(header_line);
                    if(!column_descs.size() || !column_descs.front().is_mX)
                        throw analysis::exception("Invalid table header in file '%1%'.") % path;
                }

                while(true) {
                    const auto line = ReadLine(f, line_number);
                    const auto column_values = SplitTableLine(line, true);
                    if(column_values.size() != column_descs.size())
                        throw analysis::exception("Invalid number of columns in file '%1%' at line %2%.")
                            % path % line_number;
                    double mX = std::numeric_limits<double>::quiet_NaN();
                    double sf = 1;
                    double expected_limit_value = std::numeric_limits<double>::quiet_NaN();
                    for(size_t n = 0; n < column_descs.size(); ++n) {
                        const ColumnDescriptor& c_desc = column_descs.at(n);
                        if(!c_desc.IsInformative()) continue;
                        double value = std::numeric_limits<double>::quiet_NaN();
                        if(!c_desc.ExtractValue(column_values.at(n), value, expected_limit_value) || std::isnan(value))
                            throw analysis::exception("Unable to extract value for column '%1%' in file '%2%'"
                                                      " at line %3%.") % c_desc.header % path % line_number;
                        if(c_desc.is_mX)
                            mX = value;
                        else if(c_desc.is_sf)
                            sf *= value;
                        else {
                            value *= sf;
                            if(c_desc.is_limit && c_desc.limit_type == LimitType::expected)
                                expected_limit_value = value;
                            if(std::isnan(mX))
                                throw analysis::exception("Limit column precedes a mass column at file %1%.") % path;
                            desc.limit_values.AddPoint(mX, value, c_desc.limit_type);
                        }
                    }
                    at_lease_one_limit_extracted = true;
                }

            } catch(std::ifstream::failure&) {
                if(!f.eof())
                    throw analysis::exception("I/O error while reading file '%1%'.") % path;
            }

            if(!at_lease_one_limit_extracted)
                throw analysis::exception("Unsupported table format in file '%1%'.") % path;
        }
    }

private:
    static std::string ReadLine(std::ifstream& file, size_t& line_number)
    {
        std::string line;
        while(!line.size()) {
            std::getline(file, line);
            ++line_number;
        }
        return line;
    }

    static std::vector<std::string> SplitTableLine(const std::string& line, bool allow_duplicates)
    {
        return analysis::ConfigEntryReader::ParseOrderedParameterList(line, allow_duplicates, " \t");
    }

    static std::vector<ColumnDescriptor> ParseHeaderColumns(const std::string& header_line)
    {
        const auto columns = SplitTableLine(header_line, false);
        return ParseHeaderColumns(columns);
    }

    static std::vector<ColumnDescriptor> ParseHeaderColumns(const std::vector<std::string>& columns)
    {
        std::vector<ColumnDescriptor> column_descs;
        for(const std::string& header : columns)
            column_descs.push_back(ColumnDescriptor(header));
        return column_descs;
    }

    static void FindHeaderLine(std::ifstream& file, size_t& line_number,
                               const std::vector<ColumnDescriptor>& column_descs)
    {
        std::vector<std::string> columns;
        do {
            const std::string line = ReadLine(file, line_number);
            columns = SplitTableLine(line, true);
        } while(!columns.size() || columns.front() != column_descs.front().header);
    }
};

} // namespace hh_analysis
