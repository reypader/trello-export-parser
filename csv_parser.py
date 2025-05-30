#!/usr/bin/env python3
"""
Trello CSV Parser

This script parses a CSV export from Trello, filters cards based on specific criteria,
and prepares them for markdown formatting.
"""

import csv
import sys
import re
from typing import List, Dict, Any, Optional


class TrelloCSVParser:
    """Class to handle parsing and filtering of Trello CSV exports"""
    
    def __init__(self, csv_file_path: str):
        """
        Initialize with path to CSV file
        
        Args:
            csv_file_path: Path to the Trello CSV export file
        """
        self.csv_file_path = csv_file_path
        self.cards = []
    
    def parse_csv(self) -> List[Dict[str, Any]]:
        """
        Parse the CSV file into a list of dictionaries
        
        Returns:
            List of dictionaries, each representing a card
        """
        try:
            with open(self.csv_file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                self.cards = list(csv_reader)
            return self.cards
        except Exception as e:
            print(f"Error parsing CSV file: {e}")
            return []
    
    def filter_cards(self, list_name: str = "Project List", 
                    label_filter: str = "Reportable (black_dark)",
                    include_archived: bool = False) -> List[Dict[str, Any]]:
        """
        Filter cards based on list name, label, and archived status
        
        Args:
            list_name: Name of the list to filter by
            label_filter: Label to filter by
            include_archived: Whether to include archived cards
            
        Returns:
            Filtered list of card dictionaries
        """
        if not self.cards:
            self.parse_csv()
        
        filtered_cards = []
        
        for card in self.cards:
            # Check if card is in the specified list
            if card.get('List Name') != list_name:
                continue
            
            # Check if card is archived (if we don't want archived cards)
            if not include_archived and card.get('Archived', '').lower() == 'true':
                continue
            
            # Check if card has the specified label
            # The Labels column contains comma-separated values
            labels = card.get('Labels', '').split(',')
            labels = [label.strip() for label in labels]
            
            if label_filter in labels:
                filtered_cards.append(card)
        
        return filtered_cards
    
    def extract_team_name(self, label: str) -> str:
        """
        Extract team name from a label by removing the color in parentheses
        
        Args:
            label: Label string potentially containing color in parentheses
            
        Returns:
            Team name without color information
        """
        # Remove color information in parentheses
        return re.sub(r'\s*\([^)]*\)\s*$', '', label).strip()
    
    def get_team_label(self, labels: List[str], reportable_label: str = "Reportable (black_dark)") -> str:
        """
        Find the team label from a list of labels, excluding the reportable label
        
        Args:
            labels: List of label strings
            reportable_label: The reportable label to exclude
            
        Returns:
            Team name without color information, or "Uncategorized" if no team label found
        """
        for label in labels:
            if label != reportable_label and label.strip():
                return self.extract_team_name(label)
        
        return "Uncategorized"
    
    def extract_card_info(self, cards: List[Dict[str, Any]], 
                         reportable_label: str = "Reportable (black_dark)") -> List[Dict[str, str]]:
        """
        Extract relevant information from cards
        
        Args:
            cards: List of card dictionaries from CSV
            reportable_label: The reportable label to exclude when finding team labels
            
        Returns:
            List of dictionaries with extracted card information
        """
        extracted_info = []
        
        for card in cards:
            # Get all labels
            labels = card.get('Labels', '').split(',')
            labels = [label.strip() for label in labels if label.strip()]
            
            # Get team label
            team = self.get_team_label(labels, reportable_label)
            
            card_info = {
                'id': card.get('Card ID', ''),
                'name': card.get('Card Name', ''),
                'description': card.get('Card Description', ''),
                'url': card.get('Card URL', ''),
                'labels': labels,
                'team': team,
                'due_date': card.get('Due Date', None),
                'list_name': card.get('List Name', ''),
                'board_name': card.get('Board Name', '')
            }
            extracted_info.append(card_info)
            
        return extracted_info


def main():
    """Main function to demonstrate the usage of TrelloCSVParser"""
    if len(sys.argv) < 2:
        print("Usage: python csv_parser.py <path_to_csv_file>")
        return 1
    
    csv_file_path = sys.argv[1]
    
    try:
        parser = TrelloCSVParser(csv_file_path)
        
        # Filter cards from "Project List" with label "Reportable (black_dark)"
        filtered_cards = parser.filter_cards(
            list_name="Project List",
            label_filter="Reportable (black_dark)",
            include_archived=False
        )
        
        # Extract relevant information
        card_info = parser.extract_card_info(filtered_cards)
        
        print(f"Found {len(card_info)} cards matching the criteria:")
        for card in card_info:
            print(f"\nTeam: {card['team']}")
            print(f"Name: {card['name']}")
            print(f"Description: {card['description'][:100]}..." if len(card['description']) > 100 
                  else f"Description: {card['description']}")
        
        # Here we would format to markdown, but we'll implement that later
        print("\nReady to format these cards to markdown.")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
