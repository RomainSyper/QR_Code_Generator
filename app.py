from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form["data"]
        qr = qrcode.make(data)
        qr.save("static/qrcode.png")
        return render_template("index.html", qr_code="static/qrcode.png")
    return render_template("index.html")

if __name__ == "__main__":
    # Important: Assurez-vous que l'application écoute sur toutes les interfaces
    app.run(host='0.0.0.0', port=10000)  # Port par défaut sur Render
