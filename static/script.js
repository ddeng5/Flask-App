function submitBooking() {
  $(document).ready(function(){

     $('#bookingSub').click(function(){

         $.ajax({
           type: 'POST',
           url: '/Authenticate',
           success: function(data){
             alert(data);
           }
         });
     });

});
}

function select() {
  $(document).ready(function(){

         $.ajax({
           type: 'POST',
           url: '/test',
           success: function(data){
             alert(data);
           }
     });

});
}
