var login_form = $('#login_form');

login_form.on('submit', function(event) {

    'since fucking login_form.serialize() refuses to work';
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var email = login_form.find('input[name=email]').val();
    var password = login_form.find('input[name=password]').val();
    var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                     '&email=' + email + '&password=' + password;

    event.preventDefault();
    $.ajax({
      url: '/accounts/login/',
      type: 'post',
      data: data_string,
      success: function(event) {
        $('#auth_window').modal('toggle');
        location.reload();
        console.log('login form submitted successfully');
      },
      error: function(event) {
        console.log('error occured while submitting login form');
        console.log('sanity check');
        login_form = document.getElementById('login_form');
        login_form.innerHTML += 'some fail';
      }
    });
});
