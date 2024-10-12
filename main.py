from fastapi import FastAPI
import requests
from datetime import datetime

from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]  # Replace with your Flutter app's URL in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

API_URL = 'https://www.gamerpower.com/api/giveaways'


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}


@app.get("/giveaways")
async def get_giveaways() -> dict:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

    total_worth = 0
    relevant_giveaways = []

    for item in data:
        if item['worth'] == 'N/A' or item['end_date'] == 'N/A':
            continue

        worth = float(item['worth'].replace('$', ''))
        total_worth += worth

        end_date_obj = datetime.strptime(item['end_date'][:10], '%Y-%m-%d')
        formatted_end_date = end_date_obj.strftime('%b %d %Y')

        relevant_giveaways.append({
            "title": item['title'],
            "platforms": item['platforms'],
            "worth": item['worth'],
            "end_date": formatted_end_date,
            "image_url": item['image'],
            "open_giveaway_url": item['open_giveaway_url']
        })

    return {
        "total_worth": f"${total_worth:.2f}",
        "total_giveaways": len(relevant_giveaways),
        "giveaways": relevant_giveaways
    }


@app.get("/other-giveaways")
async def get_othergiveaways() -> dict:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

    total_worth = 0
    relevant_giveaways = []

    for item in data:
        if item['worth'] == 'N/A':
            continue

        platforms = item['platforms'].split(', ')
        if not any(platform in ['DRM-Free', 'Itch.io', 'GOG'] for platform in platforms):
            continue

        worth = float(item['worth'].replace('$', ''))
        total_worth += worth

        relevant_giveaways.append({
            "title": item['title'],
            "platforms": item['platforms'],
            "worth": item['worth'],
            "image_url": item['image'],
            "open_giveaway_url": item['open_giveaway_url']
        })

    return {
        "total_worth": f"${total_worth:.2f}",
        "total_giveaways": len(relevant_giveaways),
        "giveaways": relevant_giveaways
    }


@app.get("/dlc-giveaways")
async def get_dlc_giveaways() -> dict:
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

    dlc_giveaways = []

    for item in data:
        if item['type'] != 'DLC':
            continue

        end_date_obj = datetime.strptime(item['end_date'][:10], '%Y-%m-%d') if item['end_date'] != 'N/A' else "N/A"
        formatted_end_date = end_date_obj.strftime('%b %d %Y') if isinstance(end_date_obj, datetime) else "N/A"

        dlc_giveaways.append({
            "title": item['title'],
            "description": item['description'],
            "platforms": item['platforms'],
            "end_date": formatted_end_date,
            "image_url": item['image'],
            "open_giveaway_url": item['open_giveaway_url']
        })

    return {
        "total_dlc_giveaways": len(dlc_giveaways),
        "dlc_giveaways": dlc_giveaways
    }
