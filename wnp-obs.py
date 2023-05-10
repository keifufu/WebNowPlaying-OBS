from threading import Thread
import urllib.request, json
from pywnp import WNPRedux
import obspython as obs
import time

# WNP Variables
player_name = 'N/A'
title  = 'N/A'
artist = 'N/A'
album = 'N/A'
duration = '0:00'
position = '0:00'
position_percent = '0'
cover_url = ''

# Script Settings
selected_widget = 'None'
widgets_manifest = None
default_cover_url = ''
custom_format = '{title} - {artist} ({position}/{duration})    '

fallback_default_cover_url = 'https://raw.githubusercontent.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/images/nocover.png'
custom_css = r'body { background-color: rgba(0, 0, 0, 0); margin: 0px auto; overflow: hidden; } '
custom_css += r':root { --default-cover-url: url("{default_cover_url}"); }'

def script_description():
  description = '<b>WebNowPlaying for OBS</b>'
  description += '<br>'
  description += 'Available placeholders:'
  description += '<br>'
  description += '{player_name}, {title}, {artist}, {album}, {duration}, {position}, {position_percent}'
  return description

def script_defaults(settings):
  obs.obs_data_set_default_string(settings, 'custom_format', custom_format)
  obs.obs_data_set_default_string(settings, 'default_cover_url', default_cover_url)

def script_properties():
  props = obs.obs_properties_create()

  list = obs.obs_properties_add_list(props, 'selected_widget', 'Widget', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  obs.obs_property_list_add_string(list, 'None', 'None')
  req = urllib.request.Request('https://raw.githubusercontent.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/manifest.json', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0'})
  with urllib.request.urlopen(req) as url:
    data = json.loads(url.read().decode())
    global widgets_manifest
    widgets_manifest = data
    for widget in data:
      obs.obs_property_list_add_string(list, widget['name'], widget['name'])

  obs.obs_properties_add_text(props, 'custom_format', 'Format', obs.OBS_TEXT_DEFAULT)
  obs.obs_properties_add_button(props, 'cs', 'Create Sources', create_sources)
  obs.obs_properties_add_text(props, 'default_cover_url', 'Default Cover URL', obs.OBS_TEXT_DEFAULT)
  
  return props

def script_update(settings):
  global custom_format, default_cover_url, selected_widget
  selected_widget = obs.obs_data_get_string(settings, 'selected_widget')
  custom_format = obs.obs_data_get_string(settings, 'custom_format')
  default_cover_url = obs.obs_data_get_string(settings, 'default_cover_url')
  update_widget()

def script_load(settings):
  def logger(type, message):
    print(f'WNP - {type}: {message}')
  print('load')
  WNPRedux.start(6534, '2.0.0', logger)
  obs.timer_add(update, 250)

def script_unload():
  Thread(target=WNPRedux.stop).start()
  time.sleep(1) # sorry but this at least prevents reloading the script breaking it
  obs.timer_remove(update)

def update():
  if WNPRedux.is_started:
    global player_name, title, artist, album, duration, position, position_percent, cover_url
    player_name = WNPRedux.media_info.player_name or 'N/A'
    title = WNPRedux.media_info.title or 'N/A'
    artist = WNPRedux.media_info.artist or 'N/A'
    album = WNPRedux.media_info.album or 'N/A'
    duration = WNPRedux.media_info.duration
    position = WNPRedux.media_info.position
    position_percent = str(int(WNPRedux.media_info.position_percent))
    cover_url = WNPRedux.media_info.cover_url
    update_source('Player', 'text', player_name)
    update_source('Title', 'text', title)
    update_source('Artist', 'text', artist)
    update_source('Album', 'text', album)
    update_source('Duration', 'text', duration)
    update_source('Position', 'text', position)
    update_source('Cover', 'url', cover_url or default_cover_url or fallback_default_cover_url)
    try:
      update_source('Formatted', 'text', custom_format.format(player_name=player_name, title=title, artist=artist, album=album, duration=duration, position=position, positionPercent=position_percent))
    except:
      pass

def create_sources(props, prop):
  create_text_source('WNP-PlayerName', 'N/A')
  create_text_source('WNP-Title', 'N/A')
  create_text_source('WNP-Artist', 'N/A')
  create_text_source('WNP-Album', 'N/A')
  create_text_source('WNP-Duration', '0:00')
  create_text_source('WNP-Position', '0:00')
  create_cover_source('WNP-Cover', default_cover_url or fallback_default_cover_url)
  try:
    create_text_source('WNP-Formatted', custom_format.format(player_name=player_name, title=title, artist=artist, album=album, duration=duration, position=position, positionPercent=position_percent))
  except:
    pass

def update_source(type, key, value):
  source = obs.obs_get_source_by_name(f'WNP-{type}')
  if source is not None:
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, key, value)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
    obs.obs_source_release(source)

def create_text_source(name, placeholder):
  source = obs.obs_get_source_by_name(name)
  if source is None:
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, 'text', placeholder)
    source = obs.obs_source_create('text_gdiplus', name, settings, None)
    obs.obs_scene_add(scene, source)
    obs.obs_scene_release(scene)
    obs.obs_data_release(settings)
  obs.obs_source_release(source)
  return source

