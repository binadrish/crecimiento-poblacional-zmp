import requests
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv

load_dotenv()

token=os.getenv('TOKEN')
syntax={'Pachuca de soto':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130048/false/BISE/2.0/',
        'Mineral de la Reforma':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130051/false/BISE/2.0/',
        'Epazoyucan':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130022/false/BISE/2.0/',
        'Mineral del Monte':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130039/false/BISE/2.0/',
        'San Agustín Tlaxiaca':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130052/false/BISE/2.0/',
        'Zapotlán de Juárez':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130082/false/BISE/2.0/',
        'Zempoala':'https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000001/es/070000130083/false/BISE/2.0/'}

dfs=[]
# Iterar sobre el diccionario
for municipio, url in syntax.items():
    # Realizar la petición para cada municipio
    response = requests.get(url + token + '?type=json')
    
    # Verificar que la petición fue exitosa
    if response.status_code == 200:
        # Convertir el contenido a JSON
        json_data = response.json()
        
        # Extraer las observaciones (OBSERVATIONS)
        observations = json_data['Series'][0]['OBSERVATIONS']
        
        # Crear un DataFrame con TIME_PERIOD (año) y OBS_VALUE (población)
        df = pd.DataFrame(observations)[['TIME_PERIOD', 'OBS_VALUE']]
        
        # Convertir la columna OBS_VALUE a tipo numérico (float)
        df['OBS_VALUE'] = pd.to_numeric(df['OBS_VALUE'])
        
        # Renombrar columnas para mayor claridad
        df.columns = ['Año', 'Población']
        
        # Añadir una columna que indique el municipio
        df['Municipio'] = municipio
        
        # Añadir este DataFrame a la lista
        dfs.append(df)
    else:
        print(f"Error en la petición para {municipio}: {response.status_code}")

# Concatenar todos los DataFrames en uno solo
df_total = pd.concat(dfs)

# Mostrar el DataFrame combinado
# Suponiendo que df_total es tu DataFrame combinado
df_1995 = df_total[df_total['Año'] == '1995']
df_2000 = df_total[df_total['Año'] == '2000']
df_2005 = df_total[df_total['Año'] == '2005']
df_2010 = df_total[df_total['Año'] == '2010']
df_2020 = df_total[df_total['Año'] == '2020']


def crecimientoZmp(df_total):
    # Graficar el crecimiento poblacional por municipio
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='Año', y='Población', hue='Municipio', data=df_total, marker='o')

    # Añadir título y etiquetas
    plt.title('Crecimiento Poblacional Zona Metropolitana de Pachuca', fontsize=16)
    plt.xlabel('Año', fontsize=12)
    plt.ylabel('Población', fontsize=12)

    # Mover la leyenda fuera del gráfico
    plt.legend(title='Municipio', bbox_to_anchor=(1.05, 1), loc='upper left')
    # Mostrar la cuadrícula
    plt.grid(True)
    # Guardar el gráfico como una imagen PNG
    plt.savefig('crecimiento_poblacional_zmp.png', bbox_inches='tight')

def anilloPoblacionYear(df):
    df_year=df.copy()
    # Calcular el total de población en un año 
    total_poblacion = df_year['Población'].sum()

    # Calcular el porcentaje de población para cada municipio
    df_year.loc[:, 'Porcentaje'] = (df_year['Población'] / total_poblacion) * 100

    # Crear el gráfico de anillo
    plt.figure(figsize=(8, 8))
    plt.pie(df_2020['Población'], labels=df_year['Municipio'], autopct='%1.1f%%', startangle=90, pctdistance=0.85)

    # Dibujar un círculo en el centro para hacer el anillo
    centre_circle = plt.Circle((0, 0), 0.70, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Añadir título
    plt.title('Distribución Poblacional de la ZMP* en 2020', fontsize=16)

    # Mostrar el gráfico
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.tight_layout()
    plt.savefig('distribucion_poblacional_anillo_year.png', bbox_inches='tight')

crecimientoZmp(df_total)

anilloPoblacionYear(df_2020)