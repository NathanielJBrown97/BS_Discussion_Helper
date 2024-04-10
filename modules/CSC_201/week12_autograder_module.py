import pandas as pd
import os

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input

# Function: Determine if the response discusses data storytelling effectiveness adequately.
# Arguments (1): Response from the discussion board CSV
# Summary: Establishes categories with key phrases for each of the topic metrics; sets a score. Iterates through the categories searching the response
# for matches with the keywords of each category. Incrementing the score for each metric that is present in the response. Returning either 2 or the score,
# whichever is lower. Ensuring 0-2 points; and that the student has responded to multiple metrics in order to gain full credit.
def score_data_storytelling_content(response):
    effectiveness_keywords = {
        "most_effective": ["most effective", "best example", "most impactful"],
        "least_effective": ["least effective", "worst example", "least impactful"],
        "improvement_ideas": ["crafting your own data story", "improve", "lessons learned", "applying examples"]
    }

    score = 0

    for category in effectiveness_keywords.values():
        if any(keyword in response.lower() for keyword in category):
            score += 1

    return min(2, score)

def main():
    # Gather Due Dates and Set Word Count Thresholds
    due_date_str = get_due_date_input()
    word_counts = [75, 125]

    # Paths to csv, and stats for grading.
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week12.csv'))
    df_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))
    
    # Set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(df_stats_path)


    ### EVALUATION OF STUDENTS ###


    # Evaluate Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Evaluate Content of original post; pass responses to information collection content check.
    df['Content of Original Post'] = df['response'].apply(score_data_storytelling_content)

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
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week12_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()