import random
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import openpyxl
import time

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


def calculatePopularity(allRobotDataSet, allQuestionData, allAnswerDataSet, randomRobotWithCodesData, randomRobotAllData):
    allPopularityFactorsQuestions = calculatePopularityAllRobotQuestions(allRobotDataSet, allQuestionData)
    allPopularityFactorsAnswers = calculatePopularityAllRobotAnswers(allRobotDataSet, allAnswerDataSet)

    dataSpecifications = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'api') | (randomRobotWithCodesData['code'] == 'hr') | (randomRobotWithCodesData['code'] == 'os') | (randomRobotWithCodesData['code'] == 'lu')]
    calculatePopularityCategoriesGeneral(dataSpecifications, "Specifications", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataRemote = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'wireless') | (randomRobotWithCodesData['code'] == 'cpmr')]
    calculatePopularityCategoriesGeneral(dataRemote, "Remote", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataConnections = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'internet') | (randomRobotWithCodesData['code'] == 'wpi') | (randomRobotWithCodesData['code'] == 'sc')]
    calculatePopularityCategoriesGeneral(dataConnections, "Connections", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataCoordinates = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'position') | (randomRobotWithCodesData['code'] == 'orientation')]
    calculatePopularityCategoriesGeneral(dataCoordinates, "Coordinates", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataMoving = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'mp') | (randomRobotWithCodesData['code'] == 'obstacles') | (randomRobotWithCodesData['code'] == 'mapping') | (randomRobotWithCodesData['code'] == 'SLAM')]
    calculatePopularityCategoriesGeneral(dataMoving, "Moving", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataActuator = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'ik') | (randomRobotWithCodesData['code'] == 'hc') | (randomRobotWithCodesData['code'] == 'wc') | (randomRobotWithCodesData['code'] == 'mc') | (randomRobotWithCodesData['code'] == 'balance')]
    calculatePopularityCategoriesGeneral(dataActuator, "Actuator", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataProgramming = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'pointers') | (randomRobotWithCodesData['code'] == 'dt') | (randomRobotWithCodesData['code'] == 'overflow') | (randomRobotWithCodesData['code'] == 'list')]
    calculatePopularityCategoriesGeneral(dataProgramming, "Programming", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataLibrary = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'li') | (randomRobotWithCodesData['code'] == 'bf')]
    calculatePopularityCategoriesGeneral(dataLibrary, "Library", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataTiming = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'timing') | (randomRobotWithCodesData['code'] == 'multithreading') | (randomRobotWithCodesData['code'] == 'rg')]
    calculatePopularityCategoriesGeneral(dataTiming, "Timing", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

    dataIncoming = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'cameras') | (randomRobotWithCodesData['code'] == 'vision') | (randomRobotWithCodesData['code'] == 'line tracking') | (randomRobotWithCodesData['code'] == 'sensors')]
    calculatePopularityCategoriesGeneral(dataIncoming, "Incoming", allPopularityFactorsQuestions, allPopularityFactorsAnswers)



def calculatePopularityAllRobotAnswers(allRobotData, allAnswerData):
    allRobotAnswerPopularityFactors = getRobotAnswersPopularityFactors(allRobotData)
    allAnswersPopularityFactors = getAllAnswersPopularityFactors(allAnswerData)

    normalizedAllRobotAnswerPopularityFactors = normalizePopularityFactors(allRobotAnswerPopularityFactors, allAnswersPopularityFactors)
    score = normalizedAllRobotAnswerPopularityFactors[0]
    commentCount = normalizedAllRobotAnswerPopularityFactors[1]
    popularity = (score + commentCount) / 2
    
    print(f'''All Robot Answer Popularity Factors:  
    Score: {score:.2f}
    Comment Count: {commentCount:.2f}
    Popularity: {popularity:.2f}\n''')

    allScores = allAnswersPopularityFactors[0]
    allCommentCounts = allAnswersPopularityFactors[1]
    return allScores, allCommentCounts

def getRobotAnswersPopularityFactors(robotData):
    score = calculatePopularityFactorAvg('answerScore', robotData, 'answerId')
    commentCount = calculatePopularityFactorAvg('answerCommentCount', robotData, 'answerId')
    return score, commentCount

def getAllAnswersPopularityFactors(allAnswersData):
    score = calculatePopularityFactorAvg('Score', allAnswersData, 'Id')
    commentCount = calculatePopularityFactorAvg('CommentCount', allAnswersData, 'Id')
    return score, commentCount


def calculatePopularityAllRobotQuestions(allRobotData, allQuestionData):
    allRobotPopularityFactors = getRobotQuestionsPopularityFactors(allRobotData)
    allQuestionsPopularityFactors = getAllQuestionsPopularityFactors(allQuestionData)

    normalizedAllRobotPopularityFactors = normalizePopularityFactors(allRobotPopularityFactors, allQuestionsPopularityFactors)
    score = normalizedAllRobotPopularityFactors[0]
    answerCount = normalizedAllRobotPopularityFactors[1]
    commentCount = normalizedAllRobotPopularityFactors[2]
    viewCount = normalizedAllRobotPopularityFactors[3]
    popularity = (score + answerCount + commentCount + viewCount) / 4

    print(f'''All Robot Questions Popularity Factors:   
    Score: {score:.2f}
    Answer Count: {answerCount:.2f}
    Comment Count: {commentCount:.2f} 
    View Count: {viewCount:.2f}
    Popularity: {popularity:.2f}\n''')

    allScores = allQuestionsPopularityFactors[0]
    allAnswerCounts = allQuestionsPopularityFactors[1]
    allCommentCounts = allQuestionsPopularityFactors[2]
    allViewCounts = allQuestionsPopularityFactors[3]
    return allScores, allAnswerCounts, allCommentCounts, allViewCounts

