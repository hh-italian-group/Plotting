# CMS HH plotting tools

## HH common plot tool
**hh-common-plot** is a configuration-based plotting tool that allows to superimpose several one-dimensional limits in a single plot.

### How to install

#### CMSSW-based installation
```shell
cmsrel CMSSW_7_4_7
cd CMSSW_7_4_7/src
cmsenv
git clone -o upstream git@github.com:cms-hh/Plotting.git HHStatAnalysis/Plotting
git clone -o upstream git@github.com:cms-hh/Resources.git HHStatAnalysis/Resources
scram b
```

#### Prerequisites for standalone installation
Xcode Command Line Tools (*OS X only*), CERN ROOT, Boost C++ Libraries.

#### Standalone installation
```shell
git clone -o upstream git@github.com:cms-hh/Plotting.git HHStatAnalysis/Plotting
git clone -o upstream git@github.com:cms-hh/Resources.git HHStatAnalysis/Resources
cd HHStatAnalysis
mkdir build
cd build
cmake ../Plotting
make
cd ..
```

### How to run

```shell
hh-common-plot --help  # output command line help
hh-common-plot --config configs/run1_plot.cfg --input Resources/Limits --output plots/run1_plot.pdf --plot hh_common_plot_cms # produce CMS-only Run 1 common plot
hh-common-plot --config configs/run1_plot.cfg --input Resources/Limits --output plots/run1_plot_lhc.pdf --plot hh_common_plot # produce CMS and ATLAS Run 1 common plot
```
For standalone installation run *./build/hh-common-plot*.

### Configuration description

#### Overview

