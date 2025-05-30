# Trello Project List Exporter

A Python utility to process Trello CSV exports, filter cards based on specific criteria, and export them to markdown format.

## Features

- Parse Trello CSV exports
- Filter cards by list name, label, and archived status
- Extract card information (name, description, etc.)
- Export to markdown format with "Transaction Management and Middleware" as the header
- Group cards by team labels with specific ordering (TMM first, SRE second, then alphabetical)
- Automatically delete input CSV file after processing (optional)

## Requirements

- Python 3.6+
- CSV file exported from Trello with the following columns:
  - Card ID, Card Name, Card URL, Card Description, Labels, Members, Due Date, Attachment Count, 
  - Attachment Links, Checklist Item Total Count, Checklist Item Completed Count, Vote Count, 
  - Comment Count, Last Activity Date, List ID, List Name, Board ID, Board Name, Archived, 
  - Start Date, Due Complete

## Installation

1. Clone this repository:
   ```
   git clone <repository-url>
   cd trello-project-list-exporter
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the main script with your Trello CSV export file:

```
python trello_exporter.py path/to/trello_export.csv
```

### Command Line Arguments

- `csv_file`: Path to the Trello CSV export file (required)
- `--output`, `-o`: Output markdown file (default: trello_export_TIMESTAMP.md)
- `--list-name`, `-l`: Name of the list to filter by (default: "Project List")
- `--label`: Label to filter by (default: "Reportable (black_dark)")
- `--include-archived`: Include archived cards (default: False)
- `--keep-csv`: Keep the input CSV file after processing (default: False)

### Examples

Basic usage:
```
python trello_exporter.py trello_export.csv
```

Specify output file:
```
python trello_exporter.py trello_export.csv -o project_report.md
```

Filter different list and label:
```
python trello_exporter.py trello_export.csv --list-name "Done" --label "Important"
```

Include archived cards:
```
python trello_exporter.py trello_export.csv --include-archived
```

Keep the input CSV file:
```
python trello_exporter.py trello_export.csv --keep-csv
```

## How to Export CSV from Trello

1. Open your Trello board in a web browser
2. Click on "Show Menu" (three dots in the top right)
3. Click "More"
4. Select "Print and Export"
5. Choose "Export as CSV"

## Project Structure

- `trello_exporter.py`: Main script with command-line interface
- `csv_parser.py`: Module for parsing and filtering Trello CSV data
- `markdown_formatter.py`: Module for formatting card data into markdown with "Transaction Management and Middleware" as the header
- `requirements.txt`: Project dependencies
