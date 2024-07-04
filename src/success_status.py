import pandas as pd

def getSuccessStatusPercentagePerTheme(dataset: pd.DataFrame) -> dict:
    """
    Get the percentage of unsuccessful, ordinary, and successful questions per theme

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AcceptedAnswerId", "AnswerCount", and "code"
            Also, the dataset should NOT have any duplicate questions

    Returns:
        dict: a dictionary where the keys are the major themes and the values are the percentage of unsuccessful, ordinary, and successful questions per theme
        In the form of: {theme: {'Unsuccessful': percentage%, 'Ordinary': percentage%, 'Successful': percentage%}}
    """

    unsuccessfulQuestionsPerTheme = getUnsuccessfulQuestionsPerTheme(dataset)
    ordinaryQuestionsPerTheme = getOrdinaryQuestionsPerTheme(dataset)
    successfulQuestionsPerTheme = getSuccessfulQuestionsPerTheme(dataset)

    successStatusPercentagePerTheme = {}

    for theme in unsuccessfulQuestionsPerTheme.keys():
        unsuccessfulPercentage = (unsuccessfulQuestionsPerTheme[theme] / (unsuccessfulQuestionsPerTheme[theme] + ordinaryQuestionsPerTheme[theme] + successfulQuestionsPerTheme[theme])) * 100
        ordinaryPercentage = (ordinaryQuestionsPerTheme[theme] / (unsuccessfulQuestionsPerTheme[theme] + ordinaryQuestionsPerTheme[theme] + successfulQuestionsPerTheme[theme])) * 100
        successfulPercentage = (successfulQuestionsPerTheme[theme] / (unsuccessfulQuestionsPerTheme[theme] + ordinaryQuestionsPerTheme[theme] + successfulQuestionsPerTheme[theme])) * 100
        successStatusPercentagePerTheme[theme] = {'Unsuccessful': f"{unsuccessfulPercentage:.2f}%", 'Ordinary': f"{ordinaryPercentage:.2f}%", 'Successful': f"{successfulPercentage:.2f}%"}
    
    return successStatusPercentagePerTheme

def getUnsuccessfulQuestionsPerTheme(dataset: pd.DataFrame) -> dict:
    """
    Gets the number of unsuccessful questions per theme in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            It should have a column named 'AnswerCount' that contains the number of answers to the question\n
            AND a column named 'code' that contains the MAJOR THEME LABEL\n
            The dataset should NOT have any duplicate questions

    Returns:
        dict: a dictionary where the keys are the major themes and the values are the number of unsuccessful questions per theme
        In the form of: {theme: count}
    """
    
    # An unsuccessful question is when there is no answer to the question
    unsuccessfulQuestionsPerTheme = {}

    for index, row in dataset.iterrows():
        if row['AnswerCount'] == 0:
            if row['code'] in unsuccessfulQuestionsPerTheme:
                unsuccessfulQuestionsPerTheme[row['code']] += 1
            else:
                unsuccessfulQuestionsPerTheme[row['code']] = 1
    
    return unsuccessfulQuestionsPerTheme

def getOrdinaryQuestionsPerTheme(dataset: pd.DataFrame) -> dict:
    """
    Gets the number of ordinary questions per theme in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            It should have a column named 'AcceptedAnswerId' that contains the accepted answer id
            AND a column named 'AnswerCount' that contains the number of answers to the question
            AND a column named 'code' that contains the MAJOR THEME LABEL
            The dataset should NOT have any duplicate questions

    Returns:
        dict: a dictionary where the keys are the major themes and the values are the number of ordinary questions per theme
        In the form of: {theme: count}
    """

    # An ordinary question is when there is no accepted answer to the question BUT there are answer(s) to the question
    ordinaryQuestionsPerTheme = {}

    for index, row in dataset.iterrows():
        # If no value for AcceptedAnswerId, that means no accepted answer
        if pd.isna(row['AcceptedAnswerId']) and row['AnswerCount'] > 0:
            if row['code'] in ordinaryQuestionsPerTheme:
                ordinaryQuestionsPerTheme[row['code']] += 1
            else:
                ordinaryQuestionsPerTheme[row['code']] = 1
    
    return ordinaryQuestionsPerTheme

