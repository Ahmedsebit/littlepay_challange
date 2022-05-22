from flask import Blueprint, request
from app.utils.upload_file import charge_trip, read_file, generate_output_file


littlepay_bp = Blueprint(
    'littlepay_bp', __name__,
)


@littlepay_bp.route('/trips/upload', methods=['POST'])
def upload_trips_api():
    """
    post endpoint
    ---
    tags:
      - trips
    parameters:
      - name: file
        in: formData
        required: true
        type: file
    responses:
      200:
        description: Generate charges from an uploaded trip file
    """
    file = request.files.get('file')
    trips = read_file(file)
    charged_trip = charge_trip(trips)
    output_file = generate_output_file(charged_trip)
    return output_file