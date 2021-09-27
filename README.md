## Python Script - Automatic Instagram image maker

A python script that works to pull images via the Unsplash API, resize it, cover it with an overlay (add a border and the name of the latest podcast episode from the feed), then save it and open a mobile-emulating browser logged into their Instagram account for easy posting.

This script was designed for use for a podcast, but with a little tweaking could easily be used for a blog or other type of website with regularly scheduled content. 

## Modules Used 

- requests
- bs4
- io
- PIL
- random
- time
- selenium

For this script to work, you first need to ensure these libraries are installed in your local python environment. You also need an Unsplash API token and an active Instagram account. Plug those values into the appropriate variables and the script should be good to go! 
