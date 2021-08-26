import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests


def graph(dftable):
    """
    Displays a graph using the dataframe

    Parameters
    ----------
    df   : pandas.core.frame.DataFrame
           The DataFrame to format
    """

    # Removes last from the data frame for plotting only states
    dftable = dftable.drop(dftable.index[[-1]])

    # Sorts whole dataframe in ascending order
    dftable = dftable.sort_values('Cured Cases')

    # Creates a wellspaced array equal to rows in table
    x = np.linspace(1, len(dftable.index), len(dftable.index))

    # Used for plotting multiple data in same frame
    ax = plt.subplot()

    # Creates bar according to the dataframe
    bar_a = ax.bar(x-0.2, dftable['Active Cases'], width=0.2, color='b', label='Total Active Cases')
    bar_c = ax.bar(x, dftable['Cured Cases'], width=0.2, color='g', label='Cured')
    bar_d = ax.bar(x+0.2, dftable['Death Cases'], width=0.2, color='r', label='Deaths')

    # Set the x ticks with list of ticks
    ax.set_xticks(x)

    # Set the labels to the ticks
    ax.set_xticklabels(dftable['Name of State/UT'])

    # Set the y ticks with list of ticks
    maxi = max(dftable['Cured Cases'])
    reach = maxi - maxi%10000 + 10000 # Finds roundoff of max value
    ax.set_yticks(np.linspace(0, reach, 21))

    # Create a legend
    ax.legend()

    # Adds these things to the figure: title, xticks rotation, (x,y) axis label
    plt.title('India Corona Data')
    plt.xticks(rotation=90)
    plt.xlabel('States')
    plt.ylabel('People Affected')

    # Add Height to individual bars
    def autoLabel(rects):
        for rect in rects:
            height = rect.get_height()
            
            # Formatting and placing the height
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        fontsize='5',
                        xytext=(0, 5),
                        textcoords="offset points",
                        ha='center', va='bottom', rotation='90')

    autoLabel(bar_a)
    autoLabel(bar_c)
    autoLabel(bar_d)

    # Set plot dimensions
    plt.gcf().set_size_inches(15, 5)

    # Most important thing which displays the graph
    plt.show()


def change(old, new):
    '''
    Provides the increment/decrement in cases on daily basis

    >>> change(2, 6)
    >>> 4↑

    >>> change(5, 3)
    >>> 2↓
    '''
    return '⇔ ' + str(abs(int(old) - int(new))) + ('↓' if old > new else '↑' if old < new else '•')


if __name__ == '__main__':

    # Official Covid-19 cases tracker
    urlAPI = 'https://www.mohfw.gov.in/data/datanew.json'

    # Get the response and pasrse to JSON
    response = requests.post(urlAPI).json()

    # Store the data of each state in a list
    data = []
    for x in response:
        data.append([x['sno'],
                     x['state_name'][:22],
                     int(x['new_active']),
                     change(x['active'], x['new_active']),
                     int(x['new_cured']),
                     change(x['cured'], x['new_cured']),
                     int(x['new_death']),
                     change(x['death'], x['new_death'])])

    # Create the dataframe from the data list
    df = pd.DataFrame(data, columns=['S. No.',
                                     'Name of State/UT',
                                     'Active Cases',
                                     'aChange',
                                     'Cured Cases',
                                     'cChange',
                                     'Death Cases',
                                     'dChange'])

    # Last row of dataframe is Total Case
    df.at[36, 'S. No.'] = ''
    df.at[36, 'Name of State/UT'] = 'Total Cases'

    # Prints dataframe without the indices and proper alignment
    print(df.to_string(formatters={'aChange': '{:<8s}'.format,
                                   'cChange': '{:<8s}'.format,
                                   'dChange': '{:<8s}'.format},
                       index=False,
                       justify='right'))

    # Displays the Graph
    graph(df)

