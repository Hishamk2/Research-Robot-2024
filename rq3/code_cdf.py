from datetime import datetime, timedelta
import pandas as pd
from util import graphs
import numpy as np


def build_indexes(line):
    indexes = {}
    data = line.strip().split(",")
    for i in range(len(data)):
        indexes[data[i]] = i
    return indexes

def convert_date(date):
    try:
        date_stamp = pd.to_datetime(date, format="%m/%d/%Y %H:%M")
    except:
        base_date = datetime(1899, 12, 30)
        date_stamp = base_date + timedelta(days=float(date))
    return date_stamp

def process(lines, indexes):
    codes = {}
    for line in lines:
        line =  line.strip()
        if len(line) < 3:
            break
        data = line.split(",")
        raw_date = data[indexes['questionCreationDate']]
        date = str(convert_date(raw_date))
        year = date.split("-")
        year = int(year[0])
        code = data[indexes['code']]
        id = data[indexes['questionId']]
        #print (id, code, raw_date, date, year)
        if code not in codes:
            codes[code] = {}
            codes[code][year] = 1
        else:
            if year not in codes[code]:
                codes[code][year] = 1
            else:
                codes[code][year] += 1 

    code_per_year = {}
    for code in codes:
        code_per_year[code] = []
        for year in range(2009, 2025):
            if year in codes[code]:
                code_per_year[code].append(codes[code][year])
            else:
                code_per_year[code].append(0) 

    return code_per_year

    # for year in range(2009, 2025):
    #     sm = 0
    #     for code in codes:
    #         try:
    #             sm += codes[code][year]
    #         except:
    #             pass    
    #     #print (year, sm)  
            
def cdf(a):
    tot = float(np.sum(a))
    prev = 0.0
    y = []
    for i in a:
        prob = i/tot
        y.append(prev + prob)
        prev = prev + prob
    return y    

def draw_cdf_graph(code_per_year):
    legends = []
    X = []
    Y = []
    selected_codes = ["Timing", "Specifications", "Programming",  "Moving", "Connections"]
    for code in code_per_year:
        if code not in selected_codes:
            continue
        legends.append(code)
        y = cdf(code_per_year[code])
        #y = code_per_year[code]
        x = range(2009, 2025)
        X.append(x)
        Y.append(y)

    configs = {}
    configs["x_label"] = "Year"
    configs["y_label"] = "CDF"
    configs["legends"] = legends
    configs['marker'] = True
    #configs["x_ticks"] = np.arange(20, 110, 10)
    graphs.draw_line_graph_multiple_with_x(X, Y, configs)
    

if __name__ == '__main__':

    fr = open("/home/shaiful/research/Research-Robot-2024-main/rq3/data.csv", "r")
    line = fr.readline()
    lines =  fr.readlines()
    fr.close()
    indexes = build_indexes(line)
    code_per_year = process(lines, indexes)
    draw_cdf_graph(code_per_year)