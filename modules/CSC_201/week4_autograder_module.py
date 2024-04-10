import pandas as pd
import os

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input

# Function: Determines if students are discussing the data breach article
# Arguments (1): Response from discussion post csv
# Summary: Establishs keywords for data comprimised check, breach nature, issues, and prevention. For each category; loop search the response for a related keyword.
# If any are found; increment score by 1. Ensuring at least 2 of the topics are mentioned. Returns the score counter; with a maximum return of 2. 
def score_data_breach_content(response):
    keywords = {
        "data_compromised": ["personal data", "financial information", "health records"],
        "breach_nature": ["accidental", "malicious", "hacked"],
        "issues": ["identity theft", "financial loss", "privacy violation"],
        "prevention": ["encryption", "security measures", "data protection policies"]
    }

    score = 0
    for category in keywords.values():
        if any(keyword in response.lower() for keyword in category):
            score += 1
    return min(2, score)

def main():
    # Gather Due Dates and Set Word Count Thresholds
    due_date_str = get_due_date_input()
    word_counts = [50, 100]

    # Paths to csv, and stats for grading.
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week4.csv'))
    df_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))
    
    # Set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(df_stats_path)


    ### EVALUATION OF STUDENTS ###


    # Evaluate Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Evaluate Content of Original Post; pass responses from the discussion CSV to check if they're discussing the data breach content.
    df['Content of Original Post'] = df['response'].apply(score_data_breach_content)

    # Evaluate 'Detail Level' (Word-Count); pass responses and given word count thresholds.    
    df['Details in Original Post'] = df['response'].apply(lambda response: score_detail(response, *word_counts))

    # Evaluate 'Peer Responses'; pass the full_name and run score_responses for each (Passed the df for stats)
    df['Peer Replies'] = df['full_name'].apply(lambda name: score_peer_replies(name, df_stats))

    # Determine 'Relationship to Course' metric; determined by evaluating at least 1/2 points for each Content and details.
    df['Relationship to Course Content'] = df.apply(lambda row: int(row['Content of Original Post'] >= 1) + int(row['Details in Original Post'] >= 1), axis=1)

    # Total Score; sum of Content, Details, Responses, Timeliness, and Relationship to Material. 2pts each, total of 10pts.
    df['Overall Score'] = df[['Timeliness', 'Peer Replies', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content']].sum(axis=1)


    ### OUTPUT OF RESULTS ###


    # Output in Access Topic Format Order
    print(df[['full_name', 'Timeliness', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content', 'Peer Replies', 'Overall Score']])
    
    # Write to an Excel file for alternative grading.
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week4_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()