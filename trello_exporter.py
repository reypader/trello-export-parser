#!/usr/bin/env python3
"""
Trello Project List Exporter

This script processes a Trello CSV export, filters cards based on specific criteria,
and exports them to a markdown file.
"""

import os
import sys
import argparse
from datetime import datetime
from csv_parser import TrelloCSVParser
from markdown_formatter import format_cards_to_markdown, save_markdown_to_file


def parse_arguments():
    """
    Parse command line arguments
    
    Returns:
        Parsed arguments object
    """
    parser = argparse.ArgumentParser(description='Export Trello cards from CSV to markdown')
    
    parser.add_argument('csv_file', help='Path to the Trello CSV export file')
    
    parser.add_argument('--output', '-o', 
                        help='Output markdown file (default: trello_export_TIMESTAMP.md)')
    
    parser.add_argument('--list-name', '-l', default='Project List',
                        help='Name of the list to filter by (default: "Project List")')
    
    parser.add_argument('--label', default='Reportable (black_dark)',
                        help='Label to filter by (default: "Reportable (black_dark)")')
    
    parser.add_argument('--include-archived', action='store_true',
                        help='Include archived cards (default: False)')
    
    parser.add_argument('--keep-csv', action='store_true',
                        help='Keep the input CSV file after processing (default: False)')
    
    return parser.parse_args()


def delete_file(file_path):
    """
    Delete a file if it exists
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        True if file was deleted, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Warning: Could not delete file {file_path}: {e}")
        return False


def main():
    """Main function to run the exporter"""
    args = parse_arguments()
    
    # Generate default output filename if not provided
    if not args.output:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.output = f"trello_export_{timestamp}.md"
    
    try:
        # Parse and filter the CSV
        parser = TrelloCSVParser(args.csv_file)
        filtered_cards = parser.filter_cards(
            list_name=args.list_name,
            label_filter=args.label,
            include_archived=args.include_archived
        )
        
        # Extract relevant information
        card_info = parser.extract_card_info(filtered_cards)
        
        if not card_info:
            print("No cards found matching the criteria.")
            return 1
        
        print(f"Found {len(card_info)} cards matching the criteria.")
        
        # Format to markdown
        markdown = format_cards_to_markdown(card_info)
        
        # Save to file
        save_markdown_to_file(markdown, args.output)
        
        print(f"Successfully exported {len(card_info)} cards to {args.output}")
        
        # Delete the input CSV file if --keep-csv is not specified
        if not args.keep_csv:
            if delete_file(args.csv_file):
                print(f"Deleted input file: {args.csv_file}")
            else:
                print(f"Note: Input file {args.csv_file} was not deleted")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
