from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from water_quality_model import WaterQualityEvaluator

app = FastAPI()
quality_model = WaterQualityEvaluator()


class WaterQualityData(BaseModel):
    """
    Pydantic model to define the structure and validation rules for input data.
    """

    Temperature: Optional[float] = None
    pH: Optional[float] = None
    Turbidity: Optional[float] = None
    DissolvedOxygen: Optional[float] = None
    Conductivity: Optional[float] = None
    TotalDissolvedSolids: Optional[float] = None
    Nitrate: Optional[float] = None
    Phosphate: Optional[float] = None
    TotalColiforms: Optional[float] = None
    Ecoli: Optional[float] = None
    BOD: Optional[float] = None
    COD: Optional[float] = None
    Hardness: Optional[float] = None
    Alkalinity: Optional[float] = None
    Iron: Optional[float] = None


class EvaluationResponse(BaseModel):
    """
    Pydantic model for the response data.
    """

    quality_score: float
    report: str
    graph: str


@app.post("/evaluate", response_model=EvaluationResponse)
async def evaluate_water_quality(data: WaterQualityData):
    """
    Evaluates water quality based on the provided data.

    **Input:**

    A JSON object containing at least one of the following water quality parameters:
    - Temperature (°C)
    - pH
    - Turbidity (NTU)
    - Dissolved Oxygen (mg/L)
    - Conductivity (µS/cm)
    - Total Dissolved Solids (mg/L)
    - Nitrate (mg/L)
    - Phosphate (mg/L)
    - Total Coliforms (CFU/100mL)
    - E. coli (CFU/100mL)
    - BOD (mg/L)
    - COD (mg/L)
    - Hardness (mg/L as CaCO3)
    - Alkalinity (mg/L as CaCO3)
    - Iron (mg/L)

    **Output:**

    A JSON object containing:
    - `quality_score`: The overall water quality score (0-100).
    - `report`: A detailed text report of the water quality analysis.
    - `parameter_contributions`: A dictionary showing the contribution of each parameter to the overall score.
    """
    input_data = data.dict(exclude_none=True)

    processed_data = {
        "Temperature": input_data.get("Temperature"),
        "pH": input_data.get("pH"),
        "Turbidity": input_data.get("Turbidity"),
        "Dissolved Oxygen": input_data.get("DissolvedOxygen"),
        "Conductivity": input_data.get("Conductivity"),
        "Total Dissolved Solids": input_data.get("TotalDissolvedSolids"),
        "Nitrate": input_data.get("Nitrate"),
        "Phosphate": input_data.get("Phosphate"),
        "Total Coliforms": input_data.get("TotalColiforms"),
        "E. coli": input_data.get("Ecoli"),
        "BOD": input_data.get("BOD"),
        "COD": input_data.get("COD"),
        "Hardness": input_data.get("Hardness"),
        "Alkalinity": input_data.get("Alkalinity"),
        "Iron": input_data.get("Iron"),
    }

    try:
        quality_model.validate_data(processed_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Calculate quality score
    quality_score = quality_model.calculate_overall_quality(processed_data)

    # Generate report
    report = quality_model.generate_report(processed_data, quality_score)

    # # Calculate parameter contributions
    parameter_contributions = quality_model.plot_parameter_contributions(
        processed_data, quality_score
    )

    return {
        "quality_score": quality_score,
        "report": report,
        "graph": parameter_contributions,
    }


@app.get("/")
@app.get("/index.html")
async def read_index():
    return FileResponse("client/dist/index.html")


@app.get("/assets/index.js")
async def read_js():
    return FileResponse("client/dist/assets/index.js")
