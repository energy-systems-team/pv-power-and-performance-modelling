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
save_data_csv = True
calculate_irradiance_components = True

#### SIMULATED INSTALLATION PARAMETERS BELOW:
# coordinates
latitude = 60.45
longitude = 22.30

# panel angles
tilt = 15 # degrees. Panel flat on the roof would have tilt of 0. Wall mounted panels have tilt of 90.
azimuth = 180 # degrees, north is 0 degrees, east 90. Clockwise rotation

# rated installation power in kW, PV output at standard testing conditions
rated_power = 4.5 # unit kW

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
data_resolution = 5

########### PARAMETERS FOR FMI INSTALLATIONS BELOW:


# known location specific params:
latitude_helsinki = 60.2044
longitude_helsinki = 24.9625

latitude_kuopio = 62.8919
longitude_kuopio = 27.6349

latitude_turku = 60.45
longitude_turku = 22.30

elevation_helsinki = 17
elevation_kuopio = 10
elevation_turku = 5 # What is elevation for Turku?

tilt_helsinki = 15
tilt_kuopio = 15
tilt_turku = 15

azimuth_helsinki = 135
azimuth_kuopio = 217
azimuth_turku = 180

rated_power_kuopio = 20.28
rated_power_helsinki = 21
rated_power_turku = 4.5


# functions like this can be used for easily running the code for multiple installations
def set_params_helsinki():
    latitude = latitude_helsinki
    longitude = longitude_helsinki
    tilt = tilt_helsinki
    azimuth = azimuth_helsinki
    rated_power = rated_power_helsinki
    module_elevation = elevation_helsinki

def set_params_kuopio():
    latitude = latitude_kuopio
    longitude = longitude_kuopio
    tilt = tilt_kuopio
    azimuth = azimuth_kuopio
    rated_power = rated_power_kuopio
    module_elevation = elevation_kuopio

def set_params_turku():
    latitude = latitude_turku
    longitude = longitude_turku
    tilt = tilt_turku
    azimuth = azimuth_turku
    rated_power = rated_power_turku
    module_elevation = elevation_turku


########### PARAMETERS FOR DATA FILES BELOW:
data_path = "data"
read_file_name = "turku_preprocessed.csv"
write_file_name = "turku_preprocessed_2.csv"
data_file_sep = ";"