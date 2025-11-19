from flask import Flask, request, jsonify
import pytz
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return "Time Difference Agent is running!"

@app.route("/time-difference", methods=["GET"])
def time_difference():
    # Get query parameters
    tz1 = request.args.get("tz1", "Asia/Kolkata")
    tz2 = request.args.get("tz2", "UTC")

    try:
        # Get current time in both time zones
        now = datetime.now()
        time1 = now.astimezone(pytz.timezone(tz1))
        time2 = now.astimezone(pytz.timezone(tz2))

        # Calculate difference in hours
        diff_hours = (time1.utcoffset() - time2.utcoffset()).total_seconds() / 3600

        return jsonify({
            "timezone_1": tz1,
            "timezone_2": tz2,
            "time_in_tz1": time1.strftime("%Y-%m-%d %H:%M:%S"),
            "time_in_tz2": time2.strftime("%Y-%m-%d %H:%M:%S"),
            "difference_in_hours": diff_hours
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
