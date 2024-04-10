import pandas as pd
import os

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input

# These four functions work in the same manner; they take a given student response and filter through it for keywords that indicate they are discussing the topics
# provided via the prompts. This will allow the check's to function for ALL of the articles given; considering the discussion topics remain the same across the articles.
# If any matches in keywords and phrases are found, will return credit for that section. 
def check_engagement(response):
    keywords = ["case study", "scenario", "ethical", "benefit", "harm"]
    return any(keyword in response.lower() for keyword in keywords)

def check_ethical_issues(response):
    phrases = ["ethical issue", "ethical concern", "moral dilemma", "ethical problem"]
    return any(phrase in response.lower() for phrase in phrases)

def check_common_good(response):
    phrases = ["common good", "greater good", "public benefit", "societal benefit"]
    return any(phrase in response.lower() for phrase in phrases)

def check_benefit_and_harm(response):
    benefit_phrases = ["benefit", "advantage", "positive"]
    harm_phrases = ["harm", "disadvantage", "negative", "risk"]
    return any(phrase in response.lower() for phrase in benefit_phrases) and any(phrase in response.lower() for phrase in harm_phrases)

def main():
    # Gather Due Dates and Set Word Count Thresholds
    due_date_str = get_due_date_input()
    word_counts = [50, 100]

    # Paths to CSV and stats for grading
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week2.csv'))
    file_path_stats = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))

    # Set dataframe to read CSV, same for stats
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(file_path_stats)


    ### EVALUATION OF STUDENTS ###


    # Evaluate Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Evaluate 'Peer Responses'; pass the full_name and run score_responses for each (Passed the df for stats)
    df['Peer Replies'] = df['full_name'].apply(lambda name: score_peer_replies(name, df_stats))

    # Determine 'Content of Original Post'; pass the student response to engagement and ethical issues checks returns 0-1 point per.
    df['Content of Original Post'] = df['response'].apply(lambda student_response: check_engagement(student_response) + check_ethical_issues(student_response))

    # Evaluate 'Detail Level' (Word-Count); pass responses and given word count thresholds.    
    df['Details in Original Post'] = df['response'].apply(lambda response: score_detail(response, *word_counts))

    # Determine 'Relationship to Course' metric; dpass the student response to common good and benefit and harm check, to ensure relationship to theme of discussion. 0-1 point per.
    df['Relationship to Course Content'] = df['response'].apply(lambda student_response: check_common_good(student_response) + check_benefit_and_harm(student_response))

   # Total Score; sum of Content, Details, Responses, Timeliness, and Relationship to Material. 2pts each, total of 10pts.
    df['Overall Score'] = df[['Timeliness', 'Peer Replies', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content']].sum(axis=1)


    ### OUTPUT OF RESULTS ###


    # Output in Access Topic Format Order
    print(df[['full_name', 'Timeliness', 'Content of Original Post', 'Details in Original Post', 'Relationship to Course Content', 'Peer Replies', 'Overall Score']])
    
    # Write to an Excel file for alternative grading.
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week2_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()