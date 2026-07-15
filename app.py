"""KLPMotionAI public demo app for flat Render uploads.

All runtime files live in the same directory because some upload flows do not
preserve folders.
"""

from __future__ import annotations

import importlib.util
import os
from functools import lru_cache
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, JSONResponse


APP_DIR = Path(__file__).resolve().parent
FRONTEND_PATH = APP_DIR / "index.html"
TEAM_PHOTO_PATH = APP_DIR / "Foto_equipo.jpeg"
MODEL_DIR = APP_DIR
PREDICT_V1_PATH = APP_DIR / "predict_v1.py"

app = FastAPI(
    title="KLPMotionAI Demo API",
    description="Frontend publico y API de prediccion para el modelo KLPMotionAI v1.",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    return response


@lru_cache(maxsize=1)
def _load_predict_module():
    spec = importlib.util.spec_from_file_location("klp_predict_v1", PREDICT_V1_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el adaptador del modelo v1.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _predict_v1(angle: float, speed: float, points: int) -> dict:
    predictor = _load_predict_module()
    raw = predictor.predecir_trayectoria(
        angulo_grados=angle,
        velocidad_inicial_m_s=speed,
        num_puntos=points,
        base_dir=MODEL_DIR,
    )
    frontend_points = [
        {"t": float(point["t"]), "x": float(point["x"]), "y": float(point["y"])}
        for point in raw["puntos"]
    ]
    x_values = [point["x"] for point in frontend_points]
    y_values = [point["y"] for point in frontend_points]
    return {
        "source": "modelo_v1",
        "angle": float(angle),
        "speed": float(speed),
        "duration": float(raw["duracion_s"]),
        "range": max(x_values) if x_values else 0.0,
        "maxHeight": max(y_values) if y_values else 0.0,
        "points": frontend_points,
    }


@app.get("/")
def frontend() -> FileResponse:
    return FileResponse(FRONTEND_PATH, media_type="text/html")


@app.get("/Foto_equipo.jpeg")
def team_photo() -> FileResponse:
    return FileResponse(TEAM_PHOTO_PATH, media_type="image/jpeg")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/predict-v1")
def predict_v1(
    angle: Annotated[float, Query(gt=0, lt=90)] = 45.0,
    speed: Annotated[float, Query(gt=0, le=100)] = 10.0,
    points: Annotated[int, Query(ge=2, le=300)] = 101,
) -> JSONResponse:
    try:
        payload = _predict_v1(angle=angle, speed=speed, points=points)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"No se pudo ejecutar el modelo v1: {exc}") from exc

    return JSONResponse(payload, headers={"Cache-Control": "no-store"})


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
