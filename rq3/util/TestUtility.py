import utility


def test_find_indexes(path):
    indexes = utility.find_indexes(path)
    assert indexes['SLOCStandard'] == 3
    assert indexes['SimpleReadability'] == 6
    assert indexes['n1'] == 16
    assert indexes['ChangeAtMethodAge'] == 40
    assert indexes['DiffSizes'] == 44


def test_extract_from_file_with_project():
    path = utility.BASE_PATH + "/data/cleaned/"
    indexes = utility.find_indexes(path)
    selected_features = ['ChangeAtMethodAge', 'DiffSizes', 'NewAdditions', 'EditDistances', 'RiskyCommit', 'file']
    project_data = utility.extract_from_file_with_project(indexes, path, selected_features)

    test_project_data = {}
    test_project_data["argouml.txt"] = {}
    test_project_data["argouml.txt"]["10040.json"] = {}
    test_project_data["argouml.txt"]["10040.json"]["ChangeAtMethodAge"] = ['0', '51', '339', '647', '816', '1536',
                                                                           '1949', '2019', '2271']
    test_project_data["argouml.txt"]["10040.json"]["EditDistances"] = ['0', '11', '5', '16', '19', '1', '0', '0', '31']

    assert project_data["argouml.txt"]["10040.json"]["ChangeAtMethodAge"] == \
           test_project_data["argouml.txt"]["10040.json"]["ChangeAtMethodAge"]


def test_extract_from_file(path):
    given_list_revisions = [[0, 0, 0, 13, 10, 7, 2, 10, 10], [0, 0, 0, 2, 2], [0], [0, 0, 0],
                            [0], [0, 0], [0, 0, 2, 0, 2], [0, 21], [0, 2, 1, 1], [0, 0, 2, 2]
                            ]

    given_ages = [5167, 5167, 2035, 5647, 1165, 1034, 6184, 1908, 1644, 4520]

    indexes = utility.find_indexes(path)
    features = set()
    features.add("ChangeAtMethodAge")
    features.add("DiffSizes")
    features_values = utility.extract_from_file(indexes, path, features)
    equal = 1
    for i in range(len(features_values["ages"])):
        if given_ages[i] != features_values["ages"][i]:
            equal = 0
            break
    assert equal == 1

    equal = 1
    for i in range(len(given_list_revisions)):
        given_revisions = given_list_revisions[i]
        revisions = features_values["DiffSizes"][i]
        for j in range(len(revisions)):
            if int(revisions[j]) != given_revisions[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1

    given_list_change_dates = [[0, 279, 660, 1002, 1402, 1405, 1419, 1509, 1884],
                               [0, 279, 660, 3043, 3139],
                               [0],
                               [0, 758, 1139],
                               [0],
                               [336],
                               [0, 3934, 4255, 4394, 4473],
                               [0, 1010],
                               [0, 0, 212, 221],
                               [0, 2271, 2800, 3586],
                               ]
    equal = 1
    for i in range(len(given_list_change_dates)):
        given_change_dates = given_list_change_dates[i]
        change_dates = features_values["ChangeAtMethodAge"][i]
        for j in range(len(given_change_dates)):
            if int(change_dates[j]) != given_change_dates[j]:
                equal = 0
                break
        if equal == 0:
            break
    assert equal == 1


def calculate_years_from_days_with_ceil():
    assert utility.calculate_years_from_days_with_ceil(731) == 3
    assert utility.calculate_years_from_days_with_ceil(730) == 2
    assert utility.calculate_years_from_days_with_ceil(729) == 2
    assert utility.calculate_years_from_days_with_ceil(366) == 2
    assert utility.calculate_years_from_days_with_ceil(365) == 1
    assert utility.calculate_years_from_days_with_ceil(364) == 1


def test_years_from_days():
    assert utility.calculate_years_from_days(729) == 1
    assert utility.calculate_years_from_days(730) == 2
    assert utility.calculate_years_from_days(731) == 2
    assert utility.calculate_years_from_days(1094) == 2
    assert utility.calculate_years_from_days(1095) == 3
    assert utility.calculate_years_from_days(1096) == 3


def test_ecdf():
    a = [1, 1, 2.2, 2.2, 2, 3, 2, 4]
    x, y = utility.ecdf(a)
    y_expected = [0.25,  0.5,   0.75,  0.875, 1.]
    assert y.tolist() == y_expected


if __name__ == '__main__':
    path = utility.BASE_PATH + "/data/testing_data/"
    test_find_indexes(path)
    test_extract_from_file(path)
    calculate_years_from_days_with_ceil()
    test_years_from_days()
    test_extract_from_file_with_project()
    test_ecdf()