def create_cover_source(name, url):
  source = obs.obs_get_source_by_name(name)
  if source is None:
    current_scene = obs.obs_frontend_get_current_scene()
    scene = obs.obs_scene_from_source(current_scene)
    settings = obs.obs_data_create()
    obs.obs_data_set_string(settings, 'url', url)
    obs.obs_data_set_int(settings, 'width', 300)
    obs.obs_data_set_int(settings, 'height', 300)
    obs.obs_data_set_string(settings, 'css', 'img { width: auto; height: 100%; aspect-ratio: 1; object-fit:cover; }')
    source = obs.obs_source_create('browser_source', name, settings, None)
    obs.obs_scene_add(scene, source)
    obs.obs_scene_release(scene)
    obs.obs_data_release(settings)
  obs.obs_source_release(source)
  return source

def update_widget():
  if widgets_manifest == None: return
  if selected_widget == 'None':
    source = obs.obs_get_source_by_name('WNP-Widget')
    if source is not None:
      obs.obs_source_remove(source)
      obs.obs_source_release(source)
  else:
    source = obs.obs_get_source_by_name('WNP-Widget')
    if source is None:
      current_scene = obs.obs_frontend_get_current_scene()
      scene = obs.obs_scene_from_source(current_scene)
      settings = obs.obs_data_create()
      obs.obs_data_set_string(settings, 'url', f'https://raw.githack.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/{selected_widget}.html')
      obs.obs_data_set_int(settings, 'height', next((t['height'] for t in widgets_manifest if t['name'] == selected_widget), 0))
      obs.obs_data_set_int(settings, 'width', next((t['width'] for t in widgets_manifest if t['name'] == selected_widget), 0))
      obs.obs_data_set_string(settings, 'css', custom_css.replace(r'{default_cover_url}', default_cover_url or fallback_default_cover_url))
      source = obs.obs_source_create('browser_source', 'WNP-Widget', settings, None)
      obs.obs_scene_add(scene, source)
      obs.obs_scene_release(scene)
      obs.obs_data_release(settings)
    else:
      settings = obs.obs_data_create()
      obs.obs_data_set_string(settings, 'url', f'https://raw.githack.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/{selected_widget}.html')
      obs.obs_data_set_int(settings, 'height', next((t['height'] for t in widgets_manifest if t['name'] == selected_widget), 0))
      obs.obs_data_set_int(settings, 'width', next((t['width'] for t in widgets_manifest if t['name'] == selected_widget), 0))
      obs.obs_data_set_string(settings, 'css', custom_css.replace(r'{default_cover_url}', default_cover_url or fallback_default_cover_url))
      obs.obs_source_update(source, settings)
      obs.obs_data_release(settings)
    obs.obs_source_release(source)
    return source