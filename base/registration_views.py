from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from base.forms import SignInForm
from base.functions import get_base_context, get_user_info
from base.models import UserProfile
from django.http import HttpResponseRedirect


def user_login(request, action=""):
    context = get_base_context(request, "Авторизация")
    context['next'] = request.GET.get('next', '/')

    if request.POST:
        username = request.POST.get('username', "")
        password = request.POST.get('password', "")

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user_profile = get_user_info(request, user)

                if user_profile.is_banned:
                    return redirect("account_banned", username=user.username)
                else:
                    login(request, user)

                    if user.is_superuser:
                        return redirect('admin_panel')

                return HttpResponseRedirect(request.POST['next'])

    return render(request, 'registration/login.html', context=context)


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

            if not login in [item.username for item in User.objects.all()]:
                if pw == pw_c:
                    new_user = User.objects.create_user(username=login, first_name=fname, last_name=lname, email=email,
                                                        password=pw)
                    new_user_info = UserProfile(user=new_user, date_of_birth=date_of_birth)
                    new_user.save()
                    new_user_info.save()
                    return redirect('/login/')
                else:
                    context['errors'].append("Введенные пароли не совпадают")
            else:
                context['errors'].append("Пользователь с таким логином уже существует")

            context['form'] = f
        else:
            context['form'] = f
    else:
        f = SignInForm()
        context['form'] = f

    return render(request, 'registration/sign_up.html', context=context)


def account_banned_page(request, username=""):
    user = User.objects.get(username=username)
    context = get_base_context(request, "Ваш аккаунт заблокирован!")
    user_info = get_user_info(request, user)
    context['reason'] = user_info.ban_reason
    context['user'] = user
    context['report_status'] = "not reported" if user_info.is_reported == 0 else "report cancelled" if user_info.is_reported == -1 else "reported"
    context['user_profile'] = user_info

    if user_info.is_reported == 0:
        if request.method == "POST":
            report_text = request.POST.get('report_text', '')

            user_info.is_reported = 1
            user_info.report_text = report_text
            user_info.save()
            return redirect('account_banned', username=username)

    return render(request, "registration/account_banned.html", context=context)




