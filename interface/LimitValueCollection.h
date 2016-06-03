/*! Definition of classes related to the limits definition.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <set>
#include <map>
#include <list>
#include <memory>
#include <TGraph.h>
#include "EnumNameMap.h"
#include "PlotPrimitives.h"

namespace hh_analysis {

ENUM_OSTREAM_OPERATOR()

enum class LimitSourceFormat { CombineRootFiles, CombineLogFiles, HepDataTxt, TextTable };
ENUM_NAMES(LimitSourceFormat) = {
    { LimitSourceFormat::CombineRootFiles, "combine_root" },
    { LimitSourceFormat::CombineLogFiles, "combine_log" },
    { LimitSourceFormat::TextTable, "text_table" }
};

enum class CrossSectionUnits { pb, fb };
ENUM_NAMES(CrossSectionUnits) = {
    { CrossSectionUnits::pb, "pb" },
    { CrossSectionUnits::fb, "fb" }
};

enum class LimitType { predicted, observed, expected, expected_plus_1sigma, expected_minus_1sigma,
                       expected_plus_2sigma, expected_minus_2sigma };
ENUM_NAMES(LimitType) = {
    { LimitType::predicted, "predicted" },
    { LimitType::observed, "observed" },
    { LimitType::expected, "expected" },
    { LimitType::expected_plus_1sigma, "expected+1sigma" },
    { LimitType::expected_minus_1sigma, "expected-1sigma" },
    { LimitType::expected_plus_2sigma, "expected+2sigma" },
    { LimitType::expected_minus_2sigma, "expected-2sigma" }
};

struct LimitValueCollection {
private:
    static double GetUnitsConversionFactor(CrossSectionUnits original_units, CrossSectionUnits new_units)
    {
        static const std::map<CrossSectionUnits, double> units_factors = {
            { CrossSectionUnits::pb, 1. },
            { CrossSectionUnits::fb, 1e-3 }
        };
        return units_factors.at(original_units) / units_factors.at(new_units);
    }

    struct Point {
        double resonance_mass;
        double cross_section_limit;
        bool operator<(const Point& other) const { return resonance_mass < other.resonance_mass; }
        Point() : resonance_mass(0.), cross_section_limit(0.) {}
        Point(double _resonance_mass, double _cross_section_limit)
            : resonance_mass(_resonance_mass), cross_section_limit(_cross_section_limit) {}
    };

    typedef std::set<Point> Sequence;
    typedef std::map<LimitType, Sequence> SequenceMap;

    struct Region {
        CrossSectionUnits units;
        SequenceMap sequences;

        Region() : units(CrossSectionUnits::pb) {}
        Region(CrossSectionUnits _units) : units(_units) {}
    };

public:
    void StartNewRegion(CrossSectionUnits units)
    {
        regions.push_back(Region(units));
    }

    void AddPoint(double resonance_mass, double cross_section_limit, LimitType limit_type)
    {
        AddPoint(Point(resonance_mass, cross_section_limit), limit_type);
    }

    void AddPoint(const Point& point, LimitType limit_type)
    {
        if(regions.rbegin() == regions.rend())
            throw analysis::exception("No active sequence.");
        auto& sequence = regions.rbegin()->sequences[limit_type];
        if(sequence.count(point))
            throw analysis::exception("Duplicated limit point for resonant mass = %1% GeV.") % point.resonance_mass;
        sequence.insert(point);
    }

    bool HasAllLimitTypeSequences(LimitType limit_type) const
    {
        for(const Region& region : regions) {
            if(!region.sequences.count(limit_type))
                return false;
        }
        return true;
    }

    std::list<std::shared_ptr<TGraph>> ProduceGraphs(LimitType limit_type, CrossSectionUnits graph_units,
                                                     const std::vector<double>& additional_scale_factor) const
    {
        if(!HasAllLimitTypeSequences(limit_type))
            throw analysis::exception("Information about %1% limits is not available.") % limit_type;

        std::list<std::shared_ptr<TGraph>> graphs;
        size_t n = 0;
        double aux_sf = 1.;
        for(const Region& region : regions) {
            std::vector<double> x, y;
            if(n < additional_scale_factor.size())
                aux_sf = additional_scale_factor.at(n);
            const double sf = GetUnitsConversionFactor(region.units, graph_units) * aux_sf;
            for(const Point& point : region.sequences.at(limit_type)) {
                x.push_back(point.resonance_mass);
                y.push_back(point.cross_section_limit * sf);
            }
            graphs.push_back(std::shared_ptr<TGraph>(new TGraph(x.size(), x.data(), y.data())));
            ++n;
        }
        return graphs;
    }

private:
    std::list<Region> regions;
};

struct PositionedElementDescriptor {
    root_ext::Point<double, 2> position;
    std::string position_reference;

    PositionedElementDescriptor() : position(0.5, 0.5) {}
    virtual ~PositionedElementDescriptor() {}
};

typedef std::unordered_map<std::string, PositionedElementDescriptor> PositionedElementDescriptorCollection;

} // namespace hh_analysis
