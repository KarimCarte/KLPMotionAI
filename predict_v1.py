"""Adaptador de inferencia para los artefactos entrenados de KLPMotionAI v1.

Convierte angulo + rapidez inicial a las features reales del modelo:
[tiempo, tiempo**2, velocidad_x_inicial, velocidad_y_inicial].
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np


BASE_DIR = Path(__file__).resolve().parent
G = 9.81


def cargar_modelo_v1(base_dir: str | Path = BASE_DIR):
    """Carga y devuelve (modelo, scaler_x, scaler_y)."""
    base_dir = Path(base_dir)
    modelo = joblib.load(base_dir / "modelo_v1.pkl")
    scaler_x = joblib.load(base_dir / "scaler_x_v1.pkl")
    scaler_y = joblib.load(base_dir / "scaler_y_v1.pkl")

    if getattr(scaler_x, "n_features_in_", None) != 4:
        raise ValueError("El scaler de entrada no tiene las 4 features esperadas.")
    if getattr(scaler_y, "n_features_in_", None) != 4:
        raise ValueError("El scaler de salida no tiene las 4 salidas esperadas.")
    return modelo, scaler_x, scaler_y


def predecir_trayectoria(
    angulo_grados: float,
    velocidad_inicial_m_s: float,
    num_puntos: int = 101,
    duracion_s: float | None = None,
    base_dir: str | Path = BASE_DIR,
) -> dict:
    """Predice una trayectoria y devuelve valores en unidades físicas.

    Si no se proporciona ``duracion_s``, se usa 2*v0y/g como ventana temporal.
    Esa fórmula solo define la malla; los puntos (x, y, vx, vy) los genera el MLP.
    """
    angulo_grados = float(angulo_grados)
    velocidad_inicial_m_s = float(velocidad_inicial_m_s)
    num_puntos = int(num_puntos)

    if not 0 < angulo_grados < 90:
        raise ValueError("angulo_grados debe estar entre 0 y 90 (sin incluirlos).")
    if velocidad_inicial_m_s <= 0:
        raise ValueError("velocidad_inicial_m_s debe ser positiva.")
    if num_puntos < 2:
        raise ValueError("num_puntos debe ser al menos 2.")

    theta = np.deg2rad(angulo_grados)
    vx0 = velocidad_inicial_m_s * np.cos(theta)
    vy0 = velocidad_inicial_m_s * np.sin(theta)

    if duracion_s is None:
        duracion_s = 2.0 * vy0 / G
    duracion_s = float(duracion_s)
    if duracion_s <= 0:
        raise ValueError("duracion_s debe ser positiva.")

    tiempos = np.linspace(0.0, duracion_s, num_puntos)
    features = np.column_stack(
        [
            tiempos,
            tiempos**2,
            np.full_like(tiempos, vx0),
            np.full_like(tiempos, vy0),
        ]
    )

    modelo, scaler_x, scaler_y = cargar_modelo_v1(base_dir)
    features_norm = scaler_x.transform(features)
    salidas_norm = modelo.predict(features_norm)
    salidas = scaler_y.inverse_transform(salidas_norm)

    puntos = [
        {
            "t": float(t),
            "x": float(x),
            "y": float(y),
            "vx": float(vx),
            "vy": float(vy),
        }
        for t, (x, y, vx, vy) in zip(tiempos, salidas)
    ]
    return {
        "angulo_grados": angulo_grados,
        "velocidad_inicial_m_s": velocidad_inicial_m_s,
        "vx0_m_s": float(vx0),
        "vy0_m_s": float(vy0),
        "duracion_s": duracion_s,
        "puntos": puntos,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Inferencia de KLPMotionAI v1")
    parser.add_argument("angulo", type=float, help="Angulo en grados")
    parser.add_argument("velocidad", type=float, help="Rapidez inicial en m/s")
    parser.add_argument("--puntos", type=int, default=101)
    parser.add_argument("--duracion", type=float, default=None)
    args = parser.parse_args()
    resultado = predecir_trayectoria(
        args.angulo, args.velocidad, args.puntos, args.duracion
    )
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
