var providers = ['google', 'facebook', 'github'];

providers.forEach( provider => {
  var btn_id = '#' + provider + '_auth_btn';
  $(btn_id).on('click', function (event) {
    event.preventDefault();
    social_auth(provider);
  });
});

function social_auth (provider) {
  console.log(provider + '_auth_btn clicked');
}
