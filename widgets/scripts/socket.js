const defaultMediaInfo = {
  state: 'STOPPED',
  player_name: '',
  title: '',
  artist: '',
  album: '',
  cover_url: '',
  duration: '0:00',
  duration_seconds: 0,
  position: '0:00',
  position_seconds: 0,
  position_percent: 0,
  volume: 100,
  rating: 0,
  repeat_mode: 'NONE',
  shuffle_active: false,
  timestamp: 0
}

function registerSocket(_onMediaInfoChange) {
  function onMediaInfoChange(mediaInfo) {
    try { _onMediaInfoChange(mediaInfo) } catch {}
  }
  
  let ws = null
  let timeout = null
  open()
  onMediaInfoChange(defaultMediaInfo)

  function retry() {
    clearTimeout(timeout)
    onMediaInfoChange(defaultMediaInfo)
    try {
      ws.onclose = null
      ws.onerror = null
      ws.close()
    } catch {}
    ws = null
    open()
  }

  function open() {
    ws = new WebSocket('ws://localhost:6534')
    timeout = setTimeout(() => {
      // Retry if connection is not established after 5 seconds
      // and the websocket still hasn't errored/closed
      if (ws.readyState !== WebSocket.OPEN) retry()
    }, 5000)
    ws.onopen = () => ws.send('RECIPIENT')
    ws.onclose = () => retry()
    ws.onerror = () => retry()
    ws.onmessage = (e) => {
      try {
        const mediaInfo = JSON.parse(mapJsonKeys(e.data))
        onMediaInfoChange(mediaInfo)
      } catch {}
    }
  }
}

// Maps keys from pywnp < 2.0.0 to pywnp > 2.0.0
// Example: Player -> player_name
function mapJsonKeys(jsonStr) {
  return jsonStr
    .replace('State', 'state')
    .replace('player', 'player_name')
    .replace('Title', 'title')
    .replace('Artist', 'artist')
    .replace('Album', 'album')
    .replace('CoverUrl', 'cover_url')
    .replace('Duration', 'duration')
    .replace('DurationSeconds', 'duration_seconds')
    .replace('Position', 'position')
    .replace('PositionSeconds', 'position_seconds')
    .replace('PositionPercent', 'position_percent')
    .replace('Volume', 'volume')
    .replace('Rating', 'rating')
    .replace('RepeatState', 'repeat_mode')
    .replace('Shuffle', 'shuffle_active')
    .replace('Timestamp', 'timestamp')
}