def getRobotQuestionsPopularityFactors(robotData):
    score = calculatePopularityFactorAvg('questionScore', robotData, 'questionId')
    answerCount = calculatePopularityFactorAvg('AnswerCount', robotData, 'questionId')
    commentCount = calculatePopularityFactorAvg('CommentCount', robotData, 'questionId')
    viewCount = calculatePopularityFactorAvg('questionViewCount', robotData, 'questionId')
    return score, answerCount, commentCount, viewCount

def getAllQuestionsPopularityFactors(allQuestionsData):
    score = calculatePopularityFactorAvg('Score', allQuestionsData, 'Id')
    answerCount = calculatePopularityFactorAvg('AnswerCount', allQuestionsData, 'Id')
    commentCount = calculatePopularityFactorAvg('CommentCount', allQuestionsData, 'Id')
    viewCount = calculatePopularityFactorAvg('viewCount', allQuestionsData, 'Id')
    return score, answerCount, commentCount, viewCount




def calculatePopularityCategoriesGeneral(dataSet, codeLabel, allPopularityFactorsQuestions, allPopularityFactorsAnswers):
    questionScoreAll = allPopularityFactorsQuestions[0]
    questionAnswerCountAll = allPopularityFactorsQuestions[1]
    questionCommentCountAll = allPopularityFactorsQuestions[2]
    questionViewCountAll = allPopularityFactorsQuestions[3]
    answerScoreAll = allPopularityFactorsAnswers[0]
    answerCommentsAll = allPopularityFactorsAnswers[1]
    
    questionPopularityFactors = getRobotQuestionsPopularityFactors(dataSet)
    answerPopularityFactors = getRobotAnswersPopularityFactors(dataSet)

    allQuestionsPopularityFactors = (questionScoreAll, questionAnswerCountAll, questionCommentCountAll, questionViewCountAll)
    allAnswersPopularityFactors = (answerScoreAll, answerCommentsAll)

    normalizedQuestionPopularityFactors = normalizePopularityFactors(questionPopularityFactors, allQuestionsPopularityFactors)
    normalizedAnswerPopularityFactors = normalizePopularityFactors(answerPopularityFactors, allAnswersPopularityFactors)

    questionScore = normalizedQuestionPopularityFactors[0]
    answerCount = normalizedQuestionPopularityFactors[1]
    commentCount = normalizedQuestionPopularityFactors[2]
    viewCount = normalizedQuestionPopularityFactors[3]

    answerScore = normalizedAnswerPopularityFactors[0]
    answerCommentCount = normalizedAnswerPopularityFactors[1]

    questionPopularity = (questionScore + answerCount + commentCount + viewCount) / 4
    answerPopularity = (answerScore + answerCommentCount) / 2

    print(f'''Robot Questions {codeLabel} Popularity Factors:
    Score: {questionScore:.2f}
    Answer Count: {answerCount:.2f}
    Comment Count: {commentCount:.2f}
    View Count: {viewCount:.2f}
    Popularity: {questionPopularity:.2f}\n''')

    print(f'''Robot Answers {codeLabel} Popularity Factors:
    Score: {answerScore:.2f}
    Comment Count: {answerCommentCount:.2f}
    Popularity: {answerPopularity:.2f}\n''')
    

# popularityFactor is the column name of the popularity factor in the dataframe
# dataframe is the dataframe to calculate the popularity factor from
# idLabel is the column name of the id in the dataframe
def calculatePopularityFactorAvg(popularityFactor, dataframe, idLabel):
    popularityFactorTotal = 0
    questionIdsSeenSet = set()
    totalNumUniqueQuestions = 0

    for index, row in dataframe.iterrows():
        questionId = row[idLabel]
        if ((questionId is not None) and 
            (questionId not in questionIdsSeenSet) and 
            (not pd.isna(row[popularityFactor]))):
                popularityFactorCount = row[popularityFactor]
                popularityFactorTotal += popularityFactorCount
                totalNumUniqueQuestions += 1
                questionIdsSeenSet.add(questionId)

    # I don't think this is necessary, but I'm keeping it in case it is
    # because even if 0 questions are found, the popularity factor should be 0 so no division by 0 error
    if totalNumUniqueQuestions == 0:
        return 0

    # return the average popularity factor
    # This is NOT normalizing the factor, it is just the average
    return popularityFactorTotal / totalNumUniqueQuestions

def normalizePopularityFactors(popularityFactors, allPopularityFactors):
    normalizedPopularityFactors = []
    for i in range(len(popularityFactors)):
        normalizedPopularityFactors.append(normalizePopularityFactor(popularityFactors[i], allPopularityFactors[i]))
    return normalizedPopularityFactors

def normalizePopularityFactor(popularityFactor, allPopularityFactor):
    return popularityFactor / allPopularityFactor



if __name__ == "__main__":
    start_time = time.time()

    
    allRobotDataSet = pd.read_csv("RobotDataSet.csv")
    allQuestionDataSet = pd.read_csv("AllQuestionDataCombined.csv")
    allAnswerDataSet = pd.read_csv("AllAnswerDataCombined.csv")
    randomRobotWithCodesDataSet = pd.read_csv("RandomRobot - Coded.csv")
    randomRobotAllDataSet = pd.read_csv("RandomRobot-Full.csv")
    
    calculatePopularity(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # calculatePopularityAllRobotQuestions(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # calculatePopularityAllRobotAnswers(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # plotQuestionsByYear(allRobotDataSet)
    print(f"--- {time.time() - start_time:.2f} seconds ---")