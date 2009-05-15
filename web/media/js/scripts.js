$(function() {
  
  $('#q').example(function() {
    return $(this).attr('title');
  });
  
  $('.welcome_message').append('<a href="#" id="welcome_message_close">X</a>')
  
  $('#welcome_message_close').click(function() {
    $('.welcome_message').effect('blind')
  });
  
  $('#list p').click(function() {
    $('.list_items').toggle()
  });

  $('#add').hide()

  $("input:checkbox").click(function() {
    id = $(this).attr('id')  
    if ($(this).attr('checked')) {


        $.getJSON("/lists/ajax/add/" + id, function(data){
          total = data.total
        });

      $(this).parent().parent().toggle('transfer', {to : '#list p strong'}, function() {
        $('#list p').effect('highlight',null,null, function() {
          $('#list p strong').html('&euro;'+total)
          $('.list_items').load("/lists/ajax/list")
        }) 
      })
    } else {
      $.getJSON("/lists/ajax/del/" + id, function(data){
        total = data.total
      });
      
      $('#list p strong').toggle('transfer', {to : $(this).parent().parent()}, function() {
        $(this).effect('highlight',null,null, function() {
          $('#list p strong').html('&euro;'+total)
          $('.list_items').load("/lists/ajax/list")
        }) 
      })

    }
  });
  
  
  
});

