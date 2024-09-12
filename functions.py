import requests  # HTTP requests for APIs
import pandas as pd  # Data manipulation with DataFrames
import matplotlib.pyplot as plt  # Plotting and visualizations
import seaborn as sns  # Statistical data visualization
import matplotlib as mpl  # Additional plot customization
# Set the Seaborn theme to "ticks", which applies a clean style with ticks on the axes for better readability of the plots.
sns.set_theme(style="ticks")
import warnings
    

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

def generar_markdown_inicio():
 
    markdown = """
# Análisis de Datos de Consumo Eléctrico, Pérdida y Emisiones de CO2

## Introducción

Este proyecto tiene como objetivo analizar los datos de consumo de electricidad, pérdida de electricidad y emisiones de CO2 en países de Europa y Asia. La pregunta central que guía este análisis es:

**¿Cómo puede la inteligencia artificial mejorar la sostenibilidad o reducir el impacto ambiental?**

Para responder a esta pregunta, realizamos un análisis detallado de los siguientes aspectos:

1. Consumo de electricidad.
2. Pérdida de electricidad.
3. Emisiones de CO2 generadas por la producción de electricidad.

## Metodología

Las visualizaciones incluyen gráficos de barras para observar:

1. **Consumo y pérdida de electricidad** en gigavatios-hora (GWh) para cada continente.
2. **Emisiones de CO2** en millones de toneladas por país.

Los gráficos son generados usando las librerías **Seaborn** y **Matplotlib** para obtener visualizaciones claras y concisas que permitan interpretar los datos de forma efectiva.

## Aplicación de la IA a la Sostenibilidad

A partir de este análisis, exploraremos cómo la inteligencia artificial puede ser aplicada para:

- Optimizar el uso de electricidad.
- Reducir las pérdidas en la red eléctrica.
- Minimizar las emisiones de CO2 mediante tecnologías predictivas y soluciones basadas en datos.

## Conclusión

Este estudio proporciona una visión general de los patrones de consumo energético y su impacto ambiental en Europa y Asia. La inteligencia artificial tiene el potencial de mejorar la sostenibilidad mediante la optimización de recursos y la reducción del impacto ambiental.

### Realizado por Beatriz Tranche y Carlos Vergara
________________________________________________________________________________________________________________________________________________
    """
    return markdown.strip()

def markdown_EDA():
    
    markdown = '''
    
## Exploratory Data Analysis

### Gráficos de Consumo Eléctrico y Pérdida

A continuación, se presentan gráficos de barras que muestran el consumo de electricidad y la pérdida para los 10 principales países de Europa y Asia. Estos gráficos permiten comparar el uso de electricidad entre países y analizar las pérdidas en la red eléctrica.
    
'''
    
    return markdown.strip()

def markdown_data_cleaning():
    markdown = '''
## Estructura del Código

El análisis está dividido en varias funciones clave:

1. **Lectura y procesamiento de datos**: Lectura de archivos CSV que contienen los datos de países europeos y asiáticos.
2. **Fusión y limpieza de datos**: Combinación de los conjuntos de datos de Europa y Asia, y eliminación de valores nulos.
3. **Renombrar columnas**: Estandarización de los nombres de columnas para facilitar su interpretación.
4. **Filtrado por continente**: Selección de países de Europa y Asia para realizar comparaciones regionales.
5. **Creación de gráficos**: Visualización de:
- Consumo y pérdida de electricidad.
- Emisiones de CO2 por generación eléctrica.

## Análisis de Datos

El análisis incluye:

- **Consumo de electricidad**: Comparación de los países con mayor consumo de electricidad en Europa y Asia.
- **Pérdida de electricidad**: Análisis de la pérdida de electricidad como proporción del consumo.
- **Emisiones de CO2**: Identificación de los países con mayores emisiones de CO2 relacionadas con la producción de electricidad.
        '''
    return markdown.strip()

def markdown_table_info():
    
    markdown = '''
## Visualización de la Tabla de Datos

### Descripción

La tabla muestra datos de consumo de electricidad, pérdida y emisiones de CO2 para países de Europa y Asia. Los datos están organizados con las siguientes columnas:

- **Country**: Nombre del país.
- **Date_of_Consumption_and_Loss_Electricity**: Año de registro.
- **Electricity_Consumption**: Consumo de electricidad (GWh).
- **Loss_electricity**: Pérdida de electricidad (GWh).
- **Year_of_Emissions_of_CarbonDioxide_Electricity**: Año de emisiones de CO2.
- **Emissions_CarbonDioxide_ElectricityGeneration**: Emisiones de CO2 (toneladas).

### Notas

Los datos han sido limpiados y estandarizados para asegurar la calidad y consistencia en el análisis.
    '''
    return markdown.strip()

