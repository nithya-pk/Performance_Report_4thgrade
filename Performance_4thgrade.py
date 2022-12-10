"""
Code for: Final grades and secondary school mapping for 4th grade students
    Input files are:
        student_data.csv - contains firstname, lastname, SID, emailID, section
        grades_deutsch.csv - core subject, deustsch grades containing individual homework, probe and schulaufgabe scores
        grades_mathematik.csv - core subject, deustsch grades containing individual homework, probe and schulaufgabe scores
        grades_hsu.csv - core subject, hsu grades containing individual homework, probe and schulaufgabe scores
        grades_englisch.csv - englisch grades containing individual homework, probe and schulaufgabe scores
        grades_musik.csv - musik grades containing individual homework, probe and schulaufgabe scores
        grades_sport.csv - sport grades containing individual schulaufgabe scores
    core subjects (these are used to calculate overall scores) have more homework, probe and schulaufgabe as compared to non-core subjects

    Code will calculate aggregate of all the different homework, probe, schulaufgabe and create a new CSV file output. Also display graph
"""

import os  # module to interact with underlying OS for handling folders
import glob  # module for finding text in files
import csv  # module implements classes to read and write tabular data in CSV format
import pandas as pd  # module for data structure and data analysis


# read data and create array for each student with index SID.
def load_data(folder, core_subjects):
    """Load data from csv files.
    Reads student_data.csv file and creates a dictionary of dictionaries with the student's ID as the key.
    Also reads grades*.csv files and adds grades to the dictionary.
    Finally, calculates average of the core subjects and assigns student to a school based on this average.

    :parameter folder: Folder where  student_data.csv and grades*.csv files are located
    :parameter core_subjects: List of subjects that are considered core subjects
    :return: A dictionary of dictionaries
    """
    students = {}
    with open(f"{folder}/student_data.csv") as file:
        csv_reader = csv.reader(file, delimiter=",")
        line_count = 0
        for row in csv_reader:
            if line_count == 0:  # ignore first row as this has headers
                line_count += 1
            else:
                students[row[2]] = {}
                students[row[2]]["lastname"] = row[0]
                students[row[2]]["firstname"] = row[1]
                students[row[2]]["sid"] = row[2]
                students[row[2]]["email"] = row[3]
                students[row[2]]["section"] = row[4]
                line_count += 1

    # read the different grades*.csv files and calculate average of all grades
    for csv_file in glob.glob(os.path.join(folder, "grades*.csv")):
        with open(csv_file) as file:
            # create subject lines from file names
            subject = os.path.splitext(os.path.basename(file.name))[0].replace(
                "grades_", ""
            )
            csv_reader = csv.reader(file, delimiter=",")
            line_count = 0
            for row in csv_reader:
                if line_count == 0:  # ignore first row as this has headers
                    line_count += 1
                else:
                    # calculate average for subject, grades start from column 2 onwards
                    students[row[0].upper()][f"{subject}"] = round(
                        sum(float(x) for x in row[1::]) / len(row[1::]), 2
                    )
                    line_count += 1

    for student in students:  # Rounding grades to second decimal place
        average_core = round(
            sum(float(students[student][x]) for x in core_subjects)
            / len(core_subjects),
            2,
        )
        students[student]["average_core"] = average_core
        # Based on average of only the core subjects, secondary school is decided
        # 2.33 or besser - Gymnasium
        # 2.33 to 2.66 - Realschule
        # 2.66 to 3.0 - Orientierungsschule
        # 3.0 or higher - Mittelschule
        if average_core <= 2.33:
            students[student]["school"] = "Gymnasium"
        elif 2.33 < average_core <= 2.66:
            students[student]["school"] = "Realschule"
        elif 2.66 < average_core < 3:
            students[student]["school"] = "Orientierungsschule"
        else:
            students[student]["school"] = "Mittelschule"
    return students


