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
