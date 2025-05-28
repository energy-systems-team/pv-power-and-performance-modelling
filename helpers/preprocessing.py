"""
This file contains functions for pre-processing data.

Original author: Väinö Anttalainen.
"""

import pandas as pd
import numpy as np

def merge_measurements(df, col_names, diff=10):
    """
    Function for merging two measured variables.
    Checks if the difference between the measurements is less than diff and then averages them.
    Otherwise returns nan.
    :param df:
    :param col_names:
    :param diff:
    :return: 
    """
    measurement_1 = df[col_names[0]]
    measurement_2 = df[col_names[1]]

    measurements_df = pd.DataFrame({'measurement_1': measurement_1, 'measurement_2': measurement_2})

    # Calculate the average where the absolute difference is less than diff
    measurements_df['avg'] = np.where(
            np.abs(measurements_df['measurement_1'] - measurements_df['measurement_2']) < diff, 
            measurements_df[['measurement_1', 'measurement_2']].mean(axis=1), np.nan)

    return measurements_df['avg']