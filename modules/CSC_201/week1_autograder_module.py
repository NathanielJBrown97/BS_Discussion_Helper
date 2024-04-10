import pandas as pd
import os
import re

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input


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

    # Brief Explanation:
    # major(ing)? / study(ing)? considers either the root or full word
    # \b \b is a boundary; ensures separate words in evaluations
    # Essentially checks for major / majoring in _______ <--- Allows for any entry and will count this as a valid major pattern.
    # w+ just initiates the match for a word after the defined pattern.
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


def main():
    # Gather Due Dates and Set Word Count Thresholds.
    due_date_str = get_due_date_input()
    word_counts = [25,50] # This is set to 25-50. Introductions can be short and still satisfy requirements.

    # Paths to csv, and stats for grading.
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week1.csv'))
    file_path_stats = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))

    # Set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(file_path_stats)


    ### EVALUATION OF STUDENTS ###


    # Evaluate each introduction; passed responses and full_name rows
    df['Introduction Score'] = df.apply(lambda row: check_introduction(row['response'], row['full_name']), axis=1).astype(int)
    
    # Evaluate 'Relevance' Major Mentioned; pass responses.
    df['Major Mention Score'] = df['response'].apply(check_major).astype(int)

    # Determine 'Content of Original Posts'; simply add the introductory score and Major mention scores.
    df['Content of Original Post'] = df['Introduction Score'] + df['Major Mention Score']

    # Evaluate 'Detail Level' (Word-Count); pass responses and given word count thresholds.
    df['Details in Original Post'] = df['response'].apply(lambda response: score_detail(response, *word_counts))

    # Evaluate 'Peer Responses'; pass the full_name and run score_responses for each (Passed the df for stats)
    df['Peer Replies'] = df['full_name'].apply(lambda name: score_peer_replies(name, df_stats))

    # Determine 'Relationship to Course' metric; determined by evaluating at least 1/2 points for each Content and details.
    df['Relationship to Course Content'] = df.apply(lambda row: int(row['Content of Original Post'] >= 1) + int(row['Details in Original Post'] >= 1), axis=1)

    # Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Total Score; sum of Content, Details, Responses, Timeliness, and Relationship to Material. 2pts each, total of 10pts.
    df['Overall Score'] = df[['Timeliness', 'Peer Replies', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content']].sum(axis=1)


    ### OUTPUT OF RESULTS ###


    # Output in Access Topic Format Order
    print(df[['full_name', 'Timeliness', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content', 'Peer Replies', 'Overall Score']])

    # Write to an Excel file for alternative grading.
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week1_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()
