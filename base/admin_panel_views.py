from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from base.functions import get_base_context, check_existing_tags, have_access, get_user_info
from base.models import Orders, Comment, Product, UserProfile, Comment1
import datetime, re


@login_required
def admin_main_panel_page(request):
    context = get_base_context(request, "Главная панель управления")

    if not have_access(request, ""):
        return redirect('permission_error')

    context['number_of_products'] = len(Product.objects.all())
    context['orders'] = {
        'total': len(Orders.objects.all()),
        'done': len(Orders.objects.filter(status='d')),
        'accept': len(Orders.objects.filter(status='a')),
        'new':  len(Orders.objects.filter(status='p'))
    }
    admins = User.objects.filter(is_superuser=True)
    context['admins'] = {
        'count': len(admins),
        'profiles': admins
    }
    context['comments'] = {
        'с_total': len(Comment.objects.all()),
        'c1_total': len(Comment1.objects.all()),
        'с_today': len([comment for comment in Comment.objects.all() if datetime.date.today() == (comment.time + datetime.timedelta(seconds=10800)).date()]),
        'с1_today': len([comment for comment in Comment1.objects.all() if datetime.date.today() == (comment.time + datetime.timedelta(seconds=10800)).date()])
    }

    return render(request, 'admin/admin_panel.html', context=context)


@login_required
def admin_products_panel_page(request, page):
    context = get_base_context(request, "Панель управления товарами")

    if not have_access(request, "products:see"):
        return redirect('permission_error')

    products_on_page = 25
    products = []
    products_dbase = list(Product.objects.all())

    if len(request.GET) > 0:
        delete_id = int(request.GET.get('delete', "-1"))
        distribute = request.GET.get('distribute', "-1")
        search = request.GET.get('search', "")

        if search != "":
            words = search.split()
            new_products = []

            for product in products_dbase:
                score = 0

                for word in words:
                    if product.name.lower().find(word.lower()) != -1:
                        score += 1

                if score > 0:
                    new_products.append({'product': product, 'score': score})

            new_products = sorted(new_products, key=lambda x: x['score'], reverse=True)

            products_dbase = [product['product'] for product in new_products]

        else:
            if distribute != "-1":
                if have_access(request, "products:distribute"):
                    val, product_id = map(int, distribute.split(sep=","))
                    if len(Product.objects.filter(id=product_id)) > 0:
                        product = Product.objects.get(id=product_id)
                        product.is_distributing = val
                        product.save()
                else:
                    return redirect('permission_error')

            if len(Product.objects.filter(id=delete_id)) > 0:
                if have_access(request, "products:remove"):
                    product = Product.objects.get(id=delete_id)
                    for order in Orders.objects.filter(product=product.id):
                        if order.status == 'p':
                            order.status = 'c'
                            order.cancel_reason = 'Товар удалён'
                        order.save()
                    product.delete()
                    check_existing_tags()
                else:
                    return redirect("permission_error")

            return redirect('products_panel', page=page)

    if len(products_dbase) != 0:
        if len(products_dbase) <= products_on_page * (int(page) - 1):
            return redirect('404')

        range_from = products_on_page * (int(page) - 1)
        range_to = range_from + products_on_page if range_from + products_on_page < len(products_dbase) else range_from + (len(products_dbase) - range_from)

        for i in range(range_from, range_to):
            products.append({'product': products_dbase[i], 'sold': len(Orders.objects.filter(product=products_dbase[i].id)), 'photo': products_dbase[i].photo.split(",")[0]})

    context['products'] = products
    context['pages'] = {
        'max': len(products_dbase) // products_on_page  if (len(products_dbase) / products_on_page) % 1 == 0 else len(products_dbase) // products_on_page + 1,
        'current': int(page)
    }

    return render(request, 'admin/products_panel.html', context=context)


