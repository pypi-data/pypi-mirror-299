import os
import requests

class Notifier:
    def __init__(self):
        self.api_key = os.environ.get("SENDALERT_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be set as SENDALERT_API_KEY environment variable")
        self.base_url = "https://v1-alert-endpoint-d5obdxuaqq-ey.a.run.app/"

    def send_alert(self, project, mode, text):
        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "project": project,
            "mode": mode,
            "text": text
        }
        try:
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
            if 'response' in locals():
                print(f"Status code: {response.status_code}")
                print(f"Response: {response.text}")
            return None

def sendalert(text, project="default", mode="default"):
    notifier = Notifier()
    return notifier.send_alert(project, mode, text)

# Optionale globale Konfiguration
default_api_key = os.environ.get("SENDALERT_API_KEY")
