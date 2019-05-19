function go_to_next_page()
    {
    	var page = parseInt(document.getElementById('PageChanger').value) + 1;
    	document.location.href = '/products_panel/' + page;
    }

function go_to_prev_page()
    {
    	var page = parseInt(document.getElementById('PageChanger').value) - 1;
    	document.location.href = '/products_panel/' + page;
    }

function go_to_enter_page()
    {
    	var page = parseInt(document.getElementById('PageChanger').value);
    	document.location.href = '/products_panel/' + page;
    }

