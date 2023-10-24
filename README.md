# OBS Adapter for WebNowPlaying

A OBS script to display information from [WebNowPlaying](https://github.com/keifufu/WebNowPlaying)  
It also supports a lot of desktop players! Read more [here](https://wnp.keifufu.dev/desktop-players).

![widgets](./images/widgets.jpg)

This script adds widgets as seen above, it also lets you add a formatted text source like "{artist} - {title}", and individual sources for Title, Artist, etc. so you can do whatever you want!

You can modify the text sources however you want, the script will only update the text.  
If you delete a source, it will stay deleted until you click "Create Sources" again.

## Documentation

Full and up-to-date documentation is available at:  
https://wnp.keifufu.dev/obs/getting-started

## Adding python to OBS

- Install Python 3.10 ([link](https://www.python.org/downloads/release/python-31010/)) and sure to check "Add python.exe to PATH".
- In OBS, go to Tools -> Scripts -> Python Settings, and add the path to your Python installation.  
  (On windows, run `where python` in cmd to find the installation location.)

## Installing the script

- Open the command prompt and run `pip install pywnp`
- Download [wnp-obs.py](https://github.com/keifufu/WebNowPlaying-OBS/releases/latest/download/wnp-obs.py), then add it in the Scripts tab.
- Select a Widget or click "Create Sources" in the Scripts window.

## Updating

- Replace `wnp-obs.py` with the latest version from releases: [wnp-obs.py](https://github.com/keifufu/WebNowPlaying-OBS/releases/latest/download/wnp-obs.py).
- Open the command prompt and run `pip install --upgrade pywnp`.

## Known Issues

- Reloading the script might cause it to spam errors or not work at all.
  If you need to reload it for some reason, restart OBS.
  If you have reloaded the script and it still doesn't work after restarting OBS, try restarting your computer.
