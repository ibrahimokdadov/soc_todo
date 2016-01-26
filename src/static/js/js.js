$(document).ready(function() {
$('#deletionModal').on('shown.bs.modal', function () {
   
});


//list items mark done buttons

 $('.task').each(function(){

        $(this).click(function(){
        if ( $( this ).hasClass( "glyphicon-check" ) ) {
            $.getJSON($SCRIPT_ROOT + '/user/task/done/0', {
            task_id: this.id

            }, function(data) {
              var id = data.result
              if (id == false){
              document.getElementById('msg').innerHTML = 'Ops, Could not mark task as done; kindly contact us';
              }
              else if (id == null){
                document.getElementById('msg').innerHTML = 'Alright, here is the thing. The task was not found';
              }
              else{
              var x="a_"+id;
                if ($("#"+x).hasClass("strikethrough")){
                    $("#"+x).removeClass("strikethrough");
                    $("#"+id).removeClass("glyphicon-check");
                    $("#"+id).addClass("glyphicon-unchecked");

                    //location.reload();
                    }
                    else{
                    document.getElementById('msg').innerHTML = 'Out of ink. We have an issue marking this as done';
                    }
                }
              });
            return false;

        }
        else {

              $.getJSON($SCRIPT_ROOT + '/user/task/done/1', {
              task_id: this.id

              }, function(data) {
              var id = data.result
                  if (id == false){
                    document.getElementById('msg').innerHTML = 'Ops, Could not mark task as done; kindly contact us';
                  }
                  else if (id == null){
                    document.getElementById('msg').innerHTML = 'Alright, here is the thing. The task was not found';
                  }
                  else{
                  var x="a_"+id;
                  if (!$("#"+x).hasClass("strikethrough")){
                        $("#"+x).addClass("strikethrough");
                        $("#"+id).addClass("glyphicon-check");
                        $("#"+id).removeClass("glyphicon-unchecked");

                    //location.reload();
                    }
                    else
                    alert("Strikethrough exist");
                  }
              });
              return false;


        }



        });
    });


});


