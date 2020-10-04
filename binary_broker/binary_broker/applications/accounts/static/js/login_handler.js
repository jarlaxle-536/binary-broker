$(document).ready(function() {
  var rel_location = window.location.pathname;
  if (rel_location == '/accounts/login/') {
    $('#auth_window').modal('toggle');
  }
  console.log(location);
  console.log('login handler done');
});
