$(document).ready(function(){
  $("#likes").click(function(){
    var catid;
    catid = $(this).attr("data-catid");
    $.get('/rango/like_category/', {category_id: catid}, function(data){
      $('#like_count').html(data);
      $('#likes').hide();
    });
    });
  $('#suggestion').keyup(function(){
    var query;
    query = $(this).val();
    $.get('/rango/suggest_category/', {suggestion: query}, function(data){
      $('#cats').html(data);
    });
    });
  $('.add_button').click(function(){
    var link;
    var title;
    var summary;
    link = $(this).attr("link");
    title = $(this).attr("title");
    category_id = $(this).attr("category_id");
    $.get('/rango/add_page_from_search/', {link: link, title: title, category_id: category_id}, function(data){
      $('#refresh_pages').html(data);
    });
    $(this).hide();
    });
});
