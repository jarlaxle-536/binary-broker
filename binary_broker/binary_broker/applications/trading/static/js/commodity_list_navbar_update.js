function update_commodities_list() {
  console.log('cmd navbar update start');
  var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
  console.log('csrf: ' + csrf_token);
  $.ajax({
    url: '/trading/commodity/update',
    headers: {
      "X-CSRFToken": csrf_token
    },
    type: 'patch',
    success: function(e) {
      console.log('connection successful');
//      get_commodity_navbar_li(e);
      cmd_list_ul = document.getElementById('commodity_list_ul');
      cmd_list_ul.innerHTML = e;
      console.log('updated cmd list navbar');
    }
  });
}

function get_commodity_navbar_li (data) {
  console.log('building li element for data: ' + data);
}
