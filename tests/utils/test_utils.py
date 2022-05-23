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
        self.alight_1 = Trip(
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
            pan="5500005555555558"
        )
        self.alight_2 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop1",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555558"
        )
        self.boarded_3 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555557"
        )
        self.alight_3 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop1",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555557"
        )
        self.boarded_4 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555556"
        )
        self.boarded_5 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 13:00:00",
            tap_type="ON",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555555"
        )
        self.alight_5 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 13:05:00",
            tap_type="OFF",
            stop_id="Stop2",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555555"
        )
        self.boarded_5_1 = Trip(
            trip_id=1,
            date_time_utc="22-01-2018 15:00:00",
            tap_type="ON",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555555"
        )
        self.alight_5_1 = Trip(
            trip_id=2,
            date_time_utc="22-01-2018 15:05:00",
            tap_type="OFF",
            stop_id="Stop3",
            company_id="Company1",
            bus_id="Bus37",
            pan="5500005555555555"
        )
        self.trips = {
            int(5500005555555559): [{"ON": self.boarded_1, "OFF": self.alight_1}],
            int(5500005555555558): [{"ON": self.boarded_2, "OFF": self.alight_2}],
            int(5500005555555557): [{"ON": self.boarded_3, "OFF": self.alight_3}],
            int(5500005555555556): [{"ON": self.boarded_4}],
            int(5500005555555555): [{"ON": self.boarded_5, "OFF": self.alight_5},{"ON": self.boarded_5_1, "OFF": self.boarded_5_1}]
        }
        
        self.charged_trip = charge_trip(self.trips)

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_read_file(self):
        taps = read_file(self.file)
        assert taps == {
            5500005555555559: [
                {'ON': Trip(trip_id=1, 
                            date_time_utc='22-01-2018 13:00:00', 
                            tap_type='ON', stop_id='Stop1', 
                            company_id='Company1', 
                            bus_id='Bus37', 
                            pan=5500005555555559
                            ), 
                 'OFF': Trip(trip_id=2, 
                             date_time_utc='22-01-2018 13:05:00', 
                             tap_type='OFF', 
                             stop_id='Stop2', 
                             company_id='Company1', 
                             bus_id='Bus37', 
                             pan=5500005555555559
                             )
                 }
                ], 
            34343434343434: [
                {'ON': Trip(trip_id=3, 
                            date_time_utc='22-01-2018 11:00:00', 
                            tap_type='ON', stop_id='Stop1', 
                            company_id='Company1', 
                            bus_id='Bus38', 
                            pan=34343434343434
                            ),
                 'OFF': Trip(trip_id=4, 
                             date_time_utc='22-01-2018 14:05:00', 
                             tap_type='OFF', 
                             stop_id='Stop3', 
                             company_id='Company1', 
                             bus_id='Bus38', 
                             pan=34343434343434)
                        }
                ], 
            122000000000003: [
                {'ON': Trip(trip_id=5, 
                            date_time_utc='22-01-2018 10:00:00', 
                            tap_type='ON', 
                            stop_id='Stop2', 
                            company_id='Company1', 
                            bus_id='Bus39', 
                            pan=122000000000003
                            ), 
                 'OFF': Trip(trip_id=6, 
                             date_time_utc='22-01-2018 12:05:00', 
                             tap_type='OFF', 
                             stop_id='Stop31', 
                             company_id='Company1', 
                             bus_id='Bus39', 
                             pan=122000000000003
                             )
                 }
                ], 
            6011000400000000: [
                {'ON': Trip(trip_id=7, 
                            date_time_utc='22-01-2018 01:00:00', 
                            tap_type='ON', 
                            stop_id='Stop2', 
                            company_id='Company1', 
                            bus_id='Bus40', 
                            pan=6011000400000000
                            ), 
                 'OFF': Trip(trip_id=8, 
                             date_time_utc='22-01-2018 04:05:00', 
                             tap_type='OFF', 
                             stop_id='Stop3', 
                             company_id='Company1', 
                             bus_id='Bus40', 
                             pan=6011000400000000
                             )
                 }
                ], 
            4917300800000000: [
                {'ON': Trip(trip_id=7, 
                            date_time_utc='22-01-2018 11:00:00', 
                            tap_type='ON', 
                            stop_id='Stop3', 
                            company_id='Company1', 
                            bus_id='Bus41', 
                            pan=4917300800000000), 
                 'OFF': Trip(trip_id=8, 
                             date_time_utc='22-01-2018 12:55:00', 
                             tap_type='OFF', 
                             stop_id='Stop1', 
                             company_id='Company1', 
                             bus_id='Bus41', pan=4917300800000000
                             )
                 }
                ], 
            4911830000000: [
                {'ON': Trip(trip_id=7, 
                            date_time_utc='22-01-2018 09:00:00', 
                            tap_type='ON', 
                            stop_id='Stop3', 
                            company_id='Company1', 
                            bus_id='Bus42', 
                            pan=4911830000000
                            ), 
                 'OFF': Trip(trip_id=8, 
                             date_time_utc='22-01-2018 14:05:00', 
                             tap_type='OFF', 
                             stop_id='Stop2', 
                             company_id='Company1', 
                             bus_id='Bus42', 
                             pan=4911830000000
                             )
                 }
                ], 
            5454545454545454: [
                {'ON': Trip(trip_id=9, 
                            date_time_utc='22-01-2018 13:00:00', 
                            tap_type='ON', 
                            stop_id='Stop1', 
                            company_id='Company1', 
                            bus_id='Bus43', 
                            pan=5454545454545454
                            )
                 }
                ], 
            5555555555554444: [
                {'ON': Trip(trip_id=10, 
                            date_time_utc='22-01-2018 11:00:00', 
                            tap_type='ON', 
                            stop_id='Stop1', 
                            company_id='Company1', 
                            bus_id='Bus44', 
                            pan=5555555555554444
                            )
                 }
                ], 
            6799990100000000019: [
                {'ON': Trip(trip_id=11, 
                            date_time_utc='22-01-2018 11:00:00', 
                            tap_type='ON', 
                            stop_id='Stop3', 
                            company_id='Company1', 
                            bus_id='Bus45', 
                            pan=6799990100000000019
                            )
                 }
                ]
            }
        
        
    def test_get_duration_boarded_1_alight_1(self):
        duration = get_duration(self.boarded_1, self.alight_1)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_2_alight_2(self):
        duration = get_duration(self.boarded_2, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_3_alight_3(self):
        duration = get_duration(self.boarded_3, self.alight_3)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_5_alight_5(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_5_1_alight_5_1(self):
        duration = get_duration(self.boarded_5_1, self.alight_5_1)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration_boarded_3_alight_1(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_duration(self):
        duration = get_duration(self.boarded_1, self.alight_2)
        assert duration == "0 hours 05 minutes 00 seconds"

    def test_get_status_completed(self):
        status = get_status(self.boarded_1, self.alight_1)
        assert status == 'COMPLETED'

    def test_get_status_incomplete(self):
        status = get_status(self.boarded_1, None)
        assert status == 'INCOMPLETE'

    def test_get_status_canceled(self):
        status = get_status(self.boarded_1, self.boarded_1)
        assert status == 'CANCELED'

    def test_get_charge_boarded_1_alight_1(self):
        charge = get_charge(self.boarded_1, self.alight_1)
        assert charge == "$ 3.25"

    def test_get_charge_boarded_2_alight_2(self):
        charge = get_charge(self.boarded_2, self.alight_2)
        assert charge == "$ 3.25"

    def test_get_charge_boarded_3_alight_3(self):
        charge = get_charge(self.boarded_2, self.alight_3)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_5_alight_5(self):
        charge = get_charge(self.boarded_5, self.alight_5)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_3_alight_3(self):
        charge = get_charge(self.boarded_3, self.alight_3)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_1_no_alight(self):
        charge = get_charge(self.boarded_1, None)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_2_no_alight(self):
        charge = get_charge(self.boarded_2, None)
        assert charge == "$ 5.50"

    def test_get_charge_boarded_3_no_alight(self):
        charge = get_charge(self.boarded_3, None)
        assert charge == "$ 7.30"

    def test_get_charge_boarded_1_cancelled(self):
        charge = get_charge(self.boarded_1, self.boarded_1)
        assert charge == "$ 0.00"

    def test_charge_trip(self):
        charges = charge_trip(self.trips)
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
                'Status': 'COMPLETED'}, 
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:05:00', 
                'DurationSecs': '0 hours 05 minutes 00 seconds', 
                'FromStopId': 'Stop2', 
                'ToStopId': 'Stop1', 
                'ChargeAmount': '$ 3.25', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555558, 
                'Status': 'COMPLETED'}, 
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:05:00', 
                'DurationSecs': '0 hours 05 minutes 00 seconds', 
                'FromStopId': 'Stop3', 
                'ToStopId': 'Stop1', 
                'ChargeAmount': '$ 7.30', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555557, 
                'Status': 'COMPLETED'}, 
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': None, 
                'DurationSecs': None, 
                'FromStopId': 'Stop3', 
                'ToStopId': None, 
                'ChargeAmount': '$ 7.30', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555556, 
                'Status': 'INCOMPLETE'}, 
            {
                'Started': '22-01-2018 13:00:00', 
                'Finished': '22-01-2018 13:05:00', 
                'DurationSecs': '0 hours 05 minutes 00 seconds', 
                'FromStopId': 'Stop3', 
                'ToStopId': 'Stop2', 
                'ChargeAmount': '$ 5.50', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555555, 
                'Status': 'COMPLETED'}, 
            {
                'Started': '22-01-2018 15:00:00', 
                'Finished': '22-01-2018 15:00:00', 
                'DurationSecs': '0 hours 00 minutes 00 seconds', 
                'FromStopId': 'Stop3', 
                'ToStopId': 'Stop3', 
                'ChargeAmount': '$ 0.00', 
                'CompanyId': 'Company1', 
                'BusID': 'Bus37', 
                'PAN': 5500005555555555, 
                'Status': 'CANCELED'}
            ]
        
    def test_generate_output_file(self):
        output = generate_output_file(self.charged_trip)
        assert output.status_code == 200
    
