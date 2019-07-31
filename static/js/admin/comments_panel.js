function search_comment() {
    search_field = document.getElementById("SearchCommentField");
    document.location.href = "/comments_panel/1" + "?filter=" + search_field.value;
}