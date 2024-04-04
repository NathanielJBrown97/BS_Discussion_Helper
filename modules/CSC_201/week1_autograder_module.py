import pandas as pd
import re
import os
from datetime import datetime

# Function: Checks for engagement in response; specifically in reference to an introduction of the student.
# Arguments (2): Student's response and full name.
# Summary: List of common introductory words. Attempts to check response for any of the listed phrases. As a follow up check, 
# attempts to search their responses for their full name; as some attempt to give credit for weirdly just writing your name and never typing any form of introduction.
# if no indication of introduction is met; returns false (i.e. no credit).
# VULNERABILITY: There are a million ways to say hello. 'wazzupdog' is valid, but not accounted for. Solution; spend too much time adding introductions.
def check_introduction(response, student_full_name):
    intro_phrases = ["hi", "hello", "hey", "greetings", "my name", "i am", "i'm", "this is", "it's me", "introducing"]
    if any(phrase in response.lower() for phrase in intro_phrases):
        return True

    response_first_word = response.lower().split()[0]
    if student_full_name.lower().split()[0] == response_first_word:
        return True

    return False

# Function: Checks for engagement in the prompts; specifically reference of any form of major. (As per requirements).
# Arguments (1): Given response; aka large string.
# Summary: Defines common majors for the course in a list. Then check if any of these majors are within the common list. 
# Returns valid (i.e. gives credit) if found. 
# Then defines major patterns for common ways to mention a degree path; attempt to find a match within the response.
# VULNERABILITY: An inability to write english properly can result in a false negative... is English mandatory?
def check_major(response):
    common_majors = ["computer science", "data science", "business", "mathematics", "physics", "psychology", "cyber security", "criminology", "biotechnology"]

    if any(major in response.lower() for major in common_majors):
        return True

    major_patterns = [
        r"\bmajor(ing)?\b in \b\w+",    
        r"\bstudy(ing)?\b \b\w+",       
        r"\bin\b \b\w+",                
        r"\bmy field is\b \b\w+",       
        r"\bI study\b \b\w+",            
        r"\bmy degree is\b \b\w+",       
        r"\bminor(ing)?\b in \b\w+",    
    ]
    for pattern in major_patterns:
        if re.search(pattern, response.lower()):
            return True
    return False

# Function: Counts Words in a given string.
# Arguments (1): A given text string.
# Summary: Simply splits the text by whitespace; then return the length of words split.
def count_words(text):
    words = text.split()
    return len(words)

# Function: Scores the Amount of Detail in a Post
# Arguments (1): Passed a given response field; will be one very long string.
# Summary: Will call a helper function to count the words in the response. From here simply guage the level of detail based upon
# a rough word count. For the introduction it is extremely low. < 25 words == no points. 25-50 == 1/2 points. >50 == full points.
def score_details(response):
    word_count = count_words(response)
    if word_count < 25:
        return 0
    elif 25 <= word_count < 50:
        return 1
    else:
        return 2

# Function: Scores the Number of Responses Students Submit
# Arguments (2): data frame of stats (placed within feed_me_stats), and the student's full name from scraped CSV (within gather_responses).
# Summary: Normalize the name to lowercase. Search the stats df for their full name. Isolate the student's stats specifically.
# Provided the stats for the student isn't empty... return 2, 1, or 0 depending upon number of entries in the [Replies] field of stats.csv.
def score_responses(df_stats, student_full_name):
    lower_full_name = student_full_name.lower()
    df_stats['Full Name'] = df_stats['[First_name]'] + ' ' + df_stats['[Last_name]']
    student_stats = df_stats[df_stats['Full Name'].str.lower() == lower_full_name]
    
    if not student_stats.empty:
        replies = student_stats.iloc[0]['[Replies]']
        if replies >= 2:
            return 2
        elif replies == 1:
            return 1
    return 0

def parse_timestamp(timestamp_str):
    # Adjust the format based on your actual timestamp format
    return datetime.strptime(timestamp_str, '%b %d, %Y %I:%M %p')

def score_timeliness(timestamp_str):
    # Define the deadline
    deadline = datetime.strptime('Sep 6, 2023 10:00 PM', '%b %d, %Y %I:%M %p')
    
    # Parse the timestamp
    post_time = parse_timestamp(timestamp_str)

    # Calculate days difference
    days_difference = (post_time - deadline).days
    if post_time <= deadline:
        return 2
    else:
        # Subtract 1 point per day late, but don't go below 0
        return max(2 - days_difference, 0)
    
def main():
    #paths to csv, and stats for grading.
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week1.csv'))
    file_path_stats = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))

    # set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(file_path_stats)

    # Evaluate each introduction; passed responses and full_name rows
    df['Introduction Score'] = df.apply(lambda row: check_introduction(row['response'], row['full_name']), axis=1).astype(int)
    
    # Evaluate 'Relevance' Major Mentioned; pass responses.
    df['Major Mention Score'] = df['response'].apply(check_major).astype(int)

    # Evaluate 'Detail Level' (Word-Count); pass responses.
    df['Details in Post Score'] = df['response'].apply(score_details).astype(int)

    # Evaluate 'Peer Responses'; pass the full_name and run score_responses for each (Passed the df for stats)
    df['Response Score'] = df['full_name'].apply(lambda name: score_responses(df_stats, name)).astype(int)

    # Determine 'Content of Posts'; simply add the introductory score and Major mention scores.
    df['Content of Post'] = df['Introduction Score'] + df['Major Mention Score']

    # Determine 'Relationship to Course' metric; adding the content of post and detail scores together.
    df['Relationship to Course'] = df.apply(lambda row: int(row['Content of Post'] >= 1) + int(row['Details in Post Score'] >= 1), axis=1)
    df['Total Score'] = df['Content of Post'] + df['Details in Post Score'] + df['Response Score'] + df['Relationship to Course']

    # Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness Score'] = df['date_time'].apply(score_timeliness).astype(int)

    # Total Score; sum of Content, Details, Responses, Timeliness, and Relationship to Material. 2pts each, total of 10pts.
    df['Total Score'] = df['Content of Post'] + df['Details in Post Score'] + df['Response Score'] + df['Relationship to Course'] + df['Timeliness Score']

    # Ensure every column is displayed in terminal.
    columns_to_display = ['full_name', 'Details in Post Score', 'Response Score', 'Content of Post', 'Relationship to Course', 'Timeliness Score', 'Total Score']
    print(df[columns_to_display])

    # Write the columns to display for each student into a spreadsheet file
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week1_csc201_graded.xlsx'))
    df[columns_to_display].to_excel(output_file_path, index=False)

if __name__ == "__main__":
    main()
