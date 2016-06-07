/*! Class that produces a common hh analyses plot.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <TCanvas.h>
#include <TStyle.h>
#include <TAxis.h>
#include <TLegend.h>
#include <TLatex.h>
#include "PlotDescriptor.h"
#include "LimitDescriptor.h"
#include "LabelDescriptor.h"
#include "LegendDescriptor.h"
#include "TdrStyle.h"

namespace hh_analysis {

class CommonPlot {
public:
    CommonPlot(const PlotDescriptor& plot_descriptor, const LimitDescriptorCollection& limit_descriptors,
               const LabelDescriptorCollection& label_descriptors, const LegendDescriptorCollection& legend_descriptors)
        : p_desc(plot_descriptor), l_descs(limit_descriptors), label_descs(label_descriptors),
          legend_descs(legend_descriptors), canvas(new TCanvas("", "", p_desc.canvas_size.x(), p_desc.canvas_size.y())),
          left_top_origin(p_desc.margins.left(), 1 - p_desc.margins.top()),
          right_top_origin(1 - p_desc.margins.right(), 1 - p_desc.margins.top()),
          left_bottom_origin(p_desc.margins.left(), p_desc.margins.bottom()),
          right_bottom_origin(1 - p_desc.margins.right(), p_desc.margins.bottom()),
          inner_size(1 - p_desc.margins.left() - p_desc.margins.right(),
                     1 - p_desc.margins.bottom() - p_desc.margins.top())

    {
        AddPositionedElements(label_descriptors);
        AddPositionedElements(legend_descriptors);
        cms_tdr::setTDRStyle();
        main_pad = std::shared_ptr<TPad>(new TPad("", "", 0, 0, 1, 1));
        main_pad->SetLogx(p_desc.log_scale.x());
        main_pad->SetLogy(p_desc.log_scale.y());
        main_pad->SetMargin(p_desc.margins.left(), p_desc.margins.right(),
                            p_desc.margins.bottom(), p_desc.margins.top());
    }

    void Print(const std::string& output_file_name)
    {
        canvas->cd();
        main_pad->Draw();
        main_pad->cd();

        auto main_legend = CreateLegend(LegendType::main);
        auto aux_legend = CreateLegend(LegendType::auxiliary);

        std::list<std::shared_ptr<TGraph>> aux_graphs;
        if(aux_legend) {
            std::string aux_legend_name;
            FindLegendName(LegendType::auxiliary, aux_legend_name);
            const auto aux_legend_desc = legend_descs.at(aux_legend_name);
            for(const auto& style_entry : p_desc.limit_line_styles) {
                if(!p_desc.limit_legend_labels.count(style_entry.first))
                    continue;
                const std::shared_ptr<TGraph> graph(new TGraph());
                graph->SetLineColor(aux_legend_desc.color.GetColorId());
                graph->SetLineStyle(style_entry.second);
                graph->SetLineWidth(aux_legend_desc.line_width);
                const std::string label = p_desc.limit_legend_labels.at(style_entry.first);
                aux_legend->AddEntry(graph.get(), label.c_str(), "l");
                aux_graphs.push_back(graph);
            }
        }


        static const std::set<LimitType> legend_limits = { LimitType::observed, LimitType::predicted };
        std::list<std::shared_ptr<TGraph>> all_graphs;
        for(const std::string& l_desc_name : p_desc.limits) {
            if(l_desc_name == "NULL") {
                if(main_legend)
                    main_legend->AddEntry("", "", "");
                continue;
            }
            if(!l_descs.count(l_desc_name))
                throw analysis::exception("Limit descriptor with name '%1%' not found.") % l_desc_name;
            const LimitDescriptor& l_desc = l_descs.at(l_desc_name);

            for(LimitType limit_type : l_desc.limit_types) {
                const auto graphs = l_desc.limit_values.ProduceGraphs(limit_type, p_desc.units, l_desc.scale_factors);
                if(main_legend && l_desc.show_in_legend && graphs.size() && legend_limits.count(limit_type))
                    main_legend->AddEntry(graphs.front().get(), l_desc.title.c_str(), "l");
                for(auto graph : graphs) {
                    ApplyProperties(graph, l_desc, limit_type);
                    all_graphs.push_back(graph);
                }
            }
        }

        if(!all_graphs.size())
            throw analysis::exception("Plot is empty.");

        auto graph_iter = all_graphs.rbegin();
        (*graph_iter)->Draw("al");
        ApplyGlobalProperties(*graph_iter);
        ++graph_iter;
        for(; graph_iter != all_graphs.rend(); ++graph_iter)
            (*graph_iter)->Draw("l");

        if(main_legend)
            main_legend->Draw("same");
        if(aux_legend)
            aux_legend->Draw("same");

        std::list<std::shared_ptr<TLatex>> labels;
        for(const std::string& label_desc_name : p_desc.labels) {
            if(!label_descs.count(label_desc_name))
                throw analysis::exception("Label descriptor with name '%1%' not found.") % label_desc_name;
            const LabelDescriptor& label_desc = label_descs.at(label_desc_name);

            root_ext::Point<double, 2> position = GetAbsolutePosition(label_desc.name);
            for(const std::string& line : label_desc.text) {
                std::shared_ptr<TLatex> latex(new TLatex(position.x(), position.y(), line.c_str()));
                latex->SetNDC();
                latex->SetTextSize(label_desc.text_size);
                latex->SetTextFont(label_desc.font.code());
                latex->SetTextAlign(static_cast<Short_t>(label_desc.align));
                latex->Draw("same");
                labels.push_back(latex);
                position = position - root_ext::Point<double, 2>(0, (1 + label_desc.line_spacing) * latex->GetYsize());
            }
        }

        canvas->Update();
        canvas->Print(output_file_name.c_str());
    }

private:
    template<typename Collection>
    void AddPositionedElements(const Collection& descs)
    {
        for(const auto& desc_entry : descs) {
            if(positioned_elements.count(desc_entry.first))
                throw analysis::exception("Duplicated descriptor name '%1%'.") % desc_entry.first;
            positioned_elements[desc_entry.first] = desc_entry.second;
        }
    }

    void ApplyProperties(std::shared_ptr<TGraph> graph, const LimitDescriptor& l_desc, LimitType limit_type) const
    {
        graph->SetLineColor(l_desc.line_color.GetColorId());
        graph->SetLineWidth(l_desc.line_width);
        graph->SetLineStyle(p_desc.limit_line_styles.at(limit_type));
    }

    void ApplyGlobalProperties(std::shared_ptr<TGraph> graph)
    {
        graph->GetXaxis()->SetTitle(p_desc.x_title.c_str());
        graph->GetYaxis()->SetTitle(p_desc.y_title.c_str());
        graph->GetXaxis()->SetTitleSize(p_desc.axis_title_size.x());
        graph->GetYaxis()->SetTitleSize(p_desc.axis_title_size.y());
        graph->GetXaxis()->SetTitleOffset(p_desc.axis_title_offset.x());
        graph->GetYaxis()->SetTitleOffset(p_desc.axis_title_offset.y());
        graph->GetXaxis()->SetLabelSize(p_desc.axis_label_size.x());
        graph->GetYaxis()->SetLabelSize(p_desc.axis_label_size.y());
        graph->GetXaxis()->SetLabelOffset(p_desc.axis_label_offset.x());
        graph->GetYaxis()->SetLabelOffset(p_desc.axis_label_offset.y());
        graph->GetXaxis()->SetLimits(p_desc.x_range.min(), p_desc.x_range.max());
        graph->GetYaxis()->SetRangeUser(p_desc.y_range.min(), p_desc.y_range.max());
    }

    bool FindLegendName(LegendType type, std::string& name) const
    {
        for(const std::string& listed_name : p_desc.legends) {
            if(!legend_descs.count(listed_name))
                throw analysis::exception("Unable to find legend descriptor '%1%'.") % listed_name;
            if(legend_descs.at(listed_name).type == type) {
                name = listed_name;
                return true;
            }
        }
        return false;
    }

    std::shared_ptr<TLegend> CreateLegend(LegendType type)
    {
        std::string name;
        if(!FindLegendName(type, name))
            return std::shared_ptr<TLegend>();
        const LegendDescriptor& desc = legend_descs.at(name);
        const auto& position = GetAbsolutePosition(name);

        std::shared_ptr<TLegend> legend(new TLegend(position.x(), position.y(),
                                                    position.x() + desc.size.x() * inner_size.x(),
                                                    position.y() + desc.size.y() * inner_size.y()));
        legend->SetTextSize(desc.text_size);
        legend->SetTextFont(desc.font.code());
        legend->SetTextColor(desc.color.GetColorId());
        legend->SetFillStyle(0);
        legend->SetBorderSize(0);
        return legend;
    }

    root_ext::Point<double, 2> GetAbsolutePosition(const std::string& name)
    {
        std::set<std::string> previous_names;
        return GetAbsolutePosition(name, previous_names);
    }

    root_ext::Point<double, 2> GetAbsolutePosition(const std::string& name, std::set<std::string>& previous_names) const
    {
        if(!positioned_elements.count(name))
            throw analysis::exception("Element with name '%1%' not found.") % name;
        if(previous_names.count(name))
            throw analysis::exception("A loop is found in the elemnt position definition.");
        const PositionedElementDescriptor& desc = positioned_elements.at(name);
        if(!desc.position_reference.size())
            return desc.position;
        if(desc.position_reference == "inner_left_top")
            return left_top_origin + desc.position * inner_size.flip_y();
        if(desc.position_reference == "inner_right_top")
            return right_top_origin - desc.position * inner_size;
        if(desc.position_reference == "inner_left_bottom")
            return left_bottom_origin + desc.position * inner_size;
        if(desc.position_reference == "inner_right_bottom")
            return right_bottom_origin + desc.position * inner_size.flip_x();
        if(positioned_elements.count(desc.position_reference)) {
            previous_names.insert(name);
            const auto& ref_position = GetAbsolutePosition(desc.position_reference, previous_names);
            return ref_position + desc.position * inner_size;
        }
        throw analysis::exception("Unknown position reference '%1%'.") % desc.position_reference;
    }

private:
    PlotDescriptor p_desc;
    LimitDescriptorCollection l_descs;
    LabelDescriptorCollection label_descs;
    LegendDescriptorCollection legend_descs;
    PositionedElementDescriptorCollection positioned_elements;
    std::shared_ptr<TCanvas> canvas;
    std::shared_ptr<TPad> main_pad;
    root_ext::Point<double, 2> left_top_origin, right_top_origin, left_bottom_origin, right_bottom_origin, inner_size;
};

} // namespace hh_analysis
