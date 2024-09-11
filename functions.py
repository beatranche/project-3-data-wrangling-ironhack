import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Funtion to read dataframes fron a CSV file
def get_dataframes_from_csv(file_path):
    """
    Reads a CSV file and returns its content as a pandas DataFrame.

    Parameters
    ----------
    file_path : str
        The path to the CSV file to be read.

    Returns
    -------
    pandas.DataFrame
        The content of the CSV file as a pandas DataFrame.
    """
    # Read the CSV file into a DataFrame.
    # The 'pd.read_csv' function will automatically detect the delimiter and the data types of the columns.
    df_downloaded = pd.read_csv(file_path)
    
    # Return the DataFrame
    return df_downloaded



# Merge the two DataFrames  
def merge_dataframes(df_europe, df_asia):
    """
    Merge two DataFrames together.

    Parameters
    ----------
    df_europe : pandas.DataFrame
        The first DataFrame to be merged.
    df_asia : pandas.DataFrame
        The second DataFrame to be merged.

    Returns
    -------
    pandas.DataFrame
        The merged DataFrame.
    """
    # Concatenate the two DataFrames along the 0th axis (rows)
    merged_df = pd.concat([df_europe, df_asia], axis=0)

    # Return the merged DataFrame
    return merged_df

# Drop the rows with missing values
def drop_missing_values(df):
    """
    Drop the rows with missing values from the given DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be cleaned.

    Returns
    -------
    pandas.DataFrame
        The cleaned DataFrame with no missing values.
    """
    # Drop the rows with missing values
    df_clean = df.dropna()

    return df_clean

# Function to rename columns names
def rename_columns(df, columns_mapping):
    """
    Rename the columns of the given DataFrame based on the given mapping.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to be renamed.
    columns_mapping : dict
        A dictionary with the old column names as keys and the new column names as values.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the renamed columns.
    """
    # Rename the columns based on the given mapping
    df = df.rename(columns=columns_mapping)

    # Filter the columns to only include the ones we are interested in
    df = df.filter(items=['Country', 'Date_of_Consumption_and_Loss_Electricity', 
                         'Electricity_Consumption', 'Loss_electricity', 
                         'Year_of_Emissions_of_CarbonDioxide_Electricity', 
                         'Emissions_CarbonDioxide_ElectricityGeneration'])

    # Return the DataFrame with the renamed columns
    return df

# Function to convert date columns to integer 
def convert_date_to_integer(df, column_name):
    """
    Convert the given column of the given DataFrame to integer type.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame containing the column to be converted.
    column_name : str
        The name of the column to be converted.

    Returns
    -------
    pandas.DataFrame
        The DataFrame with the converted column.
    """
    # Convert the given column to integer type
    df[column_name] = df[column_name].astype('Int64')

    # Return the DataFrame with the converted column
    return df

# Function to create a grafic

def create_graph(data):
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Melt the DataFrame to plot in a grouped bar chart
    df_melted = df.melt(id_vars='Country', 
                        value_vars=['Electricity_Consumption', 'Loss_electricity', 'Emissions_CarbonDioxide_ElectricityGeneration'],
                        var_name='Metric', value_name='Value')

    # Set up the plot
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Country', y='Value', hue='Metric', data=df_melted)

    # Add labels and title
    plt.title('Electricity Consumption, Loss, and CO2 Emissions by Country')
    plt.ylabel('Value')
    plt.xticks(rotation=45)

    # Display the plot
    plt.tight_layout()
    plt.show()




def main():
    
    columns_mapping = {
        'placeName': 'Country',
        'Date:Annual_Consumption_Electricity': 'Date_of_Consumption_and_Loss_Electricity',
        'Value:Annual_Consumption_Electricity': 'Electricity_Consumption',
        'Date:Annual_Loss_Electricity': 'Date_of_Loss_Electricity',  # Updated name
        'Value:Annual_Loss_Electricity': 'Loss_electricity',
        'Date:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Year_of_Emissions_of_CarbonDioxide_Electricity',
        'Value:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Emissions_CarbonDioxide_ElectricityGeneration'
    }
    
    columns_to_int = ['Date_of_Consumption_and_Loss_Electricity', 'Year_of_Emissions_of_CarbonDioxide_Electricity']
    
    df_europe = get_dataframes_from_csv('Europe_Country.csv')
    df_asia = get_dataframes_from_csv('Asia_Country.csv')
    df_merged = merge_dataframes(df_europe, df_asia)
    df_merged = drop_missing_values(df_merged)
    df_merged = rename_columns(df_merged, columns_mapping)
    df_merged = convert_date_to_integer(df_merged, columns_to_int)
    display(df_merged.head(5))
    
    create_graph(df_merged)
    
    

    