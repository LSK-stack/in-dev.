from flask import Flask, request, send_file
import datetime
import requests

app = Flask(__name__)

LOG_FILE = "ips.txt"

def get_ip_info(ip):
    """Obtenir la géolocalisation d'une IP avec l'API ip-api.com"""
    url = f"http://ip-api.com/json/{ip}?fields=status,country,regionName,city,lat,lon,isp"
    response = requests.get(url).json()

    if response["status"] == "success":
        return {
            "pays": response.get("country", "Inconnu"),
            "région": response.get("regionName", "Inconnu"),
            "ville": response.get("city", "Inconnu"),
            "latitude": response.get("lat", "N/A"),
            "longitude": response.get("lon", "N/A"),
            "fournisseur": response.get("isp", "Inconnu")
        }
    return None

@app.route('/pixel.png')
def track_ip():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ip_info = get_ip_info(ip)

    if ip_info:
        log_data = (f"{time} - IP: {ip} - Pays: {ip_info['pays']} - Région: {ip_info['région']} - "
                    f"Ville: {ip_info['ville']} - Lat: {ip_info['latitude']} - Lon: {ip_info['longitude']} - "
                    f"Fournisseur: {ip_info['fournisseur']} - User-Agent: {user_agent}")
    else:
        log_data = f"{time} - IP: {ip} - Géolocalisation indisponible - User-Agent: {user_agent}"

    print(log_data)

    with open(LOG_FILE, "a") as file:
        file.write(log_data + "\n")

    return send_file("pixel.png", mimetype='image/png')

if __name__ == '__main__':
    print("Serveur Flask démarré... Suivi des IPs en cours...")
    app.run(host='0.0.0.0', port=5000)
