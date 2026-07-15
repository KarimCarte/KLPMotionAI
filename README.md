# KLPMotionAI Render Deploy Sin Carpetas

Este paquete es para subir archivos individualmente cuando el flujo de subida no conserva carpetas.

Todos estos archivos deben quedar en la raiz del repositorio:

- `app.py`
- `index.html`
- `Foto_equipo.jpeg`
- `requirements.txt`
- `runtime.txt`
- `render.yaml`
- `predict_v1.py`
- `modelo_v1.pkl`
- `scaler_x_v1.pkl`
- `scaler_y_v1.pkl`

Render:

- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
