/*! Definition of the text label descriptor.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <list>
#include <istream>
#include <ostream>
#include "HHStatAnalysis/Core/interface/PlotPrimitives.h"
#include "LimitValueCollection.h"

namespace hh_analysis {

struct LabelDescriptor : PositionedElementDescriptor {
    std::string name;
    std::vector<std::string> text;
    root_ext::Point<double, 1, true> text_size, line_spacing;
    root_ext::Font font;
    root_ext::Color color;
    root_ext::TextAlign align;

    LabelDescriptor()
        : text_size(1), line_spacing(0.1), font(42), color(kBlack),align(root_ext::TextAlign::LeftBottom) {}
};

typedef std::unordered_map<std::string, LabelDescriptor> LabelDescriptorCollection;

} // namespace hh_analysis
