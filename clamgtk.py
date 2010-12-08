import os,gtk,pyclamd

class ClamGtk():
	clamdsocket = '/var/lib/clamav/clamd.sock'
	def __init__(self):
		self.builder = gtk.Builder()
		self.builder.add_from_file('clamgtk.ui')
		self.builder.connect_signals(self)
		self.status = self.builder.get_object('status')
		self.about = self.builder.get_object('about')
		self.logbuff = self.builder.get_object('logbuff')
		self.clamd = self.connect_clamd()

	def connect_clamd(self):
		try:
			clamd = pyclamd.ClamdUnixSocket(self.clamdsocket)
		except:
			pass
		self.status.set_text(clamd.version())
		print clamd.version()
		return clamd

	def show_about(self,widget):
		self.about.run()
		self.about.hide()

	def scan_file(self,widget):
		self.choose_file = self.builder.get_object('choose_file')
		response = self.choose_file.run()
		if response == gtk.RESPONSE_OK:
			filename = self.choose_file.get_filename()
			self.logbuff.insert_at_cursor('start file scan:\n')
			log = self.clamd.scan_file(filename)
			if log <> None:
				for key,value in log.items():
					self.logbuff.insert_at_cursor(key+str(value)+'\n')
			self.logbuff.insert_at_cursor('END\n\n\n')
		self.choose_file.hide()

	def scan_dir(self,widget):
		self.choose_dir = self.builder.get_object('choose_dir')
		response = self.choose_dir.run()
		if response == gtk.RESPONSE_OK:
			filename = self.choose_dir.get_filename()
			self.logbuff.insert_at_cursor('start dir scan:\n')
			log = self.clamd.multiscan_file(filename)
			if log <> None:
				for key,value in log.items():
					print key,value
					self.logbuff.insert_at_cursor(key+str(value)+'\n')
			self.logbuff.insert_at_cursor('END\n\n\n')
		self.choose_dir.hide()

	def do_quit(self,widget):
		#self.config.write(open(configfile,'w'))
		gtk.main_quit()

if __name__ == '__main__':
	ClamGtk()
	gtk.main()