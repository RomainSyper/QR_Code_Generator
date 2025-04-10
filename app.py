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
        url = request.form.get('url')  # Utilise get pour éviter une KeyError si 'url' n'est pas dans le form
        texte = request.form.get('texte')  # Ajout du texte

        if url:  # Si une URL a bien été soumise
            contenu = url
        elif texte:  # Si du texte a été soumis
            contenu = texte
        else:
            error = "L'URL ou le texte ne peut pas être vide."
            return render_template('index.html', error=error, qr_code=qr_code_path)

        try:
            # Créer le QR code avec du texte ou une URL
            qr = qrcode.make(contenu)
            qr_code_filename = 'qrcode.png'
            qr_path = os.path.join('static', qr_code_filename)
            qr.save(qr_path)

            # Le chemin du QR code sera utilisé pour l'affichage et le téléchargement
            qr_code_path = qr_code_filename

            return render_template('index.html', qr_code=qr_code_path)
        except Exception as e:
            error = f"Erreur lors de la génération du QR code : {e}"

    return render_template('index.html', error=error, qr_code=qr_code_path)

@app.route('/download/<filename>')
def download(filename):
    # Le fichier sera envoyé depuis le répertoire 'static'
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)