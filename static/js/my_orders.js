function search_order() {
    search_field = document.getElementById("SearchOrderField");
    document.location.href = "/my_orders/1" + "?search=" + search_field.value;
}

function send_confirmation(order_id, val) {
    document.location.href = "/my_orders/1" + "?confirmation=" + order_id + "," + val;
}