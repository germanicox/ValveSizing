$(document).ready(function() {
    $('form').on('submit', function(event) {
        $.ajax({
            data : { //JSON Data Type for procces.py
                pipe_unit :  $('#pipe_unit').val(),
                inletD :     $('#inletD').val(),
                outletD :    $('#outletD').val(),
                liquid :     $('#liquid').val(), 
                flow_unit :  $('#flow_unit').val(),
                press_unit : $('#press_unit').val(),
                temp_unit :  $('#temp_unit').val(),
                flow_Min   : $('#flow_Min').val(), 
                P1_Min :     $('#P1_Min').val(),
                P2_Min :     $('#P2_Min').val(), 
                deltaP_Min : $('#deltaP_Min').val(),
                temp_Min :   $('#temp_Min').val(), 
                flow_Op   : $('#flow_Op').val(), 
                P1_Op :     $('#P1_Op').val(),
                P2_Op :     $('#P2_Op').val(), 
                deltaP_Op : $('#deltaP_Op').val(),
                temp_Op :   $('#temp_Op').val(), 
                flow_Max   : $('#flow_Max').val(), 
                P1_Max :     $('#P1_Max').val(),
                P2_Max :     $('#P2_Max').val(), 
                deltaP_Max : $('#deltaP_Max').val(),
                temp_Max :   $('#temp_Max').val(), 
            }, 
            type : 'POST', 
            url : '/process'
        })
        .done(function(data) {
            if (data.error){
                $('#errorAlert').text(data.error).show();
                $('#successAlert').hide();
                $('#ResultMin').hide();
            }
            else {
                $('#successAlert').text("Cv: " + data.Cv).show();
                $('#ResultMin').text("Cv: " + data.Cv).show();
                $('#errorAlert').hide();
            }
        });
        event.preventDefault();
    });
});