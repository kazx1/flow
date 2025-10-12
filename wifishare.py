
import os, qrcode

SSID = os.getenv("SSID","MyWifi")
SEC  = os.getenv("SEC","WPA")      # WEP/WPA/WPA2/WPA3 (get your wifi encryption)
PASS = os.getenv("PASS","password")

payload = f"WIFI:T:{SEC};S:{SSID};P:{PASS};H:false;;"
img = qrcode.make(payload)
img.save("homewifi.png")
print("Scan it !")
