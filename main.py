import random
import sys
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import openpyxl

# TODO how about converting the csv into a csv with no duplicate questions as we done lots of checking for duplicates

def plotQuestionsByYear():
    questionIdsSeenSet = set()
    yearCountDict = {}
    for index, row in dataRobot.iterrows():
        questionId = row["questionId"]
        #if questionId is in questionIdsSeenSet, it is a duplicate row for comments or answers
        if questionId not in questionIdsSeenSet:
            dateStamp = pd.to_datetime(row["questionCreationDate"], format="%m/%d/%Y %H:%M" )
            if dateStamp.year in yearCountDict.keys():
                yearCountDict[dateStamp.year] = yearCountDict[dateStamp.year] + 1
            else:
                yearCountDict[dateStamp.year] = 0
        questionIdsSeenSet.add(questionId)
    plt.bar(range(len(yearCountDict)), list(yearCountDict.values()), tick_label = list(yearCountDict.keys()), label = "Robot  questions on Stack Overflow by year")
    plt.xticks(fontsize = 20)
    font1 = { 'color': 'black', 'size': 35}
    font2 = { 'color': 'black', 'size': 30}
    plt.xlabel("Year", fontdict=font2)
    plt.ylabel("Number of robot questions asked", fontdict=font2)
    plt.title("Robot  Questions on Stack Overflow by Year", fontdict=font1)
    plt.show()
    return yearCountDict

# popularityFactor is the column name of the popularity factor in the dataframe
# dataframe is the dataframe to calculate the popularity factor from
# idLabel is the column name of the id in the dataframe
def calculatePopularityFactor(popularityFactor, dataframe, idLabel):
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

#creates a new excel file with a subset of X random questions from the supplied question dataset, with the same distribution of years as the original
def randomXQuestions(X, yearDict):
    datax = dataRobot.copy(deep=True)
    datax = datax.drop_duplicates('questionId')
    datax['questionCreationDate'] = pd.to_datetime(datax['questionCreationDate'], format="%m/%d/%Y %H:%M")

    totalQuestions = 0
    for year in yearDict:
        totalQuestions += yearDict[year]

    years = []
    for year in yearDict:
        datayear = datax.loc[(datax['questionCreationDate'] >= '01/01/' + str(year) + ' 0:0') & (datax['questionCreationDate'] < '01/01/' + str(year + 1) + ' 0:0')]
        #calculating the amount of questions to sample for a given year so that it matches the original distribution of questions
        sampleAmount  = round(yearDict[year] * X / totalQuestions)
        datayear = datayear.sample(sampleAmount)
        years.append(datayear)

    randomDataAllYears = pd.concat(years)


    open(randomRobotFile, 'w+')
    randomDataAllYears.to_csv(randomRobotFile)


