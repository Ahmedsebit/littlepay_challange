from flask import Blueprint, request, jsonify
from app.utils.upload_file import charge_trip, read_file, get_duration, get_charge, get_status, generate_output_file
from app.models.trips import Trip


littlepay_bp = Blueprint(
    'littlepay_bp', __name__,
)


@littlepay_bp.route('/trips/upload', methods=['POST'])
def upload_trips_api():
    data = request.data
    file = request.files.get('file')
    trips = read_file(file)
    charged_trip = charge_trip(trips)
    output_file = generate_output_file(charged_trip)
    return output_file