var signup_form = $('#signup_form');

signup_form.on('submit', function(event) {

    'since fucking login_form.serialize() refuses to work';
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var email = signup_form.find('input[name=email]').val();
    var password = signup_form.find('input[name=password]').val();
    var password_confirmation = signup_form.find(
        'input[name=password_confirmation]').val();
    var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                     '&email=' + email + '&password=' + password +
                     '&password_confirmation=' + password_confirmation;

    console.log(data_string);
    event.preventDefault();
    $.ajax({
      url: '/accounts/signup/',
      type: 'post',
      data: data_string,
      success: function(event) {
        $('#auth_window').modal('toggle');
        location.reload()
        console.log('signup form submitted successfully');
      }
    });
});
