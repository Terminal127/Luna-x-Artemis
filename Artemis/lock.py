from flask import Flask, request, jsonify

app = Flask(__name__)

lock_code = "100"  # Initial lock code

@app.route("/", methods=["GET", "POST"])
def index():
    global lock_code

    if request.method == "POST":
        try:
            data = request.json  # Read the request data as JSON
            lock_code = data["lock_code"]  # Extract the lock code from the JSON
            print(f"Lock code updated to: {lock_code}")
            return jsonify({"message": "Lock code updated successfully"}), 200  # Return success message
        except Exception as e:
            print(f"Invalid request: {e}")
            return jsonify({"error": "Invalid request format"}), 400  # Return error message

    return "Invalid Request"

@app.route("/lock", methods=["GET"])
def get_lock_code():
    # Return the current lock code in JSON format
    return jsonify({"lock_code": lock_code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)  # Set the correct host and port for this code