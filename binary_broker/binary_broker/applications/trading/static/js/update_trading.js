function update_trading() {
  console.log('update trading start');
  var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
  $.ajax({
    url: '/trading/commodity/update',
    headers: {
      "X-CSRFToken": csrf_token
    },
    type: 'patch',
    success: function(data) {
      update_commodity_list_navbar(data);
    }
  });
  var path = window.location.pathname;
  var to_split_by = '/trading/commodity/'
  if (path.startsWith(to_split_by)) {
    var cmd_id = path.split(to_split_by)[1];
    $.ajax({
      url: '/trading/commodity/' + cmd_id + '/get_price_plot',
      headers: {
        "X-CSRFToken": csrf_token
      },
      type: 'get',
      success: function(data) {
        update_price_plot(data);
      }
    });
  };
}

function update_commodity_list_navbar (data) {
  console.log('will update cmd list navbar');
  data.forEach(cmd_info => {
    price_td = document.getElementById('cmd_' + cmd_info['id'] + '_price');
    price_td.innerHTML = cmd_info['price'];
    diff_td = document.getElementById('cmd_' + cmd_info['id'] + '_diff');
    diff_td.innerHTML = cmd_info['diff'];
  });
}

function update_price_plot (data) {
  console.log('will update cmd plot');
  img = document.getElementById('prices_plot');
  img.src = data;
  console.log(img);
}
