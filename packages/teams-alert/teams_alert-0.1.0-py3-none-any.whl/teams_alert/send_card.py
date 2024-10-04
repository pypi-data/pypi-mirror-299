import requests
from .templates import gen_card_to_person, gen_card_no_person

class TeamsAlert:
    def __init__(self, url: str, title: str = "A Nice Title", message: str = "This is a message.", attention: str = None):
        self.url = url
        self.title = title
        self.attention = attention
        self.message = message

        if self.attention:
            self.send_message_with_attention()
        else:
            self.send_message()

    def send_message(self):
        payload = gen_card_no_person(self.title, self.message)
        headers = {
            'Content-Type': 'application/json'        
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        print(response)

    def send_message_with_attention(self):
        payload = gen_card_to_person(self.title, self.message, self.attention)
        print(payload)
        headers = {
            'Content-Type': 'application/json'        
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)

        print(response)