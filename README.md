# Paris Downloader Script Usage Guide

The Paris Downloader script is designed to facilitate the parallel downloading of resources specified in a CSV file. This guide explains the available command-line arguments to customize the script's behavior according to your needs.

## Prerequisites

- Python 3.6 or higher
- ChromeDriver compatible with your Chrome browser version
- Required Python packages: `pandas`, `selenium` (These dependencies should be installed in your Python environment.)

## Command-Line Arguments

The script accepts the following command-line arguments to customize its execution:

- `--driverpath`: Specifies the path to the ChromeDriver executable.
  - Default: `/Users/leolabat/Downloads/chromedriver-mac-arm64-2/chromedriver`
  - Example: `--driverpath /path/to/chromedriver`
- `--workdir`: Sets the working directory where the script will operate. This is where temporary files might be stored.
  - Default: `/Users/leolabat/Desktop/`
  - Example: `--workdir /path/to/working/directory`
- `--outputdir`: Defines the output directory path where the downloaded files will be saved.
  - Default: `/Users/leolabat/Desktop/tirage/`
  - Example: `--outputdir /path/to/output/directory`
  
  The script checks if this directory exists; if not, it will create it.
  
- `--csvpath`: The path to the CSV file that contains the data for the downloads. The CSV should have the necessary columns as expected by the Downloading_Spider class.
  - Default: `/Users/leolabat/Downloads/tirage_paris.csv`
  - Example: `--csvpath /path/to/csvfile.csv`
- `--nworkers`: Number of workers to use for parallel downloading. This defines how many parallel instances of the downloader will be run.
  - Default: `10`
  - Type: Integer
  - Example: `--nworkers 5`

## Running the Script

After adjusting the command-line arguments to fit your setup, you can run the script using a command similar to the following:

```sh
python your_script_name.py --driverpath /custom/path/to/chromedriver --workdir /custom/workdir --outputdir /custom/outputdir --csvpath /custom/path/to/csvfile --nworkers 4
```

## Important Notes

- Ensure the ChromeDriver version is compatible with your Chrome browser version.
- The script assumes the CSV file is correctly formatted and contains all the necessary information for downloads.
- Verify the output directory after running the script to ensure all files have been downloaded as expected.
- For more information or troubleshooting, please refer to the script's detailed documentation or the issue tracker on the project's repository page.
