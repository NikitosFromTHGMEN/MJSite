from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response
from base.forms import SignInForm
from django.template import RequestContext
from base.functions import get_base_context, is_existing_user, get_request_products, upload_photo, get_user_info
from django.contrib.auth.hashers import check_password
import datetime

from base.models import UserProfile, Product, ProductTags, Comment, Orders


def user_login(request):
    context = get_base_context(request, "Авторизация")
    context['next'] = request.GET.get('next', '/')

    if request.POST:
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)

                if user.is_superuser:
                    return HttpResponseRedirect('/main_panel/')

                return HttpResponseRedirect(request.POST['next'])
            else:
                context['errors'] = "Данный аккаунт заблокирован"

    return render(request, 'registration/login.html', context=context)


def index_page(request):
    context = get_base_context(request, "Главная")
    return render(request, 'index.html', context=context)


def not_found_page(request, exception, template_name="404.html"):
    context = get_base_context(request, "Страница не найдена")
    response = render_to_response("404.html", context=context)
    response.status_code = 404
    return response


def server_error_page(request, template_name="500.html"):
    context = {'title': 'Ошибка сервера'}
    response = render_to_response("500.html", context=context)
    response.status_code = 500
    return response


def sign_up_page(request):
    context = get_base_context(request, "Регистрация")

    if request.method == 'POST':
        f = SignInForm(request.POST, request.FILES)

        if f.is_valid():
            login = f.data['login']
            fname = f.data['fname']
            lname = f.data['lname']
            date_of_birth = f.data['date_of_birth']
            email = f.data['email']
            pw = f.data['password']
            pw_c = f.data['password_conf']

            if not is_existing_user(User.objects.all(), login):
                if pw == pw_c:
                    new_user = User.objects.create_user(username=login, first_name=fname, last_name=lname, email=email,
                                                        password=pw)
                    new_user_info = UserProfile(user=new_user, date_of_birth=date_of_birth)
                    new_user.save()
                    new_user_info.save()
                    return HttpResponseRedirect('/login/')
                else:
                    context['errors'].append("Введенные пароли не совпадают")
            else:
                context['errors'].append("Пользователь с таким логином уже существует")

            context['form'] = f
        else:
            print('not valid')
            context['form'] = f
    else:
        f = SignInForm()
        context['form'] = f

    return render(request, 'registration/sign_up.html', context=context)


def profile_page(request, id):
    if len(User.objects.filter(id=id)) + len(UserProfile.objects.filter(user_id=id)) != 2:
        return HttpResponseRedirect('/404/')

    context = get_base_context(request, "Профиль")

    user = User.objects.get(id=id)
    user_info = UserProfile.objects.get(user_id=id)
    context['user'] = user
    context['reg_date'] = "{:02}.{:02}.{}".format(user.date_joined.day, user.date_joined.month, user.date_joined.year)
    context['date_of_birth'] = "{:02}.{:02}.{}".format(user_info.date_of_birth.day, user_info.date_of_birth.month,
                                            user_info.date_of_birth.year)
    context['user_photo'] = user_info.photo
    context['comments'] = Comment.objects.filter(author=user_info.id)
    context['last_orders'] = []
    orders_info = Orders.objects.filter(customer=user_info.id)
    counter = 0
    for order in reversed(orders_info):
        if counter == 24:
            break

        if counter % 6 == 0:
            orders_list = []
            context['last_orders'].append(orders_list)

        orders_list.append(order)
        counter += 1

    return render(request, 'profile.html', context=context)


def catalog_page(request):
    context = get_base_context(request, "Каталог")
    return render(request, 'catalog.html', context=context)


def product_page(request, id):
    if len(Product.objects.filter(id=id)) == 0:
        return HttpResponseRedirect('/404/')

    product_info = Product.objects.get(id=id)
    context = get_base_context(request, product_info.name)
    context['product'] = product_info
    context['tags'] = product_info.tags.split()
    # context['photos'] = product_info.photos.split()
    context['comments'] = Comment.objects.filter(product_id=product_info.id)

    return render(request, 'product.html', context=context)


