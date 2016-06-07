/*! Definition of the limit descriptor.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <list>
#include <istream>
#include <ostream>
#include "PlotPrimitives.h"
#include "LimitValueCollection.h"

namespace hh_analysis {

struct LimitDescriptor {
    std::string name;
    std::string title;

    LimitSourceFormat source_format;
    std::vector<std::string> mass_value_patterns;
    std::vector<std::string> source_paths;
    CrossSectionUnits units;
    std::vector<double> scale_factors;
    std::set<LimitType> limit_types;
    root_ext::Color line_color;
    double line_width;
    bool show_in_legend;
    std::vector<std::string> columns;

    LimitValueCollection limit_values;

    LimitDescriptor()
        : source_format(LimitSourceFormat::CombineRootFiles), units(CrossSectionUnits::pb), line_width(1),
          show_in_legend(true) {}
};

typedef std::unordered_map<std::string, LimitDescriptor> LimitDescriptorCollection;

} // namespace hh_analysis
