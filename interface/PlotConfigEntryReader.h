/*! Definition of the plot configuration entry reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include "ConfigReader.h"
#include "PlotDescriptor.h"

namespace hh_analysis {

class PlotConfigEntryReader : public analysis::ConfigEntryReader {
public:
    PlotConfigEntryReader(PlotDescriptorCollection& _descriptors) : descriptors(&_descriptors) {}

    virtual void StartEntry(const std::string& name, const std::string& reference_name) override
    {
        ConfigEntryReader::StartEntry(name, reference_name);
        current = reference_name.size() ? descriptors->at(reference_name) : PlotDescriptor();
        current.name = name;
    }

    virtual void EndEntry() override
    {
        CheckReadParamCounts("canvas_size", 1, Condition::less_equal);
        CheckReadParamCounts("margins", 1, Condition::less_equal);
        CheckReadParamCounts("x_range", 1, Condition::less_equal);
        CheckReadParamCounts("y_range", 1, Condition::less_equal);
        CheckReadParamCounts("units", 1, Condition::less_equal);
        CheckReadParamCounts("x_title", 1, Condition::less_equal);
        CheckReadParamCounts("y_title", 1, Condition::less_equal);
        CheckReadParamCounts("axis_title_size", 1, Condition::less_equal);
        CheckReadParamCounts("axis_title_offset", 1, Condition::less_equal);
        CheckReadParamCounts("axis_label_size", 1, Condition::less_equal);
        CheckReadParamCounts("axis_label_offset", 1, Condition::less_equal);
        CheckReadParamCounts("log_scale", 1, Condition::less_equal);

        (*descriptors)[current.name] = current;
    }

    virtual void ReadParameter(const std::string& /*param_name*/, const std::string& /*param_value*/,
                               std::istringstream& /*ss*/) override
    {
        ParseEntry("canvas_size", current.canvas_size);
        ParseEntry("margins", current.margins);
        ParseEntry("x_range", current.x_range);
        ParseEntry("y_range", current.y_range);
        ParseEntry("units", current.units);
        ParseEntry("x_title", current.x_title);
        ParseEntry("y_title", current.y_title);
        ParseEntry("axis_title_size", current.axis_title_size);
        ParseEntry("axis_title_offset", current.axis_title_offset);
        ParseEntry("axis_label_size", current.axis_label_size);
        ParseEntry("axis_label_offset", current.axis_label_offset);
        ParseEntry("log_scale", current.log_scale);
        ParseEntry("limit_line_style", current.limit_line_styles, [](Style_t s) { return s >= 1 && s <= 10; });
        ParseEntry("limit_legend_label", current.limit_legend_labels);
        ParseEntry("limit", current.limits);
        ParseEntry("label", current.labels);
        ParseEntry("legend", current.legends);
    }

private:
    PlotDescriptor current;
    PlotDescriptorCollection* descriptors;
};

} // namespace hh_analysis
