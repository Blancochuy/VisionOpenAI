import requests
import base64
import json

class GPT4VAPIHandler:
    def __init__(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        
        self.api_endpoint = config['api_endpoint']
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config['api_key']}"
        }
        self.model = config['model']
        self.role = config['role']
        self.content = config['content']

    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def get_response(self, image_path):
        base64_image = self.encode_image(image_path)
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": self.role,
                    "content": [
                        {
                            "type": "text",
                            "text": self.content
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        response = requests.post(self.api_endpoint, headers=self.headers, json=payload)
        return response.json()  # Handle this based on your specific use case
