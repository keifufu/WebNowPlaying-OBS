const defaultMediaInfo = {
  State: 'STOPPED',
  Player: '',
  Title: '',
  Artist: '',
  Album: '',
  CoverUrl: '',
  Duration: '0:00',
  DurationSeconds: 0,
  Position: '0:00',
  PositionSeconds: 0,
  PositionPercent: 0,
  Volume: 100,
  Rating: 0,
  RepeatState: 'NONE',
  Shuffle: false,
  Timestamp: 0
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
        const mediaInfo = JSON.parse(e.data)
        onMediaInfoChange(mediaInfo)
      } catch {}
    }
  }
}