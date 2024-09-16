import pandas as pd
import argparse
import re
import os
import constants  # Make sure this file exists and is correctly imported
from utils import parse_string  # Ensure parse_string is defined in utils

def check_file(filename):
    """Checks if the file exists and is a CSV file."""
    if not filename.lower().endswith('.csv'):
        raise ValueError("Only CSV files are allowed.")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Filepath: {filename} is invalid or not found.")

def sanity_check(test_filename, output_filename):
    """Performs sanity checks on the test and output CSV files."""
    # Check if the files are valid
    check_file(test_filename)
    check_file(output_filename)
    
    try:
        # Read the CSV files
        test_df = pd.read_csv(test_filename)
        output_df = pd.read_csv(output_filename)
    except Exception as e:
        raise ValueError(f"Error reading the CSV files: {e}")
    
    # Ensure 'index' column is present in both files
    if 'index' not in test_df.columns:
        raise ValueError("Test CSV file must contain the 'index' column.")
    
    if 'index' not in output_df.columns or 'prediction' not in output_df.columns:
        raise ValueError("Output CSV file must contain 'index' and 'prediction' columns.")
    
    # Check for missing or extra index entries
    missing_index = set(test_df['index']).difference(set(output_df['index']))
    if len(missing_index) != 0:
        print(f"Missing index in output file: {missing_index}")
        
    extra_index = set(output_df['index']).difference(set(test_df['index']))
    if len(extra_index) != 0:
        print(f"Extra index in output file: {extra_index}")
    
    # Apply the custom string parser function to each prediction
    output_df.apply(lambda x: parse_string(x['prediction']), axis=1)
    print(f"Parsing successful for file: {output_filename}")
    
if __name__ == "__main__":
    # Usage example: python sanity.py --test_filename sample_test.csv --output_filename sample_test_out.csv
    parser = argparse.ArgumentParser(description="Run sanity check on a CSV file.")
    parser.add_argument("--test_filename", type=str, required=True, help="The test CSV file name.")
    parser.add_argument("--output_filename", type=str, required=True, help="The output CSV file name to check.")
    
    # Parse the command line arguments
    args = parser.parse_args()

    # Run the sanity check and handle any errors
    try:
        sanity_check(args.test_filename, args.output_filename)
    except Exception as e:
        print(f"Error: {e}")