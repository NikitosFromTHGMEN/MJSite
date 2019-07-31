function delete_photo(photo_number) {
    var photo = document.getElementById('Photo' + photo_number);
    var btn = document.getElementById('DelPhoto' + photo_number + 'Btn');
    var field = document.getElementById("RemovePhoto");

    photo.remove();
    btn.remove();

    field.value = field.value + photo_number + ";"
}