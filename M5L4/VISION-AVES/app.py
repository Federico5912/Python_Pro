import os, glob
from flask import Flask, request, render_template_string
import numpy as np
import tensorflow as tf
from PIL import Image
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(APP_ROOT, "model")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.txt")
UPLOAD_DIR = os.path.join(APP_ROOT, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

with open(LABELS_PATH, "r", encoding="utf-8") as f:
    CLASS_NAMES = [ln.strip() for ln in f if ln.strip()]

savedmodel_path = os.path.join(MODEL_DIR, "saved_model.pb")
h5_candidates = glob.glob(os.path.join(MODEL_DIR, "*.h5"))

MODEL_TYPE = None
if os.path.isfile(savedmodel_path):
    MODEL_TYPE = "savedmodel"
    _loaded = tf.saved_model.load(MODEL_DIR)
    _infer = _loaded.signatures["serving_default"]
elif h5_candidates:
    MODEL_TYPE = "h5"
    _loaded = tf.keras.models.load_model(h5_candidates[0])
else:
    raise RuntimeError("No se encontró ni SavedModel (saved_model.pb) ni un .h5 dentro de 'model/'")

def prepare_image(file, target_size=(224, 224)):
    img = Image.open(file).convert("RGB").resize(target_size)
    arr = np.asarray(img).astype(np.float32) / 255.0
    return np.expand_dims(arr, axis=0)

def predict_array(x):
    if MODEL_TYPE == "savedmodel":
        out = _infer(tf.constant(x))
        logits = None
        for v in out.values():
            if len(v.shape) == 2:
                logits = v.numpy()
                break
        if logits is None:
            raise RuntimeError("No se encontró salida de forma (1, num_clases) en el SavedModel.")
        probs = tf.nn.softmax(logits[0]).numpy()
    else:
        preds = _loaded.predict(x, verbose=0)
        if preds.ndim == 2:
            probs = tf.nn.softmax(preds[0]).numpy()
        elif preds.ndim == 1:
            probs = tf.nn.softmax(preds).numpy()
        else:
            raise RuntimeError(f"Salida inesperada del modelo .h5 con forma {preds.shape}")
    idx = int(np.argmax(probs))
    return idx, float(probs[idx]), probs

PAGE = """
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Clasificador de Aves</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; margin:0 }
    header, footer { padding: 1rem; background: #f3f3f3; }
    main { max-width: 760px; margin: 1rem auto; padding: 0 1rem; }
    form { display:flex; gap:.75rem; align-items:center; margin:1rem 0; flex-wrap:wrap }
    button { padding:.6rem 1rem; border:0; border-radius:.5rem; cursor:pointer }
    .error{ color:#b00020 } img.preview{ max-width:100%; height:auto; border-radius:.5rem; margin-top:.5rem }
    ul{ line-height:1.6 } .grid{ display:grid; grid-template-columns:1fr; gap:1rem }
    @media (min-width:700px){ .grid{ grid-template-columns:1fr 1fr } }
    .card{ border:1px solid #eee; border-radius:.75rem; padding:1rem }
    .mono{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace }
    .badge{ font-size:.8rem; padding:.2rem .4rem; border:1px solid #ccc; border-radius:.5rem; }
  </style>
</head>
<body>
  <header>
    <strong>Clasificador de Aves</strong>
    <span class="badge">{{ model_type }}</span>
  </header>
  <main>
    <section class="card">
      <h2>Subir imagen</h2>
      <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" accept="image/*" required />
        <button type="submit">Clasificar</button>
      </form>
      {% if error %}
        <p class="error">{{ error }}</p>
      {% endif %}
      {% if filename %}
        <div class="grid">
          <div>
            <h3>Tu imagen</h3>
            <img class="preview" src="{{ file_url }}" alt="Imagen subida" />
          </div>
          <div>
            <h3>Resultado</h3>
            {% if prediction %}
              <p><strong>Clase predicha:</strong> {{ prediction }}</p>
              <p><strong>Confianza:</strong> {{ confidence }}</p>
              <h4>Todas las probabilidades</h4>
              <ul>
                {% for name, p in ranking %}
                  <li>{{ name }}: {{ '%.2f'|format(p*100) }}%</li>
                {% endfor %}
              </ul>
            {% else %}
              <p class="mono">Procesando…</p>
            {% endif %}
          </div>
        </div>
      {% endif %}
    </section>
    <section class="card">
      <h2>Clases del modelo</h2>
      <ul>
        {% for name in class_names %}
          <li>{{ loop.index }}. {{ name }}</li>
        {% endfor %}
      </ul>
    </section>
  </main>
  <footer>Hecho con Flask + TensorFlow</footer>
</body>
</html>
"""

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    confidence = None
    ranking = None
    filename = None
    file_url = None
    error = None

    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            error = "Subí una imagen, por favor."
        else:
            filename = secure_filename(file.filename)
            save_path = os.path.join(UPLOAD_DIR, filename)
            file.save(save_path)
            with open(save_path, "rb") as f:
                x = prepare_image(f)
            try:
                idx, conf, probs = predict_array(x)
                prediction = CLASS_NAMES[idx]
                confidence = f"{conf:.2%}"
                ranking = sorted(
                    [(CLASS_NAMES[i], float(p)) for i, p in enumerate(probs)],
                    key=lambda t: t[1],
                    reverse=True
                )
                file_url = "/uploads/" + filename
            except Exception as e:
                error = f"Ocurrió un error al predecir: {e}"

    return render_template_string(
        PAGE,
        prediction=prediction,
        confidence=confidence,
        ranking=ranking,
        filename=filename,
        file_url=file_url,
        error=error,
        class_names=CLASS_NAMES,
        model_type=("SavedModel" if MODEL_TYPE=="savedmodel" else "Keras .h5")
    )

@app.route("/uploads/<path:name>")
def uploads(name):
    return app.send_from_directory(UPLOAD_DIR, name)

if __name__ == "__main__":
    app.run(debug=True)
