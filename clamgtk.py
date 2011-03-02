#!/usr/bin/env python2
#encoding:utf8
import os,gtk,pyclamd
import webkit,json
from urllib import quote, unquote

class ClamGtk():
	clamdsocket = '/var/lib/clamav/clamd.sock'
	functions = locals()
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('clamgtk.ui')
		self.builder.connect_signals(self)
		self.about = self.builder.get_object('about')
		self.webview = webkit.WebView()
		self.scrolledwindow = self.builder.get_object('scrolledwindow')
		self.scrolledwindow.add(self.webview)
		self.webview.show_all()
		self.webview.load_uri('file:///home/http/demo/clamgtk/demo_ui/webui/index.html')
		self.webview.connect('console-message',self.console)
		self.clamd = self.connect_clamd()
		#self.webview.execute_script('get(%s,%s)' % msg,json.dumps(templist[0][0]))

	def connect_clamd(self):
		try:
			clamd = pyclamd.ClamdUnixSocket(self.clamdsocket)
		except:
			pass
		#self.status.set_text(clamd.version())
		print clamd.version()
		return clamd

	def scan_file(self,widget):
		choose_file = gtk.FileChooserDialog(title='Choose File for scan... ',
			parent=None,
			action=gtk.FILE_CHOOSER_ACTION_OPEN,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		response = choose_file.run()
		if response == gtk.RESPONSE_OK:
			filename = choose_file.get_filename()
			self.webview.execute_script("getCmd('%s')" % "FileScan Mode Start")
			#self.logbuff.insert_at_cursor('start file scan:\n')
			log = self.clamd.scan_file(filename)
			if log <> None:
				for key,value in log.items():
					#self.logbuff.insert_at_cursor(key+str(value)+'\n')
					self.webview.execute_script("getCmd('%s')" % key)
					self.webview.execute_script("getCmd('%s')" % quote(str(value)))
			else:
				self.webview.execute_script("getCmd('%s')" % "clean!")
			#self.logbuff.insert_at_cursor('END\n\n\n')
			self.webview.execute_script("getCmd('%s')" % "END")
		choose_file.hide()

	def scan_dir(self,widget):
		choose_dir = gtk.FileChooserDialog(title='Choose Dir for scan... ',
			parent=None,
			action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
			buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		response = choose_dir.run()
		if response == gtk.RESPONSE_OK:
			filename = choose_dir.get_filename()
			self.webview.execute_script("getCmd('%s')" % "DirScan Mode Start")
			choose_dir.hide()
			log = self.clamd.multiscan_file(filename)
			if log <> None:
				for key,value in log.items():
					self.webview.execute_script("getCmd('%s')" % key)
					self.webview.execute_script("getCmd('%s')" % quote(str(value)))
			self.webview.execute_script("getCmd('%s')" % "END")

	def do_quit(self,widget):
		#self.config.write(open(configfile,'w'))
		gtk.main_quit()

	def console(self,widget,content,source,line):
		try:
			content = json.loads(content)
			func = self.functions.get(content['func'],None)
			try:
				func(self,widget,content['data'])
			except KeyError:
				func(self,widget)
			#except TypeError,e:
			#	webview.execute_script('$("body").append( "%s" )'% 'unknownController')
		except:
			pass

if __name__ == '__main__':
	ClamGtk()
	gtk.main()
