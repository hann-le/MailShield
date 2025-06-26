import os
from flask import Flask
from app.routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render uses PORT or defaults to 10000
    app.run(host="0.0.0.0", port=port)
