from bs4 import BeautifulSoup
import csv
import sys
import os

def extract_and_write_data(html_file_path, csv_file_path):
    # Load the HTML content from the file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the original data
    original_data = []
    for response_block in soup.find_all('div', class_='d2l-htmlblock-untrusted'):
        title_tag = response_block.find_previous(attrs={"title": True})
        if "Last edited" not in title_tag['title']:  
            title_name = title_tag['title']
            response_html = response_block.find('d2l-html-block').get('html')
            response_text = BeautifulSoup(response_html, 'html.parser').get_text(strip=True) if response_html else ''

            if title_name and response_text:
                original_data.append({'title': title_name, 'response': response_text})

    # Extract FULL NAME and DATE_TIME
    name_date_data = []
    for info_tag in soup.find_all('div', class_='d2l-textblock'):
        info_text = info_tag.get_text(strip=True)
        parts = info_text.split(' posted ')
        if len(parts) == 2:
            full_name = parts[0]
            date_time = parts[1]
            name_date_data.append({'full_name': full_name, 'date_time': date_time})

    # Combine the data and write to CSV
    combined_data = []
    for od, ndd in zip(original_data, name_date_data):
        combined_data.append({**od, **ndd})

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'response', 'full_name', 'date_time']
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for item in combined_data:
            csvwriter.writerow(item)


# Check if arv includes executable and given week number. If not exit w/ error.
if len(sys.argv) != 2:
    print("Usage: python scrape_csv.py <week_number>")
    sys.exit(1)

# Set week number from argv and set html/csv paths.
week_number = sys.argv[1]
# set path to current directory, enter temp/filenames
current_dir = os.path.dirname(os.path.realpath(__file__))
html_file_path = os.path.join(current_dir, 'temp', f'live_{week_number}.html')
csv_file_path = os.path.join(current_dir, 'temp', f'live_{week_number}.csv')


# Process each HTML file and write to corresponding CSV
extract_and_write_data(html_file_path, csv_file_path)

print("Data extraction and CSV writing complete.")
