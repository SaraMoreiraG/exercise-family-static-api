"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# Create the Jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# Generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member', methods=['POST'])
def add_member():
    member_data = request.json
    jackson_family.add_member(member_data)
    return jsonify(member_data), 200

@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    result = jackson_family.delete_member(id)
    if not result:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"done": True}), 200

# This only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
