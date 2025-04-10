from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
from urllib.parse import urlparse

app = Flask(__name__)

# Fonction pour vérifier si l'URL est valide
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])  # Vérifie si l'URL a un schéma (http, https, etc.) et un domaine
    except ValueError:
        return False

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        
        if not url:
            return render_template("index.html", error="Veuillez entrer une URL valide.")
        
        # Vérifier si l'URL est valide
        if not is_valid_url(url):
            return render_template("index.html", error="L'URL entrée n'est pas valide. Assurez-vous qu'elle commence par http:// ou https://.")
        
        # Génération du QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill="black", back_color="white")
        
        # Sauvegarder l'image dans un buffer pour l'envoyer à l'utilisateur
        img_io = BytesIO()
        img.save(img_io, "PNG")
        img_io.seek(0)
        
        return send_file(img_io, mimetype="image/png", as_attachment=True, download_name="qr_code.png")
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=False)  # Par défaut Flask utilise son serveur de développement