from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import qrcode
from fpdf import FPDF
import time
import requests

app = Flask(__name__)

# Crée un dossier static si nécessaire
if not os.path.exists('static'):
    os.makedirs('static')

# Fonction pour obtenir une image de la carte à partir des coordonnées (latitude, longitude)
def get_map_image(lat, lon):
    google_maps_api_key = 'VOTRE_API_KEY'  # Remplacez par votre clé API
    base_url = f'https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=14&size=600x300&markers={lat},{lon}&key={google_maps_api_key}'
    response = requests.get(base_url)
    if response.status_code == 200:
        img_filename = f"map_{int(time.time())}.png"
        img_path = os.path.join('static', img_filename)
        with open(img_path, 'wb') as f:
            f.write(response.content)
        return img_filename
    return None

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
                return redirect(url_for('result', type='qr', filename=qr_code_filename))
            except Exception as e:
                error = f"Erreur lors de la génération du QR code : {e}"
    return render_template('qr_code.html', error=error)

@app.route('/pdf', methods=['GET', 'POST'])
def create_pdf():
    error = None
    pdf_filename = None
    if request.method == 'POST':
        title = request.form.get('title')  # Titre du PDF
        text = request.form.get('text')  # Pour le PDF avec texte
        lat = request.form.get('lat')  # Latitude de la localisation
        lon = request.form.get('lon')  # Longitude de la localisation
        photo = request.files.get('photo')  # Photo à ajouter dans le PDF

        # Création du PDF avec le texte
        if text:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)

                # Ajout du titre en haut
                if not title:
                    title = "Document"
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt=title, ln=True, align='C')

                # Ajout du texte au PDF
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, text)

                # Ajouter la carte si des coordonnées sont fournies
                if lat and lon:
                    map_image = get_map_image(lat, lon)
                    if map_image:
                        pdf.ln(10)  # Espacement avant l'image
                        pdf.image(os.path.join('static', map_image), x=10, w=180)

                # Ajouter la photo dans le PDF si elle est téléchargée
                if photo:
                    photo_path = os.path.join('static', photo.filename)
                    photo.save(photo_path)
                    pdf.ln(10)
                    pdf.image(photo_path, x=10, w=180)

                # Sauvegarde du PDF
                pdf_filename = f"{title.replace(' ', '_')}_{int(time.time())}.pdf"
                pdf_output_path = os.path.join('static', pdf_filename)
                pdf.output(pdf_output_path)

                return redirect(url_for('result', type='pdf', filename=pdf_filename))
            except Exception as e:
                error = f"Erreur lors de la génération du PDF : {e}"

    return render_template('create_pdf.html', error=error)

@app.route('/result/<type>/<filename>')
def result(type, filename):
    return render_template('result.html', type=type, filename=filename)

@app.route('/download/<filename>')
def download(filename):
    if filename.endswith('.pdf'):
        response = send_from_directory('static', filename, as_attachment=True)
        os.remove(os.path.join('static', filename))  # Supprimer après téléchargement
        return response
    else:
        return send_from_directory('static', filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)