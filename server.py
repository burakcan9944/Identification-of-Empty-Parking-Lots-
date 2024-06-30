from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

free_spaces_count = 0
free_spaces_names = []
difference = ""
plate_name=""
is_free = None


@app.route('/update_spaces', methods=['POST'])
def update_spaces():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    global free_spaces_count, free_spaces_names, difference, plate_name,is_free
    free_spaces_count = data.get("free_spaces", 0)
    free_spaces_names = data.get("free_spaces_list", [])
    difference= data.get("difference", "")
    plate_name = data.get("plate_name", "")
    is_free = data.get("is_free", None)

    print(f"Free spaces count: {free_spaces_count}")
    print(f"Free spaces names: {free_spaces_names}")
    print(f"{plate_name} = {difference}")
    print(f"is_free: {is_free}")
    return jsonify({"message": "Data received successfully!"}), 200

@app.route('/get_spaces', methods=['GET'])
def get_spaces():
    global free_spaces_count, free_spaces_names, difference, plate_name,is_free
    return jsonify({
        "free_spaces_count": free_spaces_count,
        "free_spaces_names": free_spaces_names,
        "difference": difference,
        "plate_name": plate_name,
        "is_free": is_free
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
