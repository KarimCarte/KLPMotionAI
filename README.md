# KLPMotionAI Render Deploy

Paquete minimo para publicar KLPMotionAI como un Render Web Service gratis.

Rutas:

- `/`: pagina publica.
- `/api/predict-v1`: API del modelo v1.
- `/health`: verificacion del servicio.

Render:

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
