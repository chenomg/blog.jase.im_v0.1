$(document).ready(function(){
  $("#comment_submit_key").click(function(){
    $.ajax({
    //几个参数需要注意一下
        type: "POST",//方法类型
        dataType: "json",//预期服务器返回的数据类型
        url: "/blog/comment_submit/" ,//url
        data: $('#comment_submit').serialize(),
        success: function (result) {
            console.log(result);//打印服务端返回的数据(调试用)
            if (result.resultCode == 200) {
                alert("SUCCESS");
            }
            ;
        },
        error : function() {
            alert("异常！");
        }
    });

    //var post_title_slug;
    //var form = new FormData(document.getElementById('comment-submit');
    //post_title_slug = $(this).attr("post_title_slug");
    //form = $(this).attr("post_title_slug");
    //$.post('/blog/comment_submit/', {post_title_slug: post_title_slug}, function(data){
      //$('#comments-form-show').html(data);
    //});
    //});
});
});
