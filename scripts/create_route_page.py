import os
import sys
import django
import requests
import json

# Step 1: Setup Django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skycms.settings.dev")
django.setup()

# Step 2: Import models
from routes.models import RoutePage, FlightsIndexPage
from wagtail.models import Page
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

# Step 3: Get source & destination from args
if len(sys.argv) != 3:
    print("Usage: python create_route_page.py JFK LAS")
    sys.exit(1)

source = sys.argv[1].upper()
destination = sys.argv[2].upper()

# Step 4: Call the FastAPI
url = f"http://localhost:8080/report/getroutefares/{source}/{destination}"
response = requests.get(url)

if response.status_code != 200:
    print("Failed to fetch fare data from API")
    sys.exit(1)

fare_data = response.json()
sorted_fares = sorted(fare_data, key=lambda x: x["fare"])
fare_data_pretty = json.dumps(sorted_fares[:10], indent=2)


routeServedByAirLineUrl = url = f"http://localhost:8080/report/getrouteservedbyairlines/{source}/{destination}"

try:
    routeServedByAirLineResponse = requests.get(routeServedByAirLineUrl)
    routeServedByAirLineResponse.raise_for_status()
    routeServedByAirLineResponseData = routeServedByAirLineResponse.json()

    # Get unique airline codes
    routeServedByAirLine = sorted({entry["departairline"] for entry in routeServedByAirLineResponseData})
except Exception as e:
    print(f"Failed to fetch airlines: {e}")

popularRoutesUrl = f"http://localhost:8080/report/popularflightsearchroutes/{source}/{destination}"

try:
    popularRoutesResponse = requests.get(popularRoutesUrl)
    popularRoutesResponse.raise_for_status()
    popularResponseData = popularRoutesResponse.json()

    # Sort by search_count and get top 5
    top_5 = sorted(popularResponseData, key=lambda x: x['search_count'], reverse=True)[:5]
except Exception as e:
    print(f"Failed to fetch popular routes: {e}")


# Step 5: Find a parent page (for now use root)
# root_page = Page.get_first_root_node()
try:
    root_page = get_or_create_route_index()
except FlightsIndexPage.DoesNotExist:
    print("FlightsIndexPage does not exist — create it in admin first!")
    sys.exit(1)

# Step 6: Slug
slug = f"cheap-flights-from-{source.lower()}-{destination.lower()}"

# Step 7: Check if it exists already
if RoutePage.objects.filter(slug=slug).exists():
    print(f"RoutePage '{slug}' already exists.")
    sys.exit(0)

# Step 8: Create the page
new_page = RoutePage(
    title=f"Cheap Flights from {source} to {destination}",
    slug=slug,
    source=source,
    destination=destination,
    fare_data=fare_data_pretty,
    airlines_serving_route=routeServedByAirLine,
    popular_routes=top_5
)

root_page.add_child(instance=new_page)
new_page.save_revision().publish()

print(f"Page created: /{slug}/")
