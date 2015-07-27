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

from addoncommon.common_variables import *
from addoncommon.tvldutils import *
import thelogodb
import urllib
import json
import sys
import logowindow
import downloader
import automaticd
import postprocessing
import context

def main_menu(select=False,choose=''):
	print "[Tvlogo Downloader] Main menu"
	options = ["Automatic (All user channels)","Automatic (only user channels without logos)","Manual (Specific user channels)","Entire Packages (database)","Specific channels (database)"]
	optionsvar = ["autoall","automissing","manual","package","channel"]
	if not select: choose = xbmcgui.Dialog().select('TVLogo Downloader',options)
	
	if choose > -1 or select == True:	
		if optionsvar[choose] == "autoall":
			automaticd.automatic_downloader('all')
		elif optionsvar[choose] == "automissing":
			automaticd.automatic_downloader('missing')
		elif optionsvar[choose] == "manual":
			#get tv groups
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannelGroups", "params": {"channeltype" : "tv"}, "id": 1 }')
			decoded_data = json.loads(json_response)
			groupids = []
			grouplabels = []
			try: groups = decoded_data['result']['channelgroups']
			except:
				mensagemok('TVLogo Downloader','Live TV is not enabled in kodi or no channels are available.')
				sys.exit(0)
			for x in range(0, len(decoded_data['result']['channelgroups'])):
				#check if group has channels
				has_channels = False
				if groups[x]["channelgroupid"] > -1:
					json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groups[x]["channelgroupid"])+',"properties":["channel","channeltype","thumbnail"]}, "id": 1 }')
					channel_number = bool("channels" in json.loads(json_response)["result"])
					if channel_number: has_channels = True

				if has_channels:
					groupids.append(groups[x]["channelgroupid"])
					grouplabels.append('TV: ' + groups[x]["label"])
			#get radio groups		
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannelGroups", "params": {"channeltype" : "radio"}, "id": 1 }')
			decoded_data = json.loads(json_response)
			groups = decoded_data['result']['channelgroups']
			for x in range(0, len(decoded_data['result']['channelgroups'])):
				#check if group has channels
				has_channels = False
				if groups[x]["channelgroupid"] > -1:
					json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groups[x]["channelgroupid"])+',"properties":["channel","channeltype","thumbnail"]}, "id": 1 }')
					channel_number = bool("channels" in json.loads(json_response)["result"])
					if channel_number: has_channels = True

				if has_channels:
					groupids.append(groups[x]["channelgroupid"])
					grouplabels.append('Radio: ' + groups[x]["label"])
				choose = xbmcgui.Dialog().select('TVLogo Downloader - Channel Groups',grouplabels)
				if choose > -1:
					groupid = groupids[choose]
					json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groupid)+',"properties":["channel","channeltype","thumbnail"]}, "id": 1 }')
					decoded_data = json.loads(json_response)
					channel_list = []
					channel_labels = []
					if "channels" in decoded_data["result"].keys():
						for channel in decoded_data["result"]["channels"]:
							channel_list.append(channel["channelid"])
							channel_labels.append(channel["label"])
						if channel_list:
							choose = xbmcgui.Dialog().select('TVLogo Downloader - Channel List',channel_labels)
							if choose > -1:
								context.run(channel_labels[choose])
							else:
								main_menu()
						else:
							mensagemok('TVLogo Downloader','No channels available!')
							main_menu(select=True,choose=2)
					else:
						mensagemok('TVLogo Downloader',"Group doesn't have any channels.")
						main_menu(select=True,choose=2)
				else:
					main_menu()

		elif optionsvar[choose] == "package":
			entire_packages()
		elif optionsvar[choose] == "channel":
			specific_channels()
			
			
