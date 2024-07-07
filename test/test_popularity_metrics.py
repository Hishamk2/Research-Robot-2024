import sys
import os
import pytest
import pandas as pd
from datetime import datetime

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from popularity_metrics import (
    calculate_pop,
    calculate_pop_all_robot_a,
    get_robot_a_pop_factors,
    get_all_SO_a_pop_factors,
    calculate_popularity_all_robot_questions,
    get_robot_questions_popularity_factors,
    get_all_questions_popularity_factors,
    calculate_popularity_categories_general,
    calculate_popularity_factor_avg,
    normalize_popularity_factors,
    normalize_popularity_factor
)

@pytest.fixture
def sample_data():
    return pd.DataFrame({
        'questionId': [1, 2, 3, 4],
        'answerScore': [6, 11, 3, 8],
        'answerCommentCount': [2, 5, 1, 4],
        'answerId': [1, 2, 3, 4],
        'questionScore': [4, 7, 6, 9],
        'AnswerCount': [2, 3, 1, 4],
        'CommentCount': [1, 2, 1, 3],
        'questionViewCount': [100, 200, 150, 250]
    })

@pytest.fixture
def sample_data_duplicate_id():
    return pd.DataFrame({
        'questionId': [1, 2, 3, 4, 4],
        'answerScore': [6, 11, 3, 8, 8],
        'answerCommentCount': [2, 5, 1, 4, 4],
        'answerId': [1, 2, 3, 4, 5],
        'questionScore': [4, 7, 6, 9, 9],
        'AnswerCount': [2, 3, 1, 4, 4],
        'CommentCount': [1, 2, 1, 3, 3],
        'questionViewCount': [100, 200, 150, 250, 250]
    })

@pytest.fixture
def sample_data_with_themes():
    data = {
        'code': ['api', 'hr', 'internet', 'position', 'mp', 'ik', 'pointers', 'li', 'timing', 'cameras'],
        'questionScore': [10, 20, 15, 5, 30, 25, 0, 10, 5, 2],
        'AnswerCount': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'CommentCount': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'questionViewCount': [100, 200, 150, 50, 300, 250, 0, 100, 50, 20],
        'questionId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        'answerScore': [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        'answerCommentCount': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        'answerId': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    }
    return pd.DataFrame(data)

@pytest.fixture
def all_pop_factors_questions():
    # score, answer_count, comment_count, view_count
    return [1, 2, 3, 4]

@pytest.fixture
def all_pop_factors_answers():
    # score, comment_count
    return [1, 2]

def test_calculate_popularity_categories_general():
    pass


def test_calculate_popularity_factor_avg(sample_data):
    assert calculate_popularity_factor_avg('answerScore', sample_data, 'questionId') == 7
    assert calculate_popularity_factor_avg('answerCommentCount', sample_data, 'questionId') == 3
    assert calculate_popularity_factor_avg('questionScore', sample_data, 'questionId') == 6.5
    assert calculate_popularity_factor_avg('AnswerCount', sample_data, 'questionId') == 2.5
    assert calculate_popularity_factor_avg('CommentCount', sample_data, 'questionId') == 1.75
    assert calculate_popularity_factor_avg('questionViewCount', sample_data, 'questionId') == 175

    
def test_calculate_popularity_factor_avg_duplicate_id(sample_data_duplicate_id):
    assert calculate_popularity_factor_avg('answerScore', sample_data_duplicate_id, 'questionId') == 7
    assert calculate_popularity_factor_avg('answerCommentCount', sample_data_duplicate_id, 'questionId') == 3
    assert calculate_popularity_factor_avg('questionScore', sample_data_duplicate_id, 'questionId') == 6.5
    assert calculate_popularity_factor_avg('AnswerCount', sample_data_duplicate_id, 'questionId') == 2.5
    assert calculate_popularity_factor_avg('CommentCount', sample_data_duplicate_id, 'questionId') == 1.75
    assert calculate_popularity_factor_avg('questionViewCount', sample_data_duplicate_id, 'questionId') == 175


def test_normalize_popularity_factors():
    assert normalize_popularity_factors([1, 2, 3],[1, 2, 3]) == [1, 1, 1]
    assert normalize_popularity_factors([1, 2, 3],[1, 1, 1]) == [1, 2, 3]
    assert normalize_popularity_factors([1, 2, 3],[2, 2, 2]) == [0.5, 1, 1.5]
    assert normalize_popularity_factors([1, 2, 3],[3, 3, 3]) == [1/3, 2/3, 1]

def test_normalize_popularity_factor():
    assert normalize_popularity_factor(1, 1) == 1
    assert normalize_popularity_factor(2, 1) == 2
    assert normalize_popularity_factor(1, 2) == 0.5