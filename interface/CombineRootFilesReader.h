/*! Definition of the combine root files reader.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include <cmath>
#include <TTree.h>
#include "RootExt.h"
#include "LimitSourceReader.h"

namespace hh_analysis {

class CombineRootFilesReader : public LimitSourceReader {
private:

public:
    virtual void Read(LimitDescriptor& desc) override
    {
        static const std::string file_name_pattern = ".*\\.root";
        for(const auto& path : desc.source_paths) {
            desc.limit_values.StartNewRegion(desc.units);
            const auto& files = GetOrderedFileList(path, file_name_pattern, desc.mass_value_patterns);
            for(const auto& file_entry : files) {
                const std::string& file_name = file_entry.second;
                const double mass = file_entry.first;
                auto file = root_ext::OpenRootFile(file_name);
                std::shared_ptr<TTree> tree(root_ext::ReadObject<TTree>(*file, "limit"));
                double limit;
                float quantileExpected;
                tree->SetBranchAddress("limit", &limit);
                tree->SetBranchAddress("quantileExpected", &quantileExpected);
                for(Long64_t n = 0; n < tree->GetEntries(); ++n) {
                    tree->GetEntry(n);
                    const LimitType limit_type = GetLimitType(quantileExpected);
                    desc.limit_values.AddPoint(mass, limit, limit_type);
                }
            }
        }
    }
};

} // namespace hh_analysis
