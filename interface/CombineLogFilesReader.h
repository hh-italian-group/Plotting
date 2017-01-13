/*! Definition of the combine log files reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <fstream>
#include "LimitSourceReader.h"
#include "HHStatAnalysis/Core/interface/NumericPrimitives.h"

namespace hh_analysis {

class CombineLogFilesReader : public LimitSourceReader {
private:

public:
    virtual void Read(LimitDescriptor& desc) override
    {
        static const std::string file_name_pattern = ".*\\.log";
        static const std::string number_pattern = "([0-9]*\\.[0-9]+|[0-9]+)";
        static const size_t expected_n_data_lines = 7;
        static const std::vector<std::pair<std::string, size_t>> data_line_patterns = {
            { "-- Asymptotic --", 1 },
            { boost::str(boost::format("Observed Limit: r < %1%") % number_pattern), 2 },
            { boost::str(boost::format("Expected[ ]+%1%\\%%: r < %1%") % number_pattern), 3 }
        };

        for(const auto& path : desc.source_paths) {
            desc.limit_values.StartNewRegion(desc.units);
            const auto& files = GetOrderedFileList(path, file_name_pattern, desc.mass_value_patterns);
            for(const auto& file_entry : files) {
                const std::string& file_name = file_entry.second;
                const double mass = file_entry.first;
                std::ifstream file(file_name);

                size_t n_data_lines = 0;
                while(file && n_data_lines < expected_n_data_lines) {
                    std::string line;
                    std::getline(file, line);

                    const size_t pattern_index = std::min(n_data_lines, data_line_patterns.size() - 1);
                    const auto& pattern_entry = data_line_patterns.at(pattern_index);
                    boost::regex pattern(pattern_entry.first);
                    const size_t expected_match_size = pattern_entry.second;
                    boost::smatch match;
                    if(boost::regex_search(line, match, pattern) && match.size() == expected_match_size) {
                        double limit = std::numeric_limits<double>::quiet_NaN();
                        double quantile = -1;
                        if(expected_match_size > 1)
                            limit = analysis::Parse<double, char>(match[match.size() - 1]);
                        if(expected_match_size > 2)
                            quantile = analysis::Parse<double, char>(match[match.size() - 2]) / 100;
                        if(!std::isnan(limit)) {
                            const LimitType limit_type = GetLimitType(quantile);
                            desc.limit_values.AddPoint(mass, limit, limit_type);
                        }
                        ++n_data_lines;
                    } else if(n_data_lines) {
                        break;
                    }
                }
                if(n_data_lines != expected_n_data_lines)
                    throw analysis::exception("Unsupported combine log file '%1%'.") % file_name;
            }
        }
    }
};

} // namespace hh_analysis