# Recolect all the functions in one main function
def main():
    
    '''
    This function processes and analyzes data related to electricity consumption, loss, and CO2 emissions 
    for countries in Europe and Asia. The function reads data from CSV files, merges them, cleans the data, 
    renames columns, handles missing values, and generates visualizations.
    '''
    from IPython.display import Markdown, display
    
    warnings.filterwarnings('ignore')
    
    
    
   
    display(Markdown(generar_markdown_inicio()))
    
    # A dictionary to map the original column names from the dataset to more descriptive and consistent names
    columns_mapping = {
        'placeName': 'Country',
        'Date:Annual_Consumption_Electricity': 'Date_of_Consumption_and_Loss_Electricity',
        'Value:Annual_Consumption_Electricity': 'Electricity_Consumption',
        'Date:Annual_Loss_Electricity': 'Date_of_Loss_Electricity',
        'Value:Annual_Loss_Electricity': 'Loss_electricity',
        'Date:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Year_of_Emissions_of_CarbonDioxide_Electricity',
        'Value:Annual_Emissions_CarbonDioxide_ElectricityGeneration': 'Emissions_CarbonDioxide_ElectricityGeneration'
    }

    # A list of columns that contain dates, which will be converted to integers representing years
    columns_to_int = ['Date_of_Consumption_and_Loss_Electricity', 'Year_of_Emissions_of_CarbonDioxide_Electricity']

    # Load data from CSV files
    '''
    The function reads two CSV files, one for Europe and another for Asia, containing data on electricity consumption, 
    loss, and CO2 emissions. The data is loaded into pandas DataFrames for further processing.
    '''
    df_europe = get_dataframes_from_csv('Europe_Country.csv')
    df_asia = get_dataframes_from_csv('Asia_Country.csv')

    # Merge the data
    '''
    After loading, the data from Europe and Asia is merged into a single DataFrame. This allows for easier 
    comparison and analysis between the two regions.
    '''
    df_merged = merge_dataframes(df_europe, df_asia)

    # Drop missing values
    '''
    To ensure the quality of the analysis, rows with missing values are dropped from the merged DataFrame.
    This step helps to avoid errors or inconsistencies during data analysis.
    '''
    df_merged = drop_missing_values(df_merged)

    # Rename columns
    '''
    The columns in the DataFrame are renamed based on the `columns_mapping` dictionary for clarity and consistency, 
    making the dataset easier to understand and work with.
    '''
    df_merged = rename_columns(df_merged, columns_mapping)

    # Replace 'Macedonia [FYROM]' with 'Macedonia'
    '''
    This step cleans up a specific country name, replacing "Macedonia [FYROM]" with "Macedonia" for uniformity 
    in the country names.
    '''
    df_merged['Country'] = df_merged['Country'].replace('Macedonia [FYROM]', 'Macedonia')

    # Convert date columns to integer
    '''
    The columns that represent dates (years) are converted from float or string to integer format to ensure 
    consistency and make them easier to handle during analysis or visualization.
    '''
    df_merged = convert_date_to_integer(df_merged, columns_to_int)

    # Get data for each continent
    '''
    The merged dataset is split back into separate DataFrames for Europe and Asia, making it possible to analyze 
    and visualize data by continent. This helps to compare electricity consumption, loss, and CO2 emissions 
    between Europe and Asia.
    '''
    df_european_countries = get_continents(df_merged, 'Europe')
    df_asian_countries = get_continents(df_merged, 'Asia')

    
    # Sort results by electric consumption
    '''
    Both the European and Asian datasets are sorted by electricity consumption. This allows for ranking and 
    further analysis, such as identifying the top electricity-consuming countries.
    '''
    df_european_countries = sort_by_electric_consumption(df_european_countries)
    df_asian_countries = sort_by_electric_consumption(df_asian_countries)

    # Create a markdown to explain the analysis
    display(Markdown(markdown_EDA()))
    
    # Create graphs for electricity consumption
    '''
    Bar charts are created to visualize the top 10 electricity-consuming countries in Europe and Asia. These 
    visualizations help in comparing the countries within each continent.
    '''
    create_graph(df_european_countries.head(10), 'Europe')
    create_graph(df_asian_countries.head(10), 'Asia')

    # Create separate CO2 emissions graphs for Europe and Asia
    '''
    Separate graphs are generated for CO2 emissions related to electricity generation in Europe and Asia. 
    This step provides insights into the environmental impact of electricity consumption in both regions.
    '''
    create_separate_co2_graphs(df_european_countries, df_asian_countries)


    # Reset index to ensure it's continuous
    '''
    After merging the datasets, the index may not be continuous. This step resets the index to avoid any confusion 
    or issues in further analysis and visualization.
    '''
    df_merged.reset_index(drop=True, inplace=True)
    display(Markdown(markdown_data_cleaning()))
    
    # Display the cleaned and formatted DataFrame
    '''
    The full DataFrame with all rows and columns is displayed to provide a complete overview of the cleaned data. 
    This ensures that the data is correct and formatted properly before further analysis or export.
    '''
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    print('Table information:')
    display(df_merged)
    
    display(Markdown(markdown_table_info()))