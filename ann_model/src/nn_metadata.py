import itertools


# from traintest import test_indicator


# GRADES ###

grades = [
    "None",
    "6B",
    "6B+",
    "6C",
    "6C+",
    "7A",
    "7A+",
    "7B",
    "7B+",
    "7C",
    "7C+",
    "8A",
    "8A+",
    "8B",
    "8B+",
]
grade_int = {
    "None": -2,
    "6B": -1,
    "6B+": 0,
    "6C": 1,
    "6C+": 2,
    "7A": 3,
    "7A+": 4,
    "7B": 5,
    "7B+": 6,
    "7C": 7,
    "7C+": 8,
    "8A": 9,
    "8A+": 10,
    "8B": 11,
    "8B+": 12,
}


def grade_comparison(gr1, gr2):
    return grade_int[gr1] >= grade_int[gr2]


# HOLDS ###

mb_rows = [str(i) for i in range(1, 19)]
mb_columns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
column_int = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "E": 4,
    "F": 5,
    "G": 6,
    "H": 7,
    "I": 8,
    "J": 9,
    "K": 10,
}
mb_holds = [i[1] + i[0] for i in itertools.product(mb_rows, mb_columns)]


def hold_row(hold):
    return hold[1:]


def hold_row_int(hold):
    return int(hold_row(hold))


def hold_column(hold):
    return hold[0]


def hold_col_int(hold):
    return column_int[hold_column(hold)]


# TRAIN-TEST-SPLIT ###


# train_tf = [i == 0 for i in test_indicator]
# test_tf = [i == 1 for i in test_indicator]


# Converts holds to an index between 0 and 197
table = {}
for char in "abcdefghijk":
    table[char] = ord(char) - ord("a")


def get_hold_index(hold):
    return table[hold[0].lower()] + (int(hold[1]) - 1) * 11