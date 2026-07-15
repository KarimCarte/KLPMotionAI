# Como subir KLPMotionAI gratis a Render

Hugging Face Static no puede ejecutar Python ni cargar el modelo `.pkl`. Para frontend + API gratis, usa Render Web Service.

## Que subir

Sube el contenido de esta carpeta `deploy_render/`, no el proyecto completo.

Incluye:

- `index.html`: pagina publica.
- `Foto_equipo.jpeg`: imagen usada por la pagina.
- `app.py`: servidor FastAPI.
- `model_v1/`: modelo, scalers y adaptador de inferencia.
- `requirements.txt`: dependencias.
- `runtime.txt`: version de Python.
- `render.yaml`: configuracion opcional para Render.

No subas:

- `videos/`
- `data/`
- `artifacts/`
- `Video_Final.mp4`
- `.venv/`
- `.venv.nosync/`

## Opcion A: subir mediante GitHub

1. Crea un repositorio nuevo en GitHub, por ejemplo `klpmotionai-render`.
2. Sube a ese repositorio todos los archivos dentro de `deploy_render/`.
3. Entra a `https://dashboard.render.com`.
4. Presiona `New`.
5. Selecciona `Web Service`.
6. Conecta tu repositorio de GitHub.
7. En la configuracion usa:
   - Language: `Python 3`
   - Instance Type: `Free`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
8. Crea el servicio y espera el deploy.
9. Render te dara un link tipo:

```text
https://klpmotionai.onrender.com
```

## Opcion B: usar render.yaml

Si Render detecta `render.yaml`, puede crear el servicio desde Blueprint.

1. Sube esta carpeta a GitHub.
2. En Render, selecciona `New` y luego `Blueprint`.
3. Conecta el repositorio.
4. Render leera `render.yaml`.
5. Confirma la creacion del servicio.

## Pruebas despues del deploy

Abre:

```text
https://TU-SERVICIO.onrender.com/health
```

Debe responder:

```json
{"status":"ok"}
```

Luego prueba:

```text
https://TU-SERVICIO.onrender.com/api/predict-v1?angle=45&speed=10&points=10
```

Debe devolver JSON con puntos `t`, `x` y `y`.

Finalmente abre:

```text
https://TU-SERVICIO.onrender.com/
```

Y presiona `Predecir con modelo v1`.

## Limitacion del plan gratis

Render puede dormir el servicio despues de 15 minutos sin trafico. La primera visita despues de dormir puede tardar cerca de un minuto en responder. Esto es normal en el plan gratis.
