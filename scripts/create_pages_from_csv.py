import os
import sys
import django
import json

# Step 1: Setup Django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skycms.settings.dev")
django.setup()

import csv
import requests
from wagtail.models import Page
from routes.models import RoutePage, FlightsIndexPage
from home.models import HomePage

def get_or_create_route_index():
    parent = Page.objects.filter(slug="flights").first()
    if not parent:
        print("Creating /flights/ index page...")
        root = HomePage.objects.first()
        parent = FlightsIndexPage(title="Flights", slug="flights")
        root.add_child(instance=parent)
        parent.save_revision().publish()
    return parent


def create_page(origin, destination):
    url = f"http://localhost:8080/report/getroutefares/{origin}/{destination}"
    print(f"Fetching data for {origin} → {destination} ...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        fare_data = response.json()
        sorted_fares = sorted(fare_data, key=lambda x: x["fare"])
        sorted_fares = sorted(fare_data, key=lambda x: x["fare"])
        fare_data_pretty = json.dumps(sorted_fares[:10], indent=2)
    except Exception as e:
        print(f"❌ Failed to fetch data: {e}")
        return

    if not fare_data:
        print(f"⚠ No data found for {origin} → {destination}")
        return
    

    routeServedByAirLineUrl = url = f"http://localhost:8080/report/getrouteservedbyairlines/{origin}/{destination}"

    try:
        routeServedByAirLineResponse = requests.get(routeServedByAirLineUrl)
        routeServedByAirLineResponse.raise_for_status()
        routeServedByAirLineResponseData = routeServedByAirLineResponse.json()

        # Get unique airline codes
        routeServedByAirLine = sorted({entry["departairline"] for entry in routeServedByAirLineResponseData})
    except Exception as e:
        print(f"Failed to fetch airlines: {e}")

    popularRoutesUrl = f"http://localhost:8080/report/popularflightsearchroutes/{origin}/{destination}"

    try:
        popularRoutesResponse = requests.get(popularRoutesUrl)
        popularRoutesResponse.raise_for_status()
        popularResponseData = popularRoutesResponse.json()

        # Sort by search_count and get top 5
        top_5 = sorted(popularResponseData, key=lambda x: x['search_count'], reverse=True)[:5]
    except Exception as e:
        print(f"Failed to fetch popular routes: {e}")

    slug = f"cheap-flights-from-{origin.lower()}-{destination.lower()}"
    title = f"Cheap Flights from {origin} to {destination}"

    if RoutePage.objects.filter(slug=slug).exists():
        print(f"ℹ Page already exists: {slug}")
        return

    parent = get_or_create_route_index()
    if not parent:
        print("❌ FlightsIndexPage not found. Create it in Wagtail admin first.")
        return

    new_page = RoutePage(
        title=title,
        slug=slug,
        source=origin,
        destination=destination,
        fare_data=fare_data_pretty,
        airlines_serving_route=routeServedByAirLine,
        popular_routes=top_5
    )

    parent.add_child(instance=new_page)
    new_page.save_revision().publish()
    print(f"✅ Created: {title}")

def run_from_csv(csv_path):
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            origin = row['origin'].strip().upper()
            destination = row['destination'].strip().upper()
            create_page(origin, destination)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/create_pages_from_csv.py path/to/routes.csv")
        sys.exit(1)

    csv_file = sys.argv[1]
    run_from_csv(csv_file)