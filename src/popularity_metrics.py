import pandas as pd

def calculate_popularity(all_robot: pd.DataFrame, all_SO_q: pd.DataFrame , all_SO_a: pd.DataFrame, random_robot_with_codes_data: pd.DataFrame):
    all_popularity_factors_questions = calculate_popularity_all_robot_questions(all_robot, all_SO_q)
    all_popularity_factors_answers = calculate_popularity_all_robot_answers(all_robot, all_SO_a)
    
    data_specifications = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'api') | 
                                                           (random_robot_with_codes_data['code'] == 'hr') | 
                                                           (random_robot_with_codes_data['code'] == 'os') | 
                                                           (random_robot_with_codes_data['code'] == 'lu')]
    calculate_popularity_categories_general(data_specifications, "Specifications", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_remote = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'wireless') | 
                                                   (random_robot_with_codes_data['code'] == 'cpmr')]
    calculate_popularity_categories_general(data_remote, "Remote", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_connections = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'internet') | 
                                                        (random_robot_with_codes_data['code'] == 'wpi') | 
                                                        (random_robot_with_codes_data['code'] == 'sc')]
    calculate_popularity_categories_general(data_connections, "Connections", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_coordinates = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'position') | 
                                                        (random_robot_with_codes_data['code'] == 'orientation')]
    calculate_popularity_categories_general(data_coordinates, "Coordinates", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_moving = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'mp') | 
                                                   (random_robot_with_codes_data['code'] == 'obstacles') | 
                                                   (random_robot_with_codes_data['code'] == 'mapping') | 
                                                   (random_robot_with_codes_data['code'] == 'SLAM')]
    calculate_popularity_categories_general(data_moving, "Moving", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_actuator = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'ik') | 
                                                     (random_robot_with_codes_data['code'] == 'hc') | 
                                                     (random_robot_with_codes_data['code'] == 'wc') | 
                                                     (random_robot_with_codes_data['code'] == 'mc') | 
                                                     (random_robot_with_codes_data['code'] == 'balance')]
    calculate_popularity_categories_general(data_actuator, "Actuator", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_programming = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'pointers') | 
                                                        (random_robot_with_codes_data['code'] == 'dt') | 
                                                        (random_robot_with_codes_data['code'] == 'overflow') | 
                                                        (random_robot_with_codes_data['code'] == 'list')]
    calculate_popularity_categories_general(data_programming, "Programming", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_error = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'li') | 
                                                  (random_robot_with_codes_data['code'] == 'bf')]
    calculate_popularity_categories_general(data_error, "Library", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_timing = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'timing') | 
                                                   (random_robot_with_codes_data['code'] == 'multithreading') | 
                                                   (random_robot_with_codes_data['code'] == 'rg')]
    calculate_popularity_categories_general(data_timing, "Timing", all_popularity_factors_questions, all_popularity_factors_answers)
    
    data_incoming = random_robot_with_codes_data.loc[(random_robot_with_codes_data['code'] == 'cameras') | 
                                                     (random_robot_with_codes_data['code'] == 'vision') | 
                                                     (random_robot_with_codes_data['code'] == 'line tracking') | 
                                                     (random_robot_with_codes_data['code'] == 'sensors')]
    calculate_popularity_categories_general(data_incoming, "Incoming", all_popularity_factors_questions, all_popularity_factors_answers)

def calculate_popularity_all_robot_answers(all_robot_data, all_answer_data):
    all_robot_answer_popularity_factors = get_robot_answers_popularity_factors(all_robot_data)
    all_answers_popularity_factors = get_all_answers_popularity_factors(all_answer_data)
    normalized_all_robot_answer_popularity_factors = normalize_popularity_factors(all_robot_answer_popularity_factors, all_answers_popularity_factors)
    score = normalized_all_robot_answer_popularity_factors[0]
    comment_count = normalized_all_robot_answer_popularity_factors[1]
    popularity = (score + comment_count) / 2
    
    print(f'''(Hisham) All Robot Answer Popularity Factors:  
    Score: {score:.2f}
    Comment Count: {comment_count:.2f}
    Popularity: {popularity:.2f}\n''')
    all_scores = all_answers_popularity_factors[0]
    all_comment_counts = all_answers_popularity_factors[1]
    return all_scores, all_comment_counts

