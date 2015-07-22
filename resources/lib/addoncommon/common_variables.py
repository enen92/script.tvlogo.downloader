# -*- coding: utf-8 -*-

""" 
   	
"""
    
import xbmc,xbmcplugin,xbmcgui,xbmcaddon,os

addon_id = 'script.tvlogo.downloader'
art = os.path.join("resources","img")
settings = xbmcaddon.Addon(id=addon_id)
addonpath = settings.getAddonInfo('path').decode('utf-8')
version = settings.getAddonInfo('version')
profilepath= xbmc.translatePath(settings.getAddonInfo('profile')).decode('utf-8')
mensagemok = xbmcgui.Dialog().ok
mensagemprogresso = xbmcgui.DialogProgress()
MainURL = 'http'
addon_icon = settings.getAddonInfo('icon')
addon_fanart = os.path.join(addonpath,'fanart.jpg')

 
def translate(text):
      return settings.getLocalizedString(text).encode('utf-8')

