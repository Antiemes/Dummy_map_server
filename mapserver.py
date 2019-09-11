#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GLib as glib
import math
from collections import deque
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs
import cgi
import threading
from time import sleep
import json

points=deque()

#python-gobject + python-cairo packages req'd

class GP(BaseHTTPRequestHandler):
  def _set_headers(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/html')
    self.end_headers()
  def do_HEAD(self):
    self._set_headers()
  def do_GET(self):
    self._set_headers()
    #print(self.path)
    #print(parse_qs(self.path[2:]))
    #print(form.getvalue("x"))
    #print(form.getvalue("y"))
    self.wfile.write("OK".encode())
  def do_POST(self):
    self._set_headers()
    #form = cgi.FieldStorage(
    #  fp=self.rfile,
    #  headers=self.headers,
    #  environ={'REQUEST_METHOD': 'POST'}
    #)
    #print(form.getvalue("x"))
    #print(form.getvalue("y"))
    #self.wfile.write("OK".encode())
    self.data_string = self.rfile.read(int(self.headers['Content-Length']))
    self.send_response(200)
    self.end_headers()
    data = json.loads(self.data_string)
    x=data["x"]
    y=data["y"]
    points.append({"x": x, "y": y})
    da.queue_draw()
    print("({}, {})". format(x, y))
  def log_message(self, format, *args):
    return


points=deque()
points.append({"x": 100, "y": 200})
points.append({"x": 150, "y": 150})
points.append({"x": 120, "y": 80})

#class PyApp(gtk.Window):
#	
#	def __init__(self):
#		super(PyApp, self).__init__()
#		
#		self.set_title("Basic shapes using Cairo")
#		self.set_size_request(400, 250)
#		self.set_position(gtk.WIN_POS_CENTER)
#			
#		self.connect("destroy", gtk.main_quit)
#  	
#		darea = gtk.DrawingArea()
#		darea.connect("expose-event", self.expose)
#  	
#		self.add(darea)
#		self.show_all()
#  

def expose(widget, cr):
	#cr = widget.window.cairo_create()

	for point in points:
		cr.set_source_rgba(1, 0.3, 0.6, 0.7)
		cr.set_line_width(1)
		cr.arc(point["x"], point["y"], 5, 0, math.pi * 2);
		cr.stroke_preserve()
		cr.set_source_rgba(0.5, 0.15, 0.3, 0.2)
		cr.fill()
 
	#print("Foo\n")
	#cr.set_line_width(2)
	#cr.set_source_rgb(0,0,1)
	#cr.rectangle(10,10,100,100)
	#cr.stroke_preserve()
	#
	#cr.set_source_rgb(1,0,0)
	#cr.rectangle(10,125,100,100)
	#cr.stroke()
	#
	#cr.set_source_rgb(0,1,0)
	#cr.rectangle(125,10,100,100)
	#cr.fill()
	#
	#cr.set_source_rgb(0.5,0.6,0.7)
	#cr.rectangle(125,125,100,100)
	#cr.fill()
	#
	#cr.arc(300, 50, 50,0, 2*math.pi)
	#cr.set_source_rgb(0.2,0.2,0.2)
	#cr.fill()
	#
	#cr.arc(300, 200, 50, math.pi,0)
	#cr.set_source_rgb(0.1,0.1,0.1)
	#cr.stroke()
	#
	#cr.move_to(50,240)
	#cr.show_text("Hello PyGTK")
	#cr.move_to(150,240)
	#cr.line_to(400,240)
	#cr.stroke()

def stdin_handler(source, cb_condition):
	[x, y]=sys.stdin.readline().rstrip().split(" ")
	points.append({"x": int(x), "y": int(y)})
	da.queue_draw()
	return 1

#server_class=HTTPServer
#handler_class=GP
#port=8088
#server_address = ('', port)
#httpd = server_class(server_address, handler_class)
#print('Server running at localhost:8088...')
#httpd.serve_forever()


server=ThreadingHTTPServer(('localhost', 8088), GP)
print('Server running at localhost:8088...')
thread=threading.Thread(target=server.serve_forever)
thread.deamon = False
thread.start()

win = gtk.Window()
win.connect("destroy", gtk.main_quit)
win.set_size_request(800, 600)
da = gtk.DrawingArea()
da.connect("draw", expose)
win.add(da)

win.show_all()

glib.io_add_watch(0, glib.IO_IN, stdin_handler)

gtk.main() 
