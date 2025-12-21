from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote
import os, socket, stat

global info
info = {
    "version":  2
}
mimes = {
    # HTML
    "html": "text/html", "htm" : "text/html",

    # ZIP
    "zip" : "application/zip",

    # XML
    # Got horrendously confused
    # either text/xml or application/xml
    # going with application/xml
    "xml" : "application/xml",

    # PDF
    "pdf": "application/pdf",

    # TXT
    "txt": "text/plain",

    # RealAudio / RA
    "ra": "vnd.rn-realaudio", "ram": "vnd.rn-realaudio",

    # Windows Media Audio / WMA
    "wma": "audio/x-ms-wma",

    # Wave files
    "wav": "audio/x-wav", "wave": "audio/x-wav",

    # MPEG (Audio)
    "mpg": "audio/mpeg","mpeg": "audio/mpeg","m2p": "audio/mpeg","ps": "audio/mpeg",

    # MPEG (Video)
    "mpg": "video/mpeg","mpeg":"video/mpeg","m2p":"video/mpeg","ps": "video/mpeg",

    # GIF
    "gif": "image/gif",

    # JPEG
    "jpg": "image/jpeg", "jpeg": "image/jpeg", "jpe": "image/jpeg", "jif": "image/jpeg", "jfif": "image/jpeg", "jfi": "image/jpeg",

    # PNG
    "png": "image/png",

    # TIFF
    "tif": "image/tiff", "tiff": "image/tiff",

    # ICO
    # vnd.microsoft.icon / x-icon
    # Got confused, ill just use X-icon. Adjust if disagree.
    # https://stackoverflow.com/questions/13827325/correct-mime-type-for-favicon-ico

    #"ico": "image/vnd.microsoft.icon",
    "ico": "image/x-icon",

    # DJVU (wth???)
    "djv": "image/vnd.djvu", "djvu": "image/vnd.djvu",

    # SVG
    "svg": "image/svg+xml", "svgz": "image/svg+xml",

    # CSS
    "css": "text/css",

    # CSV
    "csv": "text/csv",

    # JS
    "js": "text/javascript", "mjs": "text/javascript", "cjs": "text/javascript",

    # MP4
    "mp4": "video/mp4", "m4a": "video/mp4", "m4p": "video/mp4", "m4b": "video/mp4", "m4r":"video/mp4","m4v":"video/mp4",

    # WMV
    "asf": "video/x-ms-wmv", "wmv": "video/x-ms-wmv",

    # AVI
    "avi": "video/x-msvideo",

    # Flash Video
    "flv": "video/x-flv", "fla": "video/x-flv", "f4v": "video/x-flv", "f4a":"video/x-flv", "f4b":"video/x-flv", "f4p": "video/x-flv",

    # WebM
    "webm": "video/webm",

    # APK
    "apk": "application/vnd.android.package-archive",

    # OpenDocument
    "odt": "application/vnd.oasis.opendocument.text", "ods": "application/vnd.oasis.opendocument.text", "otf": "application/vnd.oasis.opendocument.text", "odg": "application/vnd.oasis.opendocument.text", "odp": "application/vnd.oasis.opendocument.text", "odm": "application/vnd.oasis.opendocument.text", "odb": "application/vnd.oasis.opendocument.text", "odc": "application/vnd.oasis.opendocument.text", "odf": "application/vnd.oasis.opendocument.text", "otc": "application/vnd.oasis.opendocument.text", "ots": "application/vnd.oasis.opendocument.text", "ott": "application/vnd.oasis.opendocument.text", "otg": "application/vnd.oasis.opendocument.text", "oti": "application/vnd.oasis.opendocument.text", "otp": "application/vnd.oasis.opendocument.text", "oth": "application/vnd.oasis.opendocument.text", "odi": "application/vnd.oasis.opendocument.text", "fodg": "application/vnd.oasis.opendocument.text", "fodp": "application/vnd.oasis.opendocument.text", "fods": "application/vnd.oasis.opendocument.text", "fodt": "application/vnd.oasis.opendocument.text",
    # my hands hurt

    # OH GOD
    # IM NOT DOING 
    #  application/vnd.oasis.opendocument.spreadsheet  
    #  application/vnd.oasis.opendocument.presentation   
    #  application/vnd.oasis.opendocument.graphics


    # Thanks, https://stackoverflow.com/questions/4212861/what-is-a-correct-mime-type-for-docx-pptx-etc

    # Excel
    "xls": "application/vnd.ms-excel", "xlt": "application/vnd.ms-excel", "xla": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
    "xltm": "application/vnd.ms-excel.template.macroEnabled.12",
    "xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",

    # MS Access
    "mdb": "application/vnd.ms-access",

    # PowerPoint
    "ppt": "application/vnd.ms-powerpoint", "pot": "application/vnd.ms-powerpoint", "pps": "application/vnd.ms-powerpoint", "ppa": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "potx": "application/vnd.openxmlformats-officedocument.presentationml.template",
    "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow",
    "ppam": "application/vnd.ms-powerpoint.addin.macroEnabled.12", 
    "pptm": "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
    "potm": "application/vnd.ms-powerpoint.template.macroEnabled.12",
    "ppsm": "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",

    # Word
    "doc": "application/msword", "dot": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    "docm": "application/vnd.ms-word.document.macroEnabled.12",
    "dotm": "application/vnd.ms-word.template.macroEnabled.12",

    # XUL
    "xul": "application/vnd.mozilla.xul+xml"
}
def detect_http_status(file_path):
    try:
        if any(char in file_path for char in ['\0', '\r', '\n']) or not file_path or ".." in file_path: return "400"
        if not os.path.exists(file_path):                                                               return "404"
        if os.path.islink(file_path) and not os.path.exists(os.readlink(file_path)):                    return "410"
        file_stats = os.stat(file_path)
        if os.path.isdir(file_path) or not os.path.isfile(file_path) or not os.access(file_path, os.R_OK) or stat.S_ISBLK(file_stats.st_mode) or stat.S_ISCHR(file_stats.st_mode) or stat.S_ISFIFO(file_stats.st_mode): return "403"
        with open(file_path, "rb") as f: f.read(1)
            
    except FileNotFoundError:                    return "404"
    except TimeoutError:                         return "408"  
    except (PermissionError,IsADirectoryError):  return "403"
    except MemoryError:                          return "507"
    except UnicodeDecodeError:                   return "400"
    except OSError as e: 
        if e.errno == 36:                        return "414"
        elif e.errno == 28:                      return "507"  
        elif e.errno == 24:                      return "503"  
        elif e.errno == 27:                      return "413"  
        elif e.errno == 26 or e.errno == 13:     return "423" 
        else:                                    return "500"  
    except Exception:                            return "500"
    return "200"