@login_required
def admin_orders_panel_page(request, page):
    context = get_base_context(request, "Панель управления заказами")

    if not have_access(request, "orders:see"):
        return redirect('permission_error')

    orders_on_page = 25
    orders = []
    orders_dbase = [{'order': order, 'product_photo': order.product.photo.split(sep=",")[0] if order.product != None else ""} for order in Orders.objects.all()]

    if len(request.GET) > 0:
        change_orders = request.GET.get('change', '')
        status_filter = request.GET.get('filter', '')

        if change_orders != "":
            if have_access(request, "orders:edit"):
                change_orders = change_orders.split(sep=",")[:-1]

                for change_order in change_orders:
                    order_attrs = change_order.split(sep="-")

                    if len(Orders.objects.filter(id=int(order_attrs[0]))) > 0:
                        order = Orders.objects.get(id=int(order_attrs[0]))
                        order.status = order_attrs[1]
                        order.save()

                return redirect('orders_panel', page=page)
            else:
                return redirect("permission_error")

        if status_filter != "":
            orders_dbase = [{'order': order, 'product_photo': order.product.photo.split(sep=",")[0] if order.product != None else ""} for order in Orders.objects.filter(status=status_filter)]

    if len(orders_dbase) != 0:
        if len(orders_dbase) <= orders_on_page * (int(page) - 1):
            return redirect('404')

        range_from = orders_on_page * (int(page) - 1)
        range_to = range_from + orders_on_page if range_from + orders_on_page < len(orders_dbase) else range_from + (len(orders_dbase) - range_from)

        for i in range(range_from, range_to):
            orders.append(orders_dbase[i])

    context['orders'] = reversed(orders)
    context['pages'] = {
        'max': len(orders_dbase) // orders_on_page  if (len(orders_dbase) / orders_on_page) % 1 == 0 else len(orders_dbase) // orders_on_page + 1,
        'current': int(page)
    }

    return render(request, 'admin/orders_panel.html', context=context)


@login_required
def admin_comments_panel_page(request, page):
    context = get_base_context(request, "Панель управления комментариями")

    if not have_access(request, "comments:see"):
        return redirect('permission_error')

    comments_on_page = 25
    comments = []
    comments1 = []
    comments_dbase = Comment.objects.all()
    comments1_dbase = Comment1.objects.all()
    context['comments_count'] = len(comments_dbase)
    context['comments1_count'] = len(comments1_dbase)

    if len(request.GET) > 0:
        time_filter = request.GET.get('filter', '')
        delete = request.GET.get('delete', '-1')

        if delete != '-1':
            if have_access(request, "comments:delete"):
                del_type, del_id = delete.split(sep=',')
                del_type = int(del_type)
                del_id = int(del_id)

                if del_type:
                    if len(Comment1.objects.filter(id=del_id)) > 0:
                        comment = Comment1.objects.get(id=del_id)
                        comment.delete()
                else:
                    if len(Comment.objects.filter(id=del_id)) > 0:
                        comment = Comment.objects.get(id=del_id)
                        comment.delete()

                return redirect('comments_panel', page=page)

            return redirect('permission_error')

        if time_filter != "":
            if time_filter == "today":
                comments_dbase = [comment for comment in Comment.objects.all() if datetime.date.today() == (comment.time + datetime.timedelta(seconds=10800)).date()]
                comments1_dbase = [comment for comment in Comment1.objects.all() if datetime.date.today() == (comment.time + datetime.timedelta(seconds=10800)).date()]
            else:
                if re.match('\d{2}\.\d{2}\.\d{4}', time_filter) != None:
                    comments_dbase = [comment for comment in Comment.objects.all() if datetime.datetime.strptime(time_filter, "%d.%m.%Y").date() == (comment.time + datetime.timedelta(seconds=10800)).date()]
                    comments1_dbase = [comment for comment in Comment1.objects.all() if datetime.date.today() == (comment.time + datetime.timedelta(seconds=10800)).date()]
                else:
                    comments_dbase = []
                    comments1_dbase = []

    if len(comments_dbase) > comments_on_page * (int(page) - 1):
        range_from = comments_on_page * (int(page) - 1)
        range_to = range_from + comments_on_page if range_from + comments_on_page < len(comments_dbase) else range_from + (len(comments_dbase) - range_from)

        for i in range(range_from, range_to):
            comments.append(comments_dbase[i])

    if len(comments1_dbase) > comments_on_page * (int(page) - 1):
        range_from = comments_on_page * (int(page) - 1)
        range_to = range_from + comments_on_page if range_from + comments_on_page < len(comments1_dbase) else range_from + (len(comments1_dbase) - range_from)

        for i in range(range_from, range_to):
            comments1.append(comments1_dbase[i])

    if not comments and not comments1:
        return redirect('404')

    context['comments'] = reversed(comments)
    context['comments1'] = reversed(comments1)
    context['cur_comments_count'] = len(comments)
    context['cur_comments1_count'] = len(comments1)
    context['pages'] = {
        'max': len(comments_dbase) // comments_on_page  if (len(comments_dbase) / comments_on_page) % 1 == 0 else len(comments_dbase) // comments_on_page + 1,
        'current': int(page)
    }

    return render(request, 'admin/comments_panel.html', context=context)


