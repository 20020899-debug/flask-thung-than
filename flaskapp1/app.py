from flask import Flask, render_template
import os

app = Flask(__name__)

# import routes
from routes.thung_than import thung_bp
from routes.san_thao_tac import san_bp
from routes.khoi_luong_tam import tam_bp

app.register_blueprint(thung_bp)
app.register_blueprint(san_bp)
app.register_blueprint(tam_bp)


@app.route("/")
def home():
    return render_template("home.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))