def search_page(request):
    context = get_base_context(request, "Поиск")
    context['search_tags'] = ProductTags.objects.all()
    context['default_q'] = ""
    context['default_price_from'] = "0"
    context['default_price_to'] = "10000"

    if request.method == 'GET':
        if len(request.GET) > 0:
            q = request.GET.get('q', '')
            tags = request.GET.get('tags', '').split(sep=',')
            price = request.GET.get('price', '0,10000').split(sep=',')

            context['default_q'] = q
            context['default_price_from'] = price[0]
            context['default_price_to'] = price[1]
            context['products'] = []
            product_list = []
            products = Product.objects.all()
            words = q.split()

            if tags[0].isdigit():
                tags = get_request_products(req=tags, tags=context['search_tags'])


            for product in products:
                if not product.is_distributing:
                    continue

                tags_score = 0 if len(tags) > 0 else 1
                q_score = 0 if len(q) > 0 else 1
                price_score = 1 if product.price >= int(price[0]) and product.price <= int(price[1]) else 0

                for item in tags:
                    if item in product.tags.split():
                        tags_score += 1

                for word in words:
                    if product.name.lower().find(word.lower()) != -1:
                        q_score += 1

                if tags_score > 0 and q_score > 0 and price_score > 0:
                    product_list.append({'product': product, 'score': tags_score + q_score + price_score})

            product_list = sorted(product_list, key=lambda x: x['score'], reverse=True)

            for item in product_list:
                context['products'].append(item["product"])

    return render(request, 'search.html', context=context)


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
            return HttpResponseRedirect('/login/') if passwd_is_changed else render(request, 'settings.html', context=context)

    return render(request, 'settings.html', context=context)


@login_required
def upload_file(request):
    context = get_base_context(request)

    if request.method == 'POST':
        user_profile = get_user_info(request, user=request.user)
        uploaded_photo = request.FILES['document']
        url = upload_photo(uploaded_photo, uploaded_photo.name, user_profile.photo)
        user_profile.photo = url
        user_profile.save()

        return HttpResponseRedirect('/settings/')

    return render(request, 'upload.html', context=context)


@login_required
def create_order_page(request, id):
    context = get_base_context(request, "Оформление заказа")
    user_info = get_user_info(request, user=request.user)
    product = Product.objects.get(id=id)

    if len(Product.objects.filter(id=id)) == 0:
        return HttpResponseRedirect('/404/')

    if request.method == "POST":
        count = int(request.POST.get('count'))
        size = request.POST.get('size')
        phone = request.POST.get('phone_number')
        price = count * product.price

        print(price)

        new_order = Orders(customer=user_info, product=product, count=count, size=size, phone=phone, time=datetime.datetime.now(), price=price)
        new_order.save()

        return HttpResponseRedirect('/catalog/')

    else:
        context['order_number'] = len(Orders.objects.all()) + 1
        context['product'] = product
        context['user_info'] = user_info


    return render(request, 'create_order.html', context=context)


def orders_list_page(request, id):
    if len(User.objects.filter(id=id)) == 0:
        return HttpResponseRedirect('/404/')

    user = User.objects.get(id=id)
    user_info = get_user_info(request, user=user.username)

    context = get_base_context(request, "Все заказы")
    context['user_info'] = user_info
    context['orders'] = Orders.objects.filter(customer=user_info)

    return render(request, 'orders_list.html', context=context)


@login_required
def admin_main_panel_page(request):
    context = get_base_context(request, "Главная панель управления")

    if not request.user.is_superuser:
        context['title'] = "Ошибка доступа"
        return render(request, 'admin/permission_error.html', context=context)

    context['number_of_products'] = len(Product.objects.all())
    context['orders'] = {
        'total': len(Orders.objects.all()),
        'done': len(Orders.objects.filter(status='d')),
        'accept': len(Orders.objects.filter(status='a')),
        'new':  len(Orders.objects.filter(status='p'))
    }
    admins =  User.objects.filter(is_superuser=True)
    context['admins'] = {
        'count': len(admins),
        'profiles': admins
    }
    context['comments'] = {
        'total': len(Comment.objects.all()),
        'today': 0
    }


    return render(request, 'admin/admin_panel.html', context=context)


