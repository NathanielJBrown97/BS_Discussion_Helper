import sys
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Accept command-line arguments for filename
if len(sys.argv) != 2:
    print("Usage: python scrapeHTML.py <week_number>")
    sys.exit(1)

# Set selected week for saving.
week_number = sys.argv[1]
# current directory is location, then move into gather_responses/temp/filename.html
current_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(current_dir, 'temp', f'live_{week_number}.html')


# Set Regular Chrome Window
browser = webdriver.Chrome()

# Set Page to load
browser.get('https://brightspace.uri.edu')

# Input for a timer; to halt scrape until you've signed in and navigated to the desired location.
input("Press enter to continue... AFTER you have log in and navigate to the appropriate discussion page...")

# Get the entire HTML of the page
html_content = browser.page_source

# Write to an html file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

# Confirmation and Exit
print(f"Page HTML saved to '{file_path}'")
browser.quit()
