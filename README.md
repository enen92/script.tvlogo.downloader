# script.tvlogo.downloader

![](http://s27.postimg.org/v17g2o0oz/icon.png)

What is it?
----------
TVLogo Downloader is a Kodi program addon to help you find, download and set logos for your TV or Radio stations. It uses thelogodb.com as the source for logos.

Features
----------
* Download entire logo packages by country or by package name (cable, satelite, IPTV).
* Download and choose specific channel logos from a given package.
* Download and map specific logos to your configured pvr stations.
* Automatically download and map logos for all your tv stations at once.
* Download logos for pvr channels from the context menu of the channel list window or tvguide (you need the context menu addon -> https://github.com/enen92/context.tvlogo.downloader). This feature is available only for Kodi versions higher than v15.

How does it work
----------
TVLogo Downloader automatically sets the channel icons folder to the same folder the user defines in the addon settings. It tries to match each channel with the channels (that have logos) on the database. If a match is found, the logo is downloaded and the pvr is "refreshed" so the logos can be shown.
In Kodi 16+ this is achieved by triggering `PVR.SearchMissingChannelIcons`. In Kodi versions lower than v16, the pvr manager is restarted.
To improve the precision of the match the addon checks also if the channel is HD and a logo for the corresponding non-HD channel exists on the database and it checks also for the name of the channel after removing ascii characters. You can define a minimum similarity ratio to assume the channels match. Be aware that using low values for this ratio can cause certain channels to have a bad match, specially those that only differ on a single letter or number.
You can also define a set of words to be ignored/replaced from your channel names.

Showcase
----------
https://www.youtube.com/watch?v=mP4F2T7P-3o&feature=youtu.be

[![TheLogoDownloader showcase](http://s14.postimg.org/3q6k1jlch/thelogooooo.png)](https://www.youtube.com/watch?v=mP4F2T7P-3o&feature=youtu.be)

Download
----------
script.tvlogo.downloader: [Beta version!](https://github.com/enen92/script.tvlogo.downloader/releases/tag/0.0.11beta)

context.tvlogo.downloader: [Beta version!](https://github.com/enen92/context.tvlogo.downloader/releases/tag/0.0.5-beta)

License
----------
GNU GENERAL PUBLIC LICENSE. Version 2, June 1991

Donate
----------
Thelogodb has costs. To assure the future of the site please donate to thelogodb.com:

[![screenshot1](http://www.thelogodb.com/images/icons/paypal.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=ZYFYNBF3WFS94)


