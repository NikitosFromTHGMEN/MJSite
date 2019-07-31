from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from base.models import UserProfile, ProductTags, Product, AdminProfile


def get_base_context(request, page_name):
    auth = []
    is_user_auth = False
    errors = []
    user_photo = ''
    admin_profile = ''

    if request.user.is_authenticated:
        is_user_auth = True
        auth.append({'link': '/logout/', 'text': 'Выйти'})
        user_profile = UserProfile.objects.get(user_id=User.objects.get(username=request.user).id)
        user_photo = user_profile.photo
        if request.user.is_superuser:
            admin_profile = AdminProfile.objects.get(user=user_profile)

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
        'admin_profile': admin_profile
    }

    return context



def is_existing_user(users_list, login):
    if login in [user.username for user in users_list]:
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
                    print("here:", tag.tag_name)
                    tags_list.append(tag.tag_name)

    return tags_list


def upload_photo(up_file, file_name, old_photo):
    fs = FileSystemStorage()
    print(old_photo)
    old_photo = old_photo.split(sep="/")[-1]
    print(old_photo)

    if old_photo != "":
        if fs.exists(old_photo):
            fs.delete(old_photo)

    fs.save(file_name, up_file)
    url = fs.url(file_name)

    return url

def delete_photo(photos, del_photos):
    fs = FileSystemStorage()

    del_photos = sorted([int(photo) for photo in del_photos.split(sep=";")[:-1]], reverse=True)
    photos_list = photos.split(sep=",")[:-1]

    for photo_number in del_photos:
        if fs.exists('/'.join(photos_list[photo_number].split(sep='/')[2:])):
            fs.delete('/'.join(photos_list[photo_number].split(sep='/')[2:]))
            photos_list.pop(photo_number)


    photos = ""

    for photo in photos_list:
        photos += photo + ","

    return photos



def get_user_info(request, user):
    return UserProfile.objects.get(user=User.objects.get(username=user).id)


def check_new_tags(type, color, stone, mg, md):
    lists = [
        {'list': type, 'name': 'simple'},
        {'list': color, 'name': 'color'},
        {'list': stone, 'name': 'stone'},
        {'list': mg, 'name': 'mgchar'},
        {'list': md, 'name': 'mdchar'}
    ]

    for cur_list in lists:
        for cur_tag in cur_list['list'].split(sep=";"):
            if not cur_tag in [tag.tag_name for tag in ProductTags.objects.filter(type=cur_list['name'])]:
                new_tag = ProductTags(tag_name=cur_tag, type=cur_list['name'])
                new_tag.save()


def tag_cleaning(tag_list):
    tags = tag_list.split(sep=";")
    tags_str = ""

    for tag in tags:
        tag = tag.strip().lower()
        if tag != '':
            tags_str += tag + ";"

    return tags_str.rstrip(';')


def process_tags(type, color, stone, mg, md):
    type = tag_cleaning(type)
    color = tag_cleaning(color)
    stone = tag_cleaning(stone)
    mg = tag_cleaning(mg)
    md = tag_cleaning(md)

    check_new_tags(type, color, stone, mg, md)
    tags_lists_list = [type, color, stone, mg, md]

    for counter in range(len(tags_lists_list)):
        try:
            tags_lists_list.remove('')
        except ValueError:
            continue

    tags = ""

    for tags_list in tags_lists_list:
        tags += tags_list + ';'

    return tag_cleaning(tags)


def check_existing_tags():
    for tag in ProductTags.objects.all():
        is_exists = False
        for product in Product.objects.all():
            if tag.tag_name in product.tags.split(sep=';'):
                is_exists = True
                break

        if not is_exists:
            tag.delete()


def separate_tags(tags):
    separated = {
        'simple': [],
        'color': [],
        'stone': [],
        'mgchar': [],
        'mdchar': [],
    }

    for tag in tags:
        filter_list = ProductTags.objects.filter(tag_name=tag)
        if len(filter_list) > 0:
            separated[filter_list[0].type].append(tag)

    return separated


def have_access(request, requirements):
    requirements_list = requirements.split(sep=",") if requirements != "" else []

    access_score = len(requirements_list)
    score = 0
    user = request.user
    user_profile = UserProfile.objects.get(user=user)

    if not user.is_superuser:
        return False

    admin_profile = AdminProfile.objects.get(user=user_profile)

    for requirement in requirements_list:
        r_t, r_v = requirement.split(sep=":")

        if r_t == "products":
            if r_v == "see":
                score += 1 if admin_profile.see_products_panel else 0
            elif r_v == "create":
                score += 1 if admin_profile.can_create_products else 0
            elif r_v == "edit":
                score += 1 if admin_profile.can_edit_products else 0
            elif r_v == "remove":
                score += 1 if admin_profile.can_remove_products else 0
            elif r_v == "distribute":
                score += 1 if admin_profile.can_distribute_products else 0
        elif r_t == "orders":
            if r_v == "see":
                score += 1 if admin_profile.see_orders_panel else 0
            elif r_v == "check":
                score += 1 if admin_profile.can_check_orders_info else 0
            elif r_v == "edit":
                score += 1 if admin_profile.can_edit_orders else 0
        elif r_t == "comments":
            if r_v == "see":
                score += 1 if admin_profile.see_comments_panel else 0
            if r_v == "delete":
                score += 1 if admin_profile.can_delete_comments else 0
        elif r_t == "admins":
            if r_v == "see":
                score += 1 if admin_profile.see_admins_panel else 0
            elif r_v == "ban":
                score += 1 if admin_profile.can_ban_users else 0
            elif r_v == "create":
                score += 1 if admin_profile.can_create_admins else 0
            elif r_v == "demote":
                score += 1 if admin_profile.can_demote_admins else 0
            elif r_v == "products":
                score += 1 if admin_profile.can_edit_products_section else 0
            elif r_v == "orders":
                score += 1 if admin_profile.can_edit_orders_section else 0
            elif r_v == "comments":
                score += 1 if admin_profile.can_edit_comments_section else 0
            elif r_v == "admins":
                score += 1 if admin_profile.can_edit_admins_section else 0

    return True if score == access_score else False








