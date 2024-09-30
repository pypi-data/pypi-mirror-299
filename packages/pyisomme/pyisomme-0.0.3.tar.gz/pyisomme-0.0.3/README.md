# pyisomme

## Installation

```
pip install pyisomme
```

## Features
- Read/write ISO-MME (compressed/uncompressed)
- Modify Channel and calculate Injury Risk Values (HIC, a3ms, DAMAGE, OLC, BrIC, NIJ, ...)
- Plot Curves and compare multiple ISO-MMEs
- Create PowerPoint Reports (Euro-NCAP, UN-R137, UN-R94)
- Display Limit bars in plots
- Compare performance of left-hand-drive vehicle with right-hand-drive vehicle
- Command line tool script for fast and easy use [pyisomme/\_\_main__.py](pyisomme/__main__.py) (list, merge, rename, plot, report, ...)

## Command Line Interface
List all commands with description
```
python -m pyisomme --help
python -m pyisomme <command> --help
```
### Examples
Merge multiple ISO-MME container
```
python -m pyisomme merge ./iso_merged.zip ./iso_1/v1.mme ./iso_2.zip ./iso_3.tar.gz
```
Resample (start=0ms / step=1ms / stop=100ms) with linear interpolation
```
python -m pyisomme merge ./iso_1/v1.mme ./iso_1/v1.mme --resample 0 0.001 0.1 
```
Plot Channel(s) for quick visualization (automatically calculates resultant head acceleration from x/y/z-channels and filters with filter-class A / 1000 Hz)
```
python -m pyisomme plot ./iso_1/v1.mme --codes 24HEAD??????ACRA --xlim 0 100 --calculate
```
Create Report (and only consider data from 0-200 ms)
```
python -m pyisomme report EuroNCAP_Frontal_MPDB report.pptx data\nhtsa\09203 --crop 0 0.2
```

## Python Examples
- [Read ISO-MME](docs/isomme_read.ipynb)
- [Write ISO-MME](docs/isomme_write.ipynb)


- [Signal deriviation/integration](docs/channel_diff_int.ipynb)
- [Add/Subtract/Multiply/Divide Signals](docs/channel_operators.ipynb)
- [Apply cfc-filter](docs/channel_filter.ipynb)


- [Plotting](docs/plotting.ipynb)

- [Report](docs/report.ipynb)

## Limitations
- Only test-info (.mme), channel-info (.chn) and channel data files (.001/.002/...) are supported. All other files (videos, photos, txt-files) will be ignored when reading and writing.
- No warning before overwriting! Be careful with merge-command and writing methods.
