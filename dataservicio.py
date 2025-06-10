import nest_asyncio
from fastapi import FastAPI, Query
import uvicorn
import pandas as pd

# Permite que FastAPI funcione dentro de Jupyter
nest_asyncio.apply()

# Carga tu dataset
# Cambia el nombre del archivo si es necesario
df = pd.read_csv('data_actualizado.csv', parse_dates=['Date'])

app = FastAPI(
    title="Microservicio de Consulta de Dataset",
    description="Filtra registros por fecha y pagina los resultados.",
    version="1.0"
)

@app.get("/")
def home():
    return {"mensaje": "Microservicio activo. Usa /registros para consultar datos."}

@app.get("/registros")
def get_registros(
    fecha: str = Query(None, description="Fecha exacta (yyyy-mm-dd)"),
    fecha_inicio: str = Query(None, description="Fecha inicial (yyyy-mm-dd)"),
    fecha_fin: str = Query(None, description="Fecha final (yyyy-mm-dd)"),
    page: int = Query(1, ge=1, description="Número de página (empieza en 1)"),
    limit: int = Query(10, ge=1, le=100, description="Registros por página (máx 100)")
):
    data = df.copy()
    # Filtrado por fecha exacta
    if fecha:
        data = data[data['Date'] == fecha]
    # Filtrado por rango de fechas
    elif fecha_inicio and fecha_fin:
        data = data[(data['Date'] >= fecha_inicio) & (data['Date'] <= fecha_fin)]
    elif fecha_inicio:
        data = data[data['Date'] >= fecha_inicio]
    elif fecha_fin:
        data = data[data['Date'] <= fecha_fin]

    # Paginación
    total = len(data)
    start = (page - 1) * limit
    end = start + limit
    paginated = data.iloc[start:end]

    return {
        "total_registros": total,
        "pagina": page,
        "por_pagina": limit,
        "registros": paginated.to_dict(orient='records')
    }

# Dirección y puerto personalizados
DIRECCION = "127.0.0.1"  # O usa "0.0.0.0" para exponerlo en todas las interfaces
PUERTO = 3033

# Ejecuta el servidor FastAPI en Jupyter
uvicorn.run(app, host=DIRECCION, port=PUERTO)
