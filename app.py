from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from models import db
from resources.apartment import ApartmentResource, UPLOAD_FOLDER
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
app = Flask(__name__)
# Use /data for Render disk mount
data_dir = os.environ.get('DATA_DIR', '/data')
# Ensure data_dir and images subdir exist
os.makedirs(data_dir, exist_ok=True)
os.makedirs(os.path.join(data_dir, 'images'), exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{data_dir}/apartments.db')
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER', os.path.join(data_dir, 'images'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
api = Api(app)
logger.debug(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
logger.debug(f"Upload folder: {app.config['UPLOAD_FOLDER']}")
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
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))