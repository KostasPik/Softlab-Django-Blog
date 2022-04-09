 $('#newsletter-form').on('submit', function(e){
  e.preventDefault();
  var honeypot = $('#honeypot').val(); // trying to catch bot if there is a honeypot value, never send the request to the backend
  var loadingEffect =  $('.loading-effect')[0]; // loading effect DOM
  if(!honeypot){
      loadingEffect.innerHTML='<div class="spinner-border text-dark mt-2" role="status"><span class="sr-only"></span></div>'; // waiting effect bootstrap 
      $.ajax({
          type : "POST", 
          url: "new_subscriber/",
          data: {
              email : $('#newsletter-email').val(),
              honeypot : $('#honeypot').val(),
              dataType: "json",
          },
          success: function(data){
              console.log(data);
              
              loadingEffect.innerHTML='';
              loadingEffect.hidden=true;

              // TOASTBEGIN
              var toastLiveExample = document.getElementById('liveToast')
              var toast = new bootstrap.Toast(toastLiveExample)
              var toast_body = document.getElementsByClassName('toast-body')[0];
              toast_body.innerText = data['msg'];
              toast_body.style = "color: red";
              toast.show()
            
              


              // TOASTEND
              document.getElementById('newsletter-form').reset();

            },

          
          failure: function(error) {
              console.log(data);
              
              var toastLiveExample = document.getElementById('liveToast')
              var toast = new bootstrap.Toast(toastLiveExample)
              var toast_body = document.getElementsByClassName('toast-body')[0];
              toast_body.innerText = 'We are so sorry but something went wrong :(';
              toast_body.style = "color: red";
              toast.show()              
          }
      });
  }
  else {
      console.log("We got you bot!")
  }
});    