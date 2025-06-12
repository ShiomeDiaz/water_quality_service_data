import pandas as pd
from datetime import datetime, timedelta

# Cargar datos
df = pd.read_csv('dataset_con_ICA_completo.csv')

# Ordena el DataFrame por la columna de fecha original (opcional, pero recomendable)
df = df.sort_values('Date')

# Cuenta cuántos registros hay por cada fecha original (en orden de aparición)
conteo_fechas = df['Date'].value_counts().sort_index()

# Genera las nuevas fechas, desde 10 días en el futuro hacia atrás, una por cada grupo de fecha original
base_futura = datetime.now().date() + timedelta(days=10)
nuevas_fechas = [base_futura - timedelta(days=i) for i in range(len(conteo_fechas))]
nuevas_fechas = nuevas_fechas[::-1]  # Para asignar la fecha más reciente al último grupo

# Crea un diccionario de mapeo: fecha original -> nueva fecha
mapa_fechas = dict(zip(conteo_fechas.index, nuevas_fechas))

# Asigna la nueva fecha a cada registro según su fecha original
df['Date'] = df['Date'].map(mapa_fechas)

# Guarda el resultado
df.to_csv('data_actualizado.csv', index=False)
