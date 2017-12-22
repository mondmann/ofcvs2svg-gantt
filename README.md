# ofcvs2svg-gantt
Converter from OmniFocus CSV Export to Gantt Diagram (SVG)

Sometimes I want to see an overview of certain tasks in [OmniFocus](https://www.omnigroup.com/omnifocus). This script is to convert 
a CSV export of OmniFocus tasks to gantt with [python-gantt](http://xael.org/pages/python-gantt-en.html).

## Installation

    pip install git+https://github.com/mondmann/ofcvs2svg-gantt

## Usage

    usage: ofcsv2svg [-h] [--outfile OUTFILE] [--start YYYY-MM-DD]
                     [--end YYYY-MM-DD] [--notworking N]
                     infile

    Convert OmniFocus CSV export to GANTT SVG

    positional arguments:
      infile                Input file in CSV format exported from OmniFocus

    optional arguments:
      -h, --help            show this help message and exit
      --outfile OUTFILE, -o OUTFILE
                            Output filename for SVG document
      --start YYYY-MM-DD, -s YYYY-MM-DD
                            Override start date manually.
      --end YYYY-MM-DD, -e YYYY-MM-DD
                            Override end date manually.
      --notworking N, -n N  add day of week you are not working (0: monday .. 6:
                            sunday). Default is none. Use multiple times for
                            multiple days (e. g. '-n 5 -n 6' for weekends).
                            
## Development

Pull requests with bug fixes and improvements are welcome.
