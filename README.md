# Brightspace Discussion Board Helper Tool
As a teaching assistant at the University of Rhode Island, I spend a lot of time grading students weekly submissions. One of these weekly tasks is reading students responses to weekly prompts and evaluating each submission on specific criteria. As the prompts are the same for every student; answers are naturally similar. Using basic Natural Language Processing (NLP) methods these discussions can be evaluated automatically and save the individual in charge of grading 1-2 hours of their day!  

## Dependencies:
pip install openpyxl  (Used for Excel Save Files; alternative to terminal view)
FILL LATER: Soup, WebDriver, Selenium, Google Chrome Extension
  
## 1. Before Starting  
Navigate to brightspace discussion board; select the dropdown arrow and view statistics. Download the CSV and place into the 'FEED_ME_STATS' folder and rename the file to stats.csv  

## 2. Starting bs.py
In order to start this program you will run bs.py; this will prompt the user for which week they will be selecting. (This will determine the name of your graded file) 
--> A chrome window will open and prompt the user to sign in, enter get your Dou Security prompt and enter the site.
--> Navigate to the CSC 201 course  > Discussions > Select the week you will grade. (Note: Do not enter or open any of the mini-threads within the week's main thread.)
--> With the browser open; enter your terminal and hit enter to continue.  
  
Now the program will enter gather_responses folder and run the scrape_html.py and fill_csv.py scripts; placing this weeks raw html and filtered csv file into the temp folder within.   
  
## 3. Now the bs.py file will initiate the respective auto grader module
This will be determined by your week's choice at the start of bs.py, and will output the results to the terminal (as well as create a csv of the responses **TODO).  
  
## 4. Review and enter the students grades! 
At this point bs.py will clean the temporary folder and the stats.py file in feed_me_stats. Results will remain in case you wish to return to them; or do not prefer to use the terminal's output for grading.