def get_ext(filename):
    return filename[filename.rfind(".")+1:].lower() if "." in filename else ""
def localip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def clear(): os.system("cls" if os.name == "nt" else "clear")

while True:
    clear()
    print("All values in parenthesis - () - are the recommendations.")
    print("Press enter for localhost.")
    print("'localip' allows external LAN access")
    try:
        rawHost = input(":  ")
        if rawHost == "":          hostName = "localhost"
        elif rawHost == "localip": hostName = localip()
        else:                      hostName = rawHost

        clear()
        print(f"[i] Using IP: {hostName}")
        serverPort = int(input("Port (8080):  "))
        usecustomerrors = bool(input("Use HTTP errors in error/httpname.html (False):  "))
        break
    except Exception as e:
        print(f"[e] Please enter a valid setting. Error: {e}")

clear()
script_dir = os.path.dirname(os.path.abspath(__file__)) + ("\\" if os.name == "nt" else "/")
# brny tried to be here

print("[i] Script Directory:  " + script_dir)
class SERVER(BaseHTTPRequestHandler):
    def do_GET(self):
        decoded_path = unquote(self.path)
        request_path = decoded_path.lstrip("/")
        if request_path == "": request_path = "index.html"
        full_path = script_dir + request_path
        if os.path.isdir(full_path) and not decoded_path.endswith("/"):
            self.send_response(301)
            self.send_header("Location", decoded_path + "/")
            self.end_headers()
            return
        if os.path.isdir(full_path):
            request_path = request_path.rstrip("/") + "/index.html"
            full_path = script_dir + request_path

        status = detect_http_status(full_path)
        if status == "200":
            print("[$] Trying to fetch " + full_path)
            served_file = open(full_path, "rb")
            self.send_response(200)
            type = get_ext(request_path)
            if type in mimes: self.send_header("Content-type", mimes[type])
            else:             self.send_header("Content-type", "text/plain")
            self.end_headers()
            served_file_contents = served_file.read()
            self.wfile.write(served_file_contents)
            served_file.close()
        else:
            if not usecustomerrors:
                self.send_response(int(status))
                self.send_header("Content-type", "text/html")
                self.end_headers()
            else:
                try:
                    print("[$E] ( "+status+" ) :   Trying to fetch " + script_dir + self.path)
                    served_file = open(script_dir + "error" + ("\\" if os.name == "nt" else "/") + status + ".html", "rb")
                    self.send_response(int(status))
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    served_file_contents = served_file.read()
                    self.wfile.write(served_file_contents)
                except FileNotFoundError:
                    self.send_response(int(status))
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