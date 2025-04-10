from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import qrcode
from fpdf import FPDF
import time

app = Flask(__name__)

# Crée un dossier static si nécessaire
if not os.path.exists('static'):
    os.makedirs('static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/qr', methods=['GET', 'POST'])
def qr_code():
    error = None
    qr_code_path = None
    if request.method == 'POST':
        url = request.form.get('url')  # Pour QR code
        if url:  # Générer QR Code à partir d'un lien
            try:
                qr = qrcode.make(url)
                qr_code_filename = 'qrcode.png'
                qr_path = os.path.join('static', qr_code_filename)
                qr.save(qr_path)
                qr_code_path = qr_code_filename
            except Exception as e:
                error = f"Erreur lors de la génération du QR code : {e}"
    return render_template('qr_code.html', error=error, qr_code=qr_code_path)

@app.route('/pdf', methods=['GET', 'POST'])
def create_pdf():
    error = None
    pdf_filename = None
    if request.method == 'POST':
        text = request.form.get('text')  # Pour le PDF avec texte
        title = request.form.get('title')  # Titre du PDF (facultatif)

        # Création du PDF avec le texte
        if text:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Ajout du texte au PDF
                pdf.multi_cell(0, 10, text)

                # Ajout du titre du PDF
                if not title:
                    title = "Document"
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt=title, ln=True, align='C')

                # Sauvegarde du PDF
                pdf_filename = f"document_{int(time.time())}.pdf"
                pdf_output_path = os.path.join('static', pdf_filename)
                pdf.output(pdf_output_path)

            except Exception as e:
                error = f"Erreur lors de la génération du PDF : {e}"

    return render_template('create_pdf.html', error=error, pdf_filename=pdf_filename)

@app.route('/download/<filename>')
def download(filename):
    # Si c'est un PDF, on le supprime après le téléchargement
    if filename.endswith('.pdf'):
        response = send_from_directory('static', filename, as_attachment=True)
        os.remove(os.path.join('static', filename))  # Supprimer après téléchargement
        return response
    else:
        # Ne pas supprimer les QR Codes
        return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)