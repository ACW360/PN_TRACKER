import phonenumbers
from phonenumbers import geocoder, carrier
from timezonefinder import TimezoneFinder
import folium
from geopy.geocoders import Nominatim
import time
from colorama import init, Fore, Back
init(autoreset=True)

def banner():
        print(Fore.RED + """

 ____  _   _     _____ ____      _    ____ _  _______ ____
|  _ \| \ | |   |_   _|  _ \    / \  / ___| |/ / ____|  _ \
| |_) |  \| |_____| | | |_) |  / _ \| |   | ' /|  _| | |_) |
|  __/| |\  |_____| | |  _ <  / ___ \ |___| . \| |___|  _ <
|_|   |_| \_|     |_| |_| \_\/_/   \_\____|_|\_\_____|_| \_\

               <<<<=>>>> Author: ACW360 <<<<=>>>>""" + "\n")
banner()

# Step 1: Enter the phone number
number = input(Fore.GREEN + "Enter the phone number with country code: ")
phone_number = phonenumbers.parse(number)

# Step 2: Get country and location info
location = geocoder.description_for_number(phone_number, 'en')
print(Fore.GREEN + "📍 Location:", location)

# Step 3: Get the carrier (e.g. MTN, Airtel)
service_provider = carrier.name_for_number(phone_number, 'en')
print(Fore.GREEN + "📡 Carrier:", service_provider)

# Step 4: Use geopy to get coordinates with error handling
try:
    time.sleep(1)  # avoid getting rate-limited
    geolocator = Nominatim(user_agent="MrRobotTracker/1.0 (contact@example.com)")
    location_data = geolocator.geocode(location, timeout=10)

    if location_data:
        lat = location_data.latitude
        lon = location_data.longitude
        print(Fore.GREEN + "🌍 Coordinates:", lat, lon)

        # Step 5: Find timezone
        tf = TimezoneFinder()
        timezone = tf.timezone_at(lng=lon, lat=lat)
        print(Fore.GREEN + "🕒 Timezone:", timezone)

        # Step 6: Create a map with Folium
        map = folium.Map(location=[lat, lon], zoom_start=8)
        folium.Marker([lat, lon], popup=location).add_to(map)

        # Step 7: Save the map to HTML
        map.save("phone_location.html")
        print(Fore.GREEN + "📁 Map saved as phone_location.html")
    else:
        print(Fore.RED + "❌ Could not find coordinates for this location.")

except Exception as e:
    print(Fore.RED + "🚫 Error while retrieving location data:", e)
