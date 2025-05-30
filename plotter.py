"""
Functions for generating and saving plots.

Original author: TimoSalola (Timo Salola).
Edited by: Väinö Anttalainen
"""
import matplotlib.pyplot
import matplotlib.dates
import pandas
from matplotlib import dates
import datetime
#from datetime import datetime
from matplotlib.dates import DateFormatter
import config
import pytz
global fig
global ax



# INIT PLOT #################################################
def init_plot():
    global fig
    global ax
    matplotlib.pyplot.rcParams['figure.constrained_layout.use'] = True
    fig = matplotlib.pyplot.figure(figsize=(12, 8))
    ax = matplotlib.pyplot.axes()
    format_time_axis()


def ticks():
    global ax
    ax.tick_params()


def show_plot():
    matplotlib.pyplot.show()


# PLOT TITLES, LEGENDS, LABELS ETC ########################
def add_title(title, fontsize=None):
    if fontsize is None:
        matplotlib.pyplot.title(title)
    else:
        matplotlib.pyplot.title(title, fontsize=fontsize)


def add_label_x(label, fontsize=None):
    if fontsize is None:
        ax.set_xlabel(label)
    else:
        ax.set_xlabel(label, fontsize=fontsize)


def add_label_y(label, fontsize=None):
    if fontsize is None:
        ax.set_ylabel(label)
    else:
        ax.set_ylabel(label, fontsize=fontsize)


def show_legend(fontsize=None):
    if fontsize is None:
        matplotlib.pyplot.legend(loc='upper right')
    else:
        matplotlib.pyplot.legend(fontsize=fontsize, loc='upper right')


def format_time_axis():
    global ax

    xax = ax.get_xaxis()
    xax.set_major_locator(dates.DayLocator())
    xax.set_major_formatter(dates.DateFormatter('%b-%d'))

    xax.set_minor_locator(dates.HourLocator(byhour=range(0, 24, 3)))
    xax.set_minor_formatter(dates.DateFormatter('%H'))


# PLOTTING FUNCTIONS #######################################


def plot_curve(x, y, label=None, color=None, alpha=1, width=1):
    if color is not None:
        ax.plot(x, y, label=label, color=color, alpha=alpha, linewidth=width)
    else:
        ax.plot(x, y, label=label, alpha=alpha, linewidth=width)


def fill_between(x, y1, y2, label=None):
    if label is not None:
        matplotlib.pyplot.fill_between(x, y1, y2, label=label)
    else:
        matplotlib.pyplot.fill_between(x, y1, y2)


def set_size(x, y):
    matplotlib.pyplot.figure(figsize=(x, y))


# COMPOUND FUNCTIONS ############################################


def plot_kwh_labels(df, y_offset=0):
    df2 = df[["time", "output"]].copy()

    df2["date"] = pandas.to_datetime(df2["time"]).dt.date

    # df2 = df2.groupby(["date"])["output"]
    df2 = df2.drop("time", axis=1)
    df2 = df2.groupby(["date"]).sum()

    df2["output_kwh"] = df2["output"] / 1000 * (60 / config.data_resolution)

    for index, row in df2.iterrows():
        x_value = datetime.datetime(index.year, index.month, index.day, 8)
        output = round(row["output_kwh"], -1)
        text = str(output) + " kWh"
        matplotlib.pyplot.text(x_value, y_offset, text)


def default_labels_and_title(date):
    add_title("Solar PV forecast: " + str(date))
    add_label_y("Power(W)")
    add_label_x("Time")


