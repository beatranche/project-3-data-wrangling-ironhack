import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from IPython.display import display  # Import display for Jupyter notebooks


sns.set_theme(style="ticks")

# Function to read dataframes from a CSV file
def get_dataframes_from_csv(file_path):
    '''
    Reads a CSV file from the given file path and returns a DataFrame.
    
    Parameters:
    file_path (str): The path to the CSV file to be read.
    
    Returns:
    DataFrame: The DataFrame containing data from the CSV file.
    '''
    df_downloaded = pd.read_csv(file_path)
    return df_downloaded

# Function to merge two DataFrames
def merge_dataframes(df_europe, df_asia):
    '''
    Merges two DataFrames by concatenating them along the row axis.
    
    Parameters:
    df_europe (DataFrame): The DataFrame containing data for European countries.
    df_asia (DataFrame): The DataFrame containing data for Asian countries.
    
    Returns:
    DataFrame: The merged DataFrame containing data from both European and Asian countries.
    '''
    merged_df = pd.concat([df_europe, df_asia], axis=0)
    return merged_df

# Function to drop rows with missing values
def drop_missing_values(df):
    '''
    Removes rows with any missing values from the DataFrame.
    
    Parameters:
    df (DataFrame): The DataFrame from which missing values will be removed.
    
    Returns:
    DataFrame: The DataFrame with missing values removed.
    '''
    df_clean = df.dropna()
    return df_clean

# Function to rename columns
def rename_columns(df, columns_mapping):
    '''
    Renames columns in the DataFrame based on the provided mapping and filters columns.
    
    Parameters:
    df (DataFrame): The DataFrame with columns to be renamed.
    columns_mapping (dict): A dictionary mapping old column names to new column names.
    
    Returns:
    DataFrame: The DataFrame with renamed and filtered columns.
    '''
    df = df.rename(columns=columns_mapping)
    df = df.filter(items=['Country', 'Date_of_Consumption_and_Loss_Electricity', 
                         'Electricity_Consumption', 'Loss_electricity', 
                         'Year_of_Emissions_of_CarbonDioxide_Electricity', 
                         'Emissions_CarbonDioxide_ElectricityGeneration'])
    return df

# Function to convert date columns to integer 
def convert_date_to_integer(df, column_names):
    '''
    Converts specified date columns in the DataFrame to integer type.
    
    Parameters:
    df (DataFrame): The DataFrame with date columns to be converted.
    column_names (list): A list of column names to be converted to integer.
    
    Returns:
    DataFrame: The DataFrame with date columns converted to integers.
    '''
    for column_name in column_names:
        df[column_name] = df[column_name].astype('Int64')
    return df

# Function to filter data by continent
def get_continents(df, continent):
    '''
    Filters the DataFrame to include only rows for the specified continent.
    
    Parameters:
    df (DataFrame): The DataFrame to be filtered.
    continent (str): The continent to filter by ('Europe' or 'Asia').
    
    Returns:
    DataFrame: The filtered DataFrame containing data for the specified continent.
    '''
    eu_countries = {
        'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic',
        'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary',
        'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
        'Spain', 'Sweden'
    }

    asian_countries = {
        'Armenia', 'Azerbaijan', 'Georgia', 'Kazakhstan', 'Cyprus', 'Turkey', 'Russia',
        'Saudi Arabia', 'Iran', 'Iraq', 'Syria', 'Lebanon', 'Jordan', 'Israel', 'Palestine',
        'United Arab Emirates', 'Oman', 'Yemen', 'Kuwait', 'Bahrain', 'Qatar', 'Afghanistan',
        'Pakistan', 'India', 'Nepal', 'Bhutan', 'Maldives', 'Sri Lanka', 'China', 'Mongolia',
        'North Korea', 'South Korea', 'Japan', 'Taiwan'
    }

    if continent == 'Europe':
        return df[df['Country'].isin(eu_countries)]
    elif continent == 'Asia':
        return df[df['Country'].isin(asian_countries)]
    else:
        return None

# Function to sort DataFrame by electricity consumption
def sort_by_electric_consumption(df):
    '''
    Sorts the DataFrame by electricity consumption in descending order.
    
    Parameters:
    df (DataFrame): The DataFrame to be sorted.
    
    Returns:
    DataFrame: The sorted DataFrame with the highest electricity consumption first.
    '''
    return df.sort_values(by='Electricity_Consumption', ascending=False)

