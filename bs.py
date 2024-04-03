import subprocess
import os

# For filekeeping --- ask for week number, will set the filenames.
week_number = input("Enter the week number (1 through 12) for grading: ").strip()

# Validation within 1-12; inclusive.
if not week_number.isdigit() or not 1 <= int(week_number) <= 12:
    print("Invalid input. Please enter a number between 1 and 12.")
    exit(1)

week_string = f'week{week_number}'

# Get the full path of the current script to ensure the correct directory
script_dir = os.path.dirname(os.path.realpath(__file__))

# Set full paths to scrape and fill
gather_responses_folder = "gather_responses"
scrape_html_path = os.path.join(script_dir, gather_responses_folder, 'scrape_html.py')
fill_csv_path = os.path.join(script_dir, gather_responses_folder,  'fill_csv.py') 

# Run scrapeHTML.py
subprocess.run(["python", scrape_html_path, week_string], check=True)

# Run fill_csv.py 
subprocess.run(["python", fill_csv_path, week_string], check=True)

print(f"Processing for {week_string} completed.")