def specific_channels():
	options = ["By Country","By Country Package","By Package","Search"]
	optionsvar = ["country","country_package","package","search"]
	choose = xbmcgui.Dialog().select('TVLogo Downloader',options)
	if choose > -1:
		if optionsvar[choose] == 'country':
			countries = thelogodb.Channels().get_countries()
			if countries:
				country_list = []
				for country in countries:
					if country["strCountry"] and country != 'None': country_list.append(country["strCountry"])
				choose = xbmcgui.Dialog().select('TVLogo Downloader',country_list)
				if choose > -1:
					channels = thelogodb.Channels().by_country(urllib.quote(country_list[choose]))
					if channels:
						logowindow.start(channels,"True","True")
						specific_channels()
					else:
						mensagemok('TVLogo Downloader','No channels with logos in thelogodb!')
						specific_channels()
				else:
					specific_channels()
			else:
				specific_channels()
			
		elif optionsvar[choose] == 'country_package':
			country_list = []
			packages = thelogodb.Packages().get_all()
			if packages:
				for package in packages:
					country = package["strCountry"]
					if country and country != 'None' and country not in country_list: country_list.append(country)
				if country_list:
					country_list = sorted(country_list)
					choose = xbmcgui.Dialog().select('TVLogo Downloader',country_list)
					if choose > -1:
						country = country_list[choose]
						packages = thelogodb.Packages().get_all()
						package_list = []
						package_id_list = []
						if packages:
							for package in packages:
								if package["strCountry"] == country:
									package_label = '['+ str(package['strCountry']) +'] '+ package['strPackage'] + ' ('+str(package['strType'])+')'
									package_id = package['idPackage']
									package_list.append(package_label)
									package_id_list.append(package_id)
							if package_list:
								choose = xbmcgui.Dialog().select('TVLogo Downloader',package_list)
								if choose > -1:
									channels = thelogodb.Channels().by_package(package_id_list[choose])
									channels_have_logos = False
									for channel in channels:
										if channel["strLogoWide"]: channels_have_logos = True
									if channels and channels_have_logos:
										logowindow.start(channels,"True","True")
										specific_channels()
									else:
										mensagemok('TVLogo Downloader','No logos available for this package!')
										specific_channels()
								else:
									entire_packages()
					else:
						mensagemok('TVLogo Downloader','No packages available!')
						entire_packages()
				else:
					mensagemok('TVLogo Downloader','Error getting packages!')
					entire_packages()
			else:
				mensagemok('TVLogo Downloader','No packages available!')
				entire_packages()
		elif optionsvar[choose] == 'package':
			packages = thelogodb.Packages().get_all()
			package_list = []
			package_id_list = []
			if packages:
				for package in packages:
					package_label = '['+ str(package['strCountry']) +'] '+ package['strPackage'] + ' ('+str(package['strType'])+')'
					package_id = package['idPackage']
					package_list.append(package_label)
					package_id_list.append(package_id)
				if package_list:
					choose = xbmcgui.Dialog().select('TVLogo Downloader',package_list)
					if choose > -1:
						channels = thelogodb.Channels().by_package(package_id_list[choose])
						if channels:
							logowindow.start(channels,"True","True")
							specific_channels()
						else:
							mensagemok('TVLogo Downloader','No logos available for this package!')
							specific_channels()
					else:
						entire_packages()
			else:
				mensagemok('TVLogo Downloader','Error getting packages!')
				entire_packages()

		elif optionsvar[choose] == 'search':
			keyb = xbmc.Keyboard('', 'Enter channel')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search_parameter = urllib.quote_plus(keyb.getText())
				if search_parameter:
					channels = thelogodb.Channels().by_keyword(search_parameter)
					if channels:
						logowindow.start(channels,"True","True")
					else:
						mensagemok('TVLogo Downloader','No packages available!')
						specific_channels()
				else:
					specific_channels()
	else:
		main_menu()
		
