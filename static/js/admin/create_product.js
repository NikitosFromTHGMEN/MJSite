function add_item(type, placeholder)
    {
        var newDiv = document.createElement('div');
        newDiv.className = "parameters-info-item";

        var newElement = document.createElement('input');
        newElement.className = "info-item";
        newElement.name = type;
        newElement.type = "text";
        newElement.placeholder = placeholder;

        var newBtn = document.createElement('img');
        newBtn.onclick = function() {
                delete_item(this);
            };
        newBtn.className = "remove-item-btn";
        newBtn.src = "/static/images/abort-icon.png";
        newBtn.name = type + "_btn"

        newDiv.appendChild(newElement);
        newDiv.appendChild(newBtn);

        if(type == "colors")
            ColorsFormFields.appendChild(newDiv);
        else if(type == "stones")
            StonesFormFields.appendChild(newDiv);
        else if(type == "mg")
            MGFormFieilds.appendChild(newDiv);
        else if(type == "md")
            MDFormFieilds.appendChild(newDiv);
    }

function get_color_tags()
    {
        var color = document.getElementsByName("colors");
        var res = "";

        for(var i = 0; i < color.length; ++i)
            res += color[i].value + ';';

        document.getElementById("ColorTags").value = res;
    }

function get_stone_tags()
    {
        var stone = document.getElementsByName("stones");
        var res = "";

        for(var i = 0; i < stone.length; ++i)
            res += stone[i].value + ';';

        document.getElementById("StoneTags").value = res;
    }

function get_mg_tags()
    {
        var mg = document.getElementsByName("mg");
        var res = "";

        for(var i = 0; i < mg.length; ++i)
            res += mg[i].value + ';';

        document.getElementById("MGTags").value = res;
    }

function get_md_tags()
    {
        var md = document.getElementsByName("md");
        var res = "";

        for(var i = 0; i < md.length; ++i)
            res += md[i].value + ';';

        document.getElementById("MDTags").value = res;
    }


function delete_item(elem) {
    var name = elem.name

    elem.parentElement.remove()

    if(name == "colors_btn")
        get_color_tags();
    else if(name == "stones_btn")
        get_stone_tags();
    else if(name == "mg_btn")
        get_mg_tags();
    else if(name == "md_btn")
        get_md_tags()
}
