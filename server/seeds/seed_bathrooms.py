import json
import os

from app.extensions import db
from app.models.bathroom import Bathroom


def run_seed():
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'ucd_bathrooms.json')
    with open(data_path) as f:
        bathrooms = json.load(f)

    for entry in bathrooms:
        wkt = f"SRID=4326;POINT({entry['lng']} {entry['lat']})"
        bathroom = Bathroom(
            building_name=entry['building_name'],
            floor_level=entry['floor_level'],
            coordinates=wkt,
            gender_type=entry['gender_type'],
            is_accessible=entry['is_accessible'],
        )
        db.session.add(bathroom)

    db.session.commit()
    print(f'Seeded {len(bathrooms)} bathrooms.')
