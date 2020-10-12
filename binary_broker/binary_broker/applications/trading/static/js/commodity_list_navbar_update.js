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
