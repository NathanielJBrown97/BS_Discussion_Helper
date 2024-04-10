import pandas as pd
import os

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input

# Function: Evaluate if the given response discusses Python; specifically concepts, chatgpt interactions, and clarification metrics.
# Arguments (1): Response to evaluate; from discussion board CSV.
# Summary: Set 3 sets of keywords; sets a score counter. Check if any of the keywords for each of the categories is within the responses. If found
# increments score once. Return the minimum; 2 or the score. Ensuring multiple metrics are discussed in the post for full credit.
def score_python_concept_content(response):
    concept_keywords = ["understand better", "already know", "confusing", "challenging"]
    chatgpt_interaction_keywords = ["ChatGPT", "prompt", "result"]
    clarification_keywords = ["clarify", "unclear", "incorrect", "additional resources"]

    # Initialize the score
    score = 0
    
    # Check for the presence of discussion on each aspect
    if any(keyword in response.lower() for keyword in concept_keywords):
        score += 1
    if any(keyword in response.lower() for keyword in chatgpt_interaction_keywords + clarification_keywords):
        score += 1
    
    # The maximum score for each section is 2, so ensure it does not exceed this
    return min(2, score)


def main():
    # Gather Due Dates and Set Word Count Thresholds
    due_date_str = get_due_date_input()
    word_counts = [50, 100]

    # Paths to csv, and stats for grading.
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week5.csv'))
    df_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))
    
    # Set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(df_stats_path)


    ### EVALUATION OF STUDENTS ###


    # Evaluate Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Evaluate Content of original post; pass responses to python concept topic check.
    df['Content of Original Post'] = df['response'].apply(score_python_concept_content)

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
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week5_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()