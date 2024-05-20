import random
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import openpyxl
import time
import math


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
                              'Other' : ['gs', 'bp', 'repeat', 'decoupling', 'install', 'ra', 'ros', 'rn', 'dl', 'rl', 'dc', 'distance']}
    
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

    with open('testingRobotRandomSTOPPP.csv', 'w', encoding="utf-8") as f:
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

if __name__ == "__main__":
    start_time = time.time()

    
    allRobotDataSet = pd.read_csv("RobotDataSet.csv")
    allQuestionDataSet = pd.read_csv("AllQuestionDataCombined.csv")
    allAnswerDataSet = pd.read_csv("AllAnswerDataCombined.csv")
    randomRobotWithCodesDataSet = pd.read_csv("RandomRobot - Coded.csv")
    randomRobotAllDataSet = pd.read_csv("RandomRobot-Full.csv")
    
    getFalsePositiveQuestions(randomRobotWithCodesDataSet, randomRobotAllDataSet)

    # getAllMajorThemeLabels(randomRobotWithCodesDataSet)
    # randomXQuestions(300, allRobotDataSet, randomRobotAllDataSet)

    # calculatePopularity(allRobotDataSet, allQuestionDataSet, allAnswerDataSet, randomRobotWithCodesDataSet, randomRobotAllDataSet)
    # plotQuestionsByYear(allRobotDataSet)
    print(f"--- {time.time() - start_time:.2f} seconds ---")