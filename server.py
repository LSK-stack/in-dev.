from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for displaying IP addresses
html_template = '''
<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>IP Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        h1 { color: #333; }
        #ip-list { margin-top: 20px; }
        p { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Connected IP Addresses</h1>
    <div id='ip-list'>
        {% for ip in ip_addresses %}
            <p>{{ ip }}</p>
        {% endfor %}
    </div>
</body>
</html>
'''

# List to store IP addresses
ip_addresses = []

@app.route('/')
def index():
    # Get the visitor's IP address
    visitor_ip = request.remote_addr
    if visitor_ip and ',' in visitor_ip:
        visitor_ip = visitor_ip.split(',')[0]  # Take the first IP (real visitor's IP)
    
    if visitor_ip not in ip_addresses:
        ip_addresses.append(visitor_ip)
    
    return render_template_string(html_template, ip_addresses=ip_addresses)

if __name__ == '__main__':
    app.run()
