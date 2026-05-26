# Paso 1. Importar librerías
import pandas as pd
import matplotlib.pyplot as plt

# Paso 2. Cargar archivos CSV en DataFrames

df_companies = pd.read_csv('moved_project_sql_result_01.csv')
df_neighborhoods = pd.read_csv('moved_project_sql_result_04.csv')

# Paso 3. Estudiar los datos

# Primeras filas
print(df_companies.head())
print()
print(df_neighborhoods.head())

# Información general
print(df_companies.info())
print()
print(df_neighborhoods.info())

# Verificar valores nulos
print(df_companies.isnull().sum())
print()
print(df_neighborhoods.isnull().sum())

# Verificar duplicados
print(df_companies.duplicated().sum())
print(df_neighborhoods.duplicated().sum())

# Paso 4. Asegurarse de que los tipos de datos sean correctos
print(df_companies.dtypes)
print(df_neighborhoods.dtypes)

# Si fuera necesario:
# df_companies['trips_amount'] = df_companies['trips_amount'].astype(int)
# df_neighborhoods['average_trips'] = df_neighborhoods['average_trips'].astype(float)

# Paso 5. Identificar los 10 principales barrios
top_10_neighborhoods = df_neighborhoods.sort_values(
    by='average_trips',
    ascending=False
).head(10)

print(top_10_neighborhoods)

# Paso 6. Gráfico: empresas de taxis y número de viajes
df_companies_sorted = df_companies.sort_values(
    by='trips_amount',
    ascending=False
)

plt.figure(figsize=(12,6))
plt.bar(df_companies_sorted['company_name'],
        df_companies_sorted['trips_amount'])

plt.title('Número de viajes por compañía de taxis')
plt.xlabel('Compañía de taxis')
plt.ylabel('Número de viajes')
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Paso 7. Gráfico: top 10 barrios por finalizaciones
plt.figure(figsize=(12,6))
plt.bar(top_10_neighborhoods['dropoff_location_name'],
        top_10_neighborhoods['average_trips'])

plt.title('Top 10 barrios por promedio de finalización de viajes')
plt.xlabel('Barrio')
plt.ylabel('Promedio de viajes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()