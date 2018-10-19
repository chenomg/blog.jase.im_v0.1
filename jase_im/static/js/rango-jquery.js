$(document).ready(function(){
  //jQuery code here
  $("#about-btn").click(function(event)
    {
      alert("You clicked the button using jQuery.")
    });
  $(".h1").click(function(event)
    {
      alert("You clicked the H1 using jQuery.")
    });
  $("p").hover(function(){
    $(this).css('color', 'red')
  },
    function(){
      $(this).css('color', 'blue')
    });
});
