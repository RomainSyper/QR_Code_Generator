from flask import Flask, render_template, request, send_from_directory
import qrcode
import os

app = Flask(__name__)

# Crée un dossier static si nécessaire
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    qr_code_path = None  # Pour stocker le chemin du QR Code généré
    if request.method == 'POST':
        texte = request.form.get('texte')  # On récupère le texte entré par l'utilisateur

        if texte:  # Si du texte a été soumis
            try:
                # Créer le QR code avec du texte (le texte est encodé directement)
                qr = qrcode.make(texte)  # Créer le QR code à partir du texte
                qr_code_filename = 'qrcode.png'
                qr_path = os.path.join('static', qr_code_filename)
                qr.save(qr_path)

                # Le chemin du QR code sera utilisé pour l'affichage et le téléchargement
                qr_code_path = qr_code_filename

                return render_template('index.html', qr_code=qr_code_path)
            except Exception as e:
                error = f"Erreur lors de la génération du QR code : {e}"
        else:
            error = "Le texte ne peut pas être vide."

    return render_template('index.html', error=error, qr_code=qr_code_path)

@app.route('/download/<filename>')
def download(filename):
    # Le fichier sera envoyé depuis le répertoire 'static'
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)