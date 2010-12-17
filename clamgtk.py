#encoding:utf8
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
		choose_file = gtk.FileChooserDialog(title='Choose File for scan... '
			,parent=None
			,action=gtk.FILE_CHOOSER_ACTION_OPEN
			,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		response = choose_file.run()
		if response == gtk.RESPONSE_OK:
			filename = choose_file.get_filename()
			self.logbuff.insert_at_cursor('start file scan:\n')
			log = self.clamd.scan_file(filename)
			if log <> None:
				for key,value in log.items():
					self.logbuff.insert_at_cursor(key+str(value)+'\n')
			self.logbuff.insert_at_cursor('END\n\n\n')
		choose_file.hide()

	def scan_dir(self,widget):
		choose_dir = gtk.FileChooserDialog(title='Choose Dir for scan... '
			,parent=None
			,action=gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER
			,buttons=(gtk.STOCK_CANCEL,gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN,gtk.RESPONSE_OK))
		response = choose_dir.run()
		if response == gtk.RESPONSE_OK:
			filename = choose_dir.get_filename()
			self.logbuff.insert_at_cursor('start dir scan:\n')
			log = self.clamd.multiscan_file(filename)
			if log <> None:
				for key,value in log.items():
					print key,value
					self.logbuff.insert_at_cursor(key+str(value)+'\n')
			self.logbuff.insert_at_cursor('END\n\n\n')
		choose_dir.hide()

	def do_quit(self,widget):
		#self.config.write(open(configfile,'w'))
		gtk.main_quit()

if __name__ == '__main__':
	ClamGtk()
	gtk.main()