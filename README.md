# Brightspace Discussion Board Helper Tool
As a teaching assistant at the University of Rhode Island, I spend a lot of time grading students weekly submissions. One of these weekly tasks is reading students responses to weekly prompts and evaluating each submission on specific criteria. As the prompts are the same for every student; answers are naturally similar. Using basic Natural Language Processing (NLP) methods these discussions can be evaluated automatically and save the individual in charge of grading 1-2 hours of their day! Due to limited support tools and access to data from Brightspace, a work-around was developed for collecting these weekly discussions into a readable and parsable format. A simple HTML scrape and data filtering of a very large dynamic webpage. Below you will find instructions for the utilization of this program.
<br><br>
## Dependencies:
pip install openpyxl  (Used for Excel Save Files; alternative to terminal view)  
BeautifulSoup, WebDriver, and Selenium Python Libraries  
Selenium IDE (Chrome Extension -- Used for the auto scrape / Multi-Factor Authentification Verification --- Vital to Gain Access to Brightspace Discussions)
<br><br>
## 1. Before Starting  
Navigate to brightspace discussion board; select the dropdown arrow and view statistics. Download the CSV and place into the 'FEED_ME_STATS' folder and rename the file to stats.csv  
<br><br>
## 2. Starting bs.py
Start the program by running bs.py or right click 'run python in terminal'.  
The program will then ask for the given week you will be collecting, enter a number between 1-12.  
The program will then open a chrome window; and have the user navigate to the discussion page you wish to scrape. **DO NOT OPEN ANY SUBPAGES, just open the Weekly Discussion main thread.**  
Now you leave the chrome window open; and hit enter on your terminal window.  
<br><br>  
## 3. Now the bs.py script will initiate the HTML scrape of the Discussion Thread and Data Collection  
The program will scrape the raw HTML from Brightspace's discussion board, and then filter that HTML into a CSV of the students and their responses to the topic. Now the program can start to evaluate student responses and determine grading for the given module.  
<br><br>  
## 4. THe program will ask for confirmation of the intended week's module (Giving you the opportunity to correct a mistake)...  
Upon confirming the module; the script will initiate that module and evaluate the responses CSV accordingly. As it completes it will save the responses into an excel sheet in the results folder; the grades will be broken down in the terminal as well for quick access.  
<br><br>  
## 5. Review and enter the students grades! 
At this point bs.py will clean the temporary folder and the stats.py file in feed_me_stats. Results will remain in case you wish to return to them; or do not prefer to use the terminal's output for grading.

