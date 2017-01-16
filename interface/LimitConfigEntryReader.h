/*! Definition of the limit configuration entry reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <functional>
#include "HHStatAnalysis/Core/interface/ConfigReader.h"
#include "HHStatAnalysis/Core/interface/NumericPrimitives.h"
#include "LimitDescriptor.h"

namespace hh_analysis {

class LimitConfigEntryReader : public analysis::ConfigEntryReader {
public:
    LimitConfigEntryReader(LimitDescriptorCollection& _descriptors) : descriptors(&_descriptors) {}

    virtual void StartEntry(const std::string& name, const std::string& reference_name) override
    {
        ConfigEntryReader::StartEntry(name, reference_name);
        current = reference_name.size() ? descriptors->at(reference_name) : LimitDescriptor();
        current.name = name;
    }

    virtual void EndEntry() override
    {
        CheckReadParamCounts("title", 1, Condition::less_equal);
        CheckReadParamCounts("source_format", 1, Condition::less_equal);
        CheckReadParamCounts("mass_value_pattern", 0, Condition::greater_equal);
        CheckReadParamCounts("source_path", 0, Condition::greater_equal);
        CheckReadParamCounts("units", 1, Condition::less_equal);
        CheckReadParamCounts("scale_factor", 0, Condition::greater_equal);
        CheckReadParamCounts("limit_type", 0, Condition::greater_equal);
        CheckReadParamCounts("line_color", 1, Condition::less_equal);
        CheckReadParamCounts("line_width", 1, Condition::less_equal);
        CheckReadParamCounts("show_in_legend", 1, Condition::less_equal);
        CheckReadParamCounts("columns", 1, Condition::less_equal);

        (*descriptors)[current.name] = current;
    }

    virtual void ReadParameter(const std::string& /*param_name*/, const std::string& /*param_value*/,
                               std::istringstream& /*ss*/) override
    {
        ParseEntry("title", current.title);
        ParseEntry("source_format", current.source_format);
        ParseEntry("mass_value_pattern", current.mass_value_patterns);
        ParseEntry("source_path", current.source_paths);
        ParseEntry("units", current.units);
        ParseEntry<std::vector<double>, analysis::NumericalExpression>("scale_factor", current.scale_factors,
                                                          [](double s) { return s > 0; });
        ParseEntry("limit_type", current.limit_types);
        ParseEntry("line_color", current.line_color);
        ParseEntry("line_width", current.line_width, [](double w) { return w > 0; });
        ParseEntry("show_in_legend", current.show_in_legend);
        ParseEntryList("columns", current.columns);
    }

private:
    LimitDescriptor current;
    LimitDescriptorCollection* descriptors;
};

} // namespace hh_analysis
