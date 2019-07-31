function search_product() {
    search_field = document.getElementById("SearchProductField");
    document.location.href = "/products_panel/1" + "?search=" + search_field.value;
}