"""
This file contains functions for pre-processing data.

Original author: Väinö Anttalainen.
Other editors: Lauri Karttunen
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


def impute_columns(df, col_names, resolutions):
        """
        Function for imputing missing values due to the different measurement resolutions.
        :param df:
        :param col_names: List of column names that are imputed.
        :param resolution: List of measurement resolutions for the given columns in minutes.
        :return: The modified df.
        """
        if len(col_names) != len(resolutions):
                print("Length of col_names and resolutions must match. Columns not imputed.")
        else:
                num_of_rows_to_impute_list =  [res - 1 for res in resolutions]
                for i in range(len(col_names)):
                        num_of_rows_to_impute = num_of_rows_to_impute_list[i]
                        column = col_names[i]
                        values = df[column].values
                        non_na_indices = np.where(~pd.isna(values))[0]
                        ind_prev = 0
                        for ind in non_na_indices:
                                start_ind = max(0, ind - num_of_rows_to_impute) 
                                if ind - ind_prev >= num_of_rows_to_impute:
                                        values[start_ind:ind] = values[ind]
                                ind_prev = ind
                        
                        df[column] = values
        return df