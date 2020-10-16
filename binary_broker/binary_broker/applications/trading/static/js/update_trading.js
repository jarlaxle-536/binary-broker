function update_trading () {
  console.log('update trading start');
  update_price_plot();
  update_commodity_list_navbar();
}

function update_commodity_list_navbar () {
  console.log('will update cmd list navbar');
  var csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
  $.ajax({
    url: '/trading/asset/update',
    headers: {
      "X-CSRFToken": csrf_token
    },
    type: 'patch',
    success: function(data) {
      data.forEach(asset_info => {
        price_td = document.getElementById('asset_' + asset_info['id'] + '_price');
        price_td.innerHTML = asset_info['price'];
        diff_td = document.getElementById('asset_' + asset_info['id'] + '_diff');
        diff_td.innerHTML = asset_info['diff'];
      });
    }
  });
}

function update_price_plot () {
  var price_plot = document.getElementById('price_plot');
  var path = window.location.pathname;
  var to_split_by = '/trading/asset/'
  if (path.startsWith(to_split_by)) {
    var asset_id = path.split(to_split_by)[1];
    var src = price_plot.src.split('?')[0];
    console.log(price_plot.src);
    console.log('will update price plot for asset ' + asset_id);
    $('#price_plot').attr("src", src + '?timestamp=' + new Date().getTime());
  }
}

$(function(){
    setInterval(update_trading, 5000);
});
