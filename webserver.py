from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import socket

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

while True:
    clear()
    print("All values in parenthesis - () - are the recommendations.")
    print("Hostname is not required. Press enter to quickly set it to localhost")
    print("Type 'localip' to set to your LAN IP for external access")
    try:
        rawHost = input("Hostname (localhost):  ")
        if rawHost == "":
            hostName = "localhost"
        elif rawHost == "localip":
            hostName = get_local_ip()
            print(f"Using local IP: {hostName}")
        else:
            hostName = rawHost

        serverPort = int(input("Port (8080):  "))
        usecustomerrors = bool(input("Use HTTP errors in error/httpname.html (False):  "))
        break
    except Exception as e:
        print(f"Please enter a valid setting. Error: {e}")

clear()
script_dir = os.path.dirname(os.path.abspath(__file__)) + "\\" if os.name == "nt" else "/"
print("Script Directory:  " + script_dir)

class SERVER(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print("Trying to fetch " + script_dir + self.path)
            if self.path == "/" or self.path == "":
                self.path = "index.html"
            served_file = open(script_dir + self.path, "rb")
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            served_file_contents = served_file.read()
            self.wfile.write(served_file_contents)
        except FileNotFoundError:
            if not usecustomerrors:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                try:
                    print("( 404 ) Trying to fetch " + script_dir + self.path)
                    served_file = open(script_dir + "error"+ "\\" if os.name == "nt" else "/"+ "404.html", "rb")
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    served_file_contents = served_file.read()
                    self.wfile.write(served_file_contents)
                except FileNotFoundError:
                    self.send_response(404)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
        except PermissionError:
            if not usecustomerrors:
                self.send_response(403)
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                try:
                    print("( 403 ) Trying to fetch " + script_dir + self.path)
                    served_file = open(script_dir + "error"+ "\\" if os.name == "nt" else "/"+ "403.html", "rb")
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    served_file_contents = served_file.read()
                    self.wfile.write(served_file_contents)
                except FileNotFoundError:
                    self.send_response(403)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

webServer = HTTPServer((hostName, serverPort), SERVER)
print("Server started http://%s:%s" % (hostName, serverPort))
try:
    webServer.serve_forever()
except KeyboardInterrupt:
    webServer.server_close()
    print("Server stopped.")

    clear()