# Function to create graphs for electricity consumption and loss
def create_graph(df, continent_name):
    '''
    Creates a bar plot for electricity consumption and loss for the specified continent.
    
    Parameters:
    df (DataFrame): The DataFrame containing data to be plotted.
    continent_name (str): The name of the continent (e.g., 'Europe' or 'Asia').
    
    Returns:
    None: Displays the bar plot.
    '''
    # Adjust scaling based on continent
    if continent_name == 'Asia':
        df['Electricity_Consumption'] = df['Electricity_Consumption'] / 1e12  # Convert to trillions (1 trillion = 1,000 billion)
        df['Loss_electricity'] = df['Loss_electricity'] / 1e12  # Convert to trillions
        y_label = 'Gigawatt-hours (In Trillions)'
    elif continent_name == 'Europe':
        df['Electricity_Consumption'] = df['Electricity_Consumption'] / 1e9  # Convert to billions
        df['Loss_electricity'] = df['Loss_electricity'] / 1e9  # Convert to billions
        y_label = 'Gigawatt-hours (In Billions)'
    else:
        raise ValueError("Continent name must be 'Europe' or 'Asia'")
    
    df_melted = df.melt(id_vars='Country', 
                        value_vars=['Electricity_Consumption', 'Loss_electricity'],
                        var_name='Metric', value_name='Value')

    plt.figure(figsize=(14, 7))
    sns.barplot(x='Country', y='Value', hue='Metric', data=df_melted, palette='coolwarm')
    plt.xticks(rotation=45, ha='right')
    plt.title(f'Electricity Consumption and Loss in GWh - {continent_name}')
    plt.xlabel('Country')
    plt.ylabel(y_label)
    plt.legend(title='Metric')
    plt.tight_layout()
    plt.show()


# Function to create CO2 emissions graphs# Function to create CO2 emissions graphs
def create_co2_graph(df, continent_name):
    """
    Create a bar plot for CO2 emissions from electricity generation for a specific continent.
    The emissions values are divided by 1e6 to convert them from tons to millions of tons.
    """
    # Convert emissions values from tons to millions of tons
    df['Emissions_CarbonDioxide_ElectricityGeneration'] = df['Emissions_CarbonDioxide_ElectricityGeneration'] / 1e6
    
    # Filter to only include the top 10 countries with the highest emissions
    df_top_10 = df.nlargest(10, 'Emissions_CarbonDioxide_ElectricityGeneration')
    
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Country', y='Emissions_CarbonDioxide_ElectricityGeneration', data=df_top_10, palette='viridis')
    plt.xticks(rotation=45, ha='right')
    plt.title(f'CO2 Emissions from Electricity Generation - {continent_name}')
    plt.xlabel('Country')
    plt.ylabel('Emissions (In Millions of Tons per Year)')
    plt.tight_layout()
    plt.show()


# Function to create and save separate CO2 emissions graphs for Europe and Asia
def create_separate_co2_graphs(df_europe, df_asia):
    """
    Create separate CO2 emissions bar plots for Europe and Asia.
    """
    # Create CO2 emissions graph for Europe
    create_co2_graph(df_europe, 'Europe')

    # Create CO2 emissions graph for Asia
    create_co2_graph(df_asia, 'Asia')

import pandas as pd

# Recolect all the functions in one main function
def main():
    columns_mapping = {
        'placeName': 'Country',
        'Date:Annual_Consumption_Electricity': 'Date_of_Consumption_and_Loss_Electricity',
        'Value:Annual_Consumption_Electricity': 'Electricity_Consumption',
        'Date:Annual_Loss_Electricity': 'Date_of_Loss_Electricity',
        'Value:Annual_Loss_Electricity': 'Loss_electricity',
        'Date:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Year_of_Emissions_of_CarbonDioxide_Electricity',
        'Value:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Emissions_CarbonDioxide_ElectricityGeneration'
    }
    columns_to_int = ['Date_of_Consumption_and_Loss_Electricity', 'Year_of_Emissions_of_CarbonDioxide_Electricity']

    # Load data from CSV files
    df_europe = get_dataframes_from_csv('Europe_Country.csv')
    df_asia = get_dataframes_from_csv('Asia_Country.csv')

    # Merge the data
    df_merged = merge_dataframes(df_europe, df_asia)

    # Drop missing values
    df_merged = drop_missing_values(df_merged)

    # Rename columns
    df_merged = rename_columns(df_merged, columns_mapping)

    # Replace 'Macedonia [FYROM]' with 'Macedonia'
    df_merged['Country'] = df_merged['Country'].replace('Macedonia [FYROM]', 'Macedonia')

    # Convert date columns to integer
    df_merged = convert_date_to_integer(df_merged, columns_to_int)

    # Get data for each continent
    df_european_countries = get_continents(df_merged, 'Europe')
    df_asian_countries = get_continents(df_merged, 'Asia')

    # Sort results by electric consumption
    df_european_countries = sort_by_electric_consumption(df_european_countries)
    df_asian_countries = sort_by_electric_consumption(df_asian_countries)

    # Create graphs for electricity consumption
    create_graph(df_european_countries.head(10), 'Europe')
    create_graph(df_asian_countries.head(10), 'Asia')

    # Create separate CO2 emissions graphs for Europe and Asia
    create_separate_co2_graphs(df_european_countries, df_asian_countries)

    # Reset index to ensure it's continuous
    df_merged.reset_index(drop=True, inplace=True)

    # Display the cleaned and formatted DataFrame
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print('Table information:')
    display(df_merged)