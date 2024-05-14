import random
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import openpyxl

# def plotQuestionsByYear(dataRobot):
#     questionIdsSeenSet = set()
#     yearCountDict = {}
#     total_count = 0
#     for index, row in dataRobot.iterrows():
#         questionId = row["questionId"]
#         #if questionId is in questionIdsSeenSet, it is a duplicate row for comments or answers
#         if questionId not in questionIdsSeenSet:
#             dateStamp = pd.to_datetime(row["questionCreationDate"], format="%m/%d/%Y %H:%M" )
#             if dateStamp.year in yearCountDict.keys():
#                 yearCountDict[dateStamp.year] = yearCountDict[dateStamp.year] + 1
#             else:
#                 yearCountDict[dateStamp.year] = 0
#         questionIdsSeenSet.add(questionId)
    
#     # sum all counts 
#     total_count = sum(yearCountDict.values())
    
#     plt.bar(range(len(yearCountDict)), 
#             list(yearCountDict.values()), 
#             tick_label = list(yearCountDict.keys()), 
#             label = "Robot  questions on Stack Overflow by year")

#     for i, count in enumerate(yearCountDict.values()):
#         plt.text(i, count, str(count), ha='center', va='bottom', fontsize=15)

#     plt.xticks(fontsize = 20)
#     font1 = { 'color': 'black', 'size': 35}
#     font2 = { 'color': 'black', 'size': 30}
#     plt.xlabel("Year", fontdict=font2)
#     plt.ylabel("Number of robot questions asked", fontdict=font2)
#     plt.title("Robot  Questions on Stack Overflow by Year", fontdict=font1)
    
#     plt.text(-1,140, f'(DANIKA)Total: {total_count}', ha='left', fontsize=15)

    
#     plt.show()
#     return yearCountDict

def plotQuestionsByYear(dataRobot):
    # Initialize sets and dictionary
    question_ids_seen = set()
    year_count_dict = {}
    total_robot_questions = 0
    
    # Loop through the data to update the dictionary of year counts
    year_count_dict = get_year_counts(dataRobot)
        
    plot_data(year_count_dict)

    total_robot_questions = sum(year_count_dict.values())
    add_annotations(year_count_dict, total_robot_questions)
    
    plt.show()
    
    return year_count_dict

def process_row(row, question_ids_seen, year_count_dict):
    question_id = row["questionId"]
    question_creation_date = row["questionCreationDate"]

    if question_id in question_ids_seen:
        pass
    else:
        date_stamp = pd.to_datetime(question_creation_date, format="%m/%d/%Y %H:%M")
        year = date_stamp.year

        if year in year_count_dict:
            year_count_dict[year] += 1
        else:
            year_count_dict[year] = 1

        question_ids_seen.add(question_id)

    
    return year_count_dict

def get_year_counts(dataRobot):
    question_ids_seen = set()
    year_count_dict = {}

    for index, row in dataRobot.iterrows():
        year_count_dict = process_row(row, question_ids_seen, year_count_dict)

    return year_count_dict

def add_annotations(year_count_dict, total_robot_questions):
    for year, count in year_count_dict.items():
        plt.text(year, count, str(count), ha='center', va='bottom', fontsize=15)
    
    plt.text(2007,140, f'(HISHAM)Total: {total_robot_questions}', ha='left', fontsize=15)

def plot_data(year_count_dict):
    plt.bar(year_count_dict.keys(), year_count_dict.values(), label="Robot questions on Stack Overflow by year")
    plt.xlabel("Year", fontsize=30)
    plt.ylabel("Number of robot questions asked", fontsize=30)
    plt.title("Robot Questions on Stack Overflow by Year", fontsize=35)
    plt.xticks(list(year_count_dict.keys()), rotation=45, fontsize=20)





if __name__ == "__main__":
    RobotDataSet = pd.read_csv("RobotDataSet.csv")
    plotQuestionsByYear(RobotDataSet)