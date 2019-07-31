function get_orders_status()
{
    var status_buttons = document.getElementsByName('status_btn');
    var current_page = document.location.href.split('/');
    var current_page_number = parseInt(current_page[current_page.length - 1]);

    var request = "/orders_panel/" + current_page_number + "?change=";

    for(var i = 0; i < status_buttons.length; ++i)
      {
        arr = status_buttons[i].src.split('/');
        status_btn_icon = arr[arr.length - 1];
        var order_id = parseInt(status_buttons[i].id.replace("StatusBtn", ""));
        var order_status = "";

        switch(status_btn_icon)
          {
              case 'process-icon.png':
                  order_status = "p";
              break;

              case 'abort-icon.png':
                  order_status = "c";
              break;

              case 'accept-icon.png':
                  order_status = "a";
              break;

              case 'done-icon.png':
                  order_status = "d";
              break;
          }

        request += order_id + "-" + order_status + ",";
      }


    var cur_location = document.location.href.split('/');
    var filter_pos = cur_location[cur_location.length - 1].search('filter');

    if(filter_pos != -1)
        request += "&" + cur_location[cur_location.length - 1].substring(filter_pos);

    SaveBtn.href = request;
}