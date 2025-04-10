from flask import Flask, render_template, request, send_from_directory
import qrcode
import os
from fpdf import FPDF  # Pour générer le PDF

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
        input_value = request.form.get('input_value')  # On récupère soit le texte soit l'URL

        if input_value:  # Si quelque chose a été soumis (texte ou URL)
            try:
                if input_value.startswith('http://') or input_value.startswith('https://'):
                    # Cas où l'utilisateur entre un lien (URL)
                    qr = qrcode.make(input_value)  # Créer le QR code avec l'URL
                    qr_code_filename = 'qrcode.png'
                    qr_path = os.path.join('static', qr_code_filename)
                    qr.save(qr_path)
                    qr_code_path = qr_code_filename
                else:
                    # Cas où l'utilisateur entre du texte
                    qr = qrcode.make(input_value)  # Créer un QR code avec le texte
                    qr_code_filename = 'qrcode.png'
                    qr_path = os.path.join('static', qr_code_filename)
                    qr.save(qr_path)
                    qr_code_path = qr_code_filename

                    # Créer le PDF avec le texte
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.set_font("Arial", size=12)
                    pdf.multi_cell(0, 10, input_value)  # Ajouter du texte sur le PDF
                    pdf_filename = 'texte.pdf'
                    pdf_path = os.path.join('static', pdf_filename)
                    pdf.output(pdf_path)

                return render_template('index.html', qr_code=qr_code_path, pdf_file=pdf_path)

            except Exception as e:
                error = f"Erreur lors de la génération du QR code ou du PDF : {e}"
        else:
            error = "Le champ ne peut pas être vide."

    return render_template('index.html', error=error, qr_code=qr_code_path, pdf_file=pdf_path)

@app.route('/download/<filename>')
def download(filename):
    # Le fichier sera envoyé depuis le répertoire 'static'
    return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)