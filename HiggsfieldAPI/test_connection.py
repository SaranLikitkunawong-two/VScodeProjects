"""
Quick connection test — generates a single image from a text prompt.
Run: python test_connection.py
"""

import os
from dotenv import load_dotenv

load_dotenv()

from higgsfield_client import SyncClient

client = SyncClient(api_key=os.environ["HF_KEY"])

print("Submitting text-to-image request...")

result = client.subscribe(
    "bytedance/seedream/v4/text-to-image",
    arguments={
        "prompt": "a futuristic city at sunset, cinematic lighting",
        "resolution": "2K",
    },
)

print("Result:", result)
image_url = result["images"][0]["url"]
print("Image URL:", image_url)
