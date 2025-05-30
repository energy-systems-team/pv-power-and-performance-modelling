"""
Config file, used for storing parameters which are installation specific and fixed. Geolocation, panel angles, timezone
and data resolution belong here. Variables in this file should be expected to stay unmodified during a simulation.

Original author: TimoSalola (Timo Salola).
Edited by: Väinö Anttalainen
"""

##### Plotting parameters
# site name used for plotting and saved file name
site_name = "output_example"
save_directory = "output/"
save_csv = False #value= [True] or [False] this variable toggles csv file saving on or off
console_print = False #value= [True] or [False] this variable toggles console printing of the full output table on or off

########### PARAMETERS FOR FMI INSTALLATIONS BELOW:


# known location specific params:
latitude_helsinki = 60.2044
longitude_helsinki = 24.9625

latitude_kuopio = 62.8919
longitude_kuopio = 27.6349

latitude_sodankyla = 67.367
longitude_sodankyla = 26.650

latitude_turku = 60.45
longitude_turku = 22.30

elevation_helsinki = 17
elevation_kuopio = 10
elevation_sodankyla = 4
elevation_turku = 5 # What is elevation for Turku?

tilt_helsinki = 15
tilt_kuopio = 15
tilt_sodankyla_20 = 20
tilt_sodankyla_90 = 90
tilt_turku = 15

azimuth_helsinki = 135
azimuth_kuopio = 217
azimuth_sodankyla = 115
azimuth_turku = 180

rated_power_kuopio = 20.28  # [kWp]
rated_power_helsinki = 21  # [kWp]
rated_power_sodankyla = 0.260  # [kWp]
rated_power_turku = 4.5  # [kWp]


#### SIMULATED INSTALLATION PARAMETERS BELOW:
# coordinates
latitude = latitude_helsinki
longitude = longitude_helsinki

# panel angles
tilt = 15 # degrees. Panel flat on the roof would have tilt of 0. Wall mounted panels have tilt of 90.
azimuth = azimuth_helsinki # degrees, north is 0 degrees, east 90. Clockwise rotation

# rated installation power in kW, PV output at standard testing conditions
rated_power = rated_power_helsinki # unit kW

# ground albedo near solar panels, 0.25 is PVlib default. Has to be in range [0,1], typical values [0.1, 0.4]
# grass is 0.25, snow 0.8, worn asphalt 0.12. Values can be found from wikipedia https://en.wikipedia.org/wiki/Albedo
albedo = 0.151

# module elevation, measured from ground
module_elevation = 8 # unit meters

# dummy wind speed(meter per second) value, this will be used if wind speed from fmi open is not used
wind_speed = 2

# air temp in Celsius, this will be used if temp from fmi open is not used
air_temp = 20

#### OTHER PARAMETERS

# "Europe/Helsinki" should take summer/winter time into account, "GTM" is another useful timezone
# timezone is currently not utilized as it should due to plotting issues
timezone = "UTC"

# data resolution, how many minutes between measurements. Recommending values 60, 30, 15, 10, 5, 1
# will interpolate if resolution is higher than 60(30 or 15 etc.) as 60 is what fmi open data is capable of.
data_resolution = 1

# functions like this can be used for easily running the code for multiple installations
def set_params_helsinki(read_file="FMI_Helsinki_PV.csv", write_file=""):
    global latitude, longitude, tilt, azimuth, rated_power, module_elevation, site_name, read_file_name, write_file_name, save_data_csv, header_length, col_name_dict
    latitude = latitude_helsinki
    longitude = longitude_helsinki
    tilt = tilt_helsinki
    azimuth = azimuth_helsinki
    rated_power = rated_power_helsinki
    module_elevation = elevation_helsinki
    site_name = "Helsinki"
    read_file_name = read_file
    write_file_name = write_file
    if write_file != "":
        save_data_csv = True
    else:
        save_data_csv = False
    if read_file == "FMI_Helsinki_PV.csv":
        header_length = 67
    else:
        header_length = 0
    col_name_dict = col_name_dict_helsinki

