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

def channel_to_downloaddict(channel,rename_to=None):
	if not rename_to: channel_dict = {'channel_name': channel["strChannel"] ,'channel_logo': channel["strLogoWide"]}
	else: channel_dict = {'channel_name': channel["strChannel"] ,'channel_logo': channel["strLogoWide"],'selected_channel':rename_to}
	return channel_dict
	
def removeNonAscii(s): return "".join(filter(lambda x: ord(x)<128, s))
