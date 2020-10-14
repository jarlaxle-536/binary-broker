var bet_form = $('#bet_form');

bet_form.on('submit', function(event) {
  bet_submit(event);
});

function bet_submit (event) {
  event.preventDefault();
  console.log('submitted');
}
