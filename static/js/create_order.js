function get_sum()
    {
        var counter = document.getElementById("counter").value;
        var price = document.getElementById("price").innerHTML;

        document.getElementById('result_price').innerHTML = "Итого: " + parseInt(price) * parseInt(counter) + " рублей"
    }
