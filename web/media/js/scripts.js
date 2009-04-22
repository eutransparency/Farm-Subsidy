$(function() {
  $('#q').example(function() {
    return $(this).attr('title');
  });
  
  $('.welcome_message').append('<a href="#" id="welcome_message_close">X</a>')
  
  $('#welcome_message_close').click(function() {
    $('.welcome_message').effect('blind')
  });
  
});

