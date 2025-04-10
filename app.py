from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("data")
        if not data:
            error = "Le champ ne peut pas être vide"
            return render_template("index.html", error=error)
        
        qr = qrcode.make(data)
        qr_path = "static/qrcode.png"
        qr.save(qr_path)

        return render_template("index.html", qr_code=qr_path)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)