from flask import Flask, request, jsonify, send_file
import json
import ollama


class Tools:

    app = Flask(__name__)

    # Handle POST requests
    @app.route('/TOPDESK_POST/incidents', methods=['POST'])
    def handle_post():
        data = request.get_json()
        name = data.get('caller', {}).get('dynamicName')
        idnr = data.get('caller', {}).get('location', {}).get('id')
        priority_name = data.get('priority', {}).get('name')
    
        response = {
            'callerName': name,
            'locationID': idnr,
            'priorityName': priority_name
        }
    
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
        return send_file('./Responses/ID_response.json', mimetype='application/json')

    @app.route('/TOPDESK_POST/incidents', methods=['GET'])
    def handle_get_incidents():
        return send_file('./Responses/Topdesk_incidents_response.json', mimetype='application/json')


    @app.route('/<path:path>', methods=['GET'])
    def handle_404(path):
        return "Error 404: Not Found", 404

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)
