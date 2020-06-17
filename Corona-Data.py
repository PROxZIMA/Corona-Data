from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd


def graph(dftable):
    """
    Displays a graph using the dictionary's dataframe
    """
    #Removes last 2 rows from the data frame for plotting purpose
    dftable = dftable.drop(dftable.index[[-2, -1]])
    #Sorts whole dataframe in ascending order
    dftable = dftable.sort_values('Total Confirmed cases*')
    #Creates a wellspaced array equal to rows in table
    x = np.linspace(1, len(dftable.index), len(dftable.index))

    #Used for plotting multiple data in same frame
    ax = plt.subplot()
    #Creates bar according to the dataframe
    bar_c = ax.bar(x-0.2, dftable['Cured/Discharged/Migrated*'], width=0.2, color='g', label='Cured Cases')
    bar_d = ax.bar(x, dftable['Deaths**'], width=0.2, color='r', label='Deaths')
    bar_t = ax.bar(x+0.2, dftable['Total Confirmed cases*'], width=0.2, color='b', label='Total Confirmed cases')

    #Set the x ticks with list of ticks
    ax.set_xticks(x)
    #Set the labels to the ticks
    ax.set_xticklabels(dftable['Name of State / UT'])

    #Set the y ticks with list of ticks
    maxi = max(dftable['Total Confirmed cases*'])
    reach = maxi - maxi%10000 + 10000 # Finds roundoff of max value
    ax.set_yticks(np.linspace(0, reach, 21))

    #Create a legend
    ax.legend()

    #Adds these things to the figure: title, xticks rotation, (x,y) axis label
    plt.title('India Corona Data')
    plt.xticks(rotation=90)
    plt.xlabel('States')
    plt.ylabel('People Affected')

    #Add Height to individual bars
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            #Formatting and placing the height
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        fontsize='5.6',
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', rotation='90')

    autolabel(bar_c)
    autolabel(bar_d)
    autolabel(bar_t)

    #Most important thing which displays the graph
    plt.show()


if __name__ == '__main__':

    # Official Covid-19 cases tracker
    link = 'https://www.mohfw.gov.in/'

    # Extract all tables as datframe object in list
    dfs = pd.read_html(link)

    # Gets the first dataframe upto required columns
    df = dfs[0].head(37)

    # Convets string column objects(str by default) to float and thenn to int
    pd.options.mode.chained_assignment = None # hides SettingWithCopyWarning

    df['Active Cases*'] = pd.to_numeric(df['Active Cases*']).convert_dtypes()
    df['Cured/Discharged/Migrated*'] = pd.to_numeric(df['Cured/Discharged/Migrated*']).convert_dtypes()
    df['Deaths**'] = pd.to_numeric(df['Deaths**']).convert_dtypes()
    df['Total Confirmed cases*'] = pd.to_numeric(df['Total Confirmed cases*']).convert_dtypes()

    # Prints dataframe without the indices
    print(df.to_string(index=False))

    #Displays the Graph
    graph(df)
