function check_all_admins(ind) {
    switch(ind) {
        case 1:
            if(!AdminsCanSee.checked) {
                AdminsCanBanUsers.checked = false;
                AdminsCanCreateAdmin.checked = false;
                AdminsCanDemoteAdmin.checked = false;
                AdminsCanEditProducts.checked = false;
                AdminsCanEditOrders.checked = false;
                AdminsCanEditComments.checked = false;
                AdminsCanEditAdmins.checked = false;
            }
        break;

        case 2:
        case 4:
            AdminsCanSee.checked = true;

        case 3:
            if(!AdminsCanCreateAdmin) {
                AdminsCanEditProducts.checked = false;
                AdminsCanEditOrders.checked = false;
                AdminsCanEditComments.checked = false;
                AdminsCanEditAdmins.checked = false;
            }
            else
                AdminsCanSee.checked = true;
        break;

        case 5:
        case 6:
        case 7:
        case 8:
            AdminsCanSee.checked = true;
            AdminsCanCreateAdmin.checked = true;
        break;
    }
}


function check_all_products(ind) {
    switch(ind) {
        case 1:
            if(!ProductsCanSee.checked) {
                ProductsCanCreate.checked = false;
                ProductsCanEdit.checked = false;
                ProductsCanRemove.checked = false;
                ProductsCanDistribute.checked = false;
            }
        break;

        case 2:
        case 3:
        case 4:
        case 5:
            ProductsCanSee.checked = true;
        break;
    }
}

function check_all_orders(ind) {
    switch(ind) {
        case 1:
            if(!OrdersCanSee.checked) {
                OrdersCanCheck.checked = false;
                OrdersCanEdit.checked = false;
            }
        break;

        case 2:
        case 3:
            OrdersCanSee.checked = true;
        break;
    }
}

function check_all_comments(ind) {
    switch(ind) {
        case 1:
            if(!CommentsCanSee.checked) {
                CommentsCanDelete.checked = false;
            }
        break;

        case 2:
            CommentsCanSee.checked = true;
        break;
    }
}



function check_all_rights(c_pb, c_ob, c_cb, c_ab, pb_see, pb_create, pb_edit, pb_remove, pb_distribute, ob_see, ob_check, ob_edit, cb_see, cb_delete, ab_see, ab_ban, ab_create,
                          ab_demote, ab_edit_products, ab_edit_orders, ab_edit_comments, ab_edit_admins) {
    if(c_pb == "True") {
        if(pb_see == "True") ProductsCanSee.checked = true;
        if(pb_create == "True") ProductsCanCreate.checked = true;
        if(pb_edit == "True") ProductsCanEdit.checked = true;
        if(pb_remove == "True") ProductsCanRemove.checked = true;
        if(pb_distribute == "True") ProductsCanDistribute.checked = true;
    }

    if(c_ob == "True") {
        if(ob_see == "True") OrdersCanSee.checked = true;
        if(ob_check == "True") OrdersCanCheck.checked = true;
        if(ob_edit == "True") OrdersCanEdit.checked = true;
    }

    if(c_cb == "True") {
        if(cb_see == "True") CommentsCanSee.checked = true;
        if(cb_delete == "True") CommentsCanDelete.checked = true;
    }

    if(c_ab == "True"){
        if(ab_see == "True") AdminsCanSee.checked = true;
        if(ab_ban == "True") AdminsCanBanUsers.checked = true;
        if(ab_create == "True") AdminsCanCreateAdmin.checked = true;
        if(ab_demote == "True") AdminsCanDemoteAdmin.checked = true;
        if(ab_edit_products == "True") AdminsCanEditProducts.checked = true;
        if(ab_edit_orders == "True") AdminsCanEditOrders.checked = true;
        if(ab_edit_comments == "True") AdminsCanEditComments.checked = true;
        if(ab_edit_admins == "True") AdminsCanEditAdmins.checked = true;
    }
}

