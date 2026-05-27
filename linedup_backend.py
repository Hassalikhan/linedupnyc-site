"""
LinedUp NYC — Google Places API Backend v1.2
Fetches live open/closed data for 15 Manhattan venues every 5 minutes.
Outputs a JSON file that the iOS app reads from a hosted URL.
"""

import requests
import json
import time
import os
from datetime import datetime, timezone

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY", "")

VENUES = [
    {
        "id": 1, "name": "Mimi's", "subtitle": "New York. New Yogurt.",
        "place_id": "ChIJUYops4hZwokRcW8uXc9DZHY",
        "address": "231 Lafayette St", "neighborhood": "SoHo",
        "category": "Frozen Yogurt", "icon": "🍦",
        "tagline": "Aussie froyo, NYC line. The math doesn't math.",
        "peak_start": 12, "peak_end": 17,
        "avg_wait_peak": 30, "avg_wait_off": 8,
        "color": "#E8A87C",
        "ig": "https://www.instagram.com/explore/locations/120499254434498/mimis-nyc/",
    },
    {
        "id": 2, "name": "Caffè Paradiso", "subtitle": "The Salted Brown Butter Cult",
        "place_id": "ChIJJR04UgBZwokRdIavUHMRFDI",
        "address": "202B Elizabeth St", "neighborhood": "Nolita",
        "category": "Coffee", "icon": "☕",
        "tagline": "Draft latte on tap. Patience not on tap.",
        "peak_start": 9, "peak_end": 14,
        "avg_wait_peak": 25, "avg_wait_off": 8,
        "color": "#6B8F71",
        "ig": "https://www.instagram.com/explore/locations/1029821498160269/caffe-paradiso/",
    },
    {
        "id": 3, "name": "MYKA Greek", "subtitle": "Madrid → Miami → The Village",
        "place_id": "ChIJR52teQBZwokRf42Ga6nyW_o",
        "address": "159 7th Ave South", "neighborhood": "West Village",
        "category": "Frozen Yogurt", "icon": "🇬🇷🍨",
        "tagline": "Baklava crumble on Greek froyo. Hour-long line on Greek froyo.",
        "peak_start": 13, "peak_end": 20,
        "avg_wait_peak": 45, "avg_wait_off": 15,
        "color": "#1E3A5F",
        "ig": "https://www.instagram.com/explore/tags/mykagreek/",
    },
    {
        "id": 4, "name": "Birdie's", "subtitle": "Froyo Is Back",
        "place_id": "ChIJSUYWZABZwokRjwf3d3SU_30",
        "address": "152 7th Ave South", "neighborhood": "West Village",
        "category": "Frozen Yogurt & Candy", "icon": "🐦🍧",
        "tagline": "Named after a Brussels Griffon. Lines longer than the leash.",
        "peak_start": 14, "peak_end": 21,
        "avg_wait_peak": 25, "avg_wait_off": 8,
        "color": "#F4C2C2",
        "ig": "https://www.instagram.com/explore/locations/18444227862089498/birdies-nyc/",
    },
    {
        "id": 5, "name": "Fonty's Deli + Dukaan", "subtitle": "Indian Bodega Energy",
        "place_id": "ChIJ74zUVSdZwokReIHH0xHm-ws",
        "address": "20 Christopher St", "neighborhood": "West Village",
        "category": "Deli / Sandwiches", "icon": "🇮🇳🥪",
        "tagline": "Parsi Cubano worth the Christopher St commute.",
        "peak_start": 11, "peak_end": 14,
        "avg_wait_peak": 20, "avg_wait_off": 5,
        "color": "#E07B39",
        "ig": "https://www.instagram.com/fontysdeli_dukaan/",
    },
    {
        "id": 6, "name": "Prince St. Pizza", "subtitle": "The Spicy Spring OG",
        "place_id": "ChIJ6xvs94VZwokRnT1D2lX2OTw",
        "address": "27 Prince St", "neighborhood": "Nolita",
        "category": "Pizza", "icon": "🍕",
        "tagline": "Pepperoni squares worth your dignity. Since 2012.",
        "peak_start": 11, "peak_end": 22,
        "avg_wait_peak": 35, "avg_wait_off": 10,
        "color": "#D4442A",
        "ig": "https://www.instagram.com/explore/locations/285093/prince-street-pizza/",
    },
    {
        "id": 7, "name": "Caffè Panna", "subtitle": "Danny Meyer's Daughter Did That",
        "place_id": "ChIJpUwuIMNZwokRBlex2HAooM0",
        "address": "77 Irving Pl", "neighborhood": "Gramercy",
        "category": "Ice Cream", "icon": "🍨",
        "tagline": "Daily-changing flavors. Permanently-long line.",
        "peak_start": 14, "peak_end": 20,
        "avg_wait_peak": 35, "avg_wait_off": 10,
        "color": "#C4956A",
        "ig": "https://www.instagram.com/explore/locations/2230809797209498/caffe-panna/",
    },
    {
        "id": 8, "name": "Katz's Delicatessen", "subtitle": "Since 1888. Line Since 1889.",
        "place_id": "ChIJCar0f49ZwokR6ozLV-dHNTE",
        "address": "205 E Houston St", "neighborhood": "Lower East Side",
        "category": "Deli", "icon": "🥪🌭",
        "tagline": "I'll have what she's having. In 40 minutes.",
        "peak_start": 11, "peak_end": 14,
        "avg_wait_peak": 40, "avg_wait_off": 12,
        "color": "#E8B828",
        "ig": "https://www.instagram.com/explore/locations/25606741/katzs-delicatessen/",
    },
    {
        "id": 9, "name": "Levain Bakery", "subtitle": "The 6oz Cookie Empire",
        "place_id": "ChIJdXpUxMtZwokRq904Bbqnuw0",
        "address": "340 Lafayette St", "neighborhood": "NoHo",
        "category": "Bakery", "icon": "🍪",
        "tagline": "Training for an Ironman birthed this cookie. And this line.",
        "peak_start": 10, "peak_end": 15,
        "avg_wait_peak": 30, "avg_wait_off": 8,
        "color": "#D4763A",
        "ig": "https://www.instagram.com/explore/locations/270413816/levain-bakery/",
    },
    {
        "id": 10, "name": "Ceres", "subtitle": "Eleven Madison Park → Mott St",
        "place_id": "ChIJb6qAbrNZwokRg4_SLLcih-A",
        "address": "164 Mott St", "neighborhood": "Little Italy",
        "category": "Pizza", "icon": "🍕🔵",
        "tagline": "Sign up for a time slot. Sell out by 6:30. That's it. That's the review.",
        "peak_start": 11, "peak_end": 20,
        "avg_wait_peak": 50, "avg_wait_off": 15,
        "color": "#2B2B2B",
        "ig": "https://www.instagram.com/ceres.nyc/",
    },
    {
        "id": 11, "name": "Pizza Studio Tamaki", "subtitle": "Tokyo-Neapolitan in the East Village",
        "place_id": "ChIJ6wRqGwBZwokRvMOkIKk6DIc",
        "address": "123 St Marks Pl", "neighborhood": "East Village",
        "category": "Pizza", "icon": "🇯🇵🍕",
        "tagline": "Proprietary flour from Japan. Reservation-only hype. Worth the plane ticket.",
        "peak_start": 17, "peak_end": 22,
        "avg_wait_peak": 40, "avg_wait_off": 10,
        "color": "#B22222",
        "ig": "https://www.instagram.com/pst.nyc/",
    },
    {
        "id": 12, "name": "Mimi's", "subtitle": "The University Place Sequel",
        "place_id": "ChIJfeq7bFpZwokRRzmUly3QA0U",
        "address": "84 University Pl", "neighborhood": "Union Square",
        "category": "Frozen Yogurt", "icon": "🍦",
        "tagline": "Same froyo, different zip code. Line still included.",
        "peak_start": 12, "peak_end": 17,
        "avg_wait_peak": 25, "avg_wait_off": 6,
        "color": "#E8A87C",
        "ig": "https://www.instagram.com/mimis.ny/",
    },
    {
        "id": 13, "name": "Leon's Bagels", "subtitle": "Rainbow Bagels on Mulberry",
        "place_id": "ChIJKQWE8UZZwokRUFB32gGhH-Q",
        "address": "181 Mulberry St", "neighborhood": "Nolita",
        "category": "Bagels", "icon": "🥯",
        "tagline": "The BEC wait is 30 minutes. The bagel is worth 31.",
        "peak_start": 8, "peak_end": 12,
        "avg_wait_peak": 30, "avg_wait_off": 8,
        "color": "#DAA520",
        "ig": "https://www.instagram.com/leonsbagels/",
    },
    {
        "id": 14, "name": "L'industrie Pizzeria", "subtitle": "Burrata Slice Capital",
        "place_id": "ChIJ92OsaJVZwokRsC54kf-J-3g",
        "address": "104 Christopher St", "neighborhood": "West Village",
        "category": "Pizza", "icon": "🍕",
        "tagline": "Burrata slice. Burrata line. No regrets.",
        "peak_start": 12, "peak_end": 20,
        "avg_wait_peak": 35, "avg_wait_off": 10,
        "color": "#3D7B48",
        "ig": "https://www.instagram.com/lindustriepizzeria/",
    },
    {
        "id": 15, "name": "12 Matcha", "subtitle": "Ceremonial Grade on Bond St",
        "place_id": "ChIJYQM4uYJZwokRtU7IAZdSHZ0",
        "address": "54 Bond St", "neighborhood": "NoHo",
        "category": "Matcha / Coffee", "icon": "🍵",
        "tagline": "6 grams of emerald green per drink. Whisked in front of you. Line out the door.",
        "peak_start": 10, "peak_end": 15,
        "avg_wait_peak": 25, "avg_wait_off": 8,
        "color": "#4A7C59",
        "ig": "https://www.instagram.com/12.matcha/",
    },
]

