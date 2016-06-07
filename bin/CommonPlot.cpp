/*! Main entry of the tool that produces a common hh analyses plot.
This file is part of https://github.com/cms-hh/Plotting. */

#include <iostream>
#include "../interface/CommonPlot.h"
#include "../interface/PlotConfigEntryReader.h"
#include "../interface/LimitConfigEntryReader.h"
#include "../interface/LimitSourceReaderFactory.h"
#include "../interface/LabelConfigEntryReader.h"
#include "../interface/LegendConfigEntryReader.h"
#include "../interface/program_main.h"

namespace {

struct Arguments {
    run::Argument<std::string> config_file{"config", "configuration file"};
    run::Argument<std::string> plot_name{"plot", "name of the plot descriptor that should be drawn"};
    run::Argument<std::string> input_path{"input", "limit resources path"};
    run::Argument<std::string> output_file{"output", "output file where to store the plot"};
};

class Program {
public:
    Program(const Arguments& _args) : args(_args) {}

    void Run()
    {
        using namespace analysis;
        using namespace hh_analysis;

        ConfigReader config_reader;

        PlotDescriptorCollection plot_descriptors;
        PlotConfigEntryReader plot_entry_reader(plot_descriptors);
        config_reader.AddEntryReader("PLOT", plot_entry_reader, false);

        LimitDescriptorCollection limit_descriptors;
        LimitConfigEntryReader limit_entry_reader(limit_descriptors);
        config_reader.AddEntryReader("LIMIT", limit_entry_reader, true);

        LabelDescriptorCollection label_descriptors;
        LabelConfigEntryReader label_entry_reader(label_descriptors);
        config_reader.AddEntryReader("LABEL", label_entry_reader, false);

        LegendDescriptorCollection legend_descriptors;
        LegendConfigEntryReader legend_entry_reader(legend_descriptors);
        config_reader.AddEntryReader("LEGEND", legend_entry_reader, false);

        config_reader.ReadConfig(args.config_file());

        if(!plot_descriptors.count(args.plot_name()))
            throw analysis::exception("Plot descriptor with name '%1%' not found.") % args.plot_name();

        const auto& p_desc = plot_descriptors.at(args.plot_name());
        const std::unordered_set<std::string> limit_names(p_desc.limits.begin(), p_desc.limits.end());
        for(auto& desc_entry : limit_descriptors) {
            if(!limit_names.count(desc_entry.first)) continue;
            auto& desc = desc_entry.second;
            AddPathPrefix(desc);
            auto reader = LimitSourceReaderFactory::Make(desc.source_format);
            reader->Read(desc);
        }

        CommonPlot common_plot(p_desc, limit_descriptors, label_descriptors, legend_descriptors);
        common_plot.Print(args.output_file());
    }

private:
    void AddPathPrefix(hh_analysis::LimitDescriptor& desc) const
    {
        for(auto& path : desc.source_paths)
            path = args.input_path() + "/" + path;
    }

private:
    Arguments args;
};

} // anonymous namespace

PROGRAM_MAIN(Program, Arguments)