def calculatePopularity():
    #calculating robot question popularity factors
    questionScoreRobot = calculatePopularityFactor("questionScore", dataRobot,"questionId")
    answerCountRobot = calculatePopularityFactor("AnswerCount",dataRobot,"questionId")
    commentsQuestionRobot = calculatePopularityFactor("CommentCount",dataRobot,"questionId")
   # favoritesRobot = calculatePopularityFactor("questionFavoriteCount",dataRobot,"questionId")
    viewsRobot = calculatePopularityFactor("questionViewCount",dataRobot,"questionId")

    #calculating question popularity factors for all questions
    questionScoreAll = calculatePopularityFactor("Score", dataQuestionAll,"Id")
    answerCountAll = calculatePopularityFactor("AnswerCount",dataQuestionAll, "Id")
    commentsQuestionAll = calculatePopularityFactor("CommentCount",dataQuestionAll,"Id")
   # favoritesAll = calculatePopularityFactor("FavoriteCount",dataQuestionAll,"Id") 
    viewsAll = calculatePopularityFactor("viewCount",dataQuestionAll,"Id")

    #calulating normalized scores for questions
    S = questionScoreRobot / questionScoreAll
    A = answerCountRobot / answerCountAll
    C = commentsQuestionRobot / commentsQuestionAll
    V = viewsRobot / viewsAll
    P = (S + A + C + V)
    p4 = P/4
    print('S: ')
    print(S)
    print('A:')
    print(A)
    print('C')
    print(C)
    print('V:')
    print(V)
    print('P')
    print(P)
    print ('P/4')
    print(p4)

    #calculating robot answer popularity factors
    answerScoreRobot = calculatePopularityFactor("answerScore", dataRobot, "answerId")
    commentsAnswerRobot = calculatePopularityFactor("answerCommentCount", dataRobot, "answerId")


    #calculating overall answer popularity factors
    answerScoreAll = calculatePopularityFactor("Score", dataAnswerAll, "Id")
    commentsAnswerAll = calculatePopularityFactor("CommentCount", dataAnswerAll, "Id")

    # calulating normalized scores for answers
    SAnswer = answerScoreRobot / answerScoreAll
    CAnswer = commentsAnswerRobot / commentsAnswerAll
    PA = (SAnswer + CAnswer)
    PA2 = PA / 2
    print('SAnswer')
    print(SAnswer)
    print('CAnswer')
    print(CAnswer)
    print('PA')
    print(PA)
    print('PA / 2')
    print(PA2)
   # calculatePopularityCategories(questionScoreAll, answerCountAll, commentsQuestionAll, viewsAll) 
    dataConnections = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'internet') | (dataSubsetRobot['code'] == 'wpi') | (
                    dataSubsetRobot['code'] == 'sc')]
    calculatePopularityCategoriesGeneral(dataConnections, "Connections", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataSpecifications = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'api') | (dataSubsetRobot['code'] == 'hr') | (
                dataSubsetRobot['code'] == 'os') | (
                dataSubsetRobot['code'] == 'lu')]
    calculatePopularityCategoriesGeneral(dataSpecifications, "Specifications",questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataRemote = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'wireless') | (dataSubsetRobot['code'] == 'cpmr')]
    calculatePopularityCategoriesGeneral(dataRemote, "Remote",questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataCoordinates =  dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'position') | (dataSubsetRobot['code'] == 'orientation')]
    calculatePopularityCategoriesGeneral(dataCoordinates, "Coordinates", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataMotionPlanning = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'mp') | (dataSubsetRobot['code'] == 'Obstacles') | (
                dataSubsetRobot['code'] == 'Mapping') | (
                dataSubsetRobot['code'] == 'SLAM')]
    calculatePopularityCategoriesGeneral(dataMotionPlanning, "Motion Planning", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataActuator =  dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'ik') | (dataSubsetRobot['code'] == 'hc') | (
                dataSubsetRobot['code'] == 'mc') | (
                dataSubsetRobot['code'] == 'Balance')]
    calculatePopularityCategoriesGeneral(dataActuator, "Actuation ", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataProgramming = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'Pointers') | (dataSubsetRobot['code'] == 'dt') | (
                dataSubsetRobot['code'] == 'overflow') | (
                dataSubsetRobot['code'] == 'list')]
    calculatePopularityCategoriesGeneral(dataProgramming, "Programming", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataErrors = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'li') | (dataSubsetRobot['code'] == 'bf')]
    calculatePopularityCategoriesGeneral(dataErrors, "Errors",questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll )

    dataTiming = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'Timing') | (dataSubsetRobot['code'] == 'multithreading') | (
                    dataSubsetRobot['code'] == 'rg')]
    calculatePopularityCategoriesGeneral(dataTiming, "Timing", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

    dataIncoming = dataSubsetRobot.loc[
        (dataSubsetRobot['code'] == 'Cameras') | (dataSubsetRobot['code'] == 'Vision') | (
                dataSubsetRobot['code'] == 'line tracking') | (
                dataSubsetRobot['code'] == 'sensors')]
    calculatePopularityCategoriesGeneral(dataIncoming, "Incoming", questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll,answerScoreAll, commentsAnswerAll)

#generalized method for calculating the popularity for a category.
def calculatePopularityCategoriesGeneral(dataSet, themeLabel, questionScoreAll, answerCountAll, commentsQuestionAll,viewsAll, answerScoreAll, commentsAnswerAll):
    questionScoreCategory = calculatePopularityFactor("questionScore", dataSet, "questionId")
    answerCountCategory = calculatePopularityFactor("AnswerCount", dataSet, "questionId")
    commentsCategory = calculatePopularityFactor("CommentCount", dataSet, "questionId")
    viewsCategory = calculatePopularityFactor("questionViewCount", dataSet, "questionId")
    # calulating normalized scores for questions
    S = questionScoreCategory / questionScoreAll
    A = answerCountCategory / answerCountAll
    C = commentsCategory / commentsQuestionAll
    V = viewsCategory / viewsAll
    P = (S + A + C + V)
    p4 = P / 4
    print(themeLabel +' S: ')
    print(S)
    print(themeLabel +' A:')
    print(A)
    print(themeLabel + ' C')
    print(C)
    print(themeLabel +' V:')
    print(V)
    print(themeLabel +' P')
    print(P)
    print(themeLabel + ' P/4')
    print(p4)

    answerScoreCategory = calculatePopularityFactor("answerScore", dataSet, "answerId")
    commentsAnswerCategory = calculatePopularityFactor("answerCommentCount", dataSet, "answerId")

    SAnswer = answerScoreCategory / answerScoreAll
    CAnswer = commentsAnswerCategory / commentsAnswerAll
    PA = (SAnswer + CAnswer)
    PA2 = PA / 2
    print(themeLabel + ' SAnswer')
    print(SAnswer)
    print(themeLabel + ' CAnswer')
    print(CAnswer)
    print(themeLabel + ' PA')
    print(PA)
    print(themeLabel + ' PA / 2')
    print(PA2)



if __name__ == '__main__':
    if len(sys.argv)!=6:
        print('''   
                enter a csv file with the robot dataset as the first command line argument and 
                the overall question dataset as the second command line argument
                and the overall answer dataset as the third command line argument 
                and the path of the file to create for the random robot question dataset as the fourth command line argument 
                and the file of the subset of robot questions for thematic analysis as the fifth command line argument''')
    else:
        csvFileRobot = sys.argv[1]
        dataRobot = pd.read_csv(csvFileRobot)
        csvFileQuestionAll= sys.argv[2]
        dataQuestionAll = pd.read_csv(csvFileQuestionAll)
        csvFileAnswerAll = sys.argv[3]
        dataAnswerAll = pd.read_csv(csvFileAnswerAll)
        yearDict = plotQuestionsByYear()
        randomRobotFile = sys.argv[4]

        #The following is how I got my robot subset of qs, commented out to not generate new random qs
       # randomXQuestions(300, yearDict) 

        thematicAnalysisFile = sys.argv[5]
        dataSubsetRobot = pd.read_csv(thematicAnalysisFile)
        calculatePopularity()