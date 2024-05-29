import json
import os
import numpy as np
import pandas as pd

import nn_metadata as md


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
source_path = ROOT_DIR + "/dataset/problems MoonBoard 2016 .json"

with open(source_path) as file:
    source_dict = json.load(file)


holds_index = {md.mb_holds[i]: i for i in range(len(md.mb_holds))}


def get_raw_features(prob, n_repeats):
    holds = np.zeros(198, dtype=int)

    output = {}

    output["id"] = int(prob["moves"][0]["problemId"])
    if prob["userGrade"]:
        output["userGrade"] = md.grade_int[prob["userGrade"]]
        output["grade"] = md.grade_int[prob["grade"]] if prob["grade"] else -2

    else:
        output["userGrade"] = -2

    output["benchmark"] = prob["isBenchmark"]
    output["userRating"] = prob["userRating"]
    output["repeats"] = prob["repeats"]

    if (
        output["repeats"] > n_repeats
        and not output["benchmark"]
        and output["userGrade"]
    ):
        output["grade"] = output["userGrade"]

    for move in prob["moves"]:
        index = holds_index[move["description"].upper()]
        holds[index] = 1
        if move["isStart"]:
            holds[index] = 2
        if move["isEnd"]:
            holds[index] = 3

    for i, cat in enumerate(md.mb_holds):
        output[cat] = holds[i]
    # output['start_holds'] = start_holds
    # output['finish_hold'] = finish_hold
    return output


def get_df(cut_repeats, grad_repeats):
    df_ = pd.DataFrame(
        [get_raw_features(prob, grad_repeats) for prob in source_dict["data"]]
    )

    df = df_[(df_["repeats"] > cut_repeats) | (df_["benchmark"])]

    df = df[
        (df["userGrade"] == df["grade"]) & (df["grade"].isin(list(range(10))))
    ]

    df1 = df.drop(
        columns=["id", "userGrade", "benchmark", "userRating", "repeats"]
    )

    df1 = df1.drop_duplicates(subset=df1.columns[6:])

    return df1
