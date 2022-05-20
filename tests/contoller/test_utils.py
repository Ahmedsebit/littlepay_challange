import json
import unittest
from pathlib import Path
from app.app import create_app, db
from app.utils.upload_file import (read_file, 
                                   charge_trip, 
                                   get_duration, 
                                   get_charge, 
                                   get_status, 
                                   generate_output_file
                                   )
from app.models.trips import Trip


class UtillsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.file = open(Path('tests/trips.csv'), 'rb')
        self.boarded_1 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop1",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.alight_2 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop2",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.boarded_2 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop2",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.alight_1 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop1",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.boarded_3 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.alight_3 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555559"
        )
        self.trips = {
            int(5500005555555559): {
                "ON": self.boarded_1,
                "OFF": self.alight_2
            },
            int(5500005555555558): {
                "ON": self.boarded_2,
                "OFF": self.alight_3
            },
            int(5500005555555557): {
                "ON": self.boarded_3,
                "OFF": self.alight_1
            },
            int(5500005555555557): {
                "ON": self.boarded_3
            },
            int(5500005555555556): {
                "ON": self.boarded_1,
                "OFF": self.boarded_1
            }
        }
        
        self.charged_trip = charge_trip(self.trips)

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_read_file(self):
        taps = read_file(self.file)
        assert taps == {
            5500005555555559: {
                'ON': Trip(trip_id=1, 
                           date_time_utc='22-01-2018 13:00:00', 
                           tap_type='ON', 
                           stop_id='Stop1', 
                           company_id='Company1', 
                           bus_id='Bus37', 
                           pan=5500005555555559), 
                'OFF': Trip(trip_id=2, 
                            date_time_utc='22-01-2018 13:05:00', 
                            tap_type='OFF', 
                            stop_id='Stop2', 
                            company_id='Company1', 
                            bus_id='Bus37', 
                            pan=5500005555555559)
                }
            }
        
        
    def test_get_duration_boarded_1_alight_2(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_2_alight_3(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_1_alight_3(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_2_alight_1(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_3_alight_2(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_3_alight_1(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_status_completed(self):
        status = get_status(self.boarded_1, self.alight_2)
        assert status == 'COMPLETED'

    def test_get_status_incomplete(self):
        status = get_status(self.boarded_1, None)
        assert status == 'INCOMPLETE'

    def test_get_status_canceled(self):
        status = get_status(self.boarded_1, self.boarded_1)
        assert status == 'CANCELED'

    def test_get_charge_boarded_1_alight_2(self):
        charge = get_charge(self.boarded_1, self.alight_2)
        assert charge == "$ 3.25"

    def test_get_charge_boarded_2_alight_1(self):
        charge = get_charge(self.boarded_2, self.alight_1)
        assert charge == "$ 3.25"

    def test_get_charge_boarded_2_alight_3(self):
        charge = get_charge(self.boarded_2, self.alight_3)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_3_alight_2(self):
        charge = get_charge(self.boarded_3, self.alight_2)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_1_alight_3(self):
        charge = get_charge(self.boarded_1, self.alight_3)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_3_alight_1(self):
        charge = get_charge(self.boarded_3, self.alight_1)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_1_no_alight(self):
        charge = get_charge(self.boarded_1, None)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_2_no_alight(self):
        charge = get_charge(self.boarded_2, None)
        print(charge)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_3_no_alight(self):
        charge = get_charge(self.boarded_3, None)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_1_cancelled(self):
        charge = get_charge(self.boarded_1, self.boarded_1)
        assert charge == "$ 0.00"

    def test_charge_trip(self):
        charges = charge_trip(self.trips)
        print(charges)
        assert charges == [
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:05:00', 
                'DurationSecs': '0 hours 05 minutes 00 seconds', 
                'FromStopId': 'Stop1', 
                'ToStopId': 'Stop2', 
                'ChargeAmount': '$ 3.25', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555559, 
                'Status': 'COMPLETED'
            }, 
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:05:00', 
                'DurationSecs': '0 hours 05 minutes 00 seconds', 
                'FromStopId': 'Stop2', 
                'ToStopId': 'Stop3', 
                'ChargeAmount': '$ 5.50', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555558, 
                'Status': 'COMPLETED'
            },
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': None, 
                'DurationSecs': None, 
                'FromStopId': 'Stop3', 
                'ToStopId': None, 
                'ChargeAmount': '$ 7.30', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555557, 
                'Status': 'INCOMPLETE'
            },
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:00:00', 
                'DurationSecs': '0 hours 00 minutes 00 seconds', 
                'FromStopId': 'Stop1', 
                'ToStopId': 'Stop1', 
                'ChargeAmount': '$ 0.00', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555556, 
                'Status': 'CANCELED'
            }
        ]
        
    def test_generate_output_file(self):
        output = generate_output_file(self.charged_trip)
        assert output.status_code == 200
    
