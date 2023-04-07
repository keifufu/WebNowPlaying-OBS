from pywnp import WNPRedux
import obspython as obs
import urllib.request, json

# WNP Variables
Player = 'N/A'
Title  = 'N/A'
Artist = 'N/A'
Album = 'N/A'
Duration = '0:00'
Position = '0:00'
PositionPercent = '0'
CoverUrl = ''

# Script Settings
SelectedWidget = 'None'
WidgetsManifest = None
DefaultCoverUrl = 'https://raw.githubusercontent.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/images/nocover.png'
CustomFormat = '{title} - {artist} ({position}/{duration})    '

CustomCSS = r'body { background-color: rgba(0, 0, 0, 0); margin: 0px auto; overflow: hidden; } '
CustomCSS += r':root { --default-cover-url: url("{DefaultCoverUrl}"); }'

def script_description():
  description = '<b>WebNowPlaying for OBS</b>'
  description += '<br>'
  description += 'Available placeholders:'
  description += '<br>'
  description += '{player}, {title}, {artist}, {album}, {duration}, {position}, {positionPercent}'
  return description

def script_defaults(settings):
  obs.obs_data_set_default_string(settings, 'custom_format', CustomFormat)
  obs.obs_data_set_default_string(settings, 'default_cover_url', DefaultCoverUrl)

def script_properties():
  props = obs.obs_properties_create()

  list = obs.obs_properties_add_list(props, 'selected_widget', 'Widget', obs.OBS_COMBO_TYPE_LIST, obs.OBS_COMBO_FORMAT_STRING)
  obs.obs_property_list_add_string(list, 'None', 'None')
  req = urllib.request.Request('https://raw.githubusercontent.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/manifest.json', headers={'User-Agent': 'Mozilla/5.0'})
  with urllib.request.urlopen(req) as url:
    data = json.loads(url.read().decode())
    global WidgetsManifest
    WidgetsManifest = data
    for widget in data:
      obs.obs_property_list_add_string(list, widget['name'], widget['name'])

  obs.obs_properties_add_text(props, 'custom_format', 'Format', obs.OBS_TEXT_DEFAULT)
  obs.obs_properties_add_button(props, 'cs', 'Create Sources', create_sources)
  obs.obs_properties_add_text(props, 'default_cover_url', 'Default Cover URL', obs.OBS_TEXT_DEFAULT)
  
  return props

def script_update(settings):
  global CustomFormat, DefaultCoverUrl, SelectedWidget
  SelectedWidget = obs.obs_data_get_string(settings, 'selected_widget')
  CustomFormat = obs.obs_data_get_string(settings, 'custom_format')
  DefaultCoverUrl = obs.obs_data_get_string(settings, 'default_cover_url')
  updateWidget()

def script_load(settings):
  def logger(type, message):
    print(f'WNP - {type}: {message}')
  WNPRedux.Initialize(6534, '1.0.1', logger)
  obs.timer_add(update, 250)

def script_unload():
  WNPRedux.Close()
  obs.timer_remove(update)

def update():
  if WNPRedux.isInitialized:
    global Player, Title, Artist, Album, Duration, Position, PositionPercent, CoverUrl
    Player = WNPRedux.mediaInfo.Player or 'N/A'
    Title = WNPRedux.mediaInfo.Title or 'N/A'
    Artist = WNPRedux.mediaInfo.Artist or 'N/A'
    Album = WNPRedux.mediaInfo.Album or 'N/A'
    Duration = WNPRedux.mediaInfo.Duration
    Position = WNPRedux.mediaInfo.Position
    PositionPercent = str(int(WNPRedux.mediaInfo.PositionPercent))
    CoverUrl = WNPRedux.mediaInfo.CoverUrl
    update_source('Player', 'text', Player)
    update_source('Title', 'text', Title)
    update_source('Artist', 'text', Artist)
    update_source('Album', 'text', Album)
    update_source('Duration', 'text', Duration)
    update_source('Position', 'text', Position)
    update_source('Cover', 'url', CoverUrl or DefaultCoverUrl)
    try:
      update_source('Formatted', 'text', CustomFormat.format(player=Player, title=Title, artist=Artist, album=Album, duration=Duration, position=Position, positionPercent=PositionPercent))
    except:
      pass

def create_sources(props, prop):
  create_text_source('WNP-Player', 'N/A')
  create_text_source('WNP-Title', 'N/A')
  create_text_source('WNP-Artist', 'N/A')
  create_text_source('WNP-Album', 'N/A')
  create_text_source('WNP-Duration', '0:00')
  create_text_source('WNP-Position', '0:00')
  create_cover_source('WNP-Cover', DefaultCoverUrl)
  try:
    create_text_source('WNP-Formatted', CustomFormat.format(player=Player, title=Title, artist=Artist, album=Album, duration=Duration, position=Position, positionPercent=PositionPercent))
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

def updateWidget():
  if WidgetsManifest == None: return
  if SelectedWidget == 'None':
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
      obs.obs_data_set_string(settings, 'url', f'https://raw.githack.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/{SelectedWidget}.html')
      obs.obs_data_set_int(settings, 'height', next((t['height'] for t in WidgetsManifest if t['name'] == SelectedWidget), 0))
      obs.obs_data_set_int(settings, 'width', next((t['width'] for t in WidgetsManifest if t['name'] == SelectedWidget), 0))
      obs.obs_data_set_string(settings, 'css', CustomCSS.replace(r'{DefaultCoverUrl}', DefaultCoverUrl))
      source = obs.obs_source_create('browser_source', 'WNP-Widget', settings, None)
      obs.obs_scene_add(scene, source)
      obs.obs_scene_release(scene)
      obs.obs_data_release(settings)
    else:
      settings = obs.obs_data_create()
      obs.obs_data_set_string(settings, 'url', f'https://raw.githack.com/keifufu/WebNowPlaying-Redux-OBS/main/widgets/{SelectedWidget}.html')
      obs.obs_data_set_int(settings, 'height', next((t['height'] for t in WidgetsManifest if t['name'] == SelectedWidget), 0))
      obs.obs_data_set_int(settings, 'width', next((t['width'] for t in WidgetsManifest if t['name'] == SelectedWidget), 0))
      obs.obs_data_set_string(settings, 'css', CustomCSS.replace(r'{DefaultCoverUrl}', DefaultCoverUrl))
      obs.obs_source_update(source, settings)
      obs.obs_data_release(settings)
    obs.obs_source_release(source)
    return source