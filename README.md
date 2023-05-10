# OBS Adapter for WebNowPlaying-Redux
A OBS script to display information from [WebNowPlaying-Redux](https://github.com/keifufu/WebNowPlaying-Redux)  
It also supports a lot of desktop players! Read more [here](https://github.com/keifufu/WebNowPlaying-Redux/blob/main/NativeAPIs.md).

![widgets](./images/widgets.jpg)

This script adds widgets as seen above, it also lets you add a formatted text source like "{artist} - {title}", and individual sources for Title, Artist, etc. so you can do whatever you want!

You can modify the text sources however you want, the script will only update the text.  
If you delete a source, it will stay deleted until you click "Create Sources" again.

# Installing
### Adding python to OBS
- Install Python 3.10 ([download link](https://www.python.org/downloads/release/python-31010/)), make sure to check 'Add python.exe to PATH'
- In OBS, go to Tools -> Scripts -> Python Settings, and add your Python path.  
  (On windows, run `where python` to see where it installed)
### Installing the script
- Open cmd and run `pip install pywnp`
- Download wnp-obs.py from [Releases](https://github.com/keifufu/WebNowPlaying-Redux-OBS/releases/latest), then add it in the Scripts tab.
- Select a Widget or click "Create Sources" in the Scripts window.

# Updating
- Replace wnp-obs.py with the latest wnp-obs.py from [Releases](https://github.com/keifufu/WebNowPlaying-Redux-OBS/releases/latest)
- Open cmd and run `pip install --upgrade pywnp`

# Known Issues
- Reloading the script might cause it to spam errors or not work at all.  
If you need to reload it for some reason, restart OBS.  
If you DID reload the script and it doesn't work anymore even after restarting OBS, restart your computer.