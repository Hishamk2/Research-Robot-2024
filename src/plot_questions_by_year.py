import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def plot_questions_per_yr(data_robot: pd.DataFrame) -> dict:
    """
    Plots the number of questions about the passed in robot data per year

    This function is the main entry point, call this function to plot the data

    Parameters:
        data_robot: pd.DataFrame
            The DataFrame containing the question data, must have columns "questionId" and "questionCreationDate"

    Returns:
        dict
            A dictionary containing the number of questions asked per year 
            {year: count} where count corresponds to the number of questions asked in that year
    """

    year_count_dict = {}
    total_robot_questions = 0
    
    year_count_dict = get_year_counts(data_robot)
        
    plot_data(year_count_dict)

    yearly_counts = list(year_count_dict.values())    
    total_robot_questions = sum(yearly_counts)
    add_annotations(year_count_dict, total_robot_questions)
    
    # makes sure the x-axis isn't cut off
    plt.tight_layout()

    plt.show()
    
    return year_count_dict

def get_year_counts(data_robot: pd.DataFrame) -> dict:
    """
    Counts the number of robot-related questions per year from the data.

    This function iterates through each row in the DataFrame and processes 
    the data to build a dictionary with the count of questions per year.

    Parameters:
        data_robot: pd.DataFrame
            The DataFrame containing the question data, must have columns "questionId" and "questionCreationDate"
    
    Returns:
        dict
            A dictionary containing the number of questions asked per year 
            {year: count} where count corresponds to the number of questions asked in that year
    """
    question_ids_seen = set()
    year_count_dict = {}

    for index, row in data_robot.iterrows():
        year_count_dict = process_row(row, question_ids_seen, year_count_dict)

    return year_count_dict

def process_row(row: pd.Series, question_ids_seen: set, year_count_dict: dict) -> dict:
    """
    Processes a single row of data to update the year count dictionary.

    This function extracts the question ID and creation date from the row,
    ensures the question is counted only once, and updates the count of 
    questions for the corresponding year.

    Parameters:
        row: pd.Series
            The row of data containing the question ID and creation date (can have other columns, but these are required)
        question_ids_seen: set
            A set containing the question IDs that have already been processed
            This is used to ensure that a question is only counted once in case the data has duplicates
        year_count_dict: dict
            A dictionary containing the number of questions asked per year
    
    Returns:
        dict
            An updated dictionary containing the number of questions asked per year 
            {year: count} where count corresponds to the number of questions asked in that year
    """

    question_id = row["questionId"]
    question_creation_date = row["questionCreationDate"]

    if question_id in question_ids_seen:
        pass
    else:
        try:
            date_stamp = pd.to_datetime(question_creation_date, format="%m/%d/%Y %H:%M")
        except:
            base_date = datetime(1899, 12, 30)
            date_stamp = base_date + timedelta(days=float(question_creation_date))

        year = date_stamp.year

        if year in year_count_dict:
            year_count_dict[year] += 1
        else:
            year_count_dict[year] = 1

        question_ids_seen.add(question_id)

    return year_count_dict

def add_annotations(year_count_dict, total_robot_questions):
    """
    Adds annotations to the plot showing the number of questions per year as a number on top of the bars
    As well as the total number of robot questions asked

    Parameters:
        year_count_dict: dict
            A dictionary containing the number of questions asked per year 
            {year: count} where count corresponds to the number of questions asked in that year
        total_robot_questions: int
            The total number of robot questions asked
    """
    for year, count in year_count_dict.items():
        plt.text(year, count, str(count), ha='center', va='bottom', fontsize=15)

    # x and y points to make sure the total is displayed on the top right of the plot (and so it is visible) 
    x_coord_total = max(year_count_dict.keys())
    y_coord_total = max(year_count_dict.values())
    plt.text(x_coord_total, y_coord_total, f'Total: {total_robot_questions}', ha='left', fontsize=15)

def plot_data(year_count_dict):
    """
    Creates a bar plot with the yearly question data

    Parameters:
        year_count_dict: dict
            A dictionary containing the number of questions asked per year 
            {year: count} where count corresponds to the number of questions asked in that year
    
    Returns:
        None
    """
    plt.bar(year_count_dict.keys(), year_count_dict.values(), label="Robot questions on Stack Overflow by year")
    plt.xlabel("Year", fontsize=30)
    plt.ylabel("Number of robot questions asked", fontsize=30)
    plt.title("Robot Questions on Stack Overflow by Year", fontsize=35)
    plt.xticks(list(year_count_dict.keys()), rotation=45, fontsize=20)


if __name__ == "__main__":
    data_robot = pd.read_csv("../Robot Random (H & S & D) - Coded (no fp).csv")
    plot_questions_per_yr(data_robot)

