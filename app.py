import os
from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

# Créer le dossier static s'il n'existe pas
if not os.path.exists('static'):
    os.makedirs('static')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        data = request.form.get("url")  # Utilisation correcte du champ "url" du formulaire
        
        # Vérification si l'URL est valide
        if not data:
            error = "L'URL ne peut pas être vide."
            return render_template("index.html", error=error)

        try:
            qr = qrcode.make(data)
            qr_path = "static/qrcode.png"
            qr.save(qr_path)
            return render_template("index.html", qr_code=qr_path)
        except Exception as e:
            error = f"Erreur lors de la génération du QR code: {e}"
            return render_template("index.html", error=error)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)