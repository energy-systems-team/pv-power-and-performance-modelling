"""
Common data filters for PV data processing. The data filters include
- nighttime filter
- clear-sky filter
- outlier filter
- variable cutoff filter
- IEC filter:
        - Irradiance [-6, 1500] W/m^2
        - Ambient temperature [-30,50] degC
        - Wind speed [0,31] m/s
        - AC power [-0.01Pnom,1.02Pnom]

Author: Lauri Karttunen.
"""


import pandas as pd
import pvlib
import datetime
import matplotlib.pyplot as plt


def IEC(data, p_rated):
    """
    Threshold conditions:
    -6 W/m2	<	irradiance	<	1500 W/m2
    -30 ∘C	<	ambient temperature	<	50 ∘C
    0 m/s	<	wind speed	<	32 m/s
    -0.01 x Pnom	<	AC power	<	1.02 x  Pnom

    Returns: Filtering mask (Pandas Series object)
    """
    mask = (data.poa < 1500) & (data.poa > -6) & (data.t_air > -30) & (data.t_air < 50) & \
           (data.wind_speed > 0) & (data.ac_power > -0.01 * p_rated) & \
           (data.ac_power < 1.02 * p_rated)
    
    return mask


def threshold(data, parameter: str, lower=0, upper=50000):
    """
    Perform threshold filtering for given parameter.
    Args:
        lower: Lower threshold
        upper: Upper threshold
    Returns: Filtering mask (Pandas Series object)
    """
    
    mask = (lower <= data[parameter]) & (data[parameter] <= upper)
    
    return mask


def nighttime(data):
    """
    Points with irradiance below 5 W/m^2 are considerd night-time data.

    Returns: Filtering mask (Pandas Series object)
    """
    
    mask = data.poa.values < 5
    return mask


def daytime(data):
    """
    Returns: Filtering mask (Pandas Series object)
    """

    return ~nighttime(data)


def rolling_outlier_filter(data, window_size):
    """    
    Power-irradiance outliers are filtered by applying a rolling horizon filter and excluding points outside +-2 STD outside
    rolling horizon mean.

    Args:
        data (pandas DataFrame): dataframe with power and poa columns
        window_size (int): number of points withing the rolling window

    Returns: Filtering mask (Pandas Series object)
    """

    # Sort data by irradiance to perform the rolling horizon
    data = data.sort_values(by='poa')

    p_poa = data['power'] / data['poa']

    # Set rolling window size
    window_size = window_size

    # Calculate rolling mean and standard deviation
    rolling_mean = p_poa.rolling(window=window_size).mean()
    rolling_sd = p_poa.rolling(window=window_size).std()

    # Define the upper and lower bounds
    upper_bound = rolling_mean + 2 * rolling_sd
    lower_bound = rolling_mean - 2 * rolling_sd

    p_poa_mask = (p_poa < upper_bound) & (p_poa > lower_bound)

    data['filter_mask'] = p_poa_mask
    data = data.sort_values(by='utctime')

    return data.filter_mask


def clear_sky(data, latitude, longitude, altitude, threshold=0.2):
    """
    Calculate cleasky GHI using Pvlib's haurwitz function. This model has the best performance of models which
    require only zenith angle [1]

    Args:
        data (pandas DataFrame): dataframe with ghi variable in UTC+00
        latitude (float): latitude of the system
        longitude (float): longitude of the system
        altitude (float): altitude of the system
        threshold: A percentage measured GHI-values can differ from modelled clear-sky GHI-values (float)
    
    Returns:  Filtering mask (Pandas Series object)
    
    References:
        [1] M. Reno, C. Hansen, and J. Stein, "Global Horizontal Irradiance Clear
            Sky Models: Implementation and Analysis", Sandia National Laboratories, SAND2012-2389, 2012
    """

    temperature = 6
    
    # the function below returns a dictionary including different solar angles
    spa = pvlib.solarposition.spa_python(data.utctime, latitude, longitude,
                                         altitude=altitude, pressure=101325, temperature=temperature, delta_t=70,
                                         atmos_refract=None, how='numpy')
    
    # clearsky function returns a dataframe with clear-sky GHI values
    clear_sky = pvlib.clearsky.haurwitz(spa.apparent_zenith)
    cs_ghi = clear_sky.ghi.values  # Clearsky ghi values
    
    # Calculate clearsky-index
    csi = data.ghi / cs_ghi
    
    return (csi >= 1.0 - threshold) & (csi <= 1.0 + threshold)

