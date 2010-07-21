$(function() {
  
  if ($('#q').val() == '') {
    $('#q').example(function() {
      return $(this).attr('title');
    });
  }

  $('.welcome_message').append('<a href="#" id="welcome_message_close">X</a>')

  $('#welcome_message_close').click(function() {
    $('.welcome_message').effect('blind')
  });

  //show features
  if ($.cookie('display_welcome_message') == "1"){
      if($('.features')){
          $('.features').slideDown(2000);
          var date = new Date();
          date.setTime(date.getTime() + (3 * 24 * 60 * 60 * 1000));
          $.cookie('display_welcome_message', '0', { path: '/', expires: date });
      }
  }
});

