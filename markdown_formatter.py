#!/usr/bin/env python3
"""
Markdown Formatter for Trello Cards

This script takes filtered Trello card data and formats it into a markdown document.
"""

import os
import sys
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from collections import defaultdict


def replace_emoji_strings(text: str) -> str:
    """
    Replace specific emoji strings with their text equivalents
    
    Args:
        text: The text to process
        
    Returns:
        Text with emoji strings replaced
    """
    replacements = {
        ":question:": "(needs clarification)",
        ":warning:": "(important note)"
    }
    
    for emoji, replacement in replacements.items():
        text = text.replace(emoji, replacement)
    
    return text


def format_card_as_markdown(card: Dict[str, Any]) -> str:
    """
    Format a single card as markdown
    
    Args:
        card: Dictionary containing card information
        
    Returns:
        String with markdown formatted card
    """
    # Start with the card name as a header (now 3rd level since team is 2nd level)
    card_name = replace_emoji_strings(card['name'])
    markdown = f"### {card_name}\n\n"
    
    # Add the card description with emoji strings replaced
    if card['description']:
        description = replace_emoji_strings(card['description'])
        markdown += f"{description}\n\n"
    else:
        markdown += "*No description provided*\n\n"
    
    # Add an empty line instead of horizontal rule
    markdown += "\n"
    
    return markdown


def group_cards_by_team(cards: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group cards by team
    
    Args:
        cards: List of card dictionaries
        
    Returns:
        Dictionary with team names as keys and lists of cards as values
    """
    teams = defaultdict(list)
    
    for card in cards:
        team = card.get('team', 'Uncategorized')
        teams[team].append(card)
    
    # Convert to regular dict
    return dict(teams)


def get_ordered_teams(teams: Dict[str, List[Dict[str, Any]]]) -> List[str]:
    """
    Get team names in the desired order: TMM first, SRE second, then the rest alphabetically
    
    Args:
        teams: Dictionary with team names as keys and lists of cards as values
        
    Returns:
        List of team names in the desired order
    """
    ordered_teams = []
    
    # Add TMM first if it exists
    if "TMM" in teams:
        ordered_teams.append("TMM")
    
    # Add SRE second if it exists
    if "SRE" in teams:
        ordered_teams.append("SRE")
    
    # Add the rest of the teams alphabetically
    remaining_teams = sorted([team for team in teams.keys() if team not in ["TMM", "SRE"]])
    ordered_teams.extend(remaining_teams)
    
    return ordered_teams


def format_cards_to_markdown(cards: List[Dict[str, Any]], 
                           title: str = "Transaction Management and Middleware",
                           include_metadata: bool = True) -> str:
    """
    Format multiple cards into a complete markdown document, grouped by team
    
    Args:
        cards: List of card dictionaries
        title: Title for the markdown document (default now set to "Transaction Management and Middleware")
        include_metadata: Whether to include metadata about the export
        
    Returns:
        Complete markdown document as a string
    """
    if not cards:
        return "# Transaction Management and Middleware\n\n*No cards found matching the criteria.*"
    
    # Start with the fixed title
    markdown = "# Transaction Management and Middleware\n\n"
    
    # Add metadata if requested
    if include_metadata:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        markdown += f"*Generated on: {current_time}*\n\n"
        # Add empty line instead of horizontal rule
        markdown += "\n"
    
    # Group cards by team
    teams = group_cards_by_team(cards)
    
    # Get teams in the desired order
    ordered_team_names = get_ordered_teams(teams)
    
    # Add each team section in the specified order
    for team in ordered_team_names:
        team_cards = teams[team]
        
        # Add team name as second-level heading
        markdown += f"## {team}\n\n"
        
        # Add each card in this team
        for card in team_cards:
            markdown += format_card_as_markdown(card)
    
    return markdown


def save_markdown_to_file(markdown: str, output_file: str) -> None:
    """
    Save markdown content to a file
    
    Args:
        markdown: Markdown content to save
        output_file: Path to the output file
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    print(f"Markdown saved to: {output_file}")


def main():
    """
    Main function to demonstrate usage (not typically called directly)
    """
    print("This module is typically imported, not run directly.")
    print("Example usage:")
    print("  from csv_parser import TrelloCSVParser")
    print("  from markdown_formatter import format_cards_to_markdown, save_markdown_to_file")
    print("")
    print("  parser = TrelloCSVParser('trello_export.csv')")
    print("  filtered_cards = parser.filter_cards()")
    print("  card_info = parser.extract_card_info(filtered_cards)")
    print("  markdown = format_cards_to_markdown(card_info)")
    print("  save_markdown_to_file(markdown, 'output.md')")


if __name__ == "__main__":
    main()
