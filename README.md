# OBS Adapter for WebNowPlaying-Redux
A OBS script to display information from [WebNowPlaying-Redux](https://github.com/keifufu/WebNowPlaying-Redux)

This scripts adds sources for:
- Player
- Title
- Artist
- Album
- Duration
- Position
- Cover Art
- A custom format like "{artist} - {title} ({position}/{duration})"

You can modify these sources however you want, the script will only update the text.  
If you delete a source, it will stay deleted until you click "Create Sources" again.

# Installing
### Adding python to OBS
- Install Python 3.10 ([download link](https://www.python.org/downloads/release/python-31010/)), make sure to check 'Add python.exe to PATH'
- In OBS, go to Tools -> Scripts -> Python Settings, and add your Python path.  
  (On windows, run `where python` to see where it installed)
### Installing the script
- Open cmd and run `pip install pywnp`
- Download wnp-obs.py from [Releases](https://github.com/keifufu/WebNowPlaying-Redux-OBS/releases/latest), then add it in the Scripts tab.
- Click "Create Sources" in the Scripts window.

# Updating
- Replace wnp-obs.py with the latest wnp-obs.py from [Releases](https://github.com/keifufu/WebNowPlaying-Redux-OBS/releases/latest)
- Open cmd and run `pip install --upgrade pywnp`