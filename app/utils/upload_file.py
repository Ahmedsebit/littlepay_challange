import csv
import io
import boto3
import botocore
import pandas as pd
from datetime import datetime
from app.models.trips import Trip
from flask import request, current_app, Response, jsonify


def read_file(file):

    workbook = pd.read_csv(file)
    trips_d = {}
    for index, row in workbook.iterrows():
        
        trip = Trip(
            trip_id = row[0],
            date_time_utc = row[1].lstrip(),
            tap_type = row[2].lstrip(),
            stop_id = row[3].lstrip(),
            company_id = row[4].lstrip(),
            bus_id = row[5].lstrip(),
            pan = int(row[6])
        )
        
        
        if trip.pan in trips_d:
            if trip.tap_type == 'ON':
                trips_d[trip.pan].append({trip.tap_type:trip})
            else:
                trips_d[trip.pan][-1][trip.tap_type]=trip
        else:
            trips_d[trip.pan] = [{trip.tap_type:trip}]
    
    return trips_d


def charge_trip(trips):

    charges = []
    for key, taps in trips.items():
        for tap in taps:
            
            boarded = tap.get('ON')
            alight = tap.get('OFF')
            
            charge = {}
            charge["Started"] = boarded.date_time_utc
            charge["Finished"] = alight.date_time_utc if alight else None
            charge["DurationSecs"] = get_duration(boarded, alight)
            charge["FromStopId"] = boarded.stop_id
            charge["ToStopId"] = alight.stop_id if alight else None
            charge["ChargeAmount"] = get_charge(boarded, alight)
            charge["CompanyId"] = boarded.company_id
            charge["BusID"] = boarded.bus_id
            charge["PAN"] = key
            charge["Status"] = get_status(boarded, alight)
            
            charges.append(charge)

    return charges


def get_duration(boarded, alight):

    if not alight:
        return None
    
    started = datetime.strptime(boarded.date_time_utc, "%d-%m-%Y %H:%M:%S")
    finished = datetime.strptime(alight.date_time_utc, "%d-%m-%Y %H:%M:%S")
    
    duration = str(finished - started).split(":")
    return f"{duration[0]} hours {duration[1]} minutes {duration[2]} seconds"


def get_charge(boarded, alight):

    status = get_status(boarded, alight)
    stop1_to_stop2 = set(["Stop1", "Stop2"])
    stop2_to_stop3 = set(["Stop2", "Stop3"])
    stop1_to_stop3 = set(["Stop1", "Stop3"])

    stop1_to_stop2_charges = current_app.config['STOP1_TO_STOP2']
    stop2_to_stop3_charges = current_app.config['STOP2_TO_STOP3']
    stop1_to_stop3_charges = current_app.config['STOP1_TO_STOP3']

    if status == "COMPLETED":
        if boarded.stop_id in stop1_to_stop2 and alight.stop_id in stop1_to_stop2:
            return stop1_to_stop2_charges
        elif boarded.stop_id in stop2_to_stop3 and alight.stop_id in stop2_to_stop3:
            return stop2_to_stop3_charges
        elif boarded.stop_id in stop1_to_stop3 and alight.stop_id in stop1_to_stop3:
            return stop1_to_stop3_charges
    elif status == "INCOMPLETE":
        if boarded.stop_id == "Stop1":
            return max(stop1_to_stop2_charges, stop1_to_stop3_charges)
        elif boarded.stop_id == "Stop2":
            return max(stop1_to_stop2_charges, stop2_to_stop3_charges)
        elif boarded.stop_id == "Stop3":
            return max(stop2_to_stop3_charges, stop1_to_stop3_charges)
    if status == "CANCELED":
        return "$ 0.00"


def get_status(boarded, alight):

    if not alight:
        return "INCOMPLETE"

    if boarded.stop_id == alight.stop_id:
        return "CANCELED"

    return "COMPLETED"

def generate_output_file(charges):
    
    uploaded_folder = current_app.config['AWS_BUCKET_FOLDER']
    BUCKET_NAME = current_app.config['AWS_BUCKET_NAME']
    s3_resource = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id=current_app.config['AWS_ACCESS_ID'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY']
    )
    
    writer_file =  io.StringIO()
    writer = csv.writer(writer_file, dialect='excel', delimiter=',')
    headers = [
        "Started", 
        "Finished", 
        "DurationSecs", 
        "FromStopId", 
        "ToStopId", 
        "ChargeAmount", 
        "CompanyId", 
        "BusID", 
        "PAN",
        "Status"
        ]
    writer.writerow(headers)
    for charge in charges:
        new_row = [
            charge.get("Started"),
            charge.get("Finished"),
            charge.get("DurationSecs"),
            charge.get('FromStopId'),
            charge.get('ToStopId'), 
            charge.get('ChargeAmount'), 
            charge.get('CompanyId'), 
            charge.get('BusID'), 
            charge.get('PAN'), 
            charge.get('Status')
            ]
        writer.writerow(new_row)
    
    if BUCKET_NAME:
        ts = str(datetime.utcnow())
        uploaded_filename = f'output_file_{ts}.csv'
        s3_resource.Object(BUCKET_NAME, uploaded_filename).put(
            Body=writer_file.getvalue(), Key=f'{uploaded_folder}/{uploaded_filename}')
        
    return Response(
            writer_file.getvalue(),
            mimetype='text/plain',
            headers={"Content-Disposition": f"attachment;filename=test.csv"}
        )
