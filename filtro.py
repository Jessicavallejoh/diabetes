from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Suponiendo que diabetes_list ya está definida como tu dataset
# Agregamos el endpoint principal con el formulario
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": [], "page": 1, "per_page": 10, "total": 0}
    )

# Endpoint para procesar el filtrado y paginación
@app.get("/filter", response_class=HTMLResponse)
async def filter_data(
    request: Request,
    column: Optional[str] = None,
    value: Optional[str] = None,
    page: int = 1,
    per_page: int = 10
):
    # Validación básica
    if not column or not value:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": [],
                "page": 1,
                "per_page": per_page,
                "total": 0,
                "error": "Por favor seleccione una columna y especifique un valor"
            }
        )

    # Convertir el valor al tipo correcto según la columna
    try:
        if column in ['age', 'hypertension', 'heart_disease', 'diabetes']:
            filter_value = int(value)
        elif column in ['bmi', 'HbA1c_level', 'blood_glucose_level']:
            filter_value = float(value)
        else:  # smoking_history
            filter_value = str(value).lower()
    except ValueError:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "results": [],
                "page": 1,
                "per_page": per_page,
                "total": 0,
                "error": "Valor inválido para la columna seleccionada"
            }
        )

    # Filtrar los datos
    filtered_results = [
        m for m in diabetes_list 
        if m.get(column) == filter_value
    ]

    # Paginación
    total = len(filtered_results)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = filtered_results[start:end]

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": paginated_results,
            "page": page,
            "per_page": per_page,
            "total": total,
            "column": column,
            "value": value
        }
    )
