import subprocess
import os

# Function: Prompts user for module choice
def get_week_number():
    while True:
        week_number = input("Enter the week number (1 through 12) for grading: ").strip()
        if week_number.isdigit() and 1 <= int(week_number) <= 12:
            return int(week_number)
        else:
            print("Invalid input. Please enter a number between 1 and 12.")

# Function: Sets Path and folder to open, according to selected week; run's scrape HTML script.
def scrape_html(week_string):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    scrape_html_path = os.path.join(script_dir, "gather_responses", 'scrape_html.py')
    subprocess.run(["python", scrape_html_path, week_string], check=True)

# Function: Sets Path and folder to open, according to selected week; run's filter and fill the CSV script.
def fill_csv(week_string):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    fill_csv_path = os.path.join(script_dir, "gather_responses",  'fill_csv.py')
    subprocess.run(["python", fill_csv_path, week_string], check=True)

# Function: Initiates Autograder based on selected week. Requires Confirmation; provides opportunity to correct week before running module.
def run_autograder(week_number):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    autograder_module_path = os.path.join(script_dir, 'modules', 'CSC_201', f'week{week_number}_autograder_module.py')
    
    confirmation = input(f"Confirm you wish to run the autograder for week {week_number}: (y/n) ").strip().lower()

    if confirmation == 'y':
        subprocess.run(["python", autograder_module_path], check=True)
    elif confirmation == 'n':
        new_week_number = input("Enter the correct week number (1 through 12) for grading: ").strip()
        run_autograder(int(new_week_number))
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        exit(1)

# Function: Main; collects intended week choice; passes theis string into scrape html. Subsequently creates CSV, then initiates autograder. 
def main():
    week_number = get_week_number()
    week_string = f'week{week_number}'
    
    # scrape_html(week_string)
    # fill_csv(week_string)
    run_autograder(week_number)
    
    print(f"Processing for {week_string} completed.")

if __name__ == "__main__":
    main()
