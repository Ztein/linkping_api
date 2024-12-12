# Linkping API

A Flask-based REST API that simulates a service desk system with incident management, user profiles, and knowledge base functionality.

## Setup

1. Clone the repository: 

```bash
git clone https://github.com/Ztein/linkping_api.git
cd linkping_api
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

4. Run the server:

```bash
python Flask-vers.py
```

The server will start on `http://0.0.0.0:8000`

## API Endpoints

### Incidents
- `GET /TOPDESK_POST/incidents` - Get all incidents
- `POST /TOPDESK_POST/incidents` - Create a new incident
- `GET /TOPDESK_POST/incidents/<caller_id>` - Get incidents by caller ID
- `GET /TOPDESK_POST/incidents/name/<dynamic_name>` - Get incidents by caller name

### Users
- `GET /v1.0/users` - Get all users

### Knowledge Base
- `GET /knowledgeItems` - Get all knowledge items
- `POST /knowledgeItems` - Create a new knowledge item
- `GET /knowledgeItems/<knowledge_item_id>` - Get specific knowledge item

## Example Usage

### Creating an Incident
bash
curl -X POST http://localhost:8000/TOPDESK_POST/incidents \
-H "Content-Type: application/json" \
-d '{
"caller": {
"id": "user123",
"dynamicName": "John Doe",
"location": {
"id": "loc123"
}
},
"priority": {
"name": "Hög"
},
"description": "Test incident",
"status": "Öppen",
"assigned_to": "Support Team",
"category": "Övrigt",
"urgency": "Hög",
"impact": "Hög"
}'

## Data Storage
The API uses a file-based storage system:
- `/incidents/` - Stores incident JSON files
- `/users/` - Stores user profile JSON files
- `/knowledge_items/` - Stores knowledge base item JSON files

## Error Handling
- Returns 404 for not found resources
- Returns 200 for successful operations