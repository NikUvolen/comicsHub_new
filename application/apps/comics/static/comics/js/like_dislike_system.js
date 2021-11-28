$( document ).ready(function() {
    function turnOffButtons(buttons) {
        buttons.forEach(button => {
            button.attr('disabled', true);
        }); 
    }
    
    function enableButtons(buttons) {
        buttons.forEach(button => {
            button.remove('disabled');
        })
    }
    
    
    function like()
    {
        var like = $(this);
        var type = like.data('type');
        var pk = like.data('id');
        var action = like.data('action');
        var dislike = like.next();
        
        $.ajax({
            url : type + "/" + pk + "/" + action + "/",
            type : 'POST',
            data : { 'obj' : pk },
    
            success : function (json) {
                like.find("[data-count='like']").text(json.like_count);
                dislike.find("[data-count='dislike']").text(json.dislike_count);
            }
        });
    
        return false;
    }
    
    function dislike()
    {
        var dislike = $(this);
        var type = dislike.data('type');
        var pk = dislike.data('id');
        var action = dislike.data('action');
        var like = dislike.prev();
    
        $.ajax({
            url : type +"/" + pk + "/" + action + "/",
            type : 'POST',
            data : { 'obj' : pk },
    
            success : function (json) {
                dislike.find("[data-count='dislike']").text(json.dislike_count);
                like.find("[data-count='like']").text(json.like_count);
            }
        });
    
        return false;
    }
    
    // Подключение обработчиков
    $(function() {
        $('[data-action="like"]').click(like);
        $('[data-action="dislike"]').click(dislike);
    });
})