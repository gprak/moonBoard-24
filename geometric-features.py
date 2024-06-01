
import numpy as np
import pandas as pd
import scipy.stats as sps
import metadata as md

raw_features_path = 'raw_features.csv'
full_features_path = 'full_features.csv'

def add_features(raw_df):
    df = raw_df.copy()
    df['grade'] = np.vectorize(lambda x : md.grade_int[x])(df['grade'])
    print('Start...')
    df['start1_row'] = np.vectorize(md.hold_row_int)(df['start1'])
    df['start1_col'] = np.vectorize(md.hold_col_int)(df['start1'])
    df['start2_row'] = np.vectorize(md.hold_row_int)(df['start2'])
    df['start2_col'] = np.vectorize(md.hold_col_int)(df['start2'])
    df['start_col_spread'] = df['start2_col'] - df['start1_col']
    print('End...')
    df['end_col'] = np.vectorize(md.hold_col_int)(df['end'])
    print('Holds...')
    holds = [[hold for hold in md.mb_holds if df[hold][i]] for i in raw_df.index]
    print('Rows...')
    holds_row = [[md.hold_row_int(hold) for hold in holds[i]] for i in raw_df.index]
    print('Row stats...')
    df['row_mean'] = [np.mean(holds_row[i]) for i in raw_df.index]
    df['row_std'] = [np.std(holds_row[i], ddof = 1) for i in raw_df.index]
    df['row_skew'] = [sps.skew(holds_row[i]) for i in raw_df.index]
    df['row_kurt'] = [sps.kurtosis(holds_row[i]) for i in raw_df.index]
    print('Row jumps...')
    df['row_jump1'] = [max(np.diff(np.sort(holds_row[i]))) for i in raw_df.index]
    df['row_jump2'] = [np.sort(np.diff(np.sort(holds_row[i])))[-2] for i in raw_df.index]
    df['row_jump_std'] = [np.std(np.diff(np.sort(holds_row[i]))) for i in raw_df.index]
    print('Columns...')
    holds_col = [[md.hold_col_int(hold) for hold in holds[i]] for i in raw_df.index]
    print('Column stats...')
    df['col_mean'] = [np.mean(holds_col[i]) for i in raw_df.index]
    df['col_std'] = [np.std(holds_col[i], ddof = 1) for i in raw_df.index]
    df['col_skew'] = [sps.moment(holds_col[i], 3) for i in raw_df.index]
    df['col_kurt'] = [sps.moment(holds_col[i], 4) for i in raw_df.index]
    print('Correlation...')
    df['row_col_corr'] = [np.cov(holds_row[i], holds_col[i])[0, 1] for i in raw_df.index]
    df['row_col_corr'] = [np.cov([r**2 for r in holds_row[i]], holds_col[i])[0, 1] for i in raw_df.index]
    df['row_col_corr'] = [np.cov(np.diff(holds_row[i]), np.diff(holds_col[i]))[0, 1] for i in raw_df.index]
    print('Columns, bottom to top...')
    holds_col_diff = [np.diff(holds_col[i]) for i in raw_df.index]
    df['col_diff_std'] = [np.std(holds_col_diff[i]) for i in raw_df.index]
    holds_col_diffdiff = [np.diff(holds_col_diff[i]) for i in raw_df.index]
    df['col_diffdiff_std'] = [np.std(holds_col_diffdiff[i]) for i in raw_df.index]
    print('Diagonal jumps...')
    df['diag1_jump'] = [max(np.diff(np.sort([md.hold_row_int(hold) + md.hold_col_int(hold) for hold in holds[i]]))) for i in raw_df.index]
    df['diag2_jump'] = [max(np.diff(np.sort([md.hold_row_int(hold) - md.hold_col_int(hold) for hold in holds[i]]))) for i in raw_df.index]
    return df

def run_add_features(input_path = raw_features_path, output_path = full_features_path):
    raw_df = pd.read_csv(input_path)
    full_df = add_features(raw_df)
    full_df.to_csv(output_path, index = False)
