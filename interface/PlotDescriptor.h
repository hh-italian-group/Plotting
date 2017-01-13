/*! Definition of the plot descriptor.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <list>
#include <istream>
#include <ostream>

#include "LimitValueCollection.h"
#include "HHStatAnalysis/Core/interface/PlotPrimitives.h"

namespace hh_analysis {

struct PlotDescriptor {
    std::string name;
    root_ext::Point<double, 2, true> canvas_size;
    root_ext::MarginBox<double> margins;
    analysis::Range<double> x_range, y_range;
    CrossSectionUnits units;
    std::string x_title, y_title;
    root_ext::Point<double, 2, true> axis_title_size;
    root_ext::Point<double, 2> axis_title_offset;
    root_ext::Point<double, 2, true> axis_label_size;
    root_ext::Point<double, 2> axis_label_offset;
    root_ext::Point<bool, 2> log_scale;
    std::map<LimitType, Style_t> limit_line_styles;
    std::map<LimitType, std::string> limit_legend_labels;
    std::vector<std::string> limits;
    std::set<std::string> labels;
    std::set<std::string> legends;

    PlotDescriptor()
        : canvas_size(600, 600), axis_title_size(0.04, 0.04), axis_title_offset(1, 1), axis_label_size(0.04, 0.04),
          axis_label_offset(0.005, 0.005) {}
};

typedef std::unordered_map<std::string, PlotDescriptor> PlotDescriptorCollection;

} // namespace hh_analysis