def plot_fmi_pvlib_mono(data_pvlib, data_fmi=None, data_file=None, start_date="", day_range=-1):
    """
    Generates a plot from 2 dataframes with time and output columns.
    :param data_fmi:
    :param data_pvlib:
    :return:
    """

    # Timezone of plots could be adjusted to local timezone here. Currently this does not work and thus plots are in UTC
    finnish_time = pytz.timezone("Europe/Helsinki")

    # data_pvlib["time"] = data_pvlib["time"].dt.tz_convert(finnish_time)
    # data_fmi["time"] = data_fmi["time"].dt.tz_convert(finnish_time)

    if data_fmi is not None:
        # removing leading and trailing power output is zero values from fmi open data based energy generation data
        # Find the index of the first non-zero value
        start_index = data_fmi['huld_general'].ne(0).idxmax()
    
        # Find the index of the last non-zero value
        end_index = data_fmi['huld_general'].ne(0)[::-1].idxmax()
    
        # Extract the section of the DataFrame without leading and trailing zeros
        data = data_fmi.loc[start_index:end_index]

        # generate timestamp string for file name
        date_for_simulation = data.index[0].date()
        now = datetime.datetime.now(datetime.UTC)
        timestamp = str(date_for_simulation) + " " + str(now.time())[0:5]

    elif data_file is not None:
        if start_date=="":
            start_date = data_file.index[0]
        else:
            start_date = pandas.to_datetime(start_date, utc=True)

        if day_range == -1:
            end_date = data_file.index[-1]
        else:
            end_date = start_date + datetime.timedelta(days=day_range)

        data = data_file.loc[(data_file.index >= start_date) & (data_file.index < end_date), :]
        if data_pvlib is not None:
            data_pvlib = data_pvlib.loc[(data_pvlib.index >= start_date) & (data_pvlib.index < end_date), :]

        # generate timestamp string for file name
        timestamp = str(start_date)

    f, (a0, a1) = matplotlib.pyplot.subplots(1, 2, gridspec_kw={'width_ratios': [3, 1]}, figsize=(12, 6))

    # plotting pvlib and fmi data
    if data_pvlib is not None:
        a0.plot(data_pvlib.index, data_pvlib["huld_general"], label="Theoretical clear sky generation", c="#6ec8fa")


    a0.plot(data.index, data["huld_general"],
            label="General Huld model based generation", c="#303193")
    a0.plot(data.index, data["pvwatts"],
            label="PVWatts model based generation")

    # adding legend
    a0.legend(loc='upper right')

    # adding titles for both plots
    # a0.set_title('Power generation "' + config.site_name + "\" " + timestamp + "UTC")
    a1.set_title('Energy generation')

    # plot 0 labels
    a0.set_ylabel("Power(W)")
    a0.set_xlabel("Time(UTC)")

    a1.set_xlabel("Date")
    a1.set_ylabel("Energy(kWh)")

    # calculating kwh sums for pvlib
    if data_pvlib is not None:
        pvlib_x, pvlib_y = __get_dayily_power_sums(data_pvlib, config.data_resolution) # pvlib resolution can be any

    # calculating khw sums for the other data
    if data_fmi is not None:
        data_x, data_y = __get_dayily_power_sums(data, 60) # fmi open data only gives 60min resolution data
    else:
        data_x, data_y = __get_dayily_power_sums(data, config.data_resolution)


    # plotting kwh sums on second plot
    if data_pvlib is not None:
        a1.bar(pvlib_x, pvlib_y, color="#6ec8fa")
    a1.bar(data_x, data_y, color="#303193")

    # adding simulation runtime as vertical line
    if data_fmi is not None:
        now = datetime.datetime.now(datetime.UTC)
        v_line_max = max(max(data_pvlib["huld_general"]), max(data["huld_general"]))
        a0.plot([now, now], [0, v_line_max], color="silver", linestyle='--')


    # adding xxkWh (xx%) text to second plot is pvlib data (clear-sky is given)
    if data_pvlib is not None:
        for i in range(len(data_x)):
            pvlib_kwh = pvlib_y[i]
            data_kwh = data_y[i]
            fraction_kwh = data_kwh / pvlib_kwh
            percents = round(fraction_kwh * 100)
            txt = str(data_y[i]) + "kWh\n(" + str(percents) + "%)"

            # this mess here should make sure that kwh numbers do not overlap in bar charts. This shifts
            # text in y-axis if texts are too close
            if i == 0:
                a1.text(data_x[i], data_y[i] / 2, txt, ha="center", backgroundcolor="#FFFFFFd5")
            if i > 0:
                last_y_position = data_y[i - 1] / 2
                new_y_position = data_y[i] / 2

                if last_y_position < new_y_position < last_y_position * 1.2:
                    new_y_position = last_y_position * 1.2
                if last_y_position > new_y_position > last_y_position * 0.8:
                    new_y_position = last_y_position * 0.8

                a1.text(data_x[i], new_y_position, txt, ha="center", backgroundcolor="#FFFFFFd5")

    # formatting plot 1 date axis
    a0.xaxis.set_major_formatter(DateFormatter("%m-%d"))
    a0.xaxis.set_major_locator(matplotlib.dates.DayLocator(interval=1))
    a0.xaxis.set_minor_locator(matplotlib.dates.HourLocator(interval=4))
    a0.xaxis.set_minor_formatter(DateFormatter("%H"))

    # moves major axis to top of plot
    a0.tick_params(axis="x", which="major", top=True, labeltop=True, bottom=False, labelbottom=False)

    # shifts markers for days from midnight to near middle of power generation peaks
    shifter = matplotlib.dates.HourLocator(byhour=10)
    a0.xaxis.set_major_locator(shifter)

    # formatting plot 2 date axis so that 2023-11-23 is shown as 11-23
    formatter = DateFormatter("%m-%d")
    a1.xaxis.set_major_formatter(formatter)

    # formatting plot 2 date axis so that markers are shown only once per day
    a1.xaxis.set_major_locator(matplotlib.dates.DayLocator(interval=1))

    # using tight graph layout to help with data density
    f.tight_layout()

    # saving plot as .png -file

    timestamp = timestamp.replace(":", "-")
    savepath = (config.save_directory + config.site_name + "-" + timestamp + ".png")
    matplotlib.pyplot.savefig(savepath)
    print("Simulation plot saved as '" + savepath + "'")
    print("-------------------------------------------------------------------------------------------------------")

    #matplotlib.pyplot.show()


def __get_dayily_power_sums(data, resolution=config.data_resolution):
    #  df = data[["time", "huld_general"]].copy()
#  
    #  df["date"] = pandas.to_datetime(df["time"]).dt.date

    df = data[["huld_general"]].copy()
    df["date"] = pandas.to_datetime(df.index).date

    #  df = df.drop("time", axis=1)
    df = df.groupby(["date"]).sum()

    df["huld_general_kwh"] = (df["huld_general"] / 1000) / (60 / resolution)

    xvalues = []
    yvalues = []

    for index, row in df.iterrows():
        x_value = datetime.datetime(index.year, index.month, index.day).date()
        # x_value = data(index.year, index.month, index.day)
        output = round(row["huld_general_kwh"], 1)

        # avoiding days with zero power,
        if output > 0:
            xvalues.append(x_value)
            yvalues.append(output)

    return xvalues, yvalues