@login_required
def admin_admins_panel_page(request, page):
    context = get_base_context(request, "Панель управления пользователями")

    if not have_access(request, "admins:see"):
        return redirect('permission_error')

    users_on_page = 25
    users = []
    users_dbase = UserProfile.objects.all()

    if len(request.GET) > 0:
        search = request.GET.get('search', "")
        ban = request.GET.get('ban', "-1")
        ban_report = request.GET.get('ban_report', "-1")
        status_filter = request.GET.get('filter', '')

        if search != "":
            words = search.split()
            new_users = []

            for user in users_dbase:
                score = 0

                for word in words:
                    if user.user.first_name.lower().find(word.lower()) != -1:
                        score += 1
                    if user.user.last_name.lower().find(word.lower()) != -1:
                        score += 1

                if score > 0:
                    new_users.append({'user': user, 'score': score})

            new_users = sorted(new_users, key=lambda x: x['score'], reverse=True)

            users_dbase = [user['user'] for user in new_users]

        elif status_filter != "":
            if status_filter == "banned":
                users_dbase = UserProfile.objects.filter(is_banned=True)
            elif status_filter == "admins":
                users_dbase = [item  for item in users_dbase if item.user.is_superuser]

        elif ban != "-1":
            if have_access(request, "admins:ban"):
                val, user_id, reason = ban.split(sep=",")
                val = int(val)
                user_id = int(user_id)
                if len(User.objects.filter(id=user_id)) > 0:
                    user = User.objects.get(id=user_id)
                    user_profile = get_user_info(request, user)
                    user_profile.is_banned = val
                    user_profile.is_reported = 0
                    user_profile.report_text = ""
                    user_profile.ban_reason = reason
                    user.save()
                    user_profile.save()

                return redirect('admins_panel', page=page)
            return redirect('permission_error')

        if ban_report != "-1":
            if have_access(request, "admins:ban"):
                val, user_id = map(int, ban_report.split(sep=","))

                if len(User.objects.filter(id=user_id)) > 0:
                    user = User.objects.get(id=user_id)
                    user_profile = get_user_info(request, user)
                    if val:
                        user_profile.is_banned = 0
                        user_profile.is_reported = 0
                        user_profile.ban_reason = ""
                        user_profile.report_text = ""
                    else:
                        user_profile.is_reported = -1

                    user_profile.save()

                return redirect('admins_panel', page=page)
            return redirect("permission_error")


    if len(users_dbase) != 0:
        if len(users_dbase) <= users_on_page * (int(page) - 1):
            return redirect('404')

        range_from = users_on_page * (int(page) - 1)
        range_to = range_from + users_on_page if range_from + users_on_page < len(users_dbase) else range_from + (len(users_dbase) - range_from)

        for i in range(range_from, range_to):
            users.append(users_dbase[i])

    context['users'] = users
    context['pages'] = {
        'max': len(users_dbase) // users_on_page  if (len(users_dbase) / users_on_page) % 1 == 0 else len(users_dbase) // users_on_page + 1,
        'current': int(page)
    }

    return render(request, 'admin/admins_panel.html', context=context)