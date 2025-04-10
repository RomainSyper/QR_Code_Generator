from flask import Flask, render_template, request
import qrcode

app = Flask(__name__)

# Route pour la page d'accueil
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Récupérer le texte du formulaire
        data = request.form["data"]
        # Générer le QR code
        qr = qrcode.make(data)
        # Sauvegarder l'image dans un fichier
        qr.save("static/qrcode.png")
        return render_template("index.html", qr_code="static/qrcode.png")
    return render_template("index.html")

if __name__ == "__main__":
    # On ne démarre pas le serveur ici, car il sera démarré par Gunicorn.
    pass