import os
import math
import numpy as np

BASE_PATH = "/home/shaiful/research/good_bad_ugy"

apply_age_restriction = True
age_restriction = 5 * 365
total_change = 0
minimum_required_methods = 30
given_percent_methods = [5, 10, 15, 20]
restrict_zero_revs = True
change_legends = ["Revisions", "Additions", "DiffSizes", "EditDistances"]
def find_indexes(SRC_PATH):
    indexes = {}
    fr = open(SRC_PATH + "checkstyle.txt")
    line = fr.readline()
    fr.close()
    data = line.strip().split("\t")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes


def extract_from_file(indexes, SRC_PATH, features):
    collect_fields = {}
    for feature in features:
        collect_fields[feature] = []
    collect_fields["ages"] = []
    for file in os.listdir(SRC_PATH):
        fr = open(SRC_PATH + file)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            collect_fields["ages"].append(int(data[0]))
            for feature in features:
                collect_fields[feature].append(data[indexes[feature]].split(","))
    return collect_fields


def ecdf(a):
    x, counts = np.unique(a, return_counts=True)
    cusum = np.cumsum(counts)
    return x, cusum / cusum[-1]


def extract_from_file_with_project(indexes, SRC_PATH, features):
    project_data = {}
    for project in os.listdir(SRC_PATH):
        project_data[project] = {}

        fr = open(SRC_PATH + project)
        fr.readline()  # ignore the header
        lines = fr.readlines()
        for line in lines:
            data = line.strip().split("\t")
            method = data[indexes['file']]
            project_data[project][method] = {}
            project_data[project][method]['age'] = int(data[0])

            for feature in features:
                project_data[project][method][feature] = data[indexes[feature]].split(",")
    return project_data


def calculate_years_from_days_with_ceil(days):
    years = math.ceil(float(days / 365))
    return int(years)


def calculate_years_from_days(days):
    years = int(days / 365)
    return years
