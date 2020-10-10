var login_form = $('#login_form');
var inputs = ['#login_id_email', '#login_id_password'];

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
    success: function(errors_string) {
      var errors_dict = JSON.parse(errors_string);
      if ($.isEmptyObject(errors_dict)) {
        console.log('No form errors, should redirect to main page or next.');
      }
      else {
        login_add_errors(errors_dict);
      }
    }
  });
}

function login_add_errors (errors) {
  console.log('Some form errors occured, should show them in form.');
  Object.keys(errors).forEach(field => {
    var text = '<ul>';
    errors[field].forEach(dct => {
      text += '<li class="error code-' + dct['code'] + '">' + dct['message'] + '</li>'
    });
    text += '</ul>';
    var errors_div = document.getElementById('login_id_' + field + '_errors');
    errors_div.innerHTML = text;
  });
}
