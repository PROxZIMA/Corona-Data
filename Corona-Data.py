from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd



def tabledata(tablehtml):
    """
    A function which returns data as {'cases':[1, 2, 3], 'States':['Goa', 'Kerala', 'other stater']}
    It takes html format of a table and returns a well-defined dictionery
    """
    data = {}

    #Finds column heads
    table_heads = tablehtml.find('thead').find('tr').findAll('th')
    #Create a dictionary with keys as Column head and values as empty list
    for table_head in table_heads:
        data[table_head.text.strip()] = []

    #Finds data under a specific column
    table_bodies = tablehtml.find('tbody').findAll('tr')
    count = 0
    for table_body in table_bodies:

        #Limits the total reach of the table_body
        count += 1
        if count == 38: break

        #Append each data of a row to individual key
        #If initial dict is like {'cases':[], 'States':[]}
        #The this loop gives {'cases':[1], 'States':['Goa']} if row is [1, 'Goa']
        #Then in next loop gives {'cases':[1, 2], 'States':['Goa', 'Kerala']} if next row is [2, 'Kerala']
        for (i, j), table_body_data in zip(data.items(), table_body.findAll('td')):
            try:
                j.append(int(table_body_data.text.strip()))
            except ValueError:
                j.append(table_body_data.text.strip())

    return data


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
    ax.set_yticks(np.linspace(0, 80000, 21))

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

    #Sends get request
    content = requests.get('https://www.mohfw.gov.in/')

    #Get the html content and parse it in HTML/XML format
    soup = bs(content.content, 'html.parser')

    #Find table using class attribute
    table_site = soup.find("table", attrs={'class': 'table table-striped'})

    #Get dictionary output from 'table' data function
    table = tabledata(table_site)

    #Creates a dataframe. Here table is a well defined dictionery
    dftable = pd.DataFrame(table)

    #Prints dataframe without the indices
    print(dftable.to_string(index=False))

    #Displays the Graph
    graph(dftable)