OUTPUT_FILE = "linedup_data.json"


def fetch_place_details(place_id):
    url = "https://places.googleapis.com/v1/places/" + place_id
    headers = {
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "id,displayName,currentOpeningHours,businessStatus,userRatingCount,rating",
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching {place_id}: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Exception fetching {place_id}: {e}")
        return None


def estimate_busyness(venue, hour, day_of_week):
    is_weekend = day_of_week in [5, 6]
    in_peak = venue["peak_start"] <= hour <= venue["peak_end"]

    if in_peak:
        busyness = 75
    elif hour == venue["peak_start"] - 1 or hour == venue["peak_end"] + 1:
        busyness = 50
    else:
        busyness = 25

    if is_weekend:
        busyness = min(100, int(busyness * 1.3))

    minute = datetime.now().minute
    jitter = ((venue["id"] * 17 + minute) % 20) - 10
    busyness = max(5, min(100, busyness + jitter))
    return busyness


def busyness_to_wait(venue, busyness):
    avg_peak = venue["avg_wait_peak"]
    avg_off = venue["avg_wait_off"]

    if busyness >= 80:
        base_wait = avg_peak
    elif busyness >= 60:
        base_wait = int(avg_peak * 0.7)
    elif busyness >= 40:
        base_wait = int((avg_peak + avg_off) / 2)
    elif busyness >= 20:
        base_wait = avg_off
    else:
        base_wait = max(2, avg_off // 2)

    min_wait = max(1, base_wait - int(base_wait * 0.25))
    max_wait = base_wait + int(base_wait * 0.25)
    return base_wait, min_wait, max_wait


def get_status(estimated_wait):
    if estimated_wait <= 8:
        return "WALK RIGHT IN", "#4ADE80"
    elif estimated_wait <= 20:
        return "NOT BAD AT ALL", "#FACC15"
    elif estimated_wait <= 35:
        return "IT'S MOVING, BUT MAY BE A MINUTE", "#FB923C"
    else:
        return "PREPARE TO WAIT, IT'S A HOT LINE", "#F87171"


def main():
    now = datetime.now(timezone.utc)
    local_now = datetime.now()
    hour = local_now.hour
    day_of_week = local_now.weekday()

    results = []

    for venue in VENUES:
        print(f"Fetching data for {venue['name']}...")
        place_data = fetch_place_details(venue["place_id"])

        is_open = True
        if place_data and "currentOpeningHours" in place_data:
            is_open = place_data.get("currentOpeningHours", {}).get("openNow", True)

        busyness = estimate_busyness(venue, hour, day_of_week)

        if not is_open:
            busyness = 0

        estimated_wait, min_wait, max_wait = busyness_to_wait(venue, busyness)
        status, status_color = get_status(estimated_wait)

        if not is_open:
            status = "CLOSED"
            status_color = "#6B7280"
            estimated_wait = 0
            min_wait = 0
            max_wait = 0

        google_rating = None
        google_rating_count = None
        if place_data:
            google_rating = place_data.get("rating")
            google_rating_count = place_data.get("userRatingCount")

        venue_result = {
            "id": venue["id"],
            "name": venue["name"],
            "subtitle": venue["subtitle"],
            "address": venue["address"],
            "neighborhood": venue["neighborhood"],
            "category": venue["category"],
            "icon": venue["icon"],
            "tagline": venue["tagline"],
            "peak_start": venue["peak_start"],
            "peak_end": venue["peak_end"],
            "avg_wait_peak": venue["avg_wait_peak"],
            "avg_wait_off": venue["avg_wait_off"],
            "color": venue["color"],
            "ig": venue["ig"],
            "is_open": is_open,
            "busyness": busyness,
            "estimated_wait": estimated_wait,
            "min_wait": min_wait,
            "max_wait": max_wait,
            "status": status,
            "status_color": status_color,
            "google_rating": google_rating,
            "google_rating_count": google_rating_count,
        }

        results.append(venue_result)
        time.sleep(0.2)

    output = {
        "updated_at": now.isoformat(),
        "updated_at_local": local_now.strftime("%I:%M %p"),
        "day_of_week": local_now.strftime("%A"),
        "venue_count": len(results),
        "venues": results,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Updated {len(results)} venues at {local_now.strftime('%I:%M %p')}")
    print(f"   Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