def getSuccessfulQuestionsPerTheme(dataset: pd.DataFrame) -> dict:
    """
    Gets the number of successful questions per theme in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AcceptedAnswerId" and "code"\n
            Also, the dataset should NOT have any duplicate questions\n
            AND a column named 'code' that contains the MAJOR THEME LABEL\n


    Returns:
        dict: a dictionary where the keys are the major themes and the values are the number of successful questions per theme
        In the form of: {theme: count}
    """
    
    # A successful question is when there is an accepted answer to the question
    successfulQuestionsPerTheme = {}
    for index, row in dataset.iterrows():
        if not pd.isna(row['AcceptedAnswerId']):
            if row['code'] in successfulQuestionsPerTheme:
                successfulQuestionsPerTheme[row['code']] += 1
            else:
                successfulQuestionsPerTheme[row['code']] = 1
    return successfulQuestionsPerTheme


def getSuccessStatusPercentage(dataset: pd.DataFrame) -> dict:
    """
    Get the percentage of unsuccessful, ordinary, and successful questions

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AcceptedAnswerId" and "AnswerCount"
            Also, the dataset should NOT have any duplicate questions

    Returns:
        dict: a dictionary where the keys are the success status and the values are the percentage of that success status
        In the form of: {'Unsuccessful': percentage%, 'Ordinary': percentage%, 'Successful': percentage%}
    """

    unsuccessfulQuestions = getUnsuccessfulQuestions(dataset)
    ordinaryQuestions = getOrdinaryQuestions(dataset)
    successfulQuestions = getNumSuccessfulQuestions(dataset)
    
    totalQuestions = unsuccessfulQuestions + ordinaryQuestions + successfulQuestions
    unsuccessfulPercentage = (unsuccessfulQuestions / totalQuestions) * 100
    ordinaryPercentage = (ordinaryQuestions / totalQuestions) * 100
    successfulPercentage = (successfulQuestions / totalQuestions) * 100

    return {'Unsuccessful': f"{unsuccessfulPercentage:.2f}%", 'Ordinary': f"{ordinaryPercentage:.2f}%", 'Successful': f"{successfulPercentage:.2f}%"}

def getUnsuccessfulQuestions(dataset: pd.DataFrame) -> int:
    """
    Gets the number of unsuccessful questions in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AnswerCount"
            Also, the dataset should NOT have any duplicate questions

    Returns:
        int: the number of unsuccessful questions
    """

    # An unsuccessful question is when there is no answer to the question
    count = 0
    for index, row in dataset.iterrows():
        if row['AnswerCount'] == 0:
            count += 1
    return count

def getOrdinaryQuestions(dataset: pd.DataFrame) -> int:
    """
    Gets the number of ordinary questions in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AcceptedAnswerId" and "AnswerCount"
            Also, the dataset should NOT have any duplicate questions

    Returns:
        int: the number of ordinary questions
    """
    count = 0
    # An ordinary question is when there is no accepted answer to the question BUT there are answer(s) to the question
    # If no value for AcceptedAnswerId, that means no accepted answer
    for index, row in dataset.iterrows():
        if pd.isna(row['AcceptedAnswerId']) and row['AnswerCount'] > 0:
            count += 1
    return count

def getNumSuccessfulQuestions(dataset: pd.DataFrame) -> int:
    """
    Gets the number of successful questions in the passed in data set

    Parameters:
        dataset: pd.DataFrame
            The DataFrame containing the question data, must have columns "AcceptedAnswerId"
            Also, the dataset should NOT have any duplicate questions

    Returns:
        int
            The number of successful questions
    """

    # A successful question is when there is an accepted answer to the question
    # Note this works becaue there is at most one accepted answer per question and thus the count of accepted answer ids is the number of successful questions
    return dataset['AcceptedAnswerId'].count()

if __name__ == "__main__":
    robotMajorThemesDataSet = pd.read_csv("../Robot Random (H & S & D) - Coded (no fp) (major themes) (should be updated).csv")

    print(getSuccessStatusPercentagePerTheme(robotMajorThemesDataSet))
    print(getSuccessStatusPercentage(robotMajorThemesDataSet))