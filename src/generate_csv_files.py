import pandas as pd

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

# def doesQuestionIDExist(questionID, robotDataSet):
#     return questionID in robotDataSet['questionId'].values


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



def generateCSVwithMajorThemes(robotDataSet: pd.DataFrame):
    """
    Generates a csv file with the major themes of the robot data set instead of the subthemes
    It is the exact same as the input dataset but with the subthemes replaced with the major themes

    Args:\n
    robotDataSet:
                The dataset to generate the csv file from\n
                It should have a column named 'code' that contains the subthemes\n

    Returns:
        None
    """
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

    robotDataSetCopy = robotDataSet.copy(deep=True)
    robotDataSetCopy['code'] = robotDataSetCopy['code'].apply(lambda x: getMajorTheme(x, themesAndSubThemesDict))
    
    with open('Robot Random (H & S & D) - Coded (no fp) (major themes) (should be updated).csv', 'w', encoding="utf-8") as f:
        robotDataSetCopy.to_csv(f, lineterminator='\n')

def getMajorTheme(subtheme: str, themesAndSubThemesDict: dict) -> str:
    for majorTheme, subThemes in themesAndSubThemesDict.items():
        if subtheme in subThemes:
            return majorTheme
    return 'Unknown'
