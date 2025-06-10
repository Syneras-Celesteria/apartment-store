from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from models import db
from resources.apartment import ApartmentResource, UPLOAD_FOLDER
import os

app = Flask(__name__)
# Ensure /app/data exists
data_dir = '/app/data'
os.makedirs(data_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{data_dir}/apartments.db')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', f'{data_dir}/images')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

with app.app_context():
    db.create_all()

api.add_resource(
    ApartmentResource,
    '/api/apartments',
    '/api/apartments/<int:apartment_id>'
)

@app.route('/api/images/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))