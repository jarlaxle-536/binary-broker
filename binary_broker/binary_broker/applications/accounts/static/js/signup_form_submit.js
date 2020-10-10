var signup_form = $('#signup_form');
var inputs = ['#signup_id_email', '#signup_id_password', '#signup_id_password_confirmation'];

for (var input in inputs) {
  $(input).on('keypress', function (event) {
    if(event.which === 13) { signup_submit(event); }
  });
}

signup_form.on('submit', function(event) {
  signup_submit(event);
});

function signup_submit (event) {

  console.log('signup submit start');

  var csrf_token  = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  var email       = signup_form.find('input[name=email]').val();
  var password    = signup_form.find('input[name=password]').val();
  var password_confirmation = signup_form.find(
      'input[name=password_confirmation]').val();
  var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                    '&email=' + email + '&password=' + password +
                    '&password_confirmation=' + password_confirmation;

  event.preventDefault();

  $.ajax({
    url: '/accounts/signup/',
    type: 'post',
    data: data_string,
    success: function(errors_string) {
      var errors_dict = JSON.parse(errors_string);
      if ($.isEmptyObject(errors_dict)) {
        console.log('No form errors, should redirect to main page or next.');
      }
      else {
        signup_add_errors(errors_dict);
      }
    }
  });
}

function signup_add_errors (errors) {
  console.log('Some form errors occured, should show them in form.');
  Object.keys(errors).forEach( field => {
    var text = '<ul>';
    errors[field].forEach( dct => {
      text += '<li class="error code-' + dct['code'] + '">' + dct['message'] + '</li>';
    });
    text += '</ul>';
    var errors_div = document.getElementById('signup_id_' + field + '_errors');
    errors_div.innerHTML = text;
  });
}
