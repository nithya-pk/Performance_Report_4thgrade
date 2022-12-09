## Project: Performance_Report_4thgrade ##
  This project has been conceptualised on a real-life Grundschule scenario for 4th grade students in Bavarian schooling system. 4th graders have 6 subjects - three of them are considered "core" and average score of overall year performance in these three subjects determines the secondary school students can get into.
  ####  Disclaimer: ####
  Is not accurate, it is only a conception. Data in input files are random and not based on any real-life people

## Input Files ##
Input files are: <br />
  student_data.csv - contains firstname, lastname, SID, emailID, section <br />
  grades_deutsch.csv - core subject, deustsch grades containing SID & individual homework, probe and schulaufgabe scores <br />
  grades_mathematik.csv - core subject, deustsch grades containing SID & individual homework, probe and schulaufgabe scores <br />
  grades_hsu.csv - core subject, hsu grades containing SID & individual homework, probe and schulaufgabe scores <br />
  grades_englisch.csv - englisch grades containing SID & individual homework, probe and schulaufgabe scores <br />
  grades_musik.csv - musik grades containing SID & individual homework, probe and schulaufgabe scores <br />
  grades_sport.csv - sport grades containing SID & individual schulaufgabe scores <br />

Different input files are usually because subjects are handled by different teachers. Also, these files reflect what could be dump from an application

## Input Files ##
Code looks the input files and calculates averages in individual files from the different homeworks, probes, schulaufgabes and creates an average score. <br />

Further, takes the average of the core subjects and maps this as below:  <br />
  2.33 or better - Gymnasium <br />
  2.33 to 2.66 - Realschule <br />
  2.66 to 3.0 - Orientierungsschule <br />
  3.0 or higher - Mittelschule <br />
  
This is dumped to an "output.csv" <br />

Based on an interactive menu, options are provided for: <br />
  1. Show all output data
  2. Save CSV file as <output.csv>
  3. Search by SID
  4. Search by Last Name
  5. Print Graph
  6. Exit
 There is error handling for overall menu options (if option other than 1-6 is chosesn) and option 3, 4 (for incorrect SIDs, wrong last names) based on several user testing.
 
 ## Important Considerations ##
 Folder Structure: input files have to be under "/data" folder, python file is outside the "/data" folder
 
