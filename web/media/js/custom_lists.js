$(function() {

  // Change the ID, so that the CSS for the footer kicks in
  $('#list_standard').attr('id', 'list')
  $('#list_items').attr('class', 'hide')
  
  $('#list').insertAfter('#outer')
  
  
  // $(function(){
  //  positionFooter(); 
  //  function positionFooter(){
  //    $("#list").css({position: "absolute",top:($(window).scrollTop()+$(window).height()-$("#list").height())+"px"})  
  //  }
  // 
  //  $(window)
  //    .scroll(positionFooter)
  //    .resize(positionFooter)
  // });
  
  
  // Open the list box when the total is pressed
  $('#list p').click(function() {
    $('#list_items').toggle()
  });

  $('#add').hide()

  $("input:checkbox.custom_list_toggle").click(function() {
    id = $(this).attr('name')  
    if ($(this).attr('checked')) {

        $.getJSON("/lists/ajax/add/" + id, function(data){
          total = data.total
          console.debug(total)
        });
        
        $(this).parent().parent().toggle('transfer', {to : '#list p strong'}, function() {
          $('#list p').effect('highlight',null,null, function() {
            $('#list p strong').html('&euro;'+total)
            
            $('#list_items').fadeOut(100,function(){
              $('#list_items').load("/lists/ajax/list", function() {
                if ($('#list_items').hasClass('hide')==false) {
                  $('#list_items').fadeIn(100,function(){})
                }
              })
            })
          }) 
        })
          
    } else {
      $.getJSON("/lists/ajax/del/" + id, function(data){
        total = data.total
      });

      $('#list p strong').toggle('transfer', {to : $(this).parent().parent()}, function() {
        $(this).effect('highlight',null,null, function() {
          $('#list p strong').html('&euro;'+total)
          $('#list_items').load("/lists/ajax/list")
        }) 
      })

    }
  });


});