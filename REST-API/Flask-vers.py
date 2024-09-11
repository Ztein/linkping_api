import datetime
from flask import Flask, request, jsonify, send_file
import json
import os
#import ollama


class Tools:

    app = Flask(__name__)

     # Ensure the incidents directory exists
    if not os.path.exists('./incidents'):
        os.makedirs('./incidents')

    # Handle POST requests for TOPDESK incidents
    @app.route('/TOPDESK_POST/incidents', methods=['POST'])
    def handle_post():
        data = request.get_json()
        caller_name = data.get('caller', {}).get('dynamicName')
        location_id = data.get('caller', {}).get('location', {}).get('id')
        priority_name = data.get('priority', {}).get('name')
        description = data.get('description', '')
        status = data.get('status', 'Öppen')
        assigned_to = data.get('assigned_to', 'N/A')
        category = data.get('category', 'Övrigt')
        urgency = data.get('urgency', 'Medel')
        impact = data.get('impact', 'Medel')
        created_at = data.get('created_at', datetime.now().isoformat())
        updated_at = data.get('updated_at', datetime.now().isoformat())

        # Build response
        response = {
            'callerName': caller_name,
            'locationID': location_id,
            'priorityName': priority_name,
            'description': description,
            'status': status,
            'assignedTo': assigned_to,
            'category': category,
            'urgency': urgency,
            'impact': impact,
            'createdAt': created_at,
            'updatedAt': updated_at
        }

        # Save the JSON data to a file in /incidents directory
        incident_filename = f"./incidents/incident_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(incident_filename, 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify(response), 200

    # Handle GET requests for dynamic IDs
    @app.route('/<path:subpath>', methods=['GET'])
    def handle_any_path(subpath):
        # Check if the path contains the desired string
        if 'knowledgeItems/3fa85f64' in request.path:
            return send_file('./Responses/Get_KnowledgeItems/KnowledgeItem_GetByID.json', mimetype='application/json')
        elif 'knowledgeItems' in request.path:
            return send_file('./Responses/Get_KnowledgeItems/KnowledgeItem_GetByDescription.json', mimetype='application/json')
        else:
            return "Error 404: Not Found", 404

    # Handle GET requests
    @app.route('/v1.0/users', methods=['GET'])
    def handle_get_users():
        print("Handling GET request for /v1.0/users")
        return send_file('./Responses/ID_response.json', mimetype='application/json')

    @app.route('/TOPDESK_POST/incidents', methods=['GET'])
    def handle_get_incidents():
        return send_file('./Responses/Topdesk_incidents_response.json', mimetype='application/json')


    @app.route('/<path:path>', methods=['GET'])
    def handle_404(path):
        return "Error 404: Not Found", 404

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)
