from datetime import datetime

# Function: Scores the Student's Timeliness Metric; based upon submission date and the due date.
# Arguments (2): A timestamp of submission date string taken from the stats.csv that is exported via Brightspace, and a due date string
# that is gathered within the autograder module itself. The 3rd parameter is simply a date format. DO NOT MODIFY THIS -- Matches Brightspace Export Format.
# Summary: Sets the deadline via datetime module passed the due date and given format. Then sets the post time. Then simply check if post_time is < the deadline.
# Returns 2 points if true; otherwise determine the number of days late and deduct 1 point for each in the return. Capped at 0 (No negative values).
def score_timeliness(timestamp_str, due_date_str, date_format='%b %d, %Y %I:%M %p'):
    deadline = datetime.strptime(due_date_str, date_format)
    post_time = datetime.strptime(timestamp_str, date_format)
    if post_time <= deadline:
        return 2
    else:
        days_late = (post_time - deadline).days
        return max(2 - days_late, 0)


# Function: Scores the Detail student's went into with their post. Generic metric for how much effort the student puts in. (I.E. word count.)
# Arguments (3): Response from the discussion csv for a given student, then a lower and upper threshold per module. 
# Summary: Calls word_count helper function (See Below); checks if the return is lower than the lowest threshold, if it is inbetween, or if it exceeds the 
# upper threshold. Awards 0 / 1 / 2 points accordingly.
def score_detail(response, lower_threshold, upper_threshold):
    word_count = len(response.split())
    if word_count < lower_threshold:
        return 0
    elif lower_threshold <= word_count < upper_threshold:
        return 1
    else:
        return 2


# Function: Counts Words in a given string.
# Arguments (1): A given text string; from the responses in the discussion post CSV.
# Summary: Simply splits the text by whitespace; then return the length of words split.
def count_words(text):
    words = text.split()
    return len(words)


# Function: Scores students based upon number of replies to peers.
# Arguments (2): Passed a student's name and the dataframe created from the CSV of the Statistics exported via Brightspace.
# Summary: Creates a Full Name for the students combining their first and last names; normalizes it to lowercase. Creates a dataframe of just the given student
# and returns either 2 points for 2 or more responses in the replies field of the stats.csv; or 1 / 0. Depending upon how many replies the student makes. 
def score_peer_replies(full_name, df_stats):
    df_stats['Full Name'] = df_stats['[First_name]'] + ' ' + df_stats['[Last_name]']
    student_stats = df_stats[df_stats['Full Name'].str.lower() == full_name.lower()]
    if not student_stats.empty:
        replies = student_stats.iloc[0]['[Replies]']
        if replies >= 2:
            return 2
        elif replies == 1:
            return 1
    return 0


# Function: Gathers the due date for the given discussion module (Allows for reusability WITHOUT manual code modification in future semesters)
# Arguments (0): Provides the user a prompt automatically for a due date in given format.
# Summary: Takes the input of a given date string; attempts to convert it to the datetime formatting required for the timeliness check. If not given the the 
# MM/DD/YYYY order or if ValueError, will reprompt. Returns the due_date_str for evaluation.
def get_due_date_input(prompt=">>> Provide the FRIDAY DUE DATE <<< Enter the due date (format: MM/DD/YYYY): "):
    input_date_str = input(prompt)
    try:
        input_date = datetime.strptime(input_date_str, '%m/%d/%Y')
        due_date_str = input_date.strftime('%b %d, %Y') + " 10:00 PM" # This adds the 10:00 PM which is found in the scraped responses and is REQUIRED. Do Not Modify.
        return due_date_str
    except ValueError:
        print("Invalid date format. Please enter the date in the format 'MM/DD/YYYY'.")
        return get_due_date_input(prompt)
