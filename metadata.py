
import numpy as np
import itertools
from math import sqrt


### GRADES ###

grades = ['6B', '6B+', '6C', '6C+', '7A', '7A+', '7B', '7B+', '7C', '7C+', '8A', '8A+', '8B', '8B+']
grade_int = {'6B': 0, '6B+': 1, '6C': 2, '6C+': 3, '7A': 4, '7A+': 5, '7B': 6, '7B+': 7, '7C': 8, '7C+': 9, '8A': 10, '8A+': 11, '8B': 12, '8B+': 13}
def grade_comparison(gr1, gr2):
    return grade_int[gr1] >= grade_int[gr2]

exp_grade_int = {'6B': 1, '6B+': 2, '6C': 4, '6C+': 8, '7A': 16, '7A+': 32, '7B': 64, '7B+': 128, '7C': 256, '7C+': 512, '8A': 1024, '8A+': 2048, '8B': 4096, '8B+': 8192}

def adjacent_grades(gr1,gr2):
    return (grade_int[gr1] >= grade_int[gr2] - 1) and (grade_int[gr1] <= grade_int[gr2] + 1)

def one_off_accuracy(pred,y):#Make sure y is an numpy array of target grades
    count = 0
    for i in range(len(y)):
        if adjacent_grades(y[i], pred[i]):
            count+= 1
    return (count/len(y))


### HOLDS ###

mb_rows = [str(i) for i in range(1, 19)]
mb_columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
column_int = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10}
mb_positions = [i[1] + i[0] for i in itertools.product(mb_rows, mb_columns)]
mb_holds = ['G2', 'J2', 'B3', 'D3', 'B4', 'G4', 'I4', 'A5', 'C5', 'D5', 'F5', 'H5', 'I5', 'J5', 'K5', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'I6', 'J6', 'K6', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'I7', 'J7', 'K7', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'I8', 'J8', 'K8', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'I9', 'J9', 'K9', 'A10', 'B10', 'C10', 'D10', 'E10', 'F10', 'G10', 'H10', 'I10', 'J10', 'K10', 'A11', 'B11', 'C11', 'D11', 'E11', 'F11', 'G11', 'H11', 'I11', 'J11', 'K11', 'A12', 'B12', 'C12', 'D12', 'E12', 'F12', 'G12', 'H12', 'I12', 'J12', 'K12', 'A13', 'B13', 'C13', 'D13', 'E13', 'F13', 'G13', 'H13', 'I13', 'J13', 'K13', 'A14', 'C14', 'D14', 'E14', 'F14', 'G14', 'H14', 'I14', 'J14', 'K14', 'A15', 'B15', 'C15', 'D15', 'E15', 'F15', 'G15', 'H15', 'I15', 'A16', 'B16', 'C16', 'D16', 'E16', 'F16', 'G16', 'H16', 'I16', 'J16', 'K16', 'D17', 'G17', 'A18', 'B18', 'C18', 'D18', 'E18', 'G18', 'H18', 'I18', 'K18']
def hold_row(hold): return hold[1:]
def hold_row_int(hold): return int(hold_row(hold))
def hold_column(hold): return hold[0]
def hold_col_int(hold): return column_int[hold_column(hold)]
def hold_dist(hold1, hold2): return sqrt((hold_row_int(hold1) - hold_row_int(hold2))**2 + (hold_col_int(hold1) - hold_col_int(hold2))**2)



### TRAIN-TEST SPLIT ###

from traintest import test_indicator
train_tf = [i == 0 for i in test_indicator]
test_tf = [i == 1 for i in test_indicator]


### Converts holds to an index between 0 and 197

table = dict()
for char in 'abcdefghijk':
    table[char] = ord(char) - ord('a')

def get_hold_index(hold):
    return table[hold[0].lower()] + (int(hold[1]) - 1)*11
