from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.listview import ListView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconLayout, FileChooser
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.dropdown import DropDown
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
import kivy.uix.recycleboxlayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.config import ConfigParser
from kivy.uix.settings import Settings
from kivy.uix.checkbox import CheckBox
from os.path import basename
import os.path


Builder.load_file("./kv/gui.kv")
Builder.load_file("./kv/runScreen.kv")
Builder.load_file("./kv/fileBrowser.kv")

'''
	0 --> Philips Lights
	1 --> MIDI Notes
	2 --> 3rd Interface
'''
interface = 0

''' Philips Hue Light Bulbs Interface variables '''
num_outputs = 1
detect_comps = False

'''
	MIDI notes
	VARIABLES GO HERE
'''

'''
	3rd interface
	VARIABLES GO HERE
'''

class SetupScreen(Screen):
	selected = ""

	def insert_rv(self, value):
		size = len(self.rv.data)
		self.rv.data.insert(size, {'basename': basename(value), 'pathname': value})


	def checkPathname(self, pathname, fileError):
		if os.path.isfile(pathname.text) and (pathname.text).endswith(".wav"):
			fileError.color = 1, 0, 0, 0
			self.insert_rv(pathname.text)
			pathname.text = ""
		else:
			fileError.color = 1, 0, 0, 1

		return

	def update_rv(self):
		global fc_selection
		for i in fc_selection:
			self.insert_rv(i)
		fc_selection = []

	def run(self, selection, configs):
		global interface
		global num_outputs
		global detect_comps
		global playlist

		# Create list of pathnames of audio files
		for i in self.rv.data:
			playlist.append(i['pathname'])

		if selection == "Philips Hue Lights":

			interface = 0
			num_outputs = int(self.ids.num_outputs.text)
			if self.ids.comps.state == "down":
				detect_comps = True
			else:
				detect_comps = False

			'''
				Call correct method from Haydn's API.
			'''

		elif selection == "MIDI Notes":

			interface = 1
			'''
				Break down what user setup
				inside MIDI configurations,
				and call correct mathod.
			'''

		elif selection == "Interface 3":

			interface = 2
			'''
				Break down what user setup
				inside 3rd configurations,
				and call correct method.
			'''

		#for debugging
		print(playlist)
		print(interface)
		print(num_outputs)
		print(detect_comps)

		#need to empty this global every time
		playlist = []

	pass

class RunScreen(Screen):
	pass

class FileBrowserScreen(Screen):
	def load(self, fileList):
		global fc_selection
		for pathname in fileList:
			fc_selection.append(pathname)

	pass

playlist = []
fc_selection = []

class MainApp(App):
	def build(self):
		Window.clearcolor = (0.16, 0.17, 0.20, 0.1)
		screen_manager = ScreenManager()
		screen_manager.add_widget(SetupScreen(name="setup"))
		screen_manager.add_widget(RunScreen(name="running"))
		screen_manager.add_widget(FileBrowserScreen(name="fileBrowser"))
		return screen_manager

if __name__ == "__main__":
	app = MainApp()
	app.run()
