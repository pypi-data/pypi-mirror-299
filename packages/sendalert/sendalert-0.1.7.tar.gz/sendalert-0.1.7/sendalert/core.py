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
            print("Notification sent successfully")
            return True
        except requests.exceptions.RequestException as e:
            print(f"Error sending notification: {e}")
            return False

def sendalert(text, project="default", mode="default"):
    notifier = Notifier()
    return notifier.send_alert(project, mode, text)

# Optional global configuration
default_api_key = os.environ.get("SENDALERT_API_KEY")

# Diese Zeile macht die Funktion auf Modulebene verfügbar
globals()['sendalert'] = sendalert
