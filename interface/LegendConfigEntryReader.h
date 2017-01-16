/*! Definition of the legend configuration entry reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <functional>
#include "HHStatAnalysis/Core/interface/ConfigReader.h"
#include "HHStatAnalysis/Core/interface/NumericPrimitives.h"
#include "LegendDescriptor.h"

namespace hh_analysis {

class LegendConfigEntryReader : public analysis::ConfigEntryReader {
public:
    LegendConfigEntryReader(LegendDescriptorCollection& _descriptors) : descriptors(&_descriptors) {}

    virtual void StartEntry(const std::string& name, const std::string& reference_name) override
    {
        ConfigEntryReader::StartEntry(name, reference_name);
        current = reference_name.size() ? descriptors->at(reference_name) : LegendDescriptor();
        current.name = name;
    }

    virtual void EndEntry() override
    {
        CheckReadParamCounts("type", 1, Condition::less_equal);
        CheckReadParamCounts("position", 1, Condition::less_equal);
        CheckReadParamCounts("size", 1, Condition::less_equal);
        CheckReadParamCounts("position_reference", 1, Condition::less_equal);
        CheckReadParamCounts("text_size", 1, Condition::less_equal);
        CheckReadParamCounts("font", 1, Condition::less_equal);
        CheckReadParamCounts("color", 1, Condition::less_equal);
        CheckReadParamCounts("line_width", 1, Condition::less_equal);

        (*descriptors)[current.name] = current;
    }

    virtual void ReadParameter(const std::string& /*param_name*/, const std::string& /*param_value*/,
                               std::istringstream& /*ss*/) override
    {
        ParseEntry("type", current.type);
        ParseEntry("position", current.position);
        ParseEntry("size", current.size);
        ParseEntry("position_reference", current.position_reference);
        ParseEntry("text_size", current.text_size);
        ParseEntry("font", current.font);
        ParseEntry("color", current.color);
        ParseEntry("line_width", current.line_width);
    }

private:
    LegendDescriptor current;
    LegendDescriptorCollection* descriptors;
};

} // namespace hh_analysis
