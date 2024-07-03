import pandas as pd

def calculatePopularity(allRobotDataSet, allQuestionData, allAnswerDataSet, randomRobotWithCodesData):
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

    dataOther = randomRobotWithCodesData.loc[(randomRobotWithCodesData['code'] == 'gs') | (randomRobotWithCodesData['code'] == 'bp') | (randomRobotWithCodesData['code'] == 'repeat') | (randomRobotWithCodesData['code'] == 'decoupling') | (randomRobotWithCodesData['code'] == 'install') | (randomRobotWithCodesData['code'] == 'ra') | (randomRobotWithCodesData['code'] == 'ros') | (randomRobotWithCodesData['code'] == 'rn') | (randomRobotWithCodesData['code'] == 'dl') | (randomRobotWithCodesData['code'] == 'rl') | (randomRobotWithCodesData['code'] == 'dc') | (randomRobotWithCodesData['code'] == 'distance')]
    calculatePopularityCategoriesGeneral(dataOther, "Other", allPopularityFactorsQuestions, allPopularityFactorsAnswers)

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


if __name__ == "__main__":
    allRobotData = pd.read_csv('allRobotData.csv')
    allQuestionData = pd.read_csv('allQuestionData.csv')
    allAnswerData = pd.read_csv('allAnswerData.csv')
    randomRobotWithCodesData = pd.read_csv('randomRobotWithCodesData.csv')
    randomRobotAllData = pd.read_csv('randomRobotAllData.csv')

    calculatePopularity(allRobotData, allQuestionData, allAnswerData, randomRobotWithCodesData)