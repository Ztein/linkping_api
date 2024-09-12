from datetime import datetime
from flask import Flask, request, jsonify, send_file
import json
import os
import uuid

def user_exists(user_id):
    return os.path.exists(f'./users/{user_id}.json')

    
def create_user_profile(user_id, user_data):
        user_profile = {
            "displayName": user_data.get('dynamicName', 'Unknown User'),
            "id": str(uuid.uuid4()),  # Generate a new UUID
            "signInActivity": {
                "lastSignInDateTime": datetime.now().isoformat(),
                "lastSignInRequestId": str(uuid.uuid4()),  # Random request ID
                "riskDetail": "passwordExpired",  # Default values
                "riskLevelAggregated": "high",
                "riskLevelDuringSignIn": "high",
                "riskState": "confirmedSafe"
            },
            "userPrincipalName": user_data.get('email', 'unknown@example.com')  # Assuming email is part of the data
        }

        # Save the user profile to a file
        with open(f'./users/{user_id}.json', 'w') as f:
            json.dump(user_profile, f, indent=4)

def get_fake_incident(caller_id, dynamic_name):
    fabricated_incident = {
                "caller": {
                    "id": caller_id,
                    "dynamicName": dynamic_name,
                    "location": {"id": "12345"}
                },
                "priority": {
                    "name": "Hög"
                },
                "description": "Påhittad incident för användar-ID",
                "status": "Öppen",
                "assigned_to": "Support Team",
                "category": "Övrigt",
                "urgency": "Hög",
                "impact": "Hög",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
    return fabricated_incident

class Tools:

    app = Flask(__name__)

    # Ensure the incidents directory exists
    if not os.path.exists('./incidents'):
        os.makedirs('./incidents')

    # Ensure the users directory exists
    if not os.path.exists('./users'):
        os.makedirs('./users')

    # Ensure the knowledge_items directory exists
    if not os.path.exists('./knowledge_items'):
        os.makedirs('./knowledge_items')
    

    # Handle POST requests for TOPDESK incidents
    @app.route('/TOPDESK_POST/incidents', methods=['POST'])
    def handle_post():
        data = request.get_json()
        caller = data.get('caller', {})
        caller_id = caller.get('id')
        caller_name = caller.get('dynamicName', 'Unknown')
        location_id = caller.get('location', {}).get('id', 'Unknown')
        priority_name = data.get('priority', {}).get('name', 'Medel')
        description = data.get('description', '')
        status = data.get('status', 'Öppen')
        assigned_to = data.get('assigned_to', 'N/A')
        category = data.get('category', 'Övrigt')
        urgency = data.get('urgency', 'Medel')
        impact = data.get('impact', 'Medel')
        created_at = data.get('created_at', datetime.now().isoformat())
        updated_at = data.get('updated_at', datetime.now().isoformat())

        
        #den här metoden att fejka id är inte så bra men duger för tillfället
        if not caller_id:
            caller_str = caller_name
        else:
            caller_str = caller_id 
        
        if caller_str and not user_exists(caller_str):
            create_user_profile(caller_str, caller)

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

    @app.route('/TOPDESK_POST/incidents', methods=['GET'])
    def handle_get_all_incidents():
        incident_files = [f for f in os.listdir('./incidents') if f.endswith('.json')]
        incidents = []

        for incident_file in incident_files:
            with open(f'./incidents/{incident_file}', 'r') as f:
                incident = json.load(f)
                incidents.append(incident)

        if not incidents:
            return jsonify({"message": "No incidents found"}), 404

        return jsonify(incidents), 200

    # Handle GET requests for all users
    @app.route('/v1.0/users', methods=['GET'])
    def handle_get_users():
        user_files = [f for f in os.listdir('./users') if f.endswith('.json')]
        users = []

        for user_file in user_files:
            with open(f'./users/{user_file}', 'r') as f:
                user_data = json.load(f)
                users.append(user_data)

        if not users:
            return jsonify({"message": "No users found"}), 404

        return jsonify(users), 200

    # Handle GET requests for incidents by caller ID
    @app.route('/TOPDESK_POST/incidents/<caller_id>', methods=['GET'])
    def handle_get_incidents_by_user(caller_id):
        incident_files = [f for f in os.listdir('./incidents') if f.endswith('.json')]
        incidents = []

        # If there are no incident files, return a fabricated incident for the specific caller
        if not incident_files:
            fabricated_incident = get_fake_incident(caller_id=caller_id, dynamic_name='John Doe')
            
            return jsonify([fabricated_incident]), 200

        # Read all incident files and filter by caller ID
        for incident_file in incident_files:
            with open(f'./incidents/{incident_file}', 'r') as f:
                incident = json.load(f)
                # Check if the incident's caller ID matches the requested caller ID
                if incident.get('caller', {}).get('id') == caller_id:
                    incidents.append(incident)

        # If no incidents are found for the given caller ID, return a message
        if not incidents:
            return jsonify({"message": f"No incidents found for caller ID {caller_id}"}), 404

        return jsonify(incidents), 200
    

    @app.route('/TOPDESK_POST/incidents/name/<dynamic_name>', methods=['GET'])
    def handle_get_incidents_by_name(dynamic_name):
        incident_files = [f for f in os.listdir('./incidents') if f.endswith('.json')]
        incidents = []

        # If there are no incident files, return a fabricated incident for the specific dynamicName
        if not incident_files:
            fabricated_incident = fabricated_incident = get_fake_incident(caller_id='John Doe', dynamic_name='John Doe')
            return jsonify([fabricated_incident]), 200

        # Read all incident files and filter by caller dynamicName
        for incident_file in incident_files:
            with open(f'./incidents/{incident_file}', 'r') as f:
                incident = json.load(f)
                # Check if the incident's caller dynamicName matches the requested dynamic name
                if incident.get('caller', {}).get('dynamicName') == dynamic_name:
                    incidents.append(incident)

        # If no incidents are found for the given dynamicName, return a message
        if not incidents:
            return jsonify({"message": f"No incidents found for caller dynamicName {dynamic_name}"}), 404

        return jsonify(incidents), 200
    
    # Handle GET request for a specific knowledge item by ID
    @app.route('/knowledgeItems/<knowledge_item_id>', methods=['GET'])
    def get_knowledge_item_by_id(knowledge_item_id):
        file_path = f'./knowledge_items/{knowledge_item_id}.json'
        
        # Check if the knowledge item exists
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                knowledge_item = json.load(f)
                return jsonify(knowledge_item), 200
        else:
            return jsonify({"message": f"Knowledge item with ID {knowledge_item_id} not found"}), 404

    # Handle GET request for all knowledge items
    @app.route('/knowledgeItems', methods=['GET'])
    def get_knowledge_items():
        knowledge_files = [f for f in os.listdir('./knowledge_items') if f.endswith('.json')]
        knowledge_items = []

        for knowledge_file in knowledge_files:
            with open(f'./knowledge_items/{knowledge_file}', 'r') as f:
                knowledge_item = json.load(f)
                knowledge_items.append(knowledge_item)

        if not knowledge_items:
            return jsonify({"message": "No knowledge items found"}), 404

        return jsonify(knowledge_items), 200

    # Example route to create a new knowledge item (if needed)
    @app.route('/knowledgeItems', methods=['POST'])
    def create_knowledge_item():
        data = request.get_json()
        knowledge_item_id = data.get('id', str(uuid.uuid4()))  # Generate ID if not provided

        # Save the knowledge item to a file
        file_path = f'./knowledge_items/{knowledge_item_id}.json'
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @app.route('/<path:path>', methods=['GET'])
    def handle_404(path):
        return "Error 404: Not Found", 404

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8000)