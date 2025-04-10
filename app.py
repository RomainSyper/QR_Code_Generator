from flask import Flask, render_template, request, redirect, url_for
import qrcode
import os

app = Flask(__name__)

# Crée un dossier static si nécessaire
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        url = request.form.get('url')  # Utiliser get pour éviter une KeyError si 'url' n'est pas dans le form
        if url:  # Si une URL a bien été soumise
            try:
                # Créer le QR code
                qr = qrcode.make(url)
                qr_path = os.path.join('static', 'qrcode.png')
                qr.save(qr_path)
                return render_template('index.html', qr_code=qr_path)
            except Exception as e:
                error = f"Erreur lors de la génération du QR code : {e}"
        else:
            error = "L'URL ne peut pas être vide."

    return render_template('index.html', error=error)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)