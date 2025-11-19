from flask import Flask, render_template_string, request
from datetime import datetime
import pytz

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>IST Time Difference Agent by Girish</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 50px; }
        input, button { padding: 10px; font-size: 16px; }
        .result { margin-top: 20px; font-weight: bold; color: #333; }
    </style>
</head>
<body>
    <h2>Choose Target Date for NFN Build/Cease CRQ</h2>
    <form method="POST">
        <input type="date" name="target_date" required>
        <button type="submit">Calculate</button>
    </form>
    {% if target_datetime %}
        <div class="result">
            <p>Countdown to {{ target_datetime.strftime('%Y-%m-%d %H:%M:%S') }} IST:</p>
            <div id="countdown"></div>
        </div>
        <script>
            const targetTime = new Date("{{ target_datetime.strftime('%Y-%m-%dT%H:%M:%S') }}").getTime();
            function updateCountdown() {
                const now = new Date().getTime();
                const diff = targetTime - now;
                if (diff <= 0) {
                    document.getElementById("countdown").innerHTML = "Target date has already passed.";
                    return;
                }
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                const seconds = Math.floor((diff % (1000 * 60)) / 1000);
                document.getElementById("countdown").innerHTML =
                    days + " days, " + hours + " hours, " + minutes + " minutes, " + seconds + " seconds";
            }
            setInterval(updateCountdown, 1000);
            updateCountdown();
        </script>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    target_datetime = None
    if request.method == "POST":
        target_date_str = request.form.get("target_date")
        try:
            ist = pytz.timezone('Asia/Kolkata')
            target_date = datetime.strptime(target_date_str, "%Y-%m-%d")
            target_datetime = ist.localize(target_date.replace(hour=23, minute=59, second=0))
        except ValueError:
            target_datetime = None
    return render_template_string(HTML_TEMPLATE, target_datetime=target_datetime)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