def entire_packages():
	options = ["All Packages","Packages by Region","Packages by Country"]
	optionsvar = ["all","region","country"]
	choose = xbmcgui.Dialog().select('TVLogo Downloader',options)
	if choose > -1:
		if optionsvar[choose] == 'all':
			packages = thelogodb.Packages().get_all()
			package_list = []
			package_id_list = []
			if packages:
				for package in packages:
					package_label = '['+ str(package['strCountry']) +'] '+ package['strPackage'] + ' ('+str(package['strType'])+')'
					package_id = package['idPackage']
					package_list.append(package_label)
					package_id_list.append(package_id)
				if package_list:
					choose = xbmcgui.Dialog().select('TVLogo Downloader',package_list)
					if choose > -1:
						downloader.download_entire_package(str(package_id_list[choose]))
						main_menu()
					else:
						entire_packages()
			else:
				mensagemok('TVLogo Downloader','Error getting packages!')
				entire_packages()
				
		elif optionsvar[choose] == 'region':
			options = ["Europe","America","Africa","Asia","Oceania"]
			optionsvar = ["Europe","America","Africa","Asia","Oceania"]
			choose = xbmcgui.Dialog().select('TVLogo Downloader',options)
			if choose > -1:
				packages = thelogodb.Packages().by_country(urllib.quote_plus(optionsvar[choose]))
				package_list = []
				package_id_list = []
				if packages:
					for package in packages:
						package_label = '['+ str(package['strCountry']) +'] '+ package['strPackage'] + ' ('+str(package['strType'])+')'
						package_id = package['idPackage']
						package_list.append(package_label)
						package_id_list.append(package_id)
					if package_list:
						choose = xbmcgui.Dialog().select('TVLogo Downloader',package_list)
						if choose > -1:
							downloader.download_entire_package(str(package_id_list[choose]))
							main_menu()
						else:
							entire_packages()
				else:
					mensagemok('TVLogo Downloader','No packages available!')
					entire_packages()
			else:
				entire_packages()

		elif optionsvar[choose] == 'country':
			country_list = []
			packages = thelogodb.Packages().get_all()
			if packages:
				for package in packages:
					country = package["strCountry"]
					if country and country != 'None' and country not in country_list: country_list.append(country)
				if country_list:
					country_list = sorted(country_list)
					choose = xbmcgui.Dialog().select('TVLogo Downloader',country_list)
					if choose > -1:
						country = country_list[choose]
						packages = thelogodb.Packages().get_all()
						package_list = []
						package_id_list = []
						if packages:
							for package in packages:
								if package["strCountry"] == country:
									package_label = '['+ str(package['strCountry']) +'] '+ package['strPackage'] + ' ('+str(package['strType'])+')'
									package_id = package['idPackage']
									package_list.append(package_label)
									package_id_list.append(package_id)
							if package_list:
								choose = xbmcgui.Dialog().select('TVLogo Downloader',package_list)
								if choose > -1:
									downloader.download_entire_package(str(package_id_list[choose]))
									main_menu()
								else:
									entire_packages()
					else:
						mensagemok('TVLogo Downloader','No packages available!')
						entire_packages()
				else:
					mensagemok('TVLogo Downloader','Error getting packages!')
					entire_packages()
			else:
				mensagemok('TVLogo Downloader','No packages available!')
				entire_packages()
	else:
		main_menu()
	
def get_nonhd_match(channel):
	#check if non-hd logo is available if no match is found
	if settings.getSetting('search_nonhd') == 'true' and ' hd' in urllib.unquote_plus(channel).lower():
		temp = urllib.unquote_plus(channel.lower())
		if ' hd ' in temp: newchannel = urllib.quote_plus(urllib.unquote_plus(channel.lower().replace(' hd','')))
		elif ' hd ' not in temp and ' hd' in temp: newchannel = urllib.quote_plus(urllib.unquote_plus(channel.lower()).replace(' hd',''))
		else: newchannel = urllib.quote_plus(urllib.unquote_plus(channel.lower()).replace('hd',''))
		match = thelogodb.Channels().by_keyword(newchannel)
		return match
	else:
		return []
