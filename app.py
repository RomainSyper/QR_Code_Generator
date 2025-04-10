from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import qrcode
from fpdf import FPDF
import os
import uuid
import googlemaps
import requests
from werkzeug.utils import secure_filename

# Configuration de Flask
app = Flask(__name__)

# Dossier temporaire pour stocker les fichiers générés
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Google Maps API key (assure-toi de la configurer dans ton projet Google Cloud)
GMAPS_API_KEY = 'VOTRE_API_KEY_GOOGLE_MAPS'
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Fonction pour vérifier l'extension des fichiers téléchargés (pour images)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour générer le QR code à partir d'une URL
@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    url = request.form.get('url')
    if url:
        # Créer le QR code pour l'URL
        qr = qrcode.make(url)
        qr_code_filename = f"{uuid.uuid4().hex}.png"
        qr_path = os.path.join(app.config['UPLOAD_FOLDER'], qr_code_filename)
        qr.save(qr_path)

        return render_template('result.html', qr_code=qr_code_filename)
    else:
        return "L'URL ne peut pas être vide."

# Route pour la création du PDF avec texte, photo, localisation et Google Map
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    title = request.form.get('title')
    text = request.form.get('text')
    location = request.form.get('location')
    photo = request.files.get('photo')
    map_location = request.form.get('map_location')  # Ce sera un point (latitude, longitude)

    # Créer le PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Ajouter le titre du document
    if title:
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, title, ln=True, align='C')
    
    # Ajouter le texte
    if text:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
    
    # Ajouter la localisation (si fournie)
    if location:
        pdf.ln(10)
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(200, 10, f"Localisation : {location}", ln=True)

    # Ajouter l'image (si une photo est fournie)
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        photo.save(filepath)
        pdf.ln(10)
        pdf.image(filepath, x=10, y=pdf.get_y(), w=100)  # Ajuster selon la taille de l'image

    # Ajouter une image de Google Maps pour la localisation (si fournie)
    if map_location:
        lat, lng = map_location.split(",")
        map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lng}&zoom=14&size=400x400&markers={lat},{lng}&key={GMAPS_API_KEY}"
        map_image_filename = f"{uuid.uuid4().hex}.png"
        map_image_path = os.path.join(app.config['UPLOAD_FOLDER'], map_image_filename)

        # Télécharger l'image de la carte
        map_response = requests.get(map_url)
        with open(map_image_path, 'wb') as f:
            f.write(map_response.content)

        pdf.ln(10)
        pdf.image(map_image_path, x=10, y=pdf.get_y(), w=100)  # Ajuster selon la taille de l'image

    # Enregistrer le PDF dans un fichier temporaire
    pdf_filename = f"{uuid.uuid4().hex}.pdf"
    pdf_output_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
    pdf.output(pdf_output_path)

    # Supprimer les fichiers après utilisation
    if photo and allowed_file(photo.filename):
        os.remove(filepath)

    if map_location:
        os.remove(map_image_path)

    return render_template('result.html', pdf_filename=pdf_filename)

# Route pour télécharger un fichier (PDF ou image)
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

# Suppression des fichiers après téléchargement
@app.after_request
def after_request(response):
    try:
        if request.endpoint == 'download':
            filename = request.view_args['filename']
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.remove(filepath)
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier: {e}")
    return response

if __name__ == "__main__":
    app.run(debug=True)