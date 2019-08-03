from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
import datetime, pytz
from base.functions import get_base_context, get_user_info, have_access
from base.models import Product, Orders, Comment, Comment1
from django.http import HttpResponseRedirect

@login_required
def permission_error_page(request):
    context = get_base_context(request, "Ошибка доступа")
    return render(request, "admin/permission_error.html", context=context)


def index_page(request):
    context = get_base_context(request, "Главная")
    return render(request, 'index.html', context=context)


def not_found_page(request, exception="", template_name="404.html"):
    context = get_base_context(request, "Страница не найдена")
    response = render_to_response("404.html", context=context)
    response.status_code = 404
    return response


def server_error_page(request, template_name="500.html"):
    context = {'title': 'Ошибка сервера'}
    response = render_to_response("500.html", context=context)
    response.status_code = 500
    return response


def measurement_manual_page(request):
    context = get_base_context(request, "Замер запястья")

    return render(request, "measurement_manual.html", context=context)


@login_required
def create_order_page(request, id):
    if len(Product.objects.filter(id=id)) == 0:
        return redirect('404')

    context = get_base_context(request, "Оформление заказа")
    user_info = get_user_info(request, user=request.user)
    product = Product.objects.get(id=id)

    if request.method == "POST":
        count = int(request.POST.get('count'))
        size = request.POST.get('size')
        phone = request.POST.get('phone_number')
        price = count * product.price
        wishes = request.POST.get('wishes')

        new_order = Orders(customer=user_info, product=product, count=count, size=size, phone=phone, time=datetime.datetime.now(), price=price, customer_status="n",
                           customer_wishes=wishes)
        new_order.save()

        return redirect('show_order', id=new_order.id)

    else:
        context['order_number'] = len(Orders.objects.all()) + 1
        context['product'] = product
        context['user_info'] = user_info
        context['photo'] = product.photo.split(sep=',')[0]

    return render(request, 'create_order.html', context=context)


def orders_list_page(request, id):
    if len(User.objects.filter(id=id)) == 0:
        return redirect('404')

    user = User.objects.get(id=id)
    user_info = get_user_info(request, user=user.username)

    context = get_base_context(request, "Все заказы")
    context['user_info'] = user_info
    context['orders'] = [{'order': order, 'comment': Comment1.objects.get(product=order.product, author=user_info) if len(Comment1.objects.filter(product=order.product, author=user_info)) else None} for order in Orders.objects.filter(customer=user_info)]
    context['orders_count'] = len(context['orders'])

    return render(request, 'orders_list.html', context=context)


@login_required
def show_order_page(request, id):
    if len(Orders.objects.filter(id=id)) > 0:
        order = Orders.objects.get(id=id)
    else:
        return redirect('404')

    if not have_access(request, "orders:check") and order.customer.id != get_user_info(request, request.user).id:
        return redirect('permission_error')

    context = get_base_context(request, "Заказ №" + str(order.id))
    context['order'] = order
    if order.product != None:
        context['photo'] = order.product.photo.split(sep=',')[0]

    return render(request, 'show_order.html', context=context)


@login_required
def create_comment_page(request, info):
    c_type, item_id = map(int, info.split(sep=","))

    print(request.POST)

    if request.method == "POST":
        comment_text = request.POST.get('comment_text', '')

        if c_type == 0:
            if len(Product.objects.filter(id=item_id)) > 0:
                product = Product.objects.get(id=item_id)

                Comment(author=get_user_info(request, request.user), product=product, text=comment_text, time=datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))).save()

                return redirect('product', id=item_id)
        elif c_type == 1:
            if len(Orders.objects.filter(id=item_id)) > 0:
                order = Orders.objects.get(id=item_id)

                if order.customer_id == get_user_info(request, request.user).id:
                    if order.status == "d":
                        Comment1(author=get_user_info(request, request.user), product=order.product, text=comment_text, time=datetime.datetime.now(tz=pytz.timezone('Europe/Moscow'))).save()
                        order.customer_status = "dc" if order.customer_status == "d" else "ndc"
                        order.save()
                        return redirect('my_orders', 1)

                return redirect('permission_error')

    return redirect('404')


@login_required
def delete_comment_page(request, comment):
    comment_type, comment_id = map(int, comment.split(sep=","))
    user_info = get_user_info(request, request.user)

    if comment_type:
        if Comment1.objects.filter(id=comment_id):
            comment = Comment1.objects.get(id=comment_id)
    else:
        if Comment.objects.filter(id=comment_id):
            comment = Comment.objects.get(id=comment_id)

    if comment.author.id == user_info.id:
        comment.delete()
        return HttpResponseRedirect(request.GET.get('next', '/profile/' + str(user_info.id)))

    return redirect('permission_error')



