from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from base.functions import get_base_context, get_user_info, upload_photo, have_access
from base.models import UserProfile, Orders, Comment, Comment1, AdminProfile


def profile_page(request, id):
    if len(User.objects.filter(id=id)) + len(UserProfile.objects.filter(user_id=id)) != 2:
        return redirect('404')

    context = get_base_context(request, "Профиль")

    if len(UserProfile.objects.filter(user_id=request.user)) > 0:
        context['user_info'] = UserProfile.objects.get(user_id=request.user)

    user = User.objects.get(id=id)
    user_info = UserProfile.objects.get(user_id=id)
    context['user_profile'] = user
    context['user_profile_info'] = user_info
    context['comments'] = [{'comment': comment, 'product_photo': comment.product.photo.split(',')[0] if comment.product else ''} for comment in Comment.objects.filter(author=user_info.id)]
    context['comments_count'] = len(context['comments'])
    context['comments1'] = [{'comment': comment, 'product_photo': comment.product.photo.split(',')[0] if comment.product else ''} for comment in Comment1.objects.filter(author=user_info.id)]
    context['comments1_count'] = len(context['comments1'])
    context['last_orders'] = []
    orders_info = Orders.objects.filter(customer=user_info.id)
    counter = 0
    for order in reversed(orders_info):
        if counter == 24:
            break

        if counter % 6 == 0:
            orders_list = []
            context['last_orders'].append(orders_list)

        p_photo = order.product.photo.split(',')[0] if order.product else ''

        orders_list.append({'order': order, 'product_photo': p_photo})
        counter += 1

    return render(request, 'profile.html', context=context)


@login_required
def account_settings_page(request):
    context = get_base_context(request, "Настройки")
    context['user_info'] = get_user_info(request, user=request.user)

    if request.method == 'POST':
        user = User.objects.get(username=request.user)
        user_info = get_user_info(request, user=user.username)

        passwd_is_changed = False
        phone_is_changed = False
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        d_of_b = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        old_pass = request.POST.get('old_passwd')
        new_pass = request.POST.get('new_passwd')

        user.first_name = fname
        user.last_name = lname
        user.email = email

        if user_info.phone_number != phone:
            user_info.phone_number = phone
            phone_is_changed = True

        if d_of_b != "":
            user_info.date_of_birth = d_of_b

        if user.check_password(old_pass):
            user.set_password(new_pass)
            passwd_is_changed = True
        else:
            if old_pass != "":
                context['errors'].append("Старый пароль неверный")

        user.save()
        user_info.save()

        if passwd_is_changed or phone_is_changed:
            return redirect('login') if passwd_is_changed else redirect('settings')

    return render(request, 'settings.html', context=context)


@login_required
def upload_file(request):
    context = get_base_context(request, "Загрузка фотографии")

    if request.method == 'POST':
        user_profile = get_user_info(request, user=request.user)
        uploaded_photo = request.FILES['document']
        url = upload_photo(uploaded_photo, uploaded_photo.name, user_profile.photo)
        user_profile.photo = url
        user_profile.save()

        return redirect('settings')

    return render(request, 'upload.html', context=context)


