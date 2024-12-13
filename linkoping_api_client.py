import requests
from datetime import datetime

class APIClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url

    def post_incident(self, caller_name, location_id, priority_name, description='', status='Öppen', assigned_to='N/A', category='Övrigt', urgency='Medel', impact='Medel'):
        """
        Skickar en POST-förfrågan till /TOPDESK_POST/incidents med fler detaljer för incidenten.
        """
        url = f'{self.base_url}/TOPDESK_POST/incidents'
        data = {
            "caller": {
                "dynamicName": caller_name,
                "location": {"id": location_id}
            },
            "priority": {
                "name": priority_name
            },
            "description": description,
            "status": status,
            "assigned_to": assigned_to,
            "category": category,
            "urgency": urgency,
            "impact": impact,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        response = requests.post(url, json=data)
        return self._handle_response(response)

    def get_users(self):
        """
        Hämtar användare från /v1.0/users.
        """
        url = f'{self.base_url}/v1.0/users'
        response = requests.get(url)
        return self._handle_response(response)

    def get_knowledge_item_by_id(self, knowledge_item_id):
        """
        Hämtar en specifik kunskapsartikel baserat på ID från /knowledgeItems/<id>.
        """
        url = f'{self.base_url}/knowledgeItems/{knowledge_item_id}'
        response = requests.get(url)
        return self._handle_response(response)

    def get_knowledge_items(self):
        """
        Hämtar alla kunskapsartiklar från /knowledgeItems.
        """
        url = f'{self.base_url}/knowledgeItems'
        response = requests.get(url)
        return self._handle_response(response)

    def get_incidents(self):
        """
        Hämtar alla incidenter från /TOPDESK_POST/incidents.
        """
        url = f'{self.base_url}/TOPDESK_POST/incidents'
        response = requests.get(url)
        return self._handle_response(response)

    def _handle_response(self, response):
        """
        Hjälpfunktion för att hantera HTTP-responser.
        """
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError:
                return response.text
        else:
            return f"Error {response.status_code}: {response.text}"

# Exempel på användning:
if __name__ == '__main__':
    client = APIClient()

    # Exempel: Skicka en POST-förfrågan för ett incident-ärende med fler fält
    post_response = client.post_incident(
        caller_name='John Doe',
        location_id='123',
        priority_name='High',
        description='Problem med inloggning',
        status='Öppen',
        assigned_to='IT Support',
        category='IT-problem',
        urgency='Hög',
        impact='Hög'
    )
    print("POST response:", post_response)

    # Exempel: Hämta användare
    users_response = client.get_users()
    print("GET /v1.0/users response:", users_response)

    # Exempel: Hämta en specifik kunskapsartikel baserat på ID
    knowledge_item_response = client.get_knowledge_item_by_id('3fa85f64')
    print("GET knowledge item by ID response:", knowledge_item_response)

    # Exempel: Hämta alla kunskapsartiklar
    all_knowledge_items_response = client.get_knowledge_items()
    print("GET all knowledge items response:", all_knowledge_items_response)

    # Exempel: Hämta alla incidenter
    all_incidents_response = client.get_incidents()
    print("GET all incidents response:", all_incidents_response)