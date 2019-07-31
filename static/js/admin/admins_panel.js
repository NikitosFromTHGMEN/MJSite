function search_user() {
    search_field = document.getElementById("SearchUserField");
    document.location.href = "/admins_panel/1" + "?search=" + search_field.value;
}

function ban_submit(user_id) {
    var parameters = "?ban=1," + user_id + "," + document.getElementById("BanReasonArea" + user_id).value;
    document.location.href += parameters;
}


