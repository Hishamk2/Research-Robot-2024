import sys
import os
import pytest
import pandas as pd
from datetime import datetime

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from plot_questions_by_year import plot_questions_per_yr, get_year_counts, process_row

@pytest.fixture
def sample_data():
    data = {
        "questionId": [1, 2, 3, 4],
        "questionCreationDate": ["01/01/2020 00:00", "01/01/2021 00:00", "01/01/2021 00:00", "01/01/2022 00:00"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_data_with_float_dates():
    data = {
        "questionId": [1, 2, 3, 4],
        "questionCreationDate": [43831.0, 44196.0, 44196.0, 44561.0]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_data_with_float_and_str_dates():
    data = {
        "questionId": [1, 2, 3, 4],
        "questionCreationDate": ["01/01/2020 00:00", 44196.0, 44196.0, "01/01/2022 00:00"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_data_with_duplicates():
    data = {
        "questionId": [1, 2, 3, 4, 4],
        "questionCreationDate": ["01/01/2020 00:00", "01/01/2021 00:00", "01/01/2021 00:00", "01/01/2022 00:00", "01/01/2022 00:00"]
    }
    return pd.DataFrame(data)

@pytest.fixture
def sample_row():
    return pd.Series({"questionId": 1, "questionCreationDate": "01/01/2020 00:00"})

@pytest.fixture
def sample_row_with_float_date():
    return pd.Series({"questionId": 2, "questionCreationDate": 43831.0})



def test_plot_questions_per_yr(sample_data):
    expected_result = {2020: 1, 2021: 2, 2022: 1}
    
    result = plot_questions_per_yr(sample_data)
    assert result == expected_result

def test_plot_questions_per_yr_with_float_dates(sample_data_with_float_dates):
    expected_result = {2020: 3, 2021: 1}
    
    result = plot_questions_per_yr(sample_data_with_float_dates)
    assert result == expected_result

def test_plot_questions_per_yr_with_float_and_str_dates(sample_data_with_float_and_str_dates):
    expected_result = {2020: 3, 2022: 1}
    
    result = plot_questions_per_yr(sample_data_with_float_and_str_dates)
    assert result == expected_result

def test_plot_questions_per_yr_with_duplicates(sample_data_with_duplicates):
    expected_result = {2020: 1, 2021: 2, 2022: 1}
    
    result = plot_questions_per_yr(sample_data_with_duplicates)
    assert result == expected_result



def test_get_year_counts(sample_data_with_duplicates):
    expected_result = {2020: 1, 2021: 2, 2022: 1}
    
    result = get_year_counts(sample_data_with_duplicates)
    assert result == expected_result

def test_get_year_counts_with_float_dates(sample_data_with_float_dates):
    expected_result = {2020: 3, 2021: 1}
    
    result = get_year_counts(sample_data_with_float_dates)
    assert result == expected_result

def test_get_year_counts_with_float_and_str_dates(sample_data_with_float_and_str_dates):
    expected_result = {2020: 3, 2022: 1}
    
    result = get_year_counts(sample_data_with_float_and_str_dates)
    assert result == expected_result

def test_get_year_counts_with_duplicates(sample_data_with_duplicates):
    expected_result = {2020: 1, 2021: 2, 2022: 1}
    
    result = get_year_counts(sample_data_with_duplicates)
    assert result == expected_result



def test_process_row(sample_row):
    question_ids_seen = set()
    year_count_dict = {}
    
    expected_question_ids_seen = {1}
    expected_year_count_dict = {2020: 1}
    
    result_dict = process_row(sample_row, question_ids_seen, year_count_dict)
    
    assert question_ids_seen == expected_question_ids_seen
    assert result_dict == expected_year_count_dict

def test_process_row_with_float_date(sample_row_with_float_date):
    question_ids_seen = {1}
    year_count_dict = {2020: 1}
    
    result_dict = process_row(sample_row_with_float_date, question_ids_seen, year_count_dict)
    
    expected_question_ids_seen = {1, 2}
    expected_year_count_dict = {2020: 2}
    
    assert question_ids_seen == expected_question_ids_seen
    assert result_dict == expected_year_count_dict

def test_process_row_duplicate_question(sample_row):
    question_ids_seen = {1}
    year_count_dict = {2020: 1}
    
    result_dict = process_row(sample_row, question_ids_seen, year_count_dict)
    
    assert question_ids_seen == {1}
    assert result_dict == {2020: 1}

# test process row with some numbers in questions_id_seen but not a duplicate question
def test_process_row_not_duplicate_question():
    row = pd.Series({"questionId": 3, "questionCreationDate": "01/01/2020 00:00"})
    question_ids_seen = {1, 2}
    year_count_dict = {2020: 1, 2022: 1}
    
    result_dict = process_row(row, question_ids_seen, year_count_dict)
    
    assert question_ids_seen == {1, 2, 3}
    assert result_dict == {2020: 2, 2022: 1}

def test_process_row_different_year():
    row = pd.Series({"questionId": 3, "questionCreationDate": "01/01/2023 00:00"})
    question_ids_seen = {1, 2}
    year_count_dict = {2020: 1, 2022: 1}
    
    result_dict = process_row(row, question_ids_seen, year_count_dict)
    
    assert question_ids_seen == {1, 2, 3}
    assert result_dict == {2020: 1, 2022: 1, 2023: 1}

def test_process_row_same_year():
    row = pd.Series({"questionId": 3, "questionCreationDate": "01/01/2020 00:00"})
    question_ids_seen = {1, 2}
    year_count_dict = {2020: 1, 2022: 1}
    
    result_dict = process_row(row, question_ids_seen, year_count_dict)
    
    assert question_ids_seen == {1, 2, 3}
    assert result_dict == {2020: 2, 2022: 1}


if __name__ == "__main__":
    pytest.main()
