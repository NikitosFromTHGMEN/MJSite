function go_to_next_page()
    {
        var current_page = document.getElementById('PageChanger').value
    	var page = parseInt(current_page) + 1;
    	var cur_location = document.location.href.split('/');
    	var new_href = cur_location[0] + "//" + cur_location[1] + "/" + cur_location[2] + '/' + cur_location[3] + '/' + page;

    	if(cur_location[4].split('?').length > 1)
    	   new_href += '?' + cur_location[4].split('?')[1];

    	document.location.href = new_href;
    }

function go_to_prev_page()
    {
        var current_page = document.getElementById('PageChanger').value
    	var page = parseInt(current_page) - 1;
    	var cur_location = document.location.href.split('/');
    	var new_href = cur_location[0] + "//" + cur_location[1] + "/" + cur_location[2] + '/' + cur_location[3] + '/' + page;

    	if(cur_location[4].split('?').length > 1)
    	   new_href += '?' + cur_location[4].split('?')[1];

    	document.location.href = new_href;
    }

function go_to_enter_page()
    {
    	var page = parseInt(document.getElementById('PageChanger').value);
    	var current_page_len = document.location.href.split("").reverse().join("").search("/");
    	var cur_location = document.location.href.split('/');
    	var new_href = cur_location[0] + "//" + cur_location[1] + "/" + cur_location[2] + '/' + cur_location[3] + '/' + page;

    	if(cur_location[4].split('?').length > 1)
    	   new_href += '?' + cur_location[4].split('?')[1];

    	document.location.href = new_href;
    }
