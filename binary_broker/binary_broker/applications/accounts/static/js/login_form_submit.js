var login_form = $('#login_form');

login_form.on('submit', function(event) {

    'since fucking login_form.serialize() refuses to work';
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var email = $('input[name=email]').val();
    var password = $('input[name=password]').val();
    var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                     '&email=' + email + '&password=' + password;

    console.log(data_string);
    event.preventDefault();
    $.ajax({
      url: '/accounts/login/',
      type: 'post',
      data: data_string
    });
});
