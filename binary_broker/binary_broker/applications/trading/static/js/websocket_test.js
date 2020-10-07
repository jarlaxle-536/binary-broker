$('#ws_test').on('click', function() {
  console.log('ws test button clicked');

  $.ajax({
    url: '/trading/ajax/websocket_test',
    type: 'get',
  });
  console.log('ws test complete');
})
