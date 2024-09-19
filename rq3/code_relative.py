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


    return codes

    # for year in range(2009, 2025):
    #     sm = 0
    #     for code in codes:
    #         try:
    #             sm += codes[code][year]
    #         except:
    #             pass    
    #     #print (year, sm)  
            

def cal_stat(codes):
    stats = {}
    for year in range(2009, 2025):
        sm = 0
        for code in codes:
            if year not in codes[code]:
                continue
            sm += codes[code][year]  
        stats[year] = sm 
    return stats                         

def prob(code, stats):
    y = []
    for year in range(2009, 2025):
        if year not in code:
            pr = 0.0
        else:    
            pr = float(code[year] / stats[year])
        y.append(pr)
    return y
     
def draw_graph(codes):
    stats = cal_stat(codes)
    print(stats)
    
    legends = []
    X = []
    Y = []
    selected_codes = ["Actuator", "Remote", "Incoming", "Specifications", "Moving", "Connections"]
    #selected_codes = ["Coordinates", "Error", "Incoming"]
    for code in codes:
        if code not in selected_codes:
            continue
        legends.append(code)
        y = prob(codes[code], stats)
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
    codes = process(lines, indexes)
    draw_graph(codes)
