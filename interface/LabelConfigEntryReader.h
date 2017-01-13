/*! Definition of the limit configuration entry reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <functional>
#include "HHStatAnalysis/Core/interface/ConfigReader.h"
#include "HHStatAnalysis/Core/interface/NumericPrimitives.h"
#include "LabelDescriptor.h"

namespace hh_analysis {

class LabelConfigEntryReader : public analysis::ConfigEntryReader {
public:
    LabelConfigEntryReader(LabelDescriptorCollection& _descriptors) : descriptors(&_descriptors) {}

    virtual void StartEntry(const std::string& name, const std::string& reference_name) override
    {
        ConfigEntryReader::StartEntry(name, reference_name);
        current = reference_name.size() ? descriptors->at(reference_name) : LabelDescriptor();
        current.name = name;
    }

    virtual void EndEntry() override
    {
        CheckReadParamCounts("text", 0, Condition::greater_equal);
        CheckReadParamCounts("position", 1, Condition::less_equal);
        CheckReadParamCounts("position_reference", 1, Condition::less_equal);
        CheckReadParamCounts("text_size", 1, Condition::less_equal);
        CheckReadParamCounts("line_spacing", 1, Condition::less_equal);
        CheckReadParamCounts("font", 1, Condition::less_equal);
        CheckReadParamCounts("color", 1, Condition::less_equal);
        CheckReadParamCounts("align", 1, Condition::less_equal);

        (*descriptors)[current.name] = current;
    }

    virtual void ReadParameter(const std::string& /*param_name*/, const std::string& /*param_value*/,
                               std::istringstream& /*ss*/) override
    {
        ParseEntry("text", current.text);
        ParseEntry("position", current.position);
        ParseEntry("position_reference", current.position_reference);
        ParseEntry("text_size", current.text_size);
        ParseEntry("line_spacing", current.line_spacing);
        ParseEntry("font", current.font);
        ParseEntry("color", current.color);
        ParseEntry("align", current.align);
    }

private:
    LabelDescriptor current;
    LabelDescriptorCollection* descriptors;
};

} // namespace hh_analysis
