
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime

THRESHOLD_CONDITIONS = 3
SLIDE_BACKGROUND_COLOR = '#212121'
def get_slide_background_color():
    return SLIDE_BACKGROUND_COLOR
def generate_vertical_bar_graph(df, variable, 
                                ax=None,
                                chart_title="", 
                                variable_readable="", 
                                variable_labels={}):

    if(not(variable_readable)):
        variable_readable = variable

    if not(variable_labels):
        variable_labels={key: key for key in df[variable].unique().tolist()}
    
    if not(ax):
        fig, ax = plt.subplots(figsize=(6, 4), facecolor=SLIDE_BACKGROUND_COLOR)


    variable_distribution = (df[variable]
                            .value_counts(normalize=True, sort=False) * 100
                            )
    
    
    variable_distribution.plot(kind='bar', ax=ax)

    # Adds percentages above the bars
    for i, v in enumerate(variable_distribution):
        ax.text(i, v + 1, 
                f'{int(v)}%', 
                ha='center', 
                va='bottom',
                fontsize=10)

    ax.set_title(f'Distribution of {variable_readable}', fontsize=16, pad=20)
    ax.set_xlabel(variable_readable)

    # Set custom labels for x-axis ticks
    ax.set_xticks(range(len(variable_distribution)))
    ax.set_xticklabels(
        [variable_labels.get(key, key) for key in variable_distribution.index], 
        rotation=0)
    
    ax.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False) 
    ax.spines['left'].set_visible(False) 
    ax.set_facecolor(SLIDE_BACKGROUND_COLOR) 


def generate_horizontal_bar_graph(df, 
                                  categorical_variable,
                                  variable_x="count",
                                  ax=None,
                                  chart_title="", 
                                  variable_readable="", 
                                  variable_labels={}):
    '''
    Create a horizontal bar graph showing variable_x or count 
    for each class of a categorical variable
    '''
    if(not(variable_readable)):
        variable_readable = categorical_variable

    if not(variable_labels):
        variable_labels={key: key for key in df[categorical_variable].unique().tolist()}

    if not(ax):
        fig, ax = plt.subplots(figsize=(6, 12), facecolor=SLIDE_BACKGROUND_COLOR)

    if variable_x == "count":
        variable_distribution = (df[categorical_variable]
                                .map(variable_labels)
                                .value_counts(normalize=True) * 100
                                )
        df = (variable_distribution
              .sort_values(ascending=True)
              .reset_index()
              )
        # Rename column 'index' to categorical_variable
        df = df.rename(
            columns={categorical_variable: variable_x,
                     'index': categorical_variable
                     })
        bars = ax.barh(df[categorical_variable],
                df[variable_x])
        # Adds percentages above the bars
        for i, v in enumerate(df[variable_x]):
            ax.text(v + 1, i, 
                    f'{int(v)}%', 
                    ha='left', 
                    va='center',
                    fontsize=10)

    else:
        bars = ax.barh(df[categorical_variable],
                       df[variable_x])
        # Adds labels above the bars
        for i, v in enumerate(df[variable_x]):
            ax.text(v + 1, i, 
                    f'{int(v)}', 
                    ha='left', 
                    va='center',
                    fontsize=10)

    ax.set_title(f'Distribution of {variable_readable}', 
                 fontsize=16, 
                 pad=20, 
                 loc='center')
    ax.set_ylabel(variable_readable)
    ax.set_yticklabels(df[categorical_variable])
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)
    
    if(ax.get_legend()):
        ax.get_legend().remove()
    
    ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False) 
    ax.spines['bottom'].set_visible(False) 
    ax.set_facecolor(SLIDE_BACKGROUND_COLOR) 



def generate_conditions_summary(df, conditions_readable_map):
    '''
    
    '''
    # Create subplots with one column and as many rows as there are conditions
    num_conditions = len(conditions_readable_map)
    fig, axs = plt.subplots(
        nrows=num_conditions, 
        ncols=1, 
        figsize=(8, 0.45*num_conditions),
        facecolor=SLIDE_BACKGROUND_COLOR
        )
    fig.suptitle('Presence of Chronic Illnesses', fontsize=16)
    for i, (condition_variable_name, condition_contents) in enumerate(conditions_readable_map.items()):
        
        condition_readable_name = condition_contents[0]
        conditions_map = condition_contents[1]

        # Calculate the percentage of 'Yes's in the current condition column
        percentage_condition = (
            df[condition_variable_name]
            .value_counts(normalize=True) * 100
        ).loc[conditions_map['Yes']]

        axs[i].barh([condition_readable_name], [percentage_condition])

        # Display the percentage label at the bottom
        axs[i].text(x=0,
                    y=0,
                    s=f'{condition_readable_name}: {percentage_condition:.0f}% ',
                    ha='right',
                    va='center')
        axs[i].set_xlim(0, 100) 

        axs[i].set_yticks([])
        axs[i].set_xticks([]) 
        axs[i].spines['top'].set_visible(False)   
        axs[i].spines['right'].set_visible(False) 
        axs[i].spines['bottom'].set_visible(False) 
        axs[i].set_facecolor(SLIDE_BACKGROUND_COLOR) 

    # Just want the x axis ticks at the bottom
    axs[num_conditions - 1].set_xticks([20, 40, 60, 80, 100])  

    plt.tight_layout()
    plt.show()

def get_beneficiary_age(df, age_variable, reference_date_str):
    df[age_variable] = pd.to_datetime(df[age_variable], format='%Y%m%d')
    reference_date = datetime.strptime(reference_date_str, '%Y%m%d')
    df['age'] = (reference_date - df[age_variable]).astype('<m8[Y]')

    # Create a new categorical variable 'age_group'
    bins = [-float('inf'), 25, 65, 70, 75, 80, 85, 90, float('inf')]
    ages = ['1','2','3','4','5','6','7','8']

    df['age_group'] = pd.cut(df['age'], 
                             bins=bins, 
                             labels=ages,
                             right=False)
    return df

def customise_graph_dark_mode(axis):
    '''
    Make sure to run this before setting graph titles
    '''
    axis.set_facecolor('black') 
    axis.set_title('Sample Text', color='grey')
    axis.set_xlabel('Sample Text', color='grey')
    axis.set_ylabel('Sample Text', color='grey')
    axis.tick_params(axis='x', colors='grey')  
    axis.tick_params(axis='y', colors='grey')  
    axis.spines['bottom'].set_color('grey') 
    axis.spines['left'].set_color('grey')   
    axis.spines['top'].set_visible(False)   
    axis.spines['right'].set_visible(False) 
    

def display_dataframe_with_all_rows(df):
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
#     pd.set_option('display.max_colwidth', 100)
    print(df)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')
#     pd.reset_option('display.max_colwidth')

def combine_conditions(row, columns_to_combine):
    ''' columns_to_combine is a dict'''
    conditions = []
    for col in columns_to_combine:
        condition_readable_name = columns_to_combine[col][0]
        conditions_map = columns_to_combine[col][1]

        if row[col] == conditions_map['Yes']:
            conditions.append(condition_readable_name)

    if conditions:
        if len(conditions) >= THRESHOLD_CONDITIONS:
            return 'Multiple'
        else:
            return ' & '.join(conditions)
    else:
        return 'None'


def get_illness_var_type(df):
    df['illness_var_type'] = np.where(
    (df['combined_condition'] == 'Multiple') | (df['combined_condition'] == 'None'),
    df['combined_condition'],
    'Combination of 2 illnesses')
    return df

def apply_currency_formatting(amount):
    return '${:,.0f}'.format(amount)