def save_csv(data, filename="output"):  # create output.csv file
    """Saves data. Takes the dictionary of dictionaries created earlier and writes it to CSV file ("output.csv").
    :parameter folder: Folder where  student_data.csv and grades*.csv files are located
    :parameter filename: name of the file to be created, in this case "output" (can be any name)
    """
    with open(f"{filename}.csv", mode="w") as csv_file:
        # column names being defined for output.csv file
        fieldnames = [
            "firstname",
            "lastname",
            "sid",
            "email",
            "section",
            "deutsch",
            "mathematik",
            "hsu",
            "sport",
            "musik",
            "englisch",
            "average_core",
            "school",
        ]

        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        # create row for each student
        for student in data:
            writer.writerow(data[student])


def submenu(records):
    """Prints submenu. Prints a menu of the multiple records, then asks the user to select one of them
    :parameter records: list of dictionaries
    :return: index of the record in the list of records.
    """
    print(30 * "-", "MULTIPLE RECORDS", 30 * "-")
    # print(records)
    for id, record in enumerate(records):
        print(f"{id + 1}.", record["lastname"], record["firstname"], record["sid"])
    print(67 * "-")
    element = input("Enter user number: ")
    return int(element) - 1


def search_name(name, data):
    """Serch for last name. It takes the last name and a dictionary of data as input, and returns a single record from the dictionary
    that matches the name.
    :parameter name: the name of the pupil you want to search for
    :parameter data: dictionary of dictionaries
    """
    found_records = []
    for pupil in data:
        if name.upper() in data[pupil]["lastname"].upper():
            found_records.append(data[pupil])
    if (
        len(found_records) > 1
    ):  # if there are multiple names with same last name, sub menu needed to identify single record
        single_record = submenu(found_records)
        for key in found_records[single_record]:
            print(key, ": ", found_records[single_record][key])
    elif len(found_records) == 1:
        for key in found_records[0]:
            print(key, ": ", found_records[0][key])
    else:
        print("No entries found! \n")


def save_chart(data, filename):  # creates a bar graph
    """Saves bar chart. Takes a list of dictionaries and a filename and creates a bar graph of the data.

    :parameter data: a list of dictionaries, each dictionary containing keys "school" and "section"
    :parameter filename: name of the file that the graph has to be saved as
    """
    df = pd.DataFrame(data).T
    df = pd.DataFrame(df.groupby(["section"])["school"].value_counts().unstack())
    chart = df.plot.bar(
        rot=0,
        ylabel="Number of pupils",
        title="Performance of 4th grade",
        grid=True,
        legend=True,
    ).get_figure()
    chart.savefig(filename)


def print_menu():
    """Prints menu for user to choose from"""
    print("\n", 30 * "-", "MENU", 30 * "-")
    print("1. Show all output data")
    print("2. Save CSV file as <output.csv>")
    print("3. Search by SID")
    print("4. Search by Last Name")
    print("5. Print Graph")
    print("6. Exit")
    print(67 * "-")


if __name__ == "__main__":
    core_subjects = ["deutsch", "hsu", "mathematik"]  # setting core subjects
    data = load_data(
        "data", core_subjects=core_subjects
    )  # generate array based on the core subjects
    loop = True

    while loop:  # While loop which will keep going until loop = False
        print_menu()  # Displays menu
        choice = input("Enter your choice [1-6]: ")

        if choice == "1":  # print all data
            print(data)
        elif choice == "2":  # call function save_csv
            save_csv(data)
        elif choice == "3":
            sid = input(
                "\nEnter user SID: "
            )  # since SID is unique, always one record is returned
            try:
                for key in data[sid.upper()]:
                    print(key, ": ", data[sid.upper()][key])
            except:
                print("\n Incorrect SID, no student with this ID")
        elif choice == "4":  # call function search_name
            name = input("\nEnter user name: ")
            search_name(name=name, data=data)
        elif choice == "5":
            name = input("\nEnter file name <supported pdf, jpg, png>: ")
            save_chart(data, name)
        elif choice == "6":
            print("\nBye ! \n")
            loop = False  # close loop
        else:
            print(
                f"\nBe nice, input correct number. {choice} is not an option provided. \n"
            )
