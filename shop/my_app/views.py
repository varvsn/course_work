from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.contrib.auth.forms import UserCreationForm - switched to my app RegistrationForm
from .help_functions import count_items
import datetime

from my_app.forms import Shop_Form, RegistrationForm
from my_app.models import Shop_Item, UsersAndOrders, Orders


def index(request):
    if request.method == 'GET':
        basket = request.session.get('basket', {})
        items_list = Shop_Item.objects.order_by('created_date')
        page = request.GET.get('page', 1)
        paginator = Paginator(items_list, 6)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)


        return render(request, 'index.html', {'items': items, 'basket_goods': basket, 'total_count': count_items(basket)})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'registration complete')
            return render(request, 'flash_page.html', {'form': form})
    else:
        form = RegistrationForm()

    return render(request, 'registration/registration_form.html', {'form': form})


def add_to_basket(request, item_id):
    if request.user.is_authenticated:
        messages.success(request, 'Item {} added!'.format(Shop_Item.objects.get(id=item_id)))
        basket = request.session.get('basket', {})
        basket[item_id] = 1 if item_id not in basket else (basket[item_id] + 1)
        request.session['basket'] = basket
        return render(request, 'flash_page.html', {'basket_goods': basket, 'total_count': count_items(basket)})
    else:
        messages.warning(request, "You need to login before buying something!")
        return render(request, 'flash_page.html')


def ajax_add_item(request, item_id):
    construct_basket(request, item_id, '+')
    return render(request, 'basket.html', {
                                  'new_basket': request.session['checkout'],
                                  'total_count': count_items(request.session.get('basket', {})),
                                  'total_price': request.session['total_price'],
                                  })


def ajax_del_item(request, item_id):
    construct_basket(request, item_id, '-')
    return render(request, 'basket.html', {
                                  'new_basket': request.session['checkout'],
                                  'total_count': count_items(request.session.get('basket', {})),
                                  'total_price': request.session['total_price'],
                                  })



def checkout(request):
    construct_basket(request)
    return render(request, 'basket.html', {
                                  'new_basket': request.session['checkout'],
                                  'total_count': count_items(request.session.get('basket', {})),
                                  'total_price': request.session['total_price'],
                                  })



def buy(request):
    if request.user.is_authenticated:
        try:
            with transaction.atomic():
                user_order = UsersAndOrders(user_id = request.user.id,
                                      order_date=datetime.datetime.now(),
                                      comment = 'No comment',
                                      total_sum = request.session['total_price'],
                                      )
                user_order.save()

                current_order_id = user_order.pk  #Take this saved order number
                for checkouts in request.session['checkout']:
                    detail_order = Orders(order_id = current_order_id,
                                        item_id = checkouts['id'],
                                        item_name = checkouts['item'],
                                        price = checkouts['price'],
                                        total_count = checkouts['count'],
                                        ordered_date = datetime.datetime.now()
                                        )
                    detail_order.save()

                messages.success(request, "Order id: {} saved!".format(current_order_id))
                messages.success(request, "Thanks for buying in the SHOP!")
                del request.session['total_price']
                del request.session['basket']
                del request.session['checkout']
                return render(request, 'flash_page.html')

        except IntegrityError:
            messages.warning(request, "Order id: {} was not saved properly! Contact Ded Moroz".format(order))
            return render(request, 'flash_page.html')
    else:
        messages.warning(request, "You need to login before!")
        return render(request, 'flash_page.html')


def lk(request):
    if request.user.is_authenticated:
        basket = request.session.get('basket', {})
        user_orders = UsersAndOrders.objects.filter(user_id=request.user.id)
        return render(request, 'lk.html', {'total_count': count_items(basket), 'user_orders': user_orders})
    else:
        messages.warning(request, "You need to login before")
        return render(request, 'flash_page.html')


def view_item(request, item_id):
    basket = request.session.get('basket', {})
    item = Shop_Item.objects.get(pk=item_id)
    return render(request, 'item_details.html', {'item': item, 'total_count': count_items(basket)})



def del_all(request):
    del request.session['basket']
    messages.warning(request, 'Your basket is empty now.')
    return render(request, 'flash_page.html', {'total_count': 0})


def construct_basket(request, item_id=False, changing=False):
    basket = request.session.get('basket', {})
    if changing == '+':
        basket[item_id] += 1
    if changing == '-':
        if basket[item_id] == 1:
            del basket[item_id]
        else:
            basket[item_id] -= 1
    items = Shop_Item.objects.filter(id__in=basket.keys())
    new_basket = []
    total_price = 0
    for it in items:
        total_price += basket[str(it.id)] * it.price
        new_basket.append({
                         'id': it.id,
                         'item': it.name,
                         'price': it.price,
                         'image': str(it.image),
                         'count': basket[str(it.id)],
                         'summary': basket[str(it.id)] * it.price,
                         })
    #Save all data to next 'buy' step in session
    request.session['total_price'] = total_price
    request.session['checkout'] = new_basket







