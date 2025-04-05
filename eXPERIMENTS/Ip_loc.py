import requests

def get_location(ip):
    url = f"http://ip-api.com/json/{ip}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "success":
        print("\n🌍 IP Location Details:")
        print(f"📌 IP Address: {data['query']}")
        print(f"🌎 Country: {data['country']}")
        print(f"🏙️ Region: {data['regionName']}")
        print(f"🏢 City: {data['city']}")
        print(f"📍 Latitude: {data['lat']}")
        print(f"📍 Longitude: {data['lon']}")
        print(f"📡 ISP: {data['isp']}")
    else:
        print("❌ Invalid IP or API limit reached.")

# 🔹 User chooses to enter an IP manually or track their own
choice = input("Do you want to track your own IP? (yes/no): ").strip().lower()

if choice == "yes":
    ip_address = requests.get("https://api64.ipify.org?format=json").json()["ip"]
    print(f"\n🔍 Your Public IP: {ip_address}")
else:
    ip_address = input("\nEnter the IP address to track: ").strip()

# 🔹 Fetch and display location details
get_location(ip_address)
