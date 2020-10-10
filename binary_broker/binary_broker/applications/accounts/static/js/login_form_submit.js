var login_form = $('#login_form');
var inputs = ['#id_email', '#id_password'];

for (var input in inputs) {
  $(input).on('keypress', function (event) {
    if(event.which === 13) { login_submit(event); }
  });
}

login_form.on('submit', function(event) {
  login_submit(event);
});

function login_submit (event) {

  console.log('login submit start');

  var csrf_token  = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  var email       = login_form.find('input[name=email]').val();
  var password    = login_form.find('input[name=password]').val();
  var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                    '&email=' + email + '&password=' + password;

  event.preventDefault();
  $.ajax({
    url: '/accounts/login/',
    type: 'post',
    data: data_string,
    success: function(event) {
      console.log('login form ajax post done');
      console.log(event);
    }
  });
}
