#!/usr/bin/env python3
"""
Database to JSON Extractor

This script extracts data from a SQL dump file and converts each table
to a separate JSON file. It parses INSERT statements and converts them
to structured JSON data.

Usage:
    python extract_db_to_json.py <sql_file> [output_directory]
"""

import re
import json
import os
import sys
from typing import Dict, List, Any, Tuple
from datetime import datetime
import argparse


class SQLExtractor:
    def __init__(self, sql_file_path: str, output_dir: str = "extracted_data"):
        self.sql_file_path = sql_file_path
        self.output_dir = output_dir
        self.tables_data = {}
        
    def create_output_directory(self):
        """Create output directory if it doesn't exist"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")
    
    def parse_sql_file(self):
        """Parse the SQL file and extract table data"""
        print(f"Reading SQL file: {self.sql_file_path}")
        
        with open(self.sql_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find all table sections
        table_pattern = r'-- (\w+) \((\d+) rows\)\n-- ============================================\n(.*?)(?=\n-- \w+ \(|\Z)'
        matches = re.findall(table_pattern, content, re.DOTALL)
        
        print(f"Found {len(matches)} tables to process")
        
        for table_name, row_count, table_content in matches:
            print(f"Processing table: {table_name} ({row_count} rows)")
            self.parse_table_data(table_name, table_content)
    
    def parse_table_data(self, table_name: str, table_content: str):
        """Parse individual table data from SQL content"""
        # Find all INSERT statements for this table
        insert_pattern = rf'INSERT INTO {table_name} \((.*?)\) VALUES \((.*?)\);'
        insert_matches = re.findall(insert_pattern, table_content, re.DOTALL)
        
        if not insert_matches:
            print(f"  No INSERT statements found for {table_name}")
            return
        
        # Get column names from first INSERT statement
        column_names = [col.strip() for col in insert_matches[0][0].split(',')]
        
        # Parse all rows
        rows = []
        for _, values_str in insert_matches:
            values = self.parse_values(values_str)
            if len(values) == len(column_names):
                row_dict = dict(zip(column_names, values))
                rows.append(row_dict)
            else:
                print(f"  Warning: Row has {len(values)} values but {len(column_names)} columns")
        
        self.tables_data[table_name] = {
            'columns': column_names,
            'rows': rows,
            'row_count': len(rows)
        }
        
        print(f"  Extracted {len(rows)} rows for {table_name}")
    
    def parse_values(self, values_str: str) -> List[Any]:
        """Parse VALUES clause and return list of values"""
        values = []
        current_value = ""
        in_quotes = False
        quote_char = None
        paren_count = 0
        
        i = 0
        while i < len(values_str):
            char = values_str[i]
            
            if char in ("'", '"') and not in_quotes:
                in_quotes = True
                quote_char = char
                current_value += char
            elif char == quote_char and in_quotes:
                # Check if it's escaped
                if i > 0 and values_str[i-1] == '\\':
                    current_value += char
                else:
                    in_quotes = False
                    quote_char = None
                    current_value += char
            elif char == '(' and not in_quotes:
                paren_count += 1
                current_value += char
            elif char == ')' and not in_quotes:
                paren_count -= 1
                current_value += char
            elif char == ',' and not in_quotes and paren_count == 0:
                # End of value
                values.append(self.clean_value(current_value.strip()))
                current_value = ""
            else:
                current_value += char
            
            i += 1
        
        # Add the last value
        if current_value.strip():
            values.append(self.clean_value(current_value.strip()))
        
        return values
    
    def clean_value(self, value: str) -> Any:
        """Clean and convert a value to appropriate Python type"""
        value = value.strip()
        
        # Handle NULL
        if value.upper() == 'NULL':
            return None
        
        # Handle boolean values
        if value.upper() in ('TRUE', 'FALSE'):
            return value.upper() == 'TRUE'
        
        # Handle quoted strings
        if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
            # Remove quotes and handle escaped characters
            unquoted = value[1:-1]
            # Simple unescaping for common cases
            unquoted = unquoted.replace("''", "'")  # SQL escaped single quotes
            unquoted = unquoted.replace('\\"', '"')  # Escaped double quotes
            unquoted = unquoted.replace('\\n', '\n')  # Newlines
            unquoted = unquoted.replace('\\t', '\t')  # Tabs
            return unquoted
        
        # Handle JSON arrays/objects (like '[]', '{}')
        if value.startswith('[') and value.endswith(']'):
            try:
                return json.loads(value)
            except:
                return value
        if value.startswith('{') and value.endswith('}'):
            try:
                return json.loads(value)
            except:
                return value
        
        # Try to convert to number
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Return as string if nothing else matches
        return value
    
    def save_tables_to_json(self):
        """Save all tables to individual JSON files"""
        print(f"\nSaving tables to JSON files in: {self.output_dir}")
        
        for table_name, table_data in self.tables_data.items():
            output_file = os.path.join(self.output_dir, f"{table_name}.json")
            
            # Create a structured JSON with metadata
            json_data = {
                "table_name": table_name,
                "columns": table_data["columns"],
                "row_count": table_data["row_count"],
                "extracted_at": datetime.now().isoformat(),
                "data": table_data["rows"]
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"  Saved {table_name}.json ({table_data['row_count']} rows)")
    
    def generate_summary(self):
        """Generate a summary file with all table information"""
        summary_file = os.path.join(self.output_dir, "extraction_summary.json")
        
        summary = {
            "extraction_info": {
                "source_file": self.sql_file_path,
                "extracted_at": datetime.now().isoformat(),
                "total_tables": len(self.tables_data),
                "total_rows": sum(table["row_count"] for table in self.tables_data.values())
            },
            "tables": {}
        }
        
        for table_name, table_data in self.tables_data.items():
            summary["tables"][table_name] = {
                "columns": table_data["columns"],
                "row_count": table_data["row_count"],
                "file": f"{table_name}.json"
            }
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\nGenerated summary: {summary_file}")
        print(f"Total tables extracted: {summary['extraction_info']['total_tables']}")
        print(f"Total rows extracted: {summary['extraction_info']['total_rows']}")
    
    def run(self):
        """Run the complete extraction process"""
        print("Starting database extraction to JSON...")
        
        # Create output directory
        self.create_output_directory()
        
        # Parse SQL file
        self.parse_sql_file()
        
        # Save to JSON files
        self.save_tables_to_json()
        
        # Generate summary
        self.generate_summary()
        
        print("\nExtraction completed successfully!")


def main():
    parser = argparse.ArgumentParser(description='Extract SQL database to JSON files')
    parser.add_argument('sql_file', help='Path to the SQL file')
    parser.add_argument('-o', '--output', default='extracted_data', 
                       help='Output directory for JSON files (default: extracted_data)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.sql_file):
        print(f"Error: SQL file '{args.sql_file}' not found")
        sys.exit(1)
    
    extractor = SQLExtractor(args.sql_file, args.output)
    extractor.run()


if __name__ == "__main__":
    main()
