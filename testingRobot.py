import random
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import openpyxl
import time
import math
from datetime import datetime, timedelta


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

    dataError = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'li') | (randomRobotWithCodesData['code'] == 'bf')]
    calculatePopularityCategoriesGeneral(dataError, "Library", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

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
    
    print(f'''(Hisham) All Robot Answer Popularity Factors:  
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

    print(f'''(Hisham) All Robot Questions Popularity Factors:   
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

    print(f'''(Hisham) Robot Questions {codeLabel} Popularity Factors:
    Score: {questionScore:.2f}
    Answer Count: {answerCount:.2f}
    Comment Count: {commentCount:.2f}
    View Count: {viewCount:.2f}
    Popularity: {questionPopularity:.2f}\n''')

    print(f'''(Hisham) Robot Answers {codeLabel} Popularity Factors:
    Score: {answerScore:.2f}
    Comment Count: {answerCommentCount:.2f}
    Popularity: {answerPopularity:.2f}\n''')
    


# popularityFactor is the column name of the popularity factor in the dataframe
# dataframe is the dataframe to calculate the popularity factor from
# idLabel is the column name of the id in the dataframe
# check for nan because there are a few cells that are empty fsm
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


# confirm the passed in csv files have all the above theme labels as well as make sure there are 10, and only 10, theme labels 
# the theme labels are (specifications, remote, connections, coordinates, moving, actuator, programming, error, timing, incoming)
def getAllMajorThemeLabels(robotCodedData):
    allMajorThemes = set()
    allSubThemes = getAllSubThemeLabels(robotCodedData)
    themesAndSubThemesDict = {'Specifications': ['api', 'hr', 'os', 'lu'], 
                              'Remote': ['wireless', 'cpmr'],
                              'Connections': ['internet', 'wpi', 'sc'],
                              'Coordinates': ['position', 'orientation'],
                              'Moving': ['mp', 'obstacles', 'mapping', 'SLAM'],
                              'Actuator': ['ik', 'hc', 'wc', 'mc', 'balance'],
                              'Programming': ['pointers', 'dt', 'overflow', 'list'],
                              'Error': ['li', 'bf'],
                              'Timing': ['timing', 'multithreading', 'rg'],
                              'Incoming': ['cameras', 'vision', 'line tracking', 'sensors'],
                              'Other' : ['fp', 'gs', 'bp', 'repeat', 'decoupling', 'install', 'ra', 'ros', 'rn', 'dl', 'rl', 'dc', 'distance']}
    
    # make sure all subThemes from Appendix A are in the dataset
    for theme in themesAndSubThemesDict.keys():
        allMajorThemes.add(theme)
        for subTheme in themesAndSubThemesDict[theme]:
            if subTheme not in allSubThemes.values():
                print(f"Subtheme `{subTheme}` (from Appendix A) not found in the dataset")

    # make sure all subThemes from dataset are in Appendix A
    for subTheme in allSubThemes.items():
        found = False
        for theme in themesAndSubThemesDict.keys():
            if subTheme[1] in themesAndSubThemesDict[theme]:
                found = True
                break
        if not found:
            print(f"Subtheme (from dataset) `{subTheme[1]}` at index {subTheme[0]} (probably line {subTheme[0] + 2}) not found in the theme dictionary (Appendix A)")
    

def getAllSubThemeLabels(robotCodedData):
    allSubThemes = {}
    for index, row in robotCodedData.iterrows():
        if pd.isna(row["code"]):
            print(f"Cell for codes at index {index} (probably line {index + 2}) is empty")
        else:        
            code = row["code"]
            allSubThemes[index] = code
    return allSubThemes


def randomXQuestions(numQuestions, allRobotDataSet: pd.DataFrame, previousRandomQuestions: pd.DataFrame):
    copyAllRobotDataSet = allRobotDataSet.copy(deep=True) #why do deep copy? because we don't want to change the original dataset
    copyAllRobotDataSet = copyAllRobotDataSet.drop_duplicates('questionId')
    
    listQuestionIdPreviousRandom = getListOfQuestionIds(previousRandomQuestions)    

    # now drop duplcates that are in the previous random questions
    copyAllRobotDataSet = copyAllRobotDataSet.drop(axis=0, index=copyAllRobotDataSet[copyAllRobotDataSet['questionId'].isin(listQuestionIdPreviousRandom)].index)

    randomQuestions = copyAllRobotDataSet.sample(n=numQuestions)

    with open('testingRobotRandomSTOPafsPP.csv', 'w', encoding="utf-8") as f:
        randomQuestions.to_csv(f, lineterminator='\n')

    print(f'Are questions from the new random questions unique from the previous random questions? {areQuestionsUnique(randomQuestions, previousRandomQuestions)}\n')
    plotQuestionsByYear(randomQuestions)

def areQuestionsUnique(dataSet: pd.DataFrame, previousDataSet: pd.DataFrame):
    dataSetQuestionIds = getListOfQuestionIds(dataSet)
    previousDataSetQuestionIds = getListOfQuestionIds(previousDataSet)

    for questionId in dataSetQuestionIds:
        if questionId in previousDataSetQuestionIds:
            return False
    return True

def getListOfQuestionIds(dataSet: pd.DataFrame):
    listOfQuestionIds = dataSet['questionId'].values.tolist()
    return listOfQuestionIds

def doesQuestionIDExist(questionID, robotDataSet):
    return questionID in robotDataSet['questionId'].values


# Get list of all questionIds from codedRobot and allRobot
# compare which questionIds are in allRobot but not in codedRobot (those were removed, the false positives)
# extract the rows from the above questionIds
def getFalsePositiveQuestions(codedRobot: pd.DataFrame, allRobot: pd.DataFrame):
    codedRobotQuestionIds = getListOfQuestionIds(codedRobot)
    allRobotQuestionIds = getListOfQuestionIds(allRobot)

    falsePositiveQuestionIds = list(set(allRobotQuestionIds) - set(codedRobotQuestionIds))

    falsePositiveQuestions = allRobot.loc[allRobot['questionId'].isin(falsePositiveQuestionIds)]

    with open('testingRobotFalsePositive.csv', 'w', encoding="utf-8") as f:
        falsePositiveQuestions.to_csv(f, lineterminator='\n')
    
    print(f"Number of false positive questions: {len(falsePositiveQuestions)}")



def getSuccessStatusPercentage(unsuccessfulQuestions: int, ordinaryQuestions: int, successfulQuestions: int) -> dict:
    """
    Get the percentage of unsuccessful, ordinary, and successful questions

    Args:\n
    unsuccessfulQuestions:
            The number of unsuccessful questions\n
    ordinaryQuestions:
            The number of ordinary questions\n
    successfulQuestions:
            The number of successful questions\n

    Returns:
        dict: a dictionary where the keys are the success status and the values are the percentage of that success status
    """
    totalQuestions = unsuccessfulQuestions + ordinaryQuestions + successfulQuestions
    unsuccessfulPercentage = (unsuccessfulQuestions / totalQuestions) * 100
    ordinaryPercentage = (ordinaryQuestions / totalQuestions) * 100
    successfulPercentage = (successfulQuestions / totalQuestions) * 100
    return {'Unsuccessful': f"{unsuccessfulPercentage:.2f}%", 'Ordinary': f"{ordinaryPercentage:.2f}%", 'Successful': f"{successfulPercentage:.2f}%"}

def getUnsuccessfulQuestions(dataset: pd.DataFrame):
    """
    An unsuccessful question is when there is no answer to the question

    Args:\n
    dataset:
            The dataset to get the number of unsuccessful questions from\n
            It should have a column named 'AnswerCount' that contains the number of answers to the question\n
            The dataset should NOT have any duplicate questions

    Returns:
        int: the number of unsuccessful questions
    """
    count = 0
    for index, row in dataset.iterrows():
        if row['AnswerCount'] == 0:
            count += 1
    return count

def getOrdinaryQuestions(dataset: pd.DataFrame):
    """
    An ordinary question is when there is no accepted answer to the question BUT there are answer(s) to the question

    Args:\n
    dataset:
            The dataset to get the number of ordinary questions from\n
            It should have a column named 'AcceptedAnswerId' that contains the accepted answer id\n
            AND a column named 'AnswerCount' that contains the number of answers to the question\n
            The dataset should NOT have any duplicate questions

    Returns:
        int: the number of ordinary questions
    """
    count = 0
    for index, row in dataset.iterrows():
        if pd.isna(row['AcceptedAnswerId']) and row['AnswerCount'] > 0:
            count += 1
    return count

def getNumSuccessfulQuestions(dataset: pd.DataFrame):
    """
    A successful question is when there is an accepted answer to the question

    Args:\n
    dataset: 
            The dataset to get the number of successful questions from\n
            It should have a column named 'AcceptedAnswerId' that contains the accepted answer id\n
            The dataset should NOT have any duplicate questions 

    Returns:
        int: the number of successful questions
    """
    # TODO maybe also check tomake sure answercount >= 1 to make sure no accidents
    return dataset['AcceptedAnswerId'].count()


def getPercentageMajorThemes(majorThemes: dict) -> dict:
    """
    Get percentage of each major theme in the dataset (EXCLUDING FALSE POSITIVES)

    Args:\n
    majorThemes: 
                The major themes to get the percentage of\n
                It should be a dictionary where the keys are the major themes and the values are the number of times that major theme appears in the data set
    
    Returns:
        dict: a dictionary where the keys are the major themes and the values are the percentage of that major theme in the data set
    """
    totalThemes = sum(majorThemes.values())
    percentageMajorThemes = {}
    for theme, count in majorThemes.items():
        percentage = (count / totalThemes) * 100
        percentageMajorThemes[theme] = f"{percentage:.2f}%"
    return percentageMajorThemes

def getNumMajorThemes(subThemes: dict):
    """
    Gets the number of major themes from the subthemes as defined in Appendix A (as below)
        'Specifications': ['api', 'hr', 'os', 'lu'], 
        'Remote': ['wireless', 'cpmr'],
        'Connections': ['internet', 'wpi', 'sc'],
        'Coordinates': ['position', 'orientation'],
        'Moving': ['mp', 'obstacles', 'mapping', 'SLAM'],
        'Actuator': ['ik', 'hc', 'wc', 'mc', 'balance'],
        'Programming': ['pointers', 'dt', 'overflow', 'list'],
        'Error': ['li', 'bf'],
        'Timing': ['timing', 'multithreading', 'rg'],
        'Incoming': ['cameras', 'vision', 'line tracking', 'sensors'],
        'Other' : ['gs', 'bp', 'repeat', 'decoupling', 'install', 'ra', 'ros', 'rn', 'dl', 'rl', 'dc', 'distance']

    Args:\n
    subThemes: 
                The subthemes to get the number of major themes from\n
                It should be a dictionary where the keys are the indices of the subthemes and the values are the subthemes
    
    Returns:
        dict: a dictionary where the keys are the major themes and the values are the number of times that major theme appears in the data set
    """
    majorThemes = {}
    themesAndSubThemesDict = {'Specifications': ['api', 'hr', 'os', 'lu'], 
                              'Remote': ['wireless', 'cpmr'],
                              'Connections': ['internet', 'wpi', 'sc'],
                              'Coordinates': ['position', 'orientation'],
                              'Moving': ['mp', 'obstacles', 'mapping', 'SLAM'],
                              'Actuator': ['ik', 'hc', 'wc', 'mc', 'balance'],
                              'Programming': ['pointers', 'dt', 'overflow', 'list'],
                              'Error': ['li', 'bf'],
                              'Timing': ['timing', 'multithreading', 'rg'],
                              'Incoming': ['cameras', 'vision', 'line tracking', 'sensors'],
                              'Other' : ['gs', 'bp', 'repeat', 'decoupling', 'install', 'ra', 'ros', 'rn', 'dl', 'rl', 'dc', 'distance']}
    for index, subTheme in subThemes.items():
        found = False
        for theme in themesAndSubThemesDict.keys():
            if subTheme in themesAndSubThemesDict[theme]:
                found = True
                if theme in majorThemes:
                    majorThemes[theme] += 1
                else:
                    majorThemes[theme] = 1
                break
    return majorThemes

def getNumSubThemes(allRobotDataSet):
    """
    Gets the number of subthemes in the passed in data set
    Subthemes are the 'code' column in the data set

    Args:\n
    allRobotDataSet: 
                    The dataset to get the number of sub themes from\n
                    It should have a column named 'code' that contains the sub themes

    Returns:
        dict: a dictionary where the keys are the sub themes and the values are the number of times that sub theme appears in the data set
    """
    subThemes = {}
    for index, row in allRobotDataSet.iterrows():
        # if pd.isna(row["code"]):
        #     print(f"Cell for codes at index {index} (probably line {index + 2}) is empty")            
        code = row["code"]
        if code in subThemes:
            subThemes[code] += 1
        else:
            subThemes[code] = 1
    return subThemes

def prettyPrintDict(dictionary):
    # pretty pring the dictionary in alphabetical order
    # for key in sorted(dictionary.keys()):
    #     print(f"{key}: {dictionary[key]}")
    for key, value in dictionary.items():
        print(f"{key}: {value}")

# TODO MAKE SURE GET THE NUM OF DIFF TYPES OF QUESTIONS FROM THE DATA SET WITH NOOOOO FALSE POSITIVES
if __name__ == "__main__":
    start_time = time.time()

    
    allRobotDataSet = pd.read_csv("RobotDataSet.csv")
    allQuestionDataSet = pd.read_csv("AllQuestionDataCombined.csv")
    allAnswerDataSet = pd.read_csv("AllAnswerDataCombined.csv")
    randomRobotWithCodesDataSet = pd.read_csv("Robot Random (H & S & D) - Coded (no fp).csv")
    randomRobotAllDataSet = pd.read_csv("Robot Random (H & S & D) - Full Coded.csv")
    robotMajorThemesDataSet = pd.read_csv("Robot Random (H & S & D) - Coded (no fp) (major themes).csv")
    
    # getFalsePositiveQuestions(randomRobotWithCodesDataSet, randomRobotAllDataSet)

    # getAllMajorThemeLabels(randomRobotWithCodesDataSet)
    # randomXQuestions(300, allRobotDataSet, randomRobotAllDataSet)

    # randomXQuestions(50, allRobotDataSet, randomRobotAllDataSet)

    # getAllMajorThemeLabels(randomRobotAllDataSet)

    prettyPrintDict(getSuccessStatusPercentage(getUnsuccessfulQuestions(randomRobotWithCodesDataSet), getOrdinaryQuestions(randomRobotWithCodesDataSet), getNumSuccessfulQuestions(randomRobotWithCodesDataSet)))
    prettyPrintDict(getSuccessStatusPercentagePerTheme(getUnsuccessfulQuestionsPerTheme(robotMajorThemesDataSet), getOrdinaryQuestionsPerTheme(robotMajorThemesDataSet), getSuccessfulQuestionsPerTheme(robotMajorThemesDataSet)))

    # numSubThemes = getNumSubThemes(randomRobotAllDataSet)
    # numMajorThemes = getNumMajorThemes(numSubThemes)
    # percentageMajorThemes = getPercentageMajorThemes(numMajorThemes)
    # prettyPrintDict(numSubThemes)
    # prettyPrintDict(numMajorThemes)
    # prettyPrintDict(percentageMajorThemes)
    # For SOME REASON I DONT KNOW WHY, the above code does not print the same thing a below, use below
    # prettyPrintDict(getNumSubThemes(randomRobotAllDataSet))
    # prettyPrintDict(getNumMajorThemes(getAllSubThemeLabels(randomRobotAllDataSet)))
    # prettyPrintDict(getPercentageMajorThemes(getNumMajorThemes(getAllSubThemeLabels(randomRobotAllDataSet))))

    # generateCSVwithMajorThemes(randomRobotWithCodesDataSet)

    # print(f"Number of unsuccessful questions: {getUnsuccessfulQuestions(randomRobotWithCodesDataSet)}")
    # print(f"Number of ordinary questions: {getOrdinaryQuestions(randomRobotWithCodesDataSet)}")
    # print(f"Number of successful questions: {getNumSuccessfulQuestions(randomRobotWithCodesDataSet)}")

    # calculatePopularity(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # getAllMajorThemeLabels(randomRobotWithCodesDataSet)
    # plotQuestionsByYear(randomRobotWithCodesDataSet)

    # getAllMajorThemeLabels(randomRobotAllDataSet)

    # calculatePopularity(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # plotQuestionsByYear(randomRobotWithCodesDataSet)
    # plotQuestionsByYear(allRobotDataSet)
    print(f"--- {time.time() - start_time:.2f} seconds ---")