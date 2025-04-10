from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
from fpdf import FPDF

app = Flask(__name__)

# Crée un dossier static si nécessaire
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    qr_code_path = None  # Pour stocker le chemin du QR Code généré
    pdf_path = None  # Pour stocker le chemin du PDF généré
    if request.method == 'POST':
        url = request.form.get('url')  # Récupère l'URL (si c'est un lien)
        text = request.form.get('text')  # Récupère le texte (si c'est du texte)

        if url:  # Si une URL a bien été soumise
            try:
                # Créer le QR code pour l'URL
                qr = qrcode.make(url)
                qr_code_filename = 'qrcode_url.png'
                qr_path = os.path.join('static', qr_code_filename)
                qr.save(qr_path)

                # Le chemin du QR code sera utilisé pour l'affichage et le téléchargement
                qr_code_path = qr_code_filename
            except Exception as e:
                error = f"Erreur lors de la génération du QR code pour l'URL : {e}"
        elif text:  # Si du texte a été soumis
            try:
                # Créer le QR code pour le texte
                qr = qrcode.make(text)
                qr_code_filename = 'qrcode_text.png'
                qr_path = os.path.join('static', qr_code_filename)
                qr.save(qr_path)

                # Créer un PDF avec le texte
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, text)
                pdf_filename = 'texte.pdf'
                pdf_path = os.path.join('static', pdf_filename)
                pdf.output(pdf_path)

                # Le chemin du QR code et du PDF sera utilisé pour l'affichage et le téléchargement
                qr_code_path = qr_code_filename
                pdf_path = pdf_filename
            except Exception as e:
                error = f"Erreur lors de la génération du QR code ou du PDF : {e}"
        else:
            error = "Veuillez entrer soit un lien, soit un texte."

    return render_template('index.html', error=error, qr_code=qr_code_path, pdf_file=pdf_path)

@app.route('/download/<filename>')
def download(filename):
    # Le fichier sera envoyé depuis le répertoire 'static'
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)