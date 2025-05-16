from flask import Flask, render_template_string
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

@app.route("/")
def home():
    # Simulate NEPSE data
    np.random.seed(42)
    data = np.cumsum(np.random.normal(loc=0.3, scale=5, size=100)) + 1200
    forecast = data[-1] + np.cumsum(np.random.normal(0.2, 3, 30))

    # Plot
    plt.figure(figsize=(8, 3))
    plt.plot(range(100), data, label="Historical")
    plt.plot(range(100, 130), forecast, label="Forecast")
    plt.legend()
    plt.title("NEPSE Forecast")
    plt.tight_layout()

    # Convert plot to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    html = f"""
    <html><head><title>NEPSE Forecast</title></head>
    <body>
        <h2>NEPSE Index Forecast</h2>
        <img src="data:image/png;base64,{img_base64}">
    </body></html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    