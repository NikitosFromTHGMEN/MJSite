from base.functions import get_request_products, upload_photo, process_tags, check_existing_tags, separate_tags, delete_photo
from base.models import Product, ProductTags, Comment, Comment1, UserProfile
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from base.views import get_base_context, have_access


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
                print(tags)

            for product in products:
                if not product.is_distributing:
                    continue

                tags_score = 0 if len(tags) > 0 else 1
                q_score = 0 if len(q) > 0 else 1
                price_score = 1 if product.price >= int(price[0]) and product.price <= int(price[1]) else 0

                for item in tags:
                    if item in product.tags.split(';'):
                        tags_score += 1

                for word in words:
                    if product.name.lower().find(word.lower()) != -1:
                        q_score += 1

                if tags_score >= len(tags) and q_score > 0 and price_score > 0:
                    product_list.append({'product': product, 'score': tags_score + q_score + price_score})

            product_list = sorted(product_list, key=lambda x: x['score'], reverse=True)

            for item in product_list:
                context['products'].append({'product': item["product"], 'photo': item["product"].photo.split(",")[0]})

    return render(request, 'search.html', context=context)


def product_page(request, id):
    if len(Product.objects.filter(id=id)) == 0:
        return redirect('404')

    product_info = Product.objects.get(id=id)
    context = get_base_context(request, product_info.name)
    context['product'] = product_info
    context['tags'] = product_info.tags.split(sep=";")
    context['comments'] = Comment.objects.filter(product_id=product_info.id)
    context['comments_count'] = len(context['comments'])
    context['comments1'] = Comment1.objects.filter(product_id=product_info.id)
    context['comments1_count'] = len(context['comments1'])

    if request.user.is_authenticated:
        context['user_info'] = UserProfile.objects.get(user_id=request.user.id)

    photos = product_info.photo.split(sep=",")
    photos_list = []
    photos_group = []

    for i in range(len(photos)):
        if photos[i] != '':
            photos_group.append(photos[i])

            if (i + 1) % 3 == 0:
                photos_list.append(photos_group)
                photos_group = []
        else:
            if len(photos_group) > 0:
                photos_list.append(photos_group)

    context['photos_list'] = photos_list

    return render(request, 'product.html', context=context)


def catalog_page(request, page):
    context = get_base_context(request, "Каталог")

    products_on_page = 24
    products = []
    products_dbase = list(Product.objects.all())
    number_of_products = len(products_dbase)

    if number_of_products != 0:
        if number_of_products < products_on_page * (int(page) - 1):
            return redirect('404')

        range_from = number_of_products - 1 - products_on_page * (int(page) - 1)
        range_to = range_from - products_on_page if range_from - products_on_page > 0 else -1

        for i in range(range_from, range_to, -1):
            cur_product = products_dbase[i]
            if cur_product.is_distributing:
                products.append({'product': cur_product,  'photo': cur_product.photo.split(sep=',')[0]})

    context['products'] = products
    context['pages'] = {
        'max': len(products_dbase) // products_on_page  if (len(products_dbase) / products_on_page) % 1 == 0 else len(products_dbase) // products_on_page + 1,
        'current': int(page)
    }

    return render(request, 'catalog.html', context=context)


@login_required
def create_product_page(request):
    context = get_base_context(request, "Добавить товар")

    if not have_access(request, "products:create"):
        return redirect('permission_error')

    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        type = request.POST.get('type')
        color = request.POST.get('color')
        stone = request.POST.get('stone')
        mg = request.POST.get('MG')
        md = request.POST.get('MD')
        short_description = request.POST.get('short_description')
        description = "<pre class=\"info-block-text\">" + request.POST.get('description') + "</pre>"

        tags = process_tags(type=type, color=color, stone=stone, mg=mg, md=md)

        photos = ""

        for photo in request.FILES.getlist('photos'):
            photos += upload_photo(photo, "products/product" + str(len(Product.objects.all())) + "/" + photo.name, "") + ","

        new_product = Product(name=name, price=price, tags=tags, preview_describe=short_description, describe=description, is_distributing=True, photo=photos)
        new_product.save()

        return redirect('product', id=str(new_product.id))

    return render(request, 'admin/create_product.html', context=context)


@login_required
def edit_product_page(request, id):
    if not have_access(request, "products:edit"):
            return redirect('permission_error')

    if len(Product.objects.filter(id=id)) == 0:
        return redirect('404')

    context = get_base_context(request, "Редактировать товар")
    context['product'] = Product.objects.get(id=id)
    context['product_tags'] = separate_tags(context['product'].tags.split(sep=";"))
    context['product_description'] = context['product'].describe[29:-6]

    photos = context['product'].photo.split(sep=",")
    photos_list = []
    photos_group = []

    for i in range(len(photos)):
        if photos[i] != '':
            photos_group.append({'photo': photos[i], 'number': i})

            if (i + 1) % 3 == 0:
                photos_list.append(photos_group)
                photos_group = []
        else:
            if len(photos_group) > 0:
                photos_list.append(photos_group)

    context['photos_list'] = photos_list


    if request.method == "POST":
        name = request.POST.get('name')
        price = request.POST.get('price')
        type = request.POST.get('type')
        color = request.POST.get('color')
        stone = request.POST.get('stone')
        mg = request.POST.get('MG')
        md = request.POST.get('MD')
        short_description = request.POST.get('short_description')
        description = "<pre class=\"info-block-text\">" + request.POST.get('description') + "</pre>"
        remove_photos = request.POST.get('del_photos')

        tags = process_tags(type=type, color=color, stone=stone, mg=mg, md=md)

        photos = context['product'].photo

        photos = delete_photo(photos, remove_photos)

        for photo in request.FILES.getlist('photos'):
            photos += upload_photo(photo, "products/product" + str(len(Product.objects.all())) + "/" + photo.name, "") + ","

        context['product'].name = name
        context['product'].price = price
        context['product'].tags = tags
        context['product'].preview_describe = short_description
        context['product'].describe = description
        context['product'].photo = photos
        context['product'].save()
        check_existing_tags()

        return redirect('product', id=str(context['product'].id))

    return render(request, 'admin/edit_product.html', context=context)