"""
title: Incident reports
author: Niklas Redgert, Knowit Orebro AB
version: 0.1.0
"""

import json
import os
import requests
from urllib import response

class Tools:
    def __init__(self):
        self.citation = True
        pass

    def get_incident_by_name(self, name: str) -> str:
        """
        Get the incident information.
        :name: of person who reported the incident.
        :return: The incident with matching name.
        """

        response = requests.get(f"http://10.139.136.4:8000/v1.0/users")

        if response.status_code == 200:
            try:
                displayName = response.json()["displayName"]
                description = response.json()["signInActivity"]["riskDetail"]
                priority = response.json()["signInActivity"]["riskLevelAggregated"]
            except (KeyError, IndexError):
                print(f"Incidents not found")
                return f"""parsing gone wrong"""
        else:
            return f"""Failed to retrieve incidents for {name}"""
        
        return f"""Given the name {name}, a incident was found for {displayName},
        and the description of the incident '{description}' and the priority: '{priority}'"""

    def get_incident_by_idnr(self, idnr: str) -> str:
        """
        Get the incident information.
        :idnr: The identification number of the incident.
        :return: The incident matching with matching idnr.
        """
        response = requests.get(f"http://10.139.136.4:8000/knowledgeItems/{idnr}")
        if response.status_code == 200:
            try:
                title = response.json()["title"]
                content = response.json()["content"]
                author = response.json()["author"]
                category = response.json()["category"]
            except (KeyError, IndexError):
                print(f"Incidents not found")
                return f"""parsing gone wrong"""
        else:
            return "Error 404: Not Found", 404
        
        return f"""Given the identitynumber, a incident was found by {author}, 
        with the following information:\n
        Title: {title}\n
        Category: {category}\n
        Content: {content}
        """

    def get_incident_by_description(self, **kwargs) -> str:
        """
        Get the incident information.
        :description: the description of the incident.
        :return: The incident matching with matching description.
        """

        response = requests.get(f"http://10.139.136.4:8000/knowledgeItems")
        if response.status_code == 200:
            try:
                idnr = response.json()["items"]["id"]
                title = response.json()["items"]["title"]
                author = response.json()["items"]["author"]
            except (KeyError, IndexError):
                print(f"Incidents not found")
                return f"""parsing gone wrong"""
        else:
            return "Error 404: Not Found", 404

        return f"""Given the description, a incident was found by {author}, 
        with the following information:\n
        Title: {title}\n
        ID: {idnr}
        """
    
    def get_all_incidents(self, **kwargs) -> str:
        """
        Get all the incidents.
        :param type: Optional type parameter
        :return: All incidents in the database
        """
        response = requests.get("http://10.139.136.4:8000/TOPDESK_POST/incidents")

        if response.status_code == 200:
            try:
                name = response.json()["caller"]["displayName"]
                description = response.json()["briefDescription"]
                priority = response.json()["priority"]
            except (KeyError, IndexError):
                print(f"Incidents not found")
                return f"""parsing gone wrong"""
        else:
            return f"""Failed to retrieve data for incidents: {response.status_code}"""

        return f"""Give the user information about the incident, in this case the person who reported it, which was {name},
        and the description of the incident '{description}' and the priority: '{priority}'"""
