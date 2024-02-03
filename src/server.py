from http.server import HTTPServer, CGIHTTPRequestHandler

addr = ("localhost", 9999)

httpd = HTTPServer(addr, CGIHTTPRequestHandler)
print(f"=== Server was started on {addr} ===")
httpd.serve_forever()



