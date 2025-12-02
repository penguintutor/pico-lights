

// Use global variable for status so we know if we need to send ajax if change
var button_pressed = '';

$(document).ready(function() {
// define handlers
$('#sw_on_1').click(function(){onButtonClicked('1')});
$('#sw_on_2').click(function(){onButtonClicked('2')});
$('#sw_on_3').click(function(){onButtonClicked('3')});

$('#sw_off_1').click(function(){offButtonClicked('1')});
$('#sw_off_2').click(function(){offButtonClicked('2')});
$('#sw_off_3').click(function(){offButtonClicked('3')});

$('#sw_flash_1').click(function(){flashButtonClicked('1')});
$('#sw_twinkle_1').click(function(){twinkleButtonClicked('1')});

}); // end ready



// handle on button
function onButtonClicked (button) {
    $.get ('/lights', 'light='+button+"&action=on", displayResponse);
}


// handle off button
function offButtonClicked (button) {
    $.get ('/lights', 'light='+button+"&action=off", displayResponse);
}

function flashButtonClicked (button) {
    $.get ('/lights', 'light='+button+"&action=flash", displayResponse);
}

function twinkleButtonClicked (button) {
    $.get ('/lights', 'light='+button+"&action=twinkle", displayResponse);
}

function displayResponse (data) {
    $('#status').html(data);
}