def set_params_kuopio(read_file="FMI_Kuopio_PV.csv", write_file=""):
    global latitude, longitude, tilt, azimuth, rated_power, module_elevation, site_name, read_file_name, write_file_name, save_data_csv, header_length, col_name_dict
    latitude = latitude_kuopio
    longitude = longitude_kuopio
    tilt = tilt_kuopio
    azimuth = azimuth_kuopio
    rated_power = rated_power_kuopio
    module_elevation = elevation_kuopio
    site_name = "Kuopio"
    read_file_name = read_file
    write_file_name = write_file
    if write_file != "":
        save_data_csv = True
    else:
        save_data_csv = False
    if read_file == "FMI_Kuopio_PV.csv":
        header_length = 67
    else:
        header_length = 0
    col_name_dict = col_name_dict_kuopio

def set_params_sodankyla_20(read_file="FMI_Sodankyla_20deg_PV.csv", write_file=""):
    global latitude, longitude, tilt, azimuth, rated_power, module_elevation, site_name, read_file_name, write_file_name, save_data_csv, header_length, col_name_dict
    latitude = latitude_sodankyla
    longitude = longitude_sodankyla
    tilt = tilt_sodankyla_20
    azimuth = azimuth_sodankyla
    rated_power = rated_power_sodankyla
    module_elevation = elevation_sodankyla
    site_name = "Sodankyla_20"
    #file_name = "FMI_Sodankyla_20deg_PV"
    read_file_name = read_file
    write_file_name = write_file
    if write_file != "":
        save_data_csv = True
    else:
        save_data_csv = False
    if read_file == "FMI_Sodankyla_20deg_PV.csv":
        header_length = 93
    else:
        header_length = 0
    col_name_dict = col_name_dict_sodankyla_20


def set_params_sodankyla_90(read_file="FMI_Sodankyla_90deg_PV.csv", write_file=""):
    global latitude, longitude, tilt, azimuth, rated_power, module_elevation, site_name, read_file_name, write_file_name, save_data_csv, header_length, col_name_dict
    latitude = latitude_sodankyla
    longitude = longitude_sodankyla
    tilt = tilt_sodankyla_90
    azimuth = azimuth_sodankyla
    rated_power = rated_power_sodankyla
    module_elevation = elevation_sodankyla
    site_name = "Sodankyla_90"
    #file_name = "FMI_Sodankyla_20deg_PV"
    read_file_name = read_file
    write_file_name = write_file
    if write_file_name != "":
        save_data_csv = True
    else:
        save_data_csv = False
    if read_file == "FMI_Sodankyla_90deg_PV.csv":
        header_length = 93
    else:
        header_length = 0
    col_name_dict = col_name_dict_sodankyla_90

def set_params_turku():
    global latitude, longitude, tilt, azimuth, rated_power, module_elevation, site_name, read_file_name, write_file_name, save_data_csv, header_length, col_name_dict
    latitude = latitude_turku
    longitude = longitude_turku
    tilt = tilt_turku
    azimuth = azimuth_turku
    rated_power = rated_power_turku
    module_elevation = elevation_turku
    site_name = "Turku"
    #read_file_name = "TUAS_Turku_PV"


########### PARAMETERS FOR DATA FILES BELOW:
data_path = "data"
read_file_name = "" #"b2share/FMI_Helsinki_PV.csv"
# read_file_name = "FMI_Kuopio_PV_2.csv"
write_file_name = "" #"FMI_Helsinki_PV_filtered.csv"
data_file_sep = ";"
save_data_csv = False

# Header length tells how many rows of the file are metatext
header_length_helsinki = 0 #67
header_length_kuopio = 0 #67
header_length_sodankyla = 0 #93

col_name_dict_helsinki = {
    'fmisid': 'id',
    'stationname': 'stationname',
    'utctime': 'utctime',
    'GLOB_PT1M_AVG': 'ghi',
    'DIFF_PT1M_AVG': 'dhi',
    'DIR_PT1M_AVG': 'dni',
    'GLOBA_PT1M_AVG(:31)': 'poa',
    'TTECH_PT1M_AVG(:31)': 't_roof',
    'TTECH_PT1M_AVG(:32)': 'module_temp_1',
    'TTECH_PT1M_AVG(:33)': 'module_temp_2',
    'P0_PT1M_AVG': 'pressure',
    'TA_PT1M_AVG': 'T',
    'RH_PT1M_AVG': 'relative_humid',
    'CLA_PT1M_ACC': 'cloud_coverage',
    'WS_PT10M_AVG': 'wind',
    'WD_PT10M_AVG': 'wind_dir',
    'PRA_PT1H_ACC': 'precipitation',
    'SND_P1D_INSTANT': 'snow_ground',
    'pv_inv_out': 'pv_inv_out',
    'pv_inv_in': 'power',
    'pv_str_1': 'pv_str_1',
    'pv_str_2': 'pv_str_2',
    'dataQC': 'dataQC',
    'vis_SnoP': 'snow',
    'Viss_day': 'viss_day'
}

