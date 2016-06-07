/*! Definition of the base class for limit source readers.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <cmath>
#include <boost/filesystem.hpp>
#include <boost/regex.hpp>

#include "LimitDescriptor.h"

namespace hh_analysis {

class LimitSourceReader {
public:
    virtual ~LimitSourceReader() {}
    virtual void Read(LimitDescriptor& limit_descriptor) = 0;

    static LimitType GetLimitType(double quantile)
    {
        static const double delta = 0.01;
        static const std::map<LimitType, double> limit_quantiles = {
            { LimitType::observed, -1. },
            { LimitType::expected, 0.5 },
            { LimitType::expected_plus_1sigma, 0.84 },
            { LimitType::expected_minus_1sigma,  0.16 },
            { LimitType::expected_plus_2sigma, 0.975 },
            { LimitType::expected_minus_2sigma, 0.025 },
        };

        for(const auto& entry : limit_quantiles) {
            if(std::abs(entry.second - quantile) < delta)
                return entry.first;
        }

        throw analysis::exception("Unknown quantile = %1%.") % quantile;
    }

    static std::set<std::pair<double, std::string>> GetOrderedFileList(
            const std::string& input_path_name, const std::string& file_name_pattern,
            const std::vector<std::string>& mass_value_patterns)
    {
        using namespace boost::filesystem;
        std::set<std::pair<double, std::string>> files;
        const boost::regex pattern(file_name_pattern);
        const path input_path(input_path_name);
        const directory_iterator end_iter;
        for(directory_iterator file_iter(input_path); file_iter != end_iter; ++file_iter) {
            const auto& name = file_iter->path().string();
            if(is_regular_file(file_iter->path()) && boost::regex_match(name, pattern))
                files.insert(std::make_pair(GetMass(name, mass_value_patterns), name));
        }
        return files;
    }

    static double GetMass(const std::string& file_name, const std::vector<std::string>& mass_value_patterns)
    {
        for(const std::string& mass_value_pattern : mass_value_patterns) {
            const boost::regex pattern(mass_value_pattern);
            boost::smatch mass_match;
            if(!boost::regex_search(file_name, mass_match, pattern) || mass_match.size() < 2)
                continue;
            std::istringstream ss_mass(mass_match[1]);
            double mass;
            ss_mass >> mass;
            if(!ss_mass)
                throw analysis::exception("Invalid resonace mass '%1%'.") % mass_match[1];
            return mass;
        }
        throw analysis::exception("Can't extract a resonance mass from the file name '%1%'.") % file_name;
    }
};

} // namespace hh_analysis
