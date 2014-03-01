function ShowDefault(elem1, elem2){
  if (!elem1.hasClass('hide')) {
    elem1.addClass('hide');
   }    
  if (elem2.hasClass('hide')) {
    $(elem2).removeClass('hide'); 
  }

}

  $(document).ready(function() {
    e1 = $('.usernameTaken');
    e2 = $('.help-block');
    
    $("#username").keyup(function(event){
      var inputString = $(this).val();

      if (inputString.length < 2)  
        ShowDefault(e1, e2);
                
      $.ajax({
        url: 'lookup',
        data: 'term='+inputString,
        datatype: 'json',   
        success: function(response) {
           if (response.length == 0)
             ShowDefault(e1, e2);
           else {
           $(".usernameTaken").removeClass('hide');
           $(".help-block").addClass('hide');
           }
        },
        error: response=[] 
      });
    });
  });
