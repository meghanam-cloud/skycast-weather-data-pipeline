import json
import urllib.request
import boto3
import csv
from datetime import datetime, timedelta
import io
import os

# --- AWS & API Configuration ---
BUCKET_NAME = os.environ["BUCKET_NAME"]
S3_KEY = os.environ["S3_KEY"]
API_KEY = os.environ["OPENWEATHER_API_KEY"]

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # --- Get Coordinates ---
    params = event.get("queryStringParameters") or {}

    lat = float(params.get("lat", 12.9716))
    lon = float(params.get("lon", 77.5946))

    # --- Debug Log ---
    print(f"✅ Event received: {json.dumps(event)}")
    print(f"📍 Coordinates used: lat={lat}, lon={lon}")

    # --- Fetch Weather Data ---
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    with urllib.request.urlopen(url) as response:
        weather_data = json.loads(response.read())

    # --- Convert to IST Timestamp ---
    utc_now = datetime.utcnow()
    ist_now = utc_now + timedelta(hours=5, minutes=30)
    timestamp = ist_now.strftime("%Y-%m-%d %H:%M:%S")

    # --- Flatten Weather Data ---
    row = {
        "timestamp": timestamp,
        "lat": lat,
        "lon": lon,
        "city": weather_data.get("name", ""),
        "temp": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "temp_min": weather_data["main"]["temp_min"],
        "temp_max": weather_data["main"]["temp_max"],
        "humidity": weather_data["main"]["humidity"],
        "pressure": weather_data["main"]["pressure"],
        "weather_main": weather_data["weather"][0]["main"],
        "weather_desc": weather_data["weather"][0]["description"],
        "wind_speed": weather_data["wind"].get("speed", 0),
        "wind_deg": weather_data["wind"].get("deg", 0)
    }

    # --- Read existing CSV if present ---
    try:
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=S3_KEY)
        csv_content = obj["Body"].read().decode("utf-8")

        csv_buffer = io.StringIO(csv_content)
        reader = list(csv.DictReader(csv_buffer))
        fieldnames = list(row.keys())

        output_buffer = io.StringIO()
        writer = csv.DictWriter(output_buffer, fieldnames=fieldnames)
        writer.writeheader()

        for r in reader:
            filtered = {k: r.get(k, "") for k in fieldnames}
            writer.writerow(filtered)

        writer.writerow(row)

    except s3.exceptions.NoSuchKey:
        output_buffer = io.StringIO()
        writer = csv.DictWriter(output_buffer, fieldnames=row.keys())
        writer.writeheader()
        writer.writerow(row)

    # --- Upload updated CSV to S3 ---
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=S3_KEY,
        Body=output_buffer.getvalue()
    )

    # --- API Response ---
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"✅ Weather data appended successfully at {timestamp} (IST)",
            "data": row
        })
    }
