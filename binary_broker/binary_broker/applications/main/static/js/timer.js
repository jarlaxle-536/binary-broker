function get_time () {
  console.log('getting time');
  $.ajax({
    url: '/ajax/get_time/',
    success: function(dct) {
      console.log(dct);
      var time_string = JSON.parse(dct)['time_string'];
      var time_p = document.getElementById('current_time_string');
      time_p.innerHTML = time_string;
    }
  });
};

$(function(){
    setInterval(get_time, 1000);
});
