var account_select = $('#select_account');

account_select.on('change', function(event) {

    console.log('select account change');
    console.log(this.value);
    var csrf_token = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var account_type = this.value;
    var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                     '&account_type=' + account_type;
    $.ajax({
      url: '/accounts/set_account_type/',
      type: 'post',
      data: data_string,
      success: function(event) {
        console.log('account selection complete');
      }
    });
});