@login_required
def admin_products_panel_page(request, page):
    context = get_base_context(request, "Панель управления товарами")

    if not request.user.is_superuser:
        context['title'] = "Ошибка доступа"
        return render(request, 'admin/permission_error.html', context=context)


    if len(request.GET) > 0:
        delete_id = int(request.GET.get('delete', "-1"))
        distribute = request.GET.get('distribute', "-1")

        if distribute != "-1":
            val, product_id = map(int, distribute.split(sep=","))
            if len(Product.objects.filter(id=product_id)) > 0:
                product = Product.objects.get(id=product_id)
                product.is_distributing = val
                product.save()

        if len(Product.objects.filter(id=delete_id)) > 0:
            product = Product.objects.get(id=delete_id)
            for order in Orders.objects.filter(product=product.id):
                if order.status == 'p':
                    order.status = 'c'
                order.save()
            product.delete()

        return HttpResponseRedirect('/products_panel/' + page)

    products_on_page = 25
    products = []
    products_dbase = list(Product.objects.all())

    if len(products_dbase) != 0:
        if len(products_dbase) < products_on_page * (int(page) - 1):
            return HttpResponseRedirect('/404/')

        range_from = products_on_page * (int(page) - 1)
        range_to = range_from + products_on_page if range_from + products_on_page < len(products_dbase) else range_from + (len(products_dbase) - range_from)


        for i in range(range_from, range_to):
            products.append({'product': products_dbase[i], 'sold': len(Orders.objects.filter(product=products_dbase[i].id))})


    context['products'] = products
    context['pages'] = {
        'max': len(products_dbase) // products_on_page  if (len(products_dbase) / products_on_page) % 1 == 0 else len(products_dbase) // products_on_page + 1,
        'current': int(page)
    }


    return render(request, 'admin/products_panel.html', context=context)


@login_required
def admin_orders_panel_page(request):
    context = get_base_context(request, "Панель управления заказами")

    return render(request, 'admin/orders_panel.html', context=context)


@login_required
def admin_comments_panel_page(request):
    context = get_base_context(request, "Панель управления комментариями")

    return render(request, 'admin/comments_panel.html', context=context)


@login_required
def admin_admins_panel_page(request):
    context = get_base_context(request, "Панель управления администраторами")

    return render(request, 'admin/admins_panel.html', context=context)


@login_required
def create_product_page(request):
    context = get_base_context(request, "Добавить товар")

    if not request.user.is_superuser:
        context['title'] = "Ошибка доступа"
        return render(request, 'admin/permission_error.html', context=context)

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        type = request.POST.get('type')
        color = request.POST.get('color')
        stone = request.POST.get('stone')
        mg = request.POST.get('MG')
        md = request.POST.get('MD')
        short_description = request.POST.get('short_description')
        description = "<pre>" + request.POST.get('description') + "</pre>"

        tags = type.lower() + " " + color.lower() + " " + stone.lower() + " " + mg.lower() + " " + md.lower()
        photos = ""

        for photo in request.FILES.getlist('photos'):
            photos += upload_photo(photo, "products/product" + str(len(Product.objects.all())) + photo.name, "") + ","

        new_product = Product(name=name, price=price, tags=tags, preview_describe=short_description, describe=description, is_distributing=True, photo=photos)
        new_product.save()

    return render(request, 'admin/create_product.html', context=context)


@login_required
def edit_product_page(request):
    context = get_base_context(request, "Редактировать товар")

    if not request.user.is_superuser:
        context['title'] = "Ошибка доступа"
        return render(request, 'admin/permission_error.html', context=context)



    return render(request, 'admin/admins_panel.html', context=context)

