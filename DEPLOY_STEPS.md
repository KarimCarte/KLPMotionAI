# Como corregir el deploy si no puedes subir carpetas

Usa esta carpeta `deploy_render_flat/` si GitHub o Render no te deja subir la carpeta `model_v1/`.

## Que hacer

1. En GitHub, borra o reemplaza el `app.py` anterior.
2. Sube todos los archivos de `deploy_render_flat/` directamente a la raiz del repo.
3. No crees carpeta `model_v1`.
4. Confirma que en GitHub se vea asi:

```text
app.py
index.html
Foto_equipo.jpeg
requirements.txt
runtime.txt
render.yaml
predict_v1.py
modelo_v1.pkl
scaler_x_v1.pkl
scaler_y_v1.pkl
```

5. En Render, ve a tu servicio.
6. Presiona `Manual Deploy`.
7. Selecciona `Deploy latest commit`.
8. Espera a que termine.

## Pruebas

Abre:

```text
https://klpmotionai.onrender.com/health
```

Luego:

```text
https://klpmotionai.onrender.com/api/predict-v1?angle=45&speed=10&points=10
```

Si ya no aparece `No such file or directory: .../model_v1/predict_v1.py`, el problema quedo corregido.
