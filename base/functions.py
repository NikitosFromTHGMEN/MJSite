from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from base.models import UserProfile, ProductTags



def get_base_context(request, page_name):
    auth = []
    is_user_auth = False
    errors = []
    user_photo = ''

    if request.user.is_authenticated:
        is_user_auth = True
        auth.append({'link': '/logout/', 'text': 'Выйти'})
        user_photo = UserProfile.objects.get(user_id=User.objects.get(username=request.user).id).photo
    else:
        auth.append({'link': '/login/', 'text': 'Войти'})
        auth.append({'link': '/sign_up/', 'text': 'Регистрация'})

    context = {
        'auth': auth,
        'is_user_auth': is_user_auth,
        'errors': errors,
        'user': request.user,
        'user_photo': user_photo,
        'title': page_name,
    }

    return context


def is_existing_user(users_list, login):
    for user in users_list:
        if user.username == login:
            return True

    return False


def get_request_products(req, tags):
    tags_list = []
    search_tag_types = ['simple', 'color', 'stone', 'mgchar', 'mdchar']

    for i in range(len(req)):
        count = 0

        for tag in tags:
            if tag.type == search_tag_types[i]:
                count += 1

                if count == int(req[i]):
                    tags_list.append(tag.tag_name)

    return tags_list


def upload_photo(up_file, file_name, old_photo):
    fs = fs = FileSystemStorage()
    old_photo = old_photo.split(sep="/")[-1]

    if old_photo != "":
        if fs.exists(old_photo):
            fs.delete(old_photo)

    fs.save(file_name, up_file)
    url = fs.url(file_name)

    return url


def get_user_info(request, user):
    return UserProfile.objects.get(user=User.objects.get(username=user).id)


def check_new_tags(type, color, stone, mg, md):

    for type_tag in type.split():
        type_tag = type_tag.lower()
        if not type_tag in [tag.tag_name for tag in ProductTags.objects.filter(type="simple")]:
            new_tag = ProductTags(tag_name=type_tag, type="simple")
            new_tag.save()

    for color_tag in color.split():
        color_tag = color_tag.lower()
        if not color_tag in [tag.tag_name for tag in ProductTags.objects.filter(type="color")]:
            new_tag = ProductTags(tag_name=color_tag, type="color")
            new_tag.save()

    for stone_tag in stone.split():
        stone_tag = stone_tag.lower()
        if not stone_tag in [tag.tag_name for tag in ProductTags.objects.filter(type="stone")]:
            new_tag = ProductTags(tag_name=stone_tag, type="stone")
            new_tag.save()

    for mg_tag in mg.split():
        mg_tag = mg_tag.lower()
        if not mg_tag in [tag.tag_name for tag in ProductTags.objects.filter(type="mgchar")]:
            new_tag = ProductTags(tag_name=mg_tag, type="mgchar")
            new_tag.save()

    for md_tag in md.split():
        md_tag = md_tag.lower()
        if not md_tag in [tag.tag_name for tag in ProductTags.objects.filter(type="mdchar")]:
            new_tag = ProductTags(tag_name=md_tag, type="mdchar")
            new_tag.save()