Used text-based configuration format originally implemented and used within hh-italian-group framework (https://github.com/hh-italian-group/AnalysisTools/).

Configuration is represented as a list of configuration entries. Each configuration entry starts with entry header and ends with an empty line. Entry header has a following format:

```
[TYPE entry_name]
```
*OR*
```
[TYPE entry_name : reference_entry_name]
```
where *TYPE* is entry type and can be omitted for the default entry type, *entry_name* is the entry name that should be unique for a given TYPE, *reference_entry_name* the name of a reference entry of the same type that is used to initialize the entry.

Each configuration entry is a set of properties. Each property is represented by one line in the configuration file and has a following format:
```
property_name: property_value
```
Each entry type defines its own set of properties, related parsing rules and allowed property multiplicity.

Other remarks:
- spaces in entry and property names are not allowed;
- lines that starts with "#" are considered as commentary and are ignored by the configuration parser.

#### Plot entry properties
Entry type name is *PLOT*.

Name                | Description | Value format | Multiplicity
--------------------|-------------|--------------|-------------
canvas_size         | size of the canvas | x_size y_size | &#8804; 1
margins             | main pad margins | left bottom right top | &#8804; 1
x_range             | x axis range | x_min x_max | &#8804; 1
y_range             | y axis range | y_min y_max | &#8804; 1
units               | y axis units | pb &#124; fb | &#8804; 1
x_title             | x axis title | TLatex text | &#8804; 1
y_title             | y axis title | TLatex text | &#8804; 1
axis_title_size     | size of the axis titles | x_size y_size | &#8804; 1
axis_title_offset   | offset of the axis titles | x_offset y_offset | &#8804; 1
axis_label_size     | size of the axis labels | x_size y_size | &#8804; 1
axis_label_offset   | offset of the axis labels | x_offset y_offset | &#8804; 1
log_scale           | true/false flags that indicates if log scale should be used | log_x log_y | &#8804; 1
limit_line_style    | Style_t for a given limit type | limit_type style_code | &#8805; 0
limit_legend_label  | Label for the auxiliary legend for a given limit type | limit_type label_text | &#8805; 0
limit               | Name of a limit entry that should be included in the plot. Order in which limits are specified defines order of their appearance in the legend and their drawing order. Special limit entry name *NULL* corresponds to the empty entry in the legend. | limit_entry_name | &#8805; 0
label               | Name of a label entry that should be included in the plot. | label_entry_name | &#8805; 0
legend              | Name of a legend entry that should be included in the plot. | legend_entry_name | &#8805; 0

#### Limit entry properties
Entry type name is *LIMIT*. It is the default entry type.

Name                | Description | Value format | Multiplicity
--------------------|-------------|--------------|-------------
title               | text that should be used in the legend | TLatex text | &#8804; 1
source_format       | format of the input file/files | combine_root &#124; combine_log &#124; text_table | &#8804; 1
mass_value_pattern  | in case of one input file per mass point, regular expression that should be used to extract mass value from the file name | mass_regex | &#8804; 1
source_path         | relative path to the input file or directory. Each *source_path* entry corresponds to a separate TGraph. | path | &#8805; 0
units               | input units | pb &#124; fb | &#8804; 1
scale_factor        | additional scale factor that should be used to normalize input limit values. TF1-compatible numerical equation might be used. Default value is 1. If more than one *scale_factor* properties are specified, they should be defined in the same order as *source_path* entries. | tf1_formula | &#8805; 0
limit_type          | limit type that should be plotted | predicted &#124; observed &#124; expected &#124; expected+1sigma &#124; expected-1sigma &#124; expected+2sigma &#124; expected-2sigma | &#8805; 0
line_color          | color of the limit line. It can be one of the ROOT color wheel colors (e.g. kOrange+3) or a hex RGB color code (e.g. #0000FF). | color | &#8804; 1
line_width          | width of the limit line. (*line_width* > 0) | width | &#8804; 1
show_in_legend      | true/false indicator whether the limit entry should be shown in the legend or not. | true &#124; false | &#8804; 1
columns             | for the *text_table* source format, this property describes the columns content in the input table. "mX" - column with resonance mass; "BR..." - columns with additional branching ratio factors; "*limit_type*" - columns with values for the specified limit type; "+-Xsigma" - columns with limit uncertainty values that are relative to the expected value; all other columns are considered as non informative (arbitrary column description can be used). | column_1 ... column_N | &#8804; 1

#### Label entry properties
Entry type name is *LABEL*.

Name                | Description | Value format | Multiplicity
--------------------|-------------|--------------|-------------
text                | each text property corresponds to a text line of the label | TLatex text | &#8805; 0
position            | (x, y) absolute or relative (to the *position_reference* reference) position of the entry.  In case of the relative position, position coordinates are scaled to the user plot area (i.e. excluding margins). If *position_reference* is one of the angles of the plot rectangle, the coordinate system is originated in this angle with the positive x, y directions towards center of the plot. | x y | &#8804; 1
position_reference  | reference for the label position. It could be one of the angles of the plot inner rectangle (excluding margins), other label or legend entry. | inner_left_top &#124; inner_right_top &#124; inner_left_bottom &#124; inner_right_bottom &#124; label_entry_name &#124; legend_entry_name | &#8804; 1
text_size           | size of the label text | text_size | &#8804; 1
line_spacing        | spacing between the text lines in the units relative to the line width. | spacing_size | &#8804; 1
font                | text font | font_id | &#8804; 1
color               | text color (same format as *line_color* for limit entry) | color | &#8804; 1
align               | text alignment | left_bottom &#124; left_center &#124; left_top &#124; center_bottom &#124; center &#124; center_top &#124; right_bottom &#124; right_center &#124; right_top | &#8804; 1


#### Legend entry properties
Entry type name is *LEGEND*.

Name                | Description | Value format | Multiplicity
--------------------|-------------|--------------|-------------
type                | type of the legend | main &#124; auxiliary | &#8804; 1
position            | (x, y) absolute or relative position of the entry (similar definition as for label entry) | x y | &#8804; 1
size                | (x, y) size of the legend. In case if *position_reference* is specified, size is scaled to the user plot area (i.e. excluding margins). | size_x size_y | &#8804; 1
position_reference  | reference for the legend position (similar definition as for label entry) | inner_left_top &#124; inner_right_top &#124; inner_left_bottom &#124; inner_right_bottom &#124; label_entry_name &#124; legend_entry_name | &#8804; 1
text_size           | size of the legend text | text_size | &#8804; 1
font                | text font | font_id | &#8804; 1
color               | text color (same format as *line_color* for limit entry) | color | &#8804; 1
line_width          | for auxiliary legend, width of the entry lines | width | &#8804; 1
