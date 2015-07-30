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

import xbmc
import json
import os
import sys
import urllib
import thelogodb
import logowindow
import const
import difflib
import downloader
import tvlogodownloader
import postprocessing
from addoncommon.common_variables import *
from addoncommon.tvldutils import *

def automatic_downloader(mode):
	dp = xbmcgui.DialogProgress()
	dp.create('TVLogo Downloader')
	dp.update(0,'Getting user channels')
	failed_log = []
	#grab all user channel groups
	#TV
	groupids = []
	ch_ids = []
	ch_names = []
	
	
	json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannelGroups", "params": {"channeltype" : "tv"}, "id": 1 }')
	decoded_data = json.loads(json_response)
	try: 
		groups = decoded_data['result']['channelgroups']
	except:
		mensagemok('TVLogo Downloader','Live TV is not enabled in kodi or no channels are available.')
		sys.exit(0)
	for x in range(0, len(decoded_data['result']['channelgroups'])):
		has_channels = False
		if groups[x]["channelgroupid"] > -1:
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groups[x]["channelgroupid"])+',"properties":["channel","channeltype","thumbnail","broadcastnow","broadcastnext"]}, "id": 1 }')
			channel_number = bool("channels" in json.loads(json_response)["result"])
			if channel_number: has_channels = True
		if has_channels:
			groupids.append(groups[x]["channelgroupid"])
	
	#Radio
	json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannelGroups", "params": {"channeltype" : "radio"}, "id": 1 }')
	decoded_data = json.loads(json_response)
	groups = decoded_data['result']['channelgroups']
	for x in range(0, len(decoded_data['result']['channelgroups'])):
	#check if group has channels
		has_channels = False
		if groups[x]["channelgroupid"] > -1:
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groups[x]["channelgroupid"])+',"properties":["channel","channeltype","thumbnail","broadcastnow","broadcastnext"]}, "id": 1 }')
			channel_number = bool("channels" in json.loads(json_response)["result"])
			if channel_number: has_channels = True
		if has_channels:
			groupids.append(groups[x]["channelgroupid"])
			
	#grab every channel name and label
	if groupids:
		for groupid in groupids:
			json_response = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid" : '+str(groupid)+',"properties":["channel","channeltype","thumbnail"]}, "id": 1 }')
			decoded_data = json.loads(json_response)
			if "channels" in decoded_data["result"].keys():
				for channel in decoded_data["result"]["channels"]:
					if mode == 'all':
						if channel["label"] not in ch_names:
							ch_ids.append(channel["channelid"])
							ch_names.append(channel["label"])
					else:
						json_response = xbmc.executeJSONRPC('{"jsonrpc":"2.0","method":"Settings.GetSettingValue","params":{"setting":"pvrmenu.iconpath"},"id":9}')
						decoded_data = json.loads(json_response)
						logo_folder = decoded_data['result']['value']
						logofile = os.path.join(logo_folder,channel["label"].replace('/','_')+'.png')
						if channel["label"] not in ch_names and channel['thumbnail'].replace('image://','') != (logo_folder + channel["label"].replace(' ','%20')+'.png').replace('/','%2f') + '/' and not os.path.exists(logofile): 
							ch_ids.append(channel["channelid"])
							ch_names.append(channel["label"])
	if ch_names:
		download_list = []
		initconst = const.Constr().restart_process()
		totalchannels = len(ch_names)
		
		i=1
		iscanceled = False
		for channel in ch_names:
			dp.update(int(i/float(totalchannels)),'Processing channel '+channel)
			if not dp.iscanceled():
				match = thelogodb.Channels().by_keyword(urllib.quote_plus(get_replaced_names(channel.encode('utf-8'))))
				if match:
					match = return_only_valid(match)
					if not match:
						if ' hq' in channel.encode('utf-8').lower():
							match = tvlogodownloader.get_nonhd_match(get_replaced_names(channel.encode('utf-8').lower().replace('hq',' hd')))
							match = return_only_valid(match)
						if not match:
							match = tvlogodownloader.get_nonhd_match(get_replaced_names(channel.encode('utf-8')))
							match = return_only_valid(match)
							if not match:
								#check if nonascii version exists
								match = thelogodb.Channels().by_keyword(urllib.quote_plus(removeNonAscii(get_replaced_names(channel))))
								match = return_only_valid(match)
								#if no match check if channel is HD and grab logos for nonhd
								if not match:
									match = tvlogodownloader.get_nonhd_match(removeNonAscii(get_replaced_names(channel)))
									match = return_only_valid(match)
				else:
					if ' hq' in channel.encode('utf-8').lower():
						match = tvlogodownloader.get_nonhd_match(get_replaced_names(channel.encode('utf-8').lower().replace('hq',' hd')))
						match = return_only_valid(match)
					if not match:
						match = tvlogodownloader.get_nonhd_match(get_replaced_names(channel.encode('utf-8')))
						match = return_only_valid(match)
						if not match:
							#check if nonascii version exists
							match = thelogodb.Channels().by_keyword(urllib.quote_plus(removeNonAscii(get_replaced_names(channel))))
							match = return_only_valid(match)
							#if no match check if channel is HD and grab logos for nonhd
							if not match:
								match = tvlogodownloader.get_nonhd_match(removeNonAscii(get_replaced_names(channel)))
								match = return_only_valid(match)
				
				if not match:
					if channel not in failed_log:
						failed_log.append(channel)
				if match:
					if len(match) == 1:
						obj = {'channel_name': match[0]["strChannel"],'channel_logo': match[0]["strLogoWide"],'selected_channel':channel}
						const.Constr().add_to_array(obj)
					else:
						#manipulations
						seqmatch = {}
						for canal in match:
							try:print canal["strChannel"].lower(),channel.lower()
							except: pass
							ratio = int(difflib.SequenceMatcher(None, canal["strChannel"].lower(),channel.lower()).ratio()*100)
							seqmatch[ratio] = canal
						
						already = False
						
						if settings.getSetting('auto_if_100') == 'true':
							if max(seqmatch.keys()) == 100: 
								already = True
								obj = {'channel_name': seqmatch[max(seqmatch.keys())]["strChannel"],'channel_logo': seqmatch[max(seqmatch.keys())]["strLogoWide"],'selected_channel':channel}
								const.Constr().add_to_array(obj)
						if settings.getSetting('auto_if_multiple') == 'true' and not already:
							if max(seqmatch.keys()) >= int(settings.getSetting("minimum_ratio")):
								already = True
								obj = {'channel_name': seqmatch[max(seqmatch.keys())]["strChannel"],'channel_logo': seqmatch[max(seqmatch.keys())]["strLogoWide"],'selected_channel':channel}
								const.Constr().add_to_array(obj)
						
						if not already:
							xbmc.sleep(3000)
							before = const.Constr().return_array()
							logowindow.start(match,"False","False",selected_channel=channel)
							now = const.Constr().return_array()
							if before == now:
								if channel not in failed_log:
									failed_log.append(channel)
							del before
							del now
				else:
					if channel not in failed_log:
						failed_log.append(channel)
				i +=1
			else:
				iscanceled = True
				dp.close()
		if not iscanceled:
			dp.update(100)
			dp.close()
			logos_to_download = const.Constr().return_array()
			downloader.Downloader(logos_to_download,True,failed_log)
			postprocessing.run()
			tvlogodownloader.main_menu(select=False,choose='')
			
