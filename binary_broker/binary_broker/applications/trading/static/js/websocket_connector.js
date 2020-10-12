console.log(window.location.host);
var socket = new WebSocket('ws://' + window.location.host + '/trading/');

socket.onopen = function open() {
  console.log('WebSockets connection created.');
};

socket.onmessage = function(e) {
  update_trading();
};

if (socket.readyState == WebSocket.OPEN) {
  socket.onopen();
};
