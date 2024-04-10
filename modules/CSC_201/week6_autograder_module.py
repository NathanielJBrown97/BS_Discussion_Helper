import pandas as pd
import os

from utility.grading_utility import score_timeliness, score_detail, score_peer_replies, get_due_date_input

# Function: This takes a given response and iterates through checking for keywords indicative of each category defined. Returning a content grade.
# Arugments (1): Given response from the discussion CSV.
# Summary: Establishes key words used for decision power, views of autonomous, technology decisions, moral/social/inclusive impact metrics. Set a score
# variable, and then check the response for each category and its corresponding keywords. When found; increment score. Return the minimum of 2 or the score; ensuring
# grade doesn't exceed 2, and at least 2 or more of the metrics are mentioned.
def score_moral_machine_content(response):
    keywords = {
        "decision_power": [
            "who should decide", "power to decide", "prioritized", 
            "critical moral decision", "ethical decision-making", "moral authority", 
            "decision-making authority", "ethical considerations", "judgement criteria",
            "ethical framework", "moral framework"
        ],
        "view_on_autonomous_vehicles": [
            "view on autonomous vehicles", "change your view", "autonomous cars", 
            "self-driving cars", "ethical implications", "safety concerns", "trust in technology", 
            "future of transportation", "autonomous vehicle ethics", "AI in vehicles"
        ],
        "technology_decisions": [
            "decisions about the technology", "previously unaware", "algorithmic bias", 
            "data handling", "privacy concerns", "security measures", "ethical programming", 
            "technology ethics", "algorithmic fairness", "bias in AI", "machine learning fairness",
            "data ethics", "algorithmic transparency", "data security"
        ],
        "moral_choices": [
            "saving lives", "minimizing harm", "sacrifice one to save many", 
            "ethical dilemma", "moral choice", "utilitarian approach", "ethical priorities", 
            "moral principles", "dilemma resolution", "ethical conflict", "moral judgement"
        ],
        "social_impact": [
            "impact on society", "social implications", "public opinion", 
            "social acceptance", "ethical responsibility", "social justice", 
            "community effects", "societal benefits", "societal harm", "public safety",
            "ethical stance", "social ethics", "community impact"
        ],
        "inclusive_aspects": [
            "accessibility considerations", "inclusive design", "diversity in decision-making",
            "equitable outcomes", "inclusion in technology", "representative data", 
            "universal design principles", "equity in AI", "diverse perspectives",
            "cultural considerations", "global ethical standards", "minority views"
        ]
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
    file_path_to_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'gather_responses', 'temp', 'live_week6.csv'))
    df_stats_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'FEED_ME_STATS', 'stats.csv'))

    # Set dataframe to read csv, same for stats.
    df = pd.read_csv(file_path_to_csv)
    df_stats = pd.read_csv(df_stats_path)


    ### EVALUATION OF STUDENTS ###


    # Evaluate Timeliness Score; pass date_time to the score_timeliness function.
    df['Timeliness'] = df['date_time'].apply(lambda submission_date: score_timeliness(submission_date, due_date_str))

    # Evaluate Content of original post; pass responses to moral machine check.
    df['Content of Original Post'] = df['response'].apply(score_moral_machine_content)

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
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'week6_csc201_graded.xlsx'))
    df.to_excel(output_file_path, index=False)

main()