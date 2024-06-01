
import numpy as np
import pandas as pd
import json

import metadata as md

source_path = 'Problems/problems-2016.json'

with open(source_path) as file:
    source_dict = json.load(file)

def get_raw_features(prob):
    output = dict()
    output['id'] = prob['moves'][0]['problemId']
    if prob['userGrade']:
        output['grade'] = prob['userGrade']
    else:
        output['grade'] = prob['grade']
    output['benchmark'] = 1*prob['isBenchmark']
    output['start1'] = ''
    output['start2'] = ''
    start_set = False
    output['end'] = ''
    for hold in md.mb_holds:
        output[hold] = 0
    for move in prob['moves']:
        hold = move['description']
        if hold == 'j5':
            hold = 'J5'
        output[hold] = 1
        if move['isStart']:
            if not start_set:
                output['start1'] = output['start2'] = hold
                start_set = True
            else:
                if hold < output['start1']:
                    output['start1'] = hold
                else:
                    output['start2'] = hold
        if move['isEnd']:
            output['end'] = move['description']
    return output

def clean(prob):
    if prob['isBenchmark']:
        return True
    elif prob['moves'][0]['problemId'] == 304387:
        return False
    elif prob['grade'] == '6B+':
        if prob['userGrade'] != '6B+':
            return False
        elif prob['userRating'] < 4:
            return False
        elif prob['repeats'] < 10:
            return False
        else:
            return True
    elif prob['repeats'] < 2:
        return False
    elif prob['userRating'] < 4:
        return False
    else:
        return True

list_raw_features = [get_raw_features(prob) for prob in source_dict['data'] if clean(prob)]
#list_raw_features[340]['start1'] = list_raw_features[340]['start2'] = 'J5' # Index no longer accurate
#del list_raw_features[340]['j5'] # Index no longer accurate

raw_df = pd.DataFrame(list_raw_features)

raw_df.to_csv('raw_features.csv', index = False)