def get_robot_answers_popularity_factors(robot_data):
    score = calculate_popularity_factor_avg('answer_score', robot_data, 'answer_id')
    comment_count = calculate_popularity_factor_avg('answer_comment_count', robot_data, 'answer_id')
    return score, comment_count

def get_all_answers_popularity_factors(all_answers_data):
    score = calculate_popularity_factor_avg('score', all_answers_data, 'id')
    comment_count = calculate_popularity_factor_avg('comment_count', all_answers_data, 'id')
    return score, comment_count

def calculate_popularity_all_robot_questions(all_robot_data, all_question_data):
    all_robot_popularity_factors = get_robot_questions_popularity_factors(all_robot_data)
    all_questions_popularity_factors = get_all_questions_popularity_factors(all_question_data)
    normalized_all_robot_popularity_factors = normalize_popularity_factors(all_robot_popularity_factors, all_questions_popularity_factors)
    score = normalized_all_robot_popularity_factors[0]
    answer_count = normalized_all_robot_popularity_factors[1]
    comment_count = normalized_all_robot_popularity_factors[2]
    view_count = normalized_all_robot_popularity_factors[3]
    popularity = (score + answer_count + comment_count + view_count) / 4
    print(f'''(Hisham) All Robot Questions Popularity Factors:   
    Score: {score:.2f}
    Answer Count: {answer_count:.2f}
    Comment Count: {comment_count:.2f} 
    View Count: {view_count:.2f}
    Popularity: {popularity:.2f}\n''')
    all_scores = all_questions_popularity_factors[0]
    all_answer_counts = all_questions_popularity_factors[1]
    all_comment_counts = all_questions_popularity_factors[2]
    all_view_counts = all_questions_popularity_factors[3]
    return all_scores, all_answer_counts, all_comment_counts, all_view_counts

def get_robot_questions_popularity_factors(robot_data):
    score = calculate_popularity_factor_avg('question_score', robot_data, 'question_id')
    answer_count = calculate_popularity_factor_avg('answer_count', robot_data, 'question_id')
    comment_count = calculate_popularity_factor_avg('comment_count', robot_data, 'question_id')
    view_count = calculate_popularity_factor_avg('question_view_count', robot_data, 'question_id')
    return score, answer_count, comment_count, view_count

def get_all_questions_popularity_factors(all_questions_data):
    score = calculate_popularity_factor_avg('score', all_questions_data, 'id')
    answer_count = calculate_popularity_factor_avg('answer_count', all_questions_data, 'id')
    comment_count = calculate_popularity_factor_avg('comment_count', all_questions_data, 'id')
    view_count = calculate_popularity_factor_avg('view_count', all_questions_data, 'id')
    return score, answer_count, comment_count, view_count

