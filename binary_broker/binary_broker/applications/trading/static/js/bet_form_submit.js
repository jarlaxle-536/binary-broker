var bet_form = $('#bet_form');

bet_form.on('submit', function(event) {

  console.log('submitted');

  event.preventDefault();

  var csrf_token  = document.getElementsByName('csrfmiddlewaretoken')[0].value;
  var venture     = bet_form.find('select[name=venture]').val();
  var duration    = bet_form.find('select[name=duration]').val();
  var direction = event['originalEvent']['submitter'].name;
  var data_string = '&csrfmiddlewaretoken=' + csrf_token +
                    '&venture=' + venture + '&duration=' + duration +
                    '&direction=' + direction;

  $.post({
    url: window.location.pathname + '/create_bet/',
    data: data_string,
    success: function(data) {
      console.log(data);
    }
  });
});
