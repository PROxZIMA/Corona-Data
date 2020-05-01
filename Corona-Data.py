from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd


#A function which returns data as {'cases':[1, 2, 3], 'States':['Goa', 'Kerala', 'other stater']}
def tabledata(tablehtml):
    data = {}
    #Finds column heads
    table_heads = tablehtml.find('thead').find('tr').findAll('th')
    row_h = [table_head.find('strong').text.strip() for table_head in table_heads]
    #Create a dictionary with keys as Column head and values as empty list
    for i in range(5): data[row_h[i]] = []

    #Finds data under a specific column
    table_bodys = tablehtml.find('tbody').findAll('tr')
    count = 0
    for table_body in table_bodys:
        table_body_datas = table_body.findAll('td')
        #Row as a list
        row_b = [table_body_data.text.strip() for table_body_data in table_body_datas]

        #Append each data of a row to individual key
        #If initial sict is like {'cases':[], 'States':[]}
        #The this loop gives {'cases':[1], 'States':['Goa']} if row is [1, 'Goa']
        #Then in next loop gives {'cases':[1, 2], 'States':['Goa', 'Kerala']} if next row is [2, 'Kerala']
        for (i, j), k in zip(data.items(), range(5)): j = j.append(row_b[k])

        #This prevents breaking of Panadas
        count += 1
        if count == 32: break
    
    #Converts String numbers to integer datatype
    data['Total Cases'] = data.pop('Total Confirmed cases (Including 111 foreign Nationals)')
    data['Total Cases'] = list(map(int, data['Total Cases']))
    data['Death'] = list(map(int, data['Death']))
    data['Cured/Discharged/Migrated'] = list(map(int, data['Cured/Discharged/Migrated']))
    
    return data


def graph(tabledata):
    #Creates a dataframe. Here tabledata is a well defined dictionery
    dftable = pd.DataFrame(tabledata)
    #Sorts whole dataframe in ascending order
    dftable = dftable.sort_values('Total Cases')
    #Creates a wellspaced array
    x = np.linspace(1, len(tabledata['S. No.']), len(tabledata['S. No.']))

    #Used for plotting multiple data in same frame
    ax = plt.subplot()
    #Creates bar according to the dataframe
    bar_c = ax.bar(x-0.2, list(dftable['Cured/Discharged/Migrated']), width=0.2, color='g', label='Cured Cases')
    bar_d = ax.bar(x, list(dftable['Death']), width=0.2, color='r', label='Deaths')
    bar_t = ax.bar(x+0.2, list(dftable['Total Cases']), width=0.2, color='b', label='Total Cases')
    
    #Set the x ticks with list of ticks
    ax.set_xticks(x)
    #Set the labels to the ticks
    ax.set_xticklabels(list(dftable['Name of State / UT']))

    #Set the y ticks with list of ticks
    ax.set_yticks(np.linspace(0, 10000, 21))

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
                        fontsize='5.5',
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
    soup = bs(content.content, 'lxml')

    #Find table using class attribute
    table_site = soup.find("table", attrs={'class': 'table table-striped'})

    #Get dictionary output from 'table' data function
    table = tabledata(table_site)

    #Creates a dataframe of the table
    dftable = pd.DataFrame(table)

    #Adds a row to the dataframe
    dftable.loc[dftable.index[-1]+  1] = ['','Total number of confirmed cases',dftable['Cured/Discharged/Migrated'].astype(int).sum(),dftable['Death'].astype(int).sum(),dftable['Total Cases'].astype(int).sum()]

    #Prints dataframe without the indices
    print(dftable.to_string(index=False))
    print('Active Cases:', dftable.iloc[-1]['Total Cases']-dftable.iloc[-1]['Cured/Discharged/Migrated']-dftable.iloc[-1]['Death'])
    
    #Displays the Graph
    graph(table)




