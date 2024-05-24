
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
    output['benchmark'] = prob['isBenchmark']
    output['start1'] = ''
    output['start2'] = ''
    start_set = False
    output['end'] = ''
    for hold in md.mb_holds:
        output[hold] = 0
    for move in prob['moves']:
        output[move['description']] = 1
        if move['isStart']:
            if not start_set:
                output['start1'] = output['start2'] = move['description']
                start_set = True
            else:
                output['start2'] = move['description']
        if move['isEnd']:
            output['end'] = move['description']
    return output

list_raw_features = [get_raw_features(prob) for prob in source_dict['data']]
list_raw_features[340]['start1'] = list_raw_features[340]['start2'] = 'J5'
del list_raw_features[340]['j5']

raw_df = pd.DataFrame(list_raw_features)

raw_df.to_csv('raw_features.csv', index = False)