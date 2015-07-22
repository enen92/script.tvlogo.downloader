# -*- coding: utf-8 -*-
# Copyright (C) 2015 enen92
#
# This program is free software; you can redistribute it and/or modify it under the terms 
# of the GNU General Public License as published by the Free Software Foundation; 
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program; 
# if not, see <http://www.gnu.org/licenses/>.

import xbmc,xbmcgui,xbmcaddon,xbmcplugin
import const
from downloader import *

def start(data_list,multiselect,proceed_to_download,selected_channel="False"):
	options = [multiselect,proceed_to_download]
	window = dialog_channels('DialogSelect.xml',str(data_list),str(options),selected_channel)
	window.doModal()
	
class dialog_log(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.log = args[1]
	
	def onInit(self):
		self.getControl(1).setLabel('TVLogo Downloader')
		self.getControl(5).setText(self.log)
		
		
class dialog_channels(xbmcgui.WindowXMLDialog):
	def __init__( self, *args, **kwargs ):
		xbmcgui.WindowXML.__init__(self)
		self.channels = eval(args[1])
		self.options = eval(args[2])
		self.multiselect = eval(self.options[0])
		self.proceed_to_download = eval(self.options[1])
		self.selected_channel = args[3]


	def onInit(self):
		if self.multiselect:
			self.getControl(1).setLabel('TVLogo Downloader - Select your channels')
		else:
			self.getControl(1).setLabel('TVLogo Downloader - Select the channel')
		self.getControl(3).setVisible(False)
		if self.channels:
			#order channels (if not looking for specific channels)
			if self.multiselect:
				channel_name_list = []
				for channel in self.channels:
					channel_name_list.append(channel["strChannel"])
				if channel_name_list:	
					channels = []
					for channel_ in sorted(channel_name_list):
						for channel in self.channels:
							if channel["strChannel"] == channel_:
								channels.append(channel)
								self.channels.remove(channel)
								break
				
				self.channels = channels
				del channels					

			for channel in self.channels:
				if channel["strLogoWide"]:
					channelitem = xbmcgui.ListItem(channel["strChannel"], iconImage = channel["strLogoWide"])
					channelitem.setProperty('Download',"false")
					channelitem.setProperty('channel_name',channel["strChannel"])
					channelitem.setProperty('channel_logo',channel["strLogoWide"])
					channelitem.setProperty('Addon.Summary',channel["strCountry"])
					self.getControl(6).addItem(channelitem)
					
		self.getControl(5).setLabel('Download Selected')
		if self.getControl(6).size() > 0:
			xbmc.sleep(100)
			self.setFocusId(6)
			self.getControl(6).selectItem(0)
			
	def onClick(self,controlId):
		if controlId == 6:
			if self.multiselect == True:
				is_selected = self.getControl(controlId).getSelectedItem().getProperty('Download')
				if is_selected == 'false':
					self.channel_name = self.getControl(controlId).getSelectedItem().getProperty('channel_name')
					self.getControl(controlId).getSelectedItem().setProperty('Download',"true")
					self.getControl(controlId).getSelectedItem().setLabel('[COLOR selected]' + self.channel_name + '[/COLOR]')
				else:
					self.channel_name = self.getControl(controlId).getSelectedItem().getProperty('channel_name')
					self.getControl(controlId).getSelectedItem().setProperty('Download',"false")
					self.getControl(controlId).getSelectedItem().setLabel(self.channel_name)
			else:
				selected_items = []
				total_items = self.getControl(6).size()
				for x in xrange(0,total_items):
					if self.getControl(6).getListItem(x).getProperty("Download") == "true":
						selected_items.append(x)
				#Remove all from selected
				if selected_items:
					for item in selected_items:
						channel_name = self.getControl(6).getListItem(item).getProperty('channel_name')
						self.getControl(6).getListItem(item).setProperty('Download','false')
						self.getControl(6).getListItem(item).setLabel(channel_name)
				#Now select the only one that matters
				channel_name = self.getControl(6).getSelectedItem().getProperty('channel_name')
				self.getControl(6).getSelectedItem().setProperty('Download','true')
				self.getControl(6).getSelectedItem().setLabel('[COLOR selected]' + channel_name + '[/COLOR]')
				
		elif controlId == 5:
			logos_to_download = []
			if self.multiselect:
				total_items = self.getControl(6).size()
				for x in xrange(0,total_items):
					if self.getControl(6).getListItem(x).getProperty("Download") == "true":
						logos_to_download.append({'channel_name': self.getControl(6).getListItem(x).getProperty("channel_name"),'channel_logo': self.getControl(6).getListItem(x).getProperty("channel_logo")})
				if logos_to_download:
					self.close()
					if self.proceed_to_download:
						Downloader(logos_to_download,False)
					else:
						if logos_to_download:
							for logo in logos_to_download:
								const.Constr().add_to_array(logo)
				else:
					mensagemok('TVLogo Downloader',"You haven't selected any channels")
			else:
				total_items = self.getControl(6).size()
				for x in xrange(0,total_items):
					if self.getControl(6).getListItem(x).getProperty("Download") == "true":
						logos_to_download.append({'channel_name': self.getControl(6).getListItem(x).getProperty("channel_name"),'channel_logo': self.getControl(6).getListItem(x).getProperty("channel_logo"),'selected_channel':self.selected_channel})
				if logos_to_download:
					self.close()
					if self.proceed_to_download:
						Downloader(logos_to_download,True)
					else:
						if logos_to_download:
							for logo in logos_to_download:
								const.Constr().add_to_array(logo)
				else:
					mensagemok('TVLogo Downloader',"You haven't selected any channels")
		
		elif controlId == 99:
			self.close()
		return
