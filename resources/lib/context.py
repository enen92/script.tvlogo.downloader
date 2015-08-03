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

import xbmc,xbmcgui
import urllib
import difflib
import const
import thelogodb
import downloader
import logowindow
import postprocessing
import tvlogodownloader
from addoncommon.common_variables import *
from addoncommon.tvldutils import *

def run(channel_name):
	channel_name = urllib.unquote(channel_name)
	menu_labels = ['Exact channel name','Custom channel name']
	menu_functions = ['auto','custom']
	initconst = const.Constr().restart_process()
	choose = xbmcgui.Dialog().select('TVLogo Downloader',menu_labels)
	if choose > -1:
		if menu_functions[choose] == 'auto':
			channel = urllib.quote_plus(get_replaced_names(channel_name))
		elif menu_functions[choose] == 'custom':
			keyb = xbmc.Keyboard('', 'Enter channel')
			keyb.doModal()
			if (keyb.isConfirmed()):
				search_parameter = urllib.quote_plus(get_replaced_names(keyb.getText()))
				if search_parameter:
					channel = search_parameter
					del search_parameter
		
		match = thelogodb.Channels().by_keyword(channel)
		if match:
			match = return_only_valid(match)
			if not match:
				#check if HQ exists and replace it by HD
				if '+hq' in channel.lower():
					match = thelogodb.Channels().by_keyword(channel.lower().replace('+hq','+hd'))
					match = return_only_valid(match)
				if not match:
					match = tvlogodownloader.get_nonhd_match(urllib.unquote_plus(channel))
					match = return_only_valid(match)
					if not match:
						#check if nonascii version exists
						match = thelogodb.Channels().by_keyword(urllib.quote_plus(removeNonAscii(urllib.unquote_plus(channel))))
						match = return_only_valid(match)
						#if no match check if channel is HD and grab logos for nonhd
						if not match:
							match = tvlogodownloader.get_nonhd_match(removeNonAscii(urllib.unquote_plus(channel)))
							match = return_only_valid(match)
		else:
			#check if HQ exists and replace it by HD
			if '+hq' in channel.lower():
				match = thelogodb.Channels().by_keyword(channel.lower().replace('+hq','+hd'))
				match = return_only_valid(match)
			if not match:
				match = tvlogodownloader.get_nonhd_match(urllib.unquote_plus(channel))
				match = return_only_valid(match)
				if not match:
					#check if nonascii version exists
					match = thelogodb.Channels().by_keyword(urllib.quote_plus(removeNonAscii(urllib.unquote_plus(channel))))
					match = return_only_valid(match)
					#if no match check if channel is HD and grab logos for nonhd
					if not match:
						match = tvlogodownloader.get_nonhd_match(removeNonAscii(urllib.unquote_plus(channel)))
						match = return_only_valid(match)

		if match:
			if len(match) == 1:
				obj = {'channel_name': match[0]["strChannel"],'channel_logo': match[0]["strLogoWide"],'selected_channel':channel_name}
				const.Constr().add_to_array(obj)
			else:
				#manipulations
				seqmatch = {}
				for canal in match:
					ratio = int(difflib.SequenceMatcher(None, canal["strChannel"].lower(),urllib.unquote_plus(channel).lower()).ratio()*100)
					seqmatch[ratio] = canal
						
				already = False
									
				if settings.getSetting('auto_if_100') == 'true':
					if max(seqmatch.keys()) == 100: 
						already = True
						obj = {'channel_name': seqmatch[max(seqmatch.keys())]["strChannel"],'channel_logo': seqmatch[max(seqmatch.keys())]["strLogoWide"],'selected_channel':channel_name}
						const.Constr().add_to_array(obj)
				if settings.getSetting('auto_if_multiple') == 'true' and not already:
					if max(seqmatch.keys()) >= int(settings.getSetting("minimum_ratio")):
						already = True
						obj = {'channel_name': seqmatch[max(seqmatch.keys())]["strChannel"],'channel_logo': seqmatch[max(seqmatch.keys())]["strLogoWide"],'selected_channel':channel_name}
						const.Constr().add_to_array(obj)
						
				if not already:
					logowindow.start(match,"False","False",selected_channel=channel_name)
		else: mensagemok('TVLogo Downloader','No channels match on the db. Try to use a custom search.')
		#download
		logos_to_download = const.Constr().return_array()
		if logos_to_download:
			downloader.Downloader(logos_to_download,True,'')
			postprocessing.run()
	return
		

