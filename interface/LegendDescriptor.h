/*! Definition of the plot legend descriptor.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <list>
#include <istream>
#include <ostream>
#include "HHStatAnalysis/Core/interface/PlotPrimitives.h"
#include "LimitValueCollection.h"

namespace hh_analysis {

enum class LegendType { main, auxiliary };
ENUM_NAMES(LegendType) = {
    { LegendType::main, "main" },
    { LegendType::auxiliary, "auxiliary" }
};

struct LegendDescriptor : PositionedElementDescriptor {
    std::string name;
    LegendType type;
    root_ext::Point<double, 2, true> size;
    root_ext::Point<double, 1, true> text_size;
    root_ext::Font font;
    root_ext::Color color;
    double line_width;

    LegendDescriptor()
        : type(LegendType::main), size(0.5, 0.5), text_size(0.03), font(42), color(kBlack), line_width(1) {}
};

typedef std::unordered_map<std::string, LegendDescriptor> LegendDescriptorCollection;

} // namespace hh_analysis
