$(document).ready(function() {

    
    function SetUp(){
        // Called on page load and sets everything up

        // Add the list footer tag
        $(".list_block").wrap('<div class="lists_footer" />');
        
        // Move the list block to the footer
        $('.lists_footer').remove().insertAfter('#outer');
        
        // Hide the list items by default
        $('.list_block .list_items #box_content').addClass('hide');
        
        $('#footer').css({'margin-bottom': '40px'})
        
        // Open the list box when the total is pressed
        $('.list_block .list_items .list_total').live('click', function() {
            $('.list_block .list_items #box_content').slideToggle('fast');
            $('.list_block .list_items #list_arrow').toggleClass('list_on_display');
        });
        
    }
    
    SetUp();

    
    
    
    function make_icons(){
        $('.list_form').each(function (i, el){
            alerady_converted = $(el).children('.list_item');
            if ($(alerady_converted).length == 0) {
                $(el).children().hide();
                action = $(el).children('.action').attr('name');
                if (action == "add") {
                    text = "Add to list"
                } else {
                    text = "Remove from list"
                }
                
                $(el).append('<a class="list_item list_'+action+'"><span>'+text+'</span></a>');

            }
        });
    }

    make_icons()
    

    function update_list(obj) {
        if ($('#list_arrow').attr('class') == "list_on_display") {
            $('.list_block .list_items').html(obj.html)
            $('.list_block .list_items #box_content').css({'display' : 'block'});
            $('#list_arrow').attr('class', 'list_on_display')
        } else {
            $('.list_block .list_items').html(obj.html)
            $('.list_block .list_items #box_content').hide()
        }
        
        make_icons();
    }    


    // function animate_add(obj) {
    //     obj.parent().effect('transfer', { to: $(".list_block .list_items") }, 10000);
    //     console.debug($(obj.parent()))
    // }


    $('.list_item span').live('click', function(){  
        item = $(this)
        item_form = item.parent().parent()


        object_id = $(item_form).children('.object_id').attr('value');
        content_type = $(item_form).children('.content_type').attr('value');
        list_item_id = $(item_form).children('.list_item_id').attr('value');
        action = $(item_form).children('.action').attr('name');
        form_action = $(item_form).attr('action');

        
        // animate_add(item_form)
        
        
        form_data = {
            content_type : content_type,
            object_id : object_id,
            list_item_id : list_item_id,
            action : action,
        }

        $.ajax({
            type: 'POST',
            url: form_action,
            data: form_data,
            success: function(obj){
                obj = eval('('+obj+')')
                list_item_id = obj.list_item_id
                item_forms = $("input[value='"+list_item_id+"']")

                item_forms.each(function(i, el) {
                    console.debug(el)
                    item_form = $(el).parent();
                    item_link = item_form.children('a.list_item')[0];
                    
                    if (obj.action == "add") {
                    
                        $(item_form).children('.action').attr('name', 'remove');                                        
                        $(item_link).removeClass('list_add');
                        $(item_link).addClass('list_remove');
                    }

                    if (obj.action == "remove") {
                        $(item_form).children('.action').attr('name', 'add');
                        $(item_link).removeClass('list_remove');
                        $(item_link).addClass('list_add');
                    }
                    
                });

            update_list(obj);
            
            },
        });

    });

});