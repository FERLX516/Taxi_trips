# Paso 1. Importar librerías
# pandas: carga, limpieza y manipulación de datos
# matplotlib: visualización de resultados
# scipy.stats.ttest_ind: comparación de medias entre dos grupos
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Paso 2. Cargar archivos CSV en DataFrames
# Los datos se encuentran en CSV locales dentro del workspace.
# En el proyecto de análisis esto simula la recuperación desde el origen
# de datos o desde una consulta SQL previa.
df_companies = pd.read_csv('moved_project_sql_result_01.csv')
df_neighborhoods = pd.read_csv('moved_project_sql_result_04.csv')

# Paso 3. Estudiar los datos
# Primeras filas del dataset
print(df_companies.head())
print()
print(df_neighborhoods.head())

# Información general de cada tabla
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
# Este paso asegura que las columnas numéricas tengan el tipo adecuado
# antes de hacer agregaciones o gráficas.
print(df_companies.dtypes)
print(df_neighborhoods.dtypes)

# Si fuera necesario, se podrían convertir columnas manualmente.
# df_companies['trips_amount'] = df_companies['trips_amount'].astype(int)
# df_neighborhoods['average_trips'] = df_neighborhoods['average_trips'].astype(float)

# Paso 5. Crear slices de datos
# Slice 1: seleccionamos los 10 barrios con mayor promedio de viajes.
# Esto nos ayuda a enfocar el análisis en los barrios que concentran más viajes.
top_10_neighborhoods = df_neighborhoods.sort_values(
    by='average_trips',
    ascending=False
).head(10)

print(top_10_neighborhoods)

# Paso 6. Agrupar y visualizar
# Aunque aquí no hacemos un groupby explícito, sí ordenamos los datos
# por la métrica de interés para ver el ranking de compañías y barrios.
# Esto es útil para identificar patrones de concentración.
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

# Paso 8. Prueba de hipótesis
# En este análisis se trabaja con un único dataset, por lo que no hay
# necesidad de combinaciones como merge/join. La hipótesis se evalúa
# con un slice de datos y la comparación de dos grupos.
#
# Formulación de la hipótesis:
# H0: la duración promedio de los viajes en sábados lluviosos no cambia
#     respecto a sábados con clima favorable.
# H1: la duración promedio de los viajes en sábados lluviosos cambia
#     respecto a sábados con clima favorable.
#
# Criterio de prueba: alpha = 0.05
alpha = 0.05

# Cargar el dataset de hipótesis desde archivo local.
df_hypothesis = pd.read_csv('moved_project_sql_result_07.csv')

# Limpieza y conversión de tipos.
df_hypothesis['start_ts'] = pd.to_datetime(df_hypothesis['start_ts'], errors='coerce')
df_hypothesis['duration_seconds'] = pd.to_numeric(df_hypothesis['duration_seconds'], errors='coerce')
df_hypothesis = df_hypothesis.dropna(subset=['start_ts', 'duration_seconds'])

# Slice de datos para la prueba:
# - sábados
# - clima adverso (Bad) versus clima favorable (Good)
weather = df_hypothesis['weather_conditions'].fillna('').str.lower()
df_hypothesis['is_rainy'] = weather.eq('bad') | weather.str.contains('rain', regex=False)
df_hypothesis['is_saturday'] = df_hypothesis['start_ts'].dt.dayofweek == 5

rainy = df_hypothesis[df_hypothesis['is_saturday'] & df_hypothesis['is_rainy']]
non_rainy = df_hypothesis[df_hypothesis['is_saturday'] & ~df_hypothesis['is_rainy']]

print('\nPrueba de hipótesis: duración promedio en sábados lluviosos')
print('Alpha =', alpha)
print('Observaciones lluviosas:', len(rainy))
print('Observaciones no lluviosas:', len(non_rainy))
print('Media lluviosa (s):', round(rainy['duration_seconds'].mean(), 2))
print('Media no lluviosa (s):', round(non_rainy['duration_seconds'].mean(), 2))

if rainy.empty or non_rainy.empty:
    print('No hay suficientes observaciones en ambos grupos para aplicar la prueba t.')
else:
    # Se usa la prueba t de Welch porque los grupos son independientes
    # y las varianzas pueden ser diferentes.
    t_stat, p_value = ttest_ind(rainy['duration_seconds'], non_rainy['duration_seconds'], equal_var=False)
    print('t:', round(float(t_stat), 4))
    print('p-value:', p_value)

    decision = 'rechazar H0' if p_value < alpha else 'no rechazar H0'
    print('Conclusión:', decision)

    # Resumen listo para el informe.
    print('Resumen para el informe:')
    print(f'- Alfa elegido: {alpha}')
    print(f'- Media en sábados con clima adverso (Bad): {round(rainy["duration_seconds"].mean(), 2)} s')
    print(f'- Media en sábados con clima favorable (Good): {round(non_rainy["duration_seconds"].mean(), 2)} s')
    print(f'- Prueba t de Welch: t = {round(float(t_stat), 4)}, p-value = {p_value}')

    if p_value < alpha:
        print('- Resultado: hay evidencia estadística de que la duración promedio cambia entre ambos grupos.')
        print('Interpretación final: la duración promedio de los viajes desde Loop a O\'Hare es diferente en sábados con clima adverso respecto a sábados con clima favorable.')
    else:
        print('- Resultado: no hay evidencia suficiente para afirmar que la duración promedio cambia entre ambos grupos.')
        print('Interpretación final: no se encontró evidencia estadística de un cambio en la duración promedio entre sábados con clima adverso y sábados con clima favorable.')

print('Nota: el dataset usa los valores Good/Bad en weather_conditions, por lo que Bad se trata como clima adverso/lluvioso para esta prueba.')