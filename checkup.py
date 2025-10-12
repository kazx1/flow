
import requests

url = input("Website URL: ")
try:
    r = requests.get(url, timeout=5)
    print("✅ Website up!" if r.status_code == 200 else "⚠️ Website on:", r.status_code)
except:
    print("❌ Website unreachable.")