def admin_appoint_page(request, id):
    if len(UserProfile.objects.filter(id=id)) == 0:
        return redirect('404')

    if not have_access(request, "admins:create") or UserProfile.objects.get(id=request.user.id).id == int(id):
        return redirect('permission_error')

    user = UserProfile.objects.get(id=id)
    context = get_base_context(request, "Назначить нового администратора")
    if len(AdminProfile.objects.filter(user=user)) > 0:
        context['edit_user_admin'] = AdminProfile.objects.get(user=user)
    context['user_profile'] = user

    if request.method == "POST":
        products = {
            'see': request.POST.get('ProductsCanSee'),
            'create': request.POST.get('ProductsCanCreate'),
            'edit': request.POST.get('ProductsCanEdit'),
            'remove': request.POST.get('ProductsCanRemove'),
            'distribute': request.POST.get('ProductsCanDistribute')
        }

        orders = {
            'see': request.POST.get('OrdersCanSee'),
            'check': request.POST.get('OrdersCanCheck'),
            'edit': request.POST.get('ProductsCanEdit')
        }

        comments = {
              'see': request.POST.get('CommentsCanSee'),
              'delete': request.POST.get('CommentsCanDelete')
        }

        admins = {
            'see': request.POST.get('AdminsCanSee'),
            'ban': request.POST.get('AdminsCanBanUsers'),
            'create_admin':request.POST.get('AdminsCanCreateAdmin'),
            'demote_admin': request.POST.get('AdminsCanDemoteAdmin'),
            'edit_products': request.POST.get('AdminsCanEditProducts'),
            'edit_orders': request.POST.get('AdminsCanEditOrders'),
            'edit_comments': request.POST.get('AdminsCanEditComments'),
            'edit_admins': request.POST.get('AdminsCanEditAdmins')
        }


        if len(AdminProfile.objects.filter(user_id=id)) > 0:
            admin_profile = AdminProfile.objects.get(user_id=id)

            if have_access(request, "admins:products"):
                admin_profile.see_products_panel=bool(products['see'])
                admin_profile.can_create_products=bool(products['create'])
                admin_profile.can_edit_products=bool(products['edit'])
                admin_profile.can_remove_products=bool(products['remove'])
                admin_profile.can_distribute_products=bool(products['distribute'])

            if have_access(request, "admins:orders"):
                admin_profile.see_orders_panel=bool(orders['see'])
                admin_profile.can_check_orders_info=bool(orders['check'])
                admin_profile.can_edit_orders=bool(orders['edit'])

            if have_access(request, "admins:comments"):
                admin_profile.see_comments_panel=bool(comments['see'])
                admin_profile.can_delete_comments=bool(comments['delete'])

            if have_access(request, "admins:admins"):
                admin_profile.see_admins_panel=bool(admins['see'])
                admin_profile.can_ban_users=bool(admins['ban'])
                admin_profile.can_create_admins=bool(admins['create_admin'])
                admin_profile.can_demote_admins=bool(admins['demote_admin'])
                admin_profile.can_edit_products_section=bool(admins['edit_products'])
                admin_profile.can_edit_orders_section=bool(admins['edit_orders'])
                admin_profile.can_edit_comments_section=bool(admins['edit_comments'])
                admin_profile.can_edit_admins_section=bool(admins['edit_admins'])
        else:
            admin_profile = AdminProfile(see_products_panel=bool(products['see']), can_create_products=bool(products['create']), can_edit_products=bool(products['edit']),
                                         can_remove_products=bool(products['remove']), can_distribute_products=bool(products['distribute']), see_orders_panel=bool(orders['see']),
                                         can_check_orders_info=bool(orders['check']), can_edit_orders=bool(orders['edit']), see_comments_panel=bool(comments['see']),
                                         can_delete_comments=bool(comments['delete']),see_admins_panel=bool(admins['see']), can_ban_users=bool(admins['ban']),
                                         can_create_admins=bool(admins['create_admin']), can_demote_admins=bool(admins['demote_admin']),
                                         can_edit_products_section=bool(admins['edit_products']), can_edit_orders_section=bool(admins['edit_orders']),
                                         can_edit_comments_section=bool(admins['edit_comments']), can_edit_admins_section=bool(admins['edit_admins']), user=user)

        user.user.is_superuser = True
        user.user.save()
        admin_profile.save()
        return redirect("admin_appoint", id=id)

    elif len(request.GET) > 0:
        action = request.GET.get('action', 'nothing')

        if action == "demote":
            if have_access(request, "admins:demote"):
                if len(AdminProfile.objects.filter(user_id=id)) > 0:
                    admin_profile = AdminProfile.objects.get(user_id=id)
                    admin_profile.delete()
                user.user.is_superuser = False
                user.user.save()
                return redirect("admin_appoint", id=id)
            else:
                return redirect("permission_error")

    return render(request, 'admin/appoint_admin.html', context=context)