col_name_dict_kuopio = {
    'fmisid': 'id',
    'stationname': 'stationname',
    'utctime': 'utctime',
    'GLOB_PT1M_AVG': 'ghi',
    'DIFF_PT1M_AVG': 'dhi',
    'DIR_PT1M_AVG': 'dni',
    'GLOBA_PT1M_AVG(:31)': 'poa',
    'TA_PT1M_AVG(:31)': 't_roof',
    'TTECH_PT1M_AVG(:32)': 'module_temp_1',
    'TTECH_PT1M_AVG(:33)': 'module_temp_2',
    'P0_PT1M_AVG': 'pressure',
    'TA_PT1M_AVG': 'T',
    'RH_PT1M_AVG': 'relative_humid',
    'CLA_PT1M_ACC': 'cloud_coverage',
    'WS_PT10M_AVG': 'wind',
    'WD_PT10M_AVG': 'wind_dir',
    'PRA_PT1H_ACC': 'precipitation',
    'SND_P1D_INSTANT': 'snow_ground',
    'pv_inv_out': 'pv_inv_out',
    'pv_inv_in': 'power',
    'pv_str_1': 'pv_str_1',
    'pv_str_2': 'pv_str_2',
    'dataQC': 'dataQC',
    'vis_SnoP': 'snow',
    'Viss_day': 'viss_day'
}

col_name_dict_sodankyla_20 = {
    'fmisid': 'id',
    'stationname': 'stationname',
    'utctime': 'utctime',
    'GLOB_PT1M_AVG': 'ghi',
    'DIFF_PT1M_AVG': 'dhi',
    'DIR_PT1M_AVG': 'dni',
    #'GLOBA_PT1M_AVG(:31)': 'poa', # POA is not measured here
    'TA_PT1M_AVG(:101)': 't_roof',
    'TTECH_PT1M_AVG(:102)': 'module_temp',
    'P0_PT1M_AVG': 'pressure',
    'TA_PT1M_AVG': 'T',
    'RH_PT1M_AVG': 'relative_humid',
    'CLA_PT1M_ACC': 'cloud_coverage',
    'WS_PT10M_AVG': 'wind',
    'WD_PT10M_AVG': 'wind_dir',
    'PRA_PT1H_ACC': 'precipitation',
    'SND_P1D_INSTANT': 'snow_ground',
    'pv_inv_out': 'pv_inv_out',
    'DC_P[W]': 'power',
    'dataQC': 'dataQC',
    'vis_SnoP': 'snow',
    'Viss_day': 'viss_day'
}

col_name_dict_sodankyla_90 = {
    'fmisid': 'id',
    'stationname': 'stationname',
    'utctime': 'utctime',
    'GLOB_PT1M_AVG': 'ghi',
    'DIFF_PT1M_AVG': 'dhi',
    'DIR_PT1M_AVG': 'dni',
    'GLOBA_PT1M_AVG(:101)': 'poa',
    'TA_PT1M_AVG(:101)': 't_roof',
    'TTECH_PT1M_AVG(:103)': 'module_temp',
    'P0_PT1M_AVG': 'pressure',
    'TA_PT1M_AVG': 'T',
    'RH_PT1M_AVG': 'relative_humid',
    'CLA_PT1M_ACC': 'cloud_coverage',
    'WS_PT10M_AVG': 'wind',
    'WD_PT10M_AVG': 'wind_dir',
    'PRA_PT1H_ACC': 'precipitation',
    'SND_P1D_INSTANT': 'snow_ground',
    'pv_inv_out': 'pv_inv_out',
    'DC_P[W]': 'power',
    'dataQC': 'dataQC',
    'vis_SnoP': 'snow',
    'Viss_day': 'viss_day'
}