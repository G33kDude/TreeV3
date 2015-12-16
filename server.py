import os
import SimpleHTTPServer
import time

import ev3dev.core
ev3dev.core.LegoPort.SYSTEM_CLASS_NAME = 'lego-port'

class DSwitch:
	def __init__(self, port):
		ev3dev.core.LegoPort(port).mode = 'led'
		time.sleep(1)
		self.led = ev3dev.core.Led(name=port+'::ev3dev')
	def on(self):
		self.led.brightness = self.led.max_brightness
	def off(self):
		self.led.brightness = 0

class TreeV3Handler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_POST(self):
		global dswitch
		action = self.path.split('/')[-1]
		if action == 'on':
			dswitch.on()
		elif action == 'off':
			dswitch.off()
		self.send_response(200)

def treev3(handler_class, dswitch_port, server_path='.', server_port=8080,
		server_class=SimpleHTTPServer.BaseHTTPServer.HTTPServer):
	global dswitch
	dswitch = DSwitch(dswitch_port)
	os.chdir(server_path)
	httpd = server_class(('', server_port), handler_class)
	print("Running on port {}".format(server_port))
	httpd.serve_forever()

if __name__ == '__main__':
	treev3(TreeV3Handler, 'outD', './www')