def calculate_popularity_categories_general(data_set, code_label, all_popularity_factors_questions, all_popularity_factors_answers):
    question_score_all = all_popularity_factors_questions[0]
    question_answer_count_all = all_popularity_factors_questions[1]
    question_comment_count_all = all_popularity_factors_questions[2]
    question_view_count_all = all_popularity_factors_questions[3]
    answer_score_all = all_popularity_factors_answers[0]
    answer_comments_all = all_popularity_factors_answers[1]
    
    question_popularity_factors = get_robot_questions_popularity_factors(data_set)
    answer_popularity_factors = get_robot_answers_popularity_factors(data_set)
    all_questions_popularity_factors = (question_score_all, question_answer_count_all, question_comment_count_all, question_view_count_all)
    all_answers_popularity_factors = (answer_score_all, answer_comments_all)
    normalized_question_popularity_factors = normalize_popularity_factors(question_popularity_factors, all_questions_popularity_factors)
    normalized_answer_popularity_factors = normalize_popularity_factors(answer_popularity_factors, all_answers_popularity_factors)
    question_score = normalized_question_popularity_factors[0]
    answer_count = normalized_question_popularity_factors[1]
    comment_count = normalized_question_popularity_factors[2]
    view_count = normalized_question_popularity_factors[3]
    answer_score = normalized_answer_popularity_factors[0]
    answer_comment_count = normalized_answer_popularity_factors[1]
    question_popularity = (question_score + answer_count + comment_count + view_count) / 4
    answer_popularity = (answer_score + answer_comment_count) / 2
    print(f'''(Hisham) Robot Questions {code_label} Popularity Factors:
    Score: {question_score:.2f}
    Answer Count: {answer_count:.2f}
    Comment Count: {comment_count:.2f}
    View Count: {view_count:.2f}
    Popularity: {question_popularity:.2f}\n''')
    print(f'''(Hisham) Robot Answers {code_label} Popularity Factors:
    Score: {answer_score:.2f}
    Comment Count: {answer_comment_count:.2f}
    Popularity: {answer_popularity:.2f}\n''')

# popularity_factor is the column name of the popularity factor in the dataframe
# dataframe is the dataframe to calculate the popularity factor from
# id_label is the column name of the id in the dataframe
# check for nan because there are a few cells that are empty fsm
def calculate_popularity_factor_avg(popularity_factor, dataframe, id_label):
    popularity_factor_total = 0
    question_ids_seen_set = set()
    total_num_unique_questions = 0
    for index, row in dataframe.iterrows():
        question_id = row[id_label]
        if ((question_id is not None) and 
            (question_id not in question_ids_seen_set) and 
            (not pd.isna(row[popularity_factor]))):
                popularity_factor_count = row[popularity_factor]
                popularity_factor_total += popularity_factor_count
                total_num_unique_questions += 1
                question_ids_seen_set.add(question_id)
    # I don't think this is necessary, but I'm keeping it in case it is
    # because even if 0 questions are found, the popularity factor should be 0 so no division by 0 error
    if total_num_unique_questions == 0:
        return 0
    # return the average popularity factor
    # This is NOT normalizing the factor, it is just the average
    return popularity_factor_total / total_num_unique_questions

def normalize_popularity_factors(popularity_factors, all_popularity_factors):
    normalized_popularity_factors = []
    for i in range(len(popularity_factors)):
        normalized_popularity_factors.append(normalize_popularity_factor(popularity_factors[i], all_popularity_factors[i]))
    return normalized_popularity_factors

def normalize_popularity_factor(popularity_factor, all_popularity_factor):
    return popularity_factor / all_popularity_factor

# if __name__ == "__main__":
#     all_robot_data = pd.read_csv('allRobotData.csv')
#     all_question_data = pd.read_csv('allQuestionData.csv')
#     all_answer_data = pd.read_csv('allAnswerData.csv')
#     random_robot_with_codes_data = pd.read_csv('randomRobotWithCodesData.csv')
#     random_robot_all_data = pd.read_csv('randomRobotAllData.csv')

#     calculate_popularity(all_robot_data, all_question_data, all_answer_data, random_robot_with_codes_data, random_robot_all_data)

if __name__ == "__main__":
    all_robot_data = pd.read_csv(r'C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Research\SORobotProject\RobotDataSet.csv')
    all_question_data = pd.read_csv(r'C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Research\SORobotProject\AllQuestionDataCombined.csv')
    all_answer_data = pd.read_csv(r'C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Research\SORobotProject\AllAnswerDataCombined.csv')
    random_robot_with_codes_data = pd.read_csv(r'C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Research\SORobotProject\Robot Random (H & S & D) - Coded (no fp).csv')
    random_robot_all_data = pd.read_csv(r'C:\Users\hamza\OneDrive - University of Manitoba\Documents\HISHAM\Research\SORobotProject\Robot Random (H & S & D) - Full Coded.csv')

    calculate_popularity(random_robot_with_codes_data, all_question_data, all_answer_data, random_robot_with_codes_data)
