from flask import request, current_app
from flask_restful import Resource
from models import db, Apartment
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'images'

def save_images(files, existing_images=None):
    image_filenames = existing_images or []
    for file in files:
        if file and file.filename:
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            image_filenames.append(filename)
    return image_filenames

def get_image_urls(filenames):
    if not filenames:
        return []
    base_url = request.host_url.rstrip('/')
    return [f"{base_url}/api/images/{filename}" for filename in filenames]

class ApartmentResource(Resource):
    def get(self, apartment_id=None):
        if apartment_id:
            apartment = Apartment.query.get_or_404(apartment_id)
            return {
                'id': apartment.id,
                'name': apartment.name,
                'price': apartment.price,
                'area': apartment.area,
                'region': apartment.region,
                'block': apartment.block,
                'building': apartment.building,
                'description': apartment.description,
                'categories': apartment.categories,
                'images': get_image_urls(apartment.images)
            }
        else:
            apartments = Apartment.query.all()
            return [
                {
                    'id': apt.id,
                    'name': apt.name,
                    'price': apt.price,
                    'area': apt.area,
                    'region': apt.region,
                    'block': apt.block,
                    'building': apt.building,
                    'description': apt.description,
                    'categories': apt.categories,
                    'images': get_image_urls(apt.images)
                } for apt in apartments
            ]

    def post(self):
        data = request.form
        files = request.files.getlist('images')

        if not all([data.get('name'), data.get('price'), data.get('area'), 
                   data.get('region'), data.get('building')]):
            return {'error': 'Missing required fields'}, 400

        try:
            image_filenames = save_images(files)
            categories = request.form.getlist('categories[]')

            new_apartment = Apartment(
                name=data.get('name'),
                price=float(data.get('price')),
                area=float(data.get('area')),
                region=data.get('region'),
                block=data.get('block'),
                building=data.get('building'),
                description=data.get('description'),
                categories=categories,
                images=image_filenames
            )
            db.session.add(new_apartment)
            db.session.commit()
            return {
                'message': 'Apartment created successfully',
                'apartment': {
                    'id': new_apartment.id,
                    'name': new_apartment.name,
                    'price': new_apartment.price,
                    'area': new_apartment.area,
                    'region': new_apartment.region,
                    'block': new_apartment.block,
                    'building': new_apartment.building,
                    'description': new_apartment.description,
                    'categories': new_apartment.categories,
                    'images': get_image_urls(new_apartment.images)
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def put(self, apartment_id):
        apartment = Apartment.query.get_or_404(apartment_id)
        data = request.form
        files = request.files.getlist('images')
        existing_images = request.form.getlist('existingImages[]')

        try:
            image_filenames = save_images(files, existing_images)
            categories = request.form.getlist('categories[]')

            apartment.name = data.get('name', apartment.name)
            apartment.price = float(data.get('price', apartment.price))
            apartment.area = float(data.get('area', apartment.area))
            apartment.region = data.get('region', apartment.region)
            apartment.block = data.get('block', apartment.block)
            apartment.building = data.get('building', apartment.building)
            apartment.description = data.get('description', apartment.description)
            apartment.categories = categories if categories else apartment.categories
            apartment.images = image_filenames

            db.session.commit()
            return {
                'message': 'Apartment updated successfully',
                'apartment': {
                    'id': apartment.id,
                    'name': apartment.name,
                    'price': apartment.price,
                    'area': apartment.area,
                    'region': apartment.region,
                    'block': apartment.block,
                    'building': apartment.building,
                    'description': apartment.description,
                    'categories': apartment.categories,
                    'images': get_image_urls(apartment.images)
                }
            }, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500

    def delete(self, apartment_id):
        apartment = Apartment.query.get_or_404(apartment_id)
        try:
            for filename in apartment.images or []:
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                if os.path.exists(filepath):
                    os.remove(filepath)
            db.session.delete(apartment)
            db.session.commit()
            return {'message': 'Apartment deleted successfully'}, 200
        except Exception as e:
            db.session.rollback()
            return {'error': str(e)}, 500