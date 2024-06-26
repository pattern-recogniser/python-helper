
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime

THRESHOLD_CONDITIONS = 3
SLIDE_BACKGROUND_COLOR = '#212121'
SAMPLE_PERCENTAGE = 0.05

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

    if not(chart_title):
        chart_title = f'Distribution of {variable_readable}'

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
                       df[variable_x]
                    #    ,color='lightgreen',
                    #    height=0.25
                       )
        # Adds labels above the bars
        for i, v in enumerate(df[variable_x]):
            ax.text(v + 1, i, 
                    f'{int(v)}', 
                    ha='left', 
                    va='center',
                    fontsize=10)

    ax.set_title(chart_title, 
                 fontsize=16, 
                 pad=20, 
                 loc='center')
    ax.set_ylabel(variable_readable)
    # ax.set_yticklabels(df[categorical_variable])
    
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
    # Calculate the prevalence of each condition
    condition_prevalence = {}
    for condition_variable_name, condition_contents in conditions_readable_map.items():
        conditions_map = condition_contents[1]
        prevalence = df[condition_variable_name].eq(conditions_map['Yes']).mean() * 100
        condition_prevalence[condition_variable_name] = prevalence

    # Sort conditions based on prevalence
    sorted_conditions = sorted(condition_prevalence.items(), key=lambda x: x[1], reverse=True)

    # Create subplots with one column and as many rows as there are conditions
    num_conditions = len(sorted_conditions)
    fig, axs = plt.subplots(
        nrows=num_conditions, 
        ncols=1, 
        figsize=(8, 0.45*num_conditions),
        facecolor=SLIDE_BACKGROUND_COLOR
        )
    fig.suptitle('Presence of Chronic Illnesses', fontsize=16)
    
    for i, (condition_variable_name, prevalence) in enumerate(sorted_conditions):
        condition_contents = conditions_readable_map[condition_variable_name]
        condition_readable_name = condition_contents[0]

        axs[i].barh([condition_readable_name], [prevalence])

        # Display the percentage label at the bottom
        axs[i].text(x=0,
                    y=0,
                    s=f'{condition_readable_name}: {prevalence:.0f}% ',
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
    'Combination of 1 or 2 illnesses')
    return df

def apply_currency_formatting(amount):
    return '${:,.0f}'.format(amount)

def generate_boxplot(df,
                     categorical_variable,
                     categorical_variable_label,
                     metric,
                     metric_label,
                     ax=None):
    
    # Calculate the IQR for each group
    iqr_values = (df.groupby(categorical_variable)[metric].quantile(0.75) 
                  - df.groupby(categorical_variable)[metric].quantile(0.25)
    )

    # Sort the groups by decreasing IQR
    sorted_conditions = iqr_values.sort_values(ascending=False).index

    if(not ax):
        fig, ax = plt.subplots(figsize=(12, 30), facecolor=SLIDE_BACKGROUND_COLOR)
    sns.boxplot(x=metric, 
                y=categorical_variable, 
                data=df, 
                order=sorted_conditions,
                ax=ax)

    # Customize the plot
    ax.set_title(f'Distribution of {metric_label} for Each {categorical_variable_label}')
    ax.set_xlabel(metric_label)
    ax.set_ylabel(categorical_variable_label)

    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False) 
    ax.spines['bottom'].set_visible(False) 
    ax.set_facecolor(SLIDE_BACKGROUND_COLOR) 

def generate_clustered_column(df, 
                              categorical_variable, 
                              metric1, 
                              metric1_label,
                              metric2,
                              metric2_label,
                              chart_title,
                              ax=None):

    df.sort_values(by=metric1, ascending=True, inplace=True)

    if not(ax):
        fig, ax = plt.subplots(figsize=(6, 12), facecolor=SLIDE_BACKGROUND_COLOR)

    if not(chart_title):
        chart_title = f'Metrics for Each {categorical_variable}'
    bar_width = 0.25  # Width of each bar
    index = range(len(df))

    # Bar for metric2
    bars_beneficiary_count = ax.barh([i + bar_width for i in index], 
                                     df[metric2], 
                                     bar_width, 
                                     label=metric2_label, 
                                     color='lightgreen')

    # Bar for metric1
    bars_cost_per_illness = ax.barh([i + 2 * bar_width for i in index], 
                                    df[metric1], 
                                    bar_width, 
                                    label=metric1_label, 
                                    color='lightcoral')

    # Set y-axis ticks and labels
    ax.set_yticks([i + bar_width for i in index])
    ax.set_yticklabels(df[categorical_variable])
    ax.spines['top'].set_visible(False)   
    ax.spines['right'].set_visible(False) 
    ax.spines['bottom'].set_visible(False) 

    # Set labels and title
    ax.set_xlabel('Metrics')
    ax.set_title(chart_title)
    ax.legend()
    ax.set_facecolor(SLIDE_BACKGROUND_COLOR) 

    # Adds labels above the bars for metric1
    for i, v in enumerate(df[metric1]):
        ax.text(v + 1,
                i + 0.5, 
                f'{int(v)}', 
                ha='left', 
                va='center',
                fontsize=10)
        
def subset_df_with_greater_than(df,
                               variable,
                               threshold):
    df2 = df[df[variable] > threshold]
    return df2


def get_2combination_illness(df):
    filtered_df = df[
        (df['combined_condition'] != 'Multiple') & 
        (df['combined_condition'] != 'None')
        ]
    return filtered_df

# Helper function to calculate cost reduction

def calculate_savings(new_column, 
                      old_column):
    total_cost_2years = beneficiary_claims_df['CLM_PMT_AMT'].sum()
    absolute_difference = sum(old_column) - sum(new_column) 
    perc_difference = 100 * absolute_difference / total_cost_2years
    print(f'Perc difference in total cost: {round(perc_difference)}%')
    absolute_difference_extrapolated = absolute_difference * (1 / SAMPLE_PERCENTAGE)
    print(f'Reduction in cost in 2yr period: {absolute_difference_extrapolated:,.0f}')

def get_optimised_cost(df):
    df['optimised_cost'] = (df['beneficiary_count'] * df['optimised_CPM'])
    return df

