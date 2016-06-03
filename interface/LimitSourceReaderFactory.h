/*! Definition of the LimitSourceReader factory.
This file is part of https://github.com/cms-hh/Plotting. */

#pragma once

#include "CombineRootFilesReader.h"
#include "CombineLogFilesReader.h"
#include "TextTableReader.h"

namespace hh_analysis {

struct LimitSourceReaderFactory {
    static std::shared_ptr<LimitSourceReader> Make(LimitSourceFormat source_format)
    {
        static const std::map<LimitSourceFormat, std::function<LimitSourceReader*()>> makers = {
            { LimitSourceFormat::CombineRootFiles, []() { return new CombineRootFilesReader(); } },
            { LimitSourceFormat::CombineLogFiles, []() { return new CombineLogFilesReader(); } },
            { LimitSourceFormat::TextTable, []() { return new TextTableReader(); } }
        };

        if(!makers.count(source_format))
            throw analysis::exception("Source format '%1%' is not supported.") %  source_format;
        return std::shared_ptr<LimitSourceReader>(makers.at(source_format)());
    }
};

} // namespace hh_analysis

