$(document).ready(function(){
    $.ajaxSetup({
      data: {csrfmiddlewaretoken: '{{ csrf_token }}'},
    });
  $("#comment_submit").submit(function(){
    event.preventDefault();
    $.ajax({
        type: "POST",//方法类型
        //dataType: "json",//预期服务器返回的数据类型
        url: "/blog/comment_submit/" ,//url
        data: $('#comment_submit').serialize(),
        success: function (result) {
          $('#comments-show').append('<li><div class="media mb-4">' +
            '<img class="d-flex mr-3 rounded-circle" src="http://placehold.it/50x50" alt="">' +
            '<div class="media-body">' +
            '<h5 class="mt-0">' + result.name + '</h5>' +
            '<p>' + result.content + '</p>' +
            '</div>' +
            '</div></li>');
          $('#waitting-for-comment').html('');
          $('#id_name').val('');
          $('#id_email').val('');
          $('#id_content').val('');
          $('#input-help').html('');
        },
        error : function() {
          $('#input-help').html('&nbsp&nbsp输入有误,请重新输入!');
        }
    });
});
});


