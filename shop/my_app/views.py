from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction, IntegrityError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from django.contrib.auth.forms import UserCreationForm - switched to my app RegistrationForm
from .help_functions import count_items
import datetime
from django.http import JsonResponse

from my_app.forms import Shop_Form, RegistrationForm, PerPageSelectForm
from my_app.models import Shop_Item, UsersAndOrders, Orders


def user_session_settings(request, item_per_page=6):
    if request.method == 'POST':
        if request.POST.get('item_per_page', '') in ['6', '12', '999']:
            request.session['item_per_page'] = request.POST.get('item_per_page')
            return redirect('index')
        else:
            return redirect('index')


def index(request):
    if request.method == 'GET':
        select_per_page = PerPageSelectForm(request)
        basket = request.session.get('basket', {})
        items_list = Shop_Item.objects.order_by('created_date')
        page = request.GET.get('page', 1)
        item_per_page = request.session.get('item_per_page', '6')
        paginator = Paginator(items_list, item_per_page)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return render(request, 'index.html', {'items': items, 'basket_goods': basket, 'total_count': count_items(basket), 'select': select_per_page})


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
    if request.user.is_authenticated:
        construct_basket(request, item_id, '+')
        items = [a for a in request.session['checkout'] if a['id'] == int(item_id)]
        return JsonResponse({
                        'basket_total': count_items(request.session.get('basket', {})),
                        'basket_summary': request.session['total_price'],
                        'item_count': items[0]['count'],
                        'item_summary': items[0]['summary'],
                         })
    else:
        messages.warning(request, "You need to login before buying something!")
        return render(request, 'flash_page.html')

#        return render(request, 'basket.html', {
#                                  'new_basket': request.session['checkout'],
#                                  'total_count': count_items(request.session.get('basket', {})),
#                                  'total_price': request.session['total_price'],
#                                  })


def ajax_del_item(request, item_id):
    if request.user.is_authenticated:
        construct_basket(request, item_id, '-')
        items = [a for a in request.session['checkout'] if a['id'] == int(item_id)]
        return JsonResponse({
                        'basket_total': count_items(request.session.get('basket', {})),
                        'basket_summary': request.session['total_price'],
                        'item_count': items[0]['count'] if len(items) > 0 else 0,
                        'item_summary': items[0]['summary'] if len(items) > 0 else 0,
                         })
    else:
        messages.warning(request, "You need to login before buying something!")
        return render(request, 'flash_page.html')

#    return render(request, 'basket.html', {
#                                  'new_basket': request.session['checkout'],
#                                  'total_count': count_items(request.session.get('basket', {})),
#                                  'total_price': request.session['total_price'],
#                                  })



def checkout(request):
    if request.user.is_authenticated:
        construct_basket(request)
        return render(request, 'basket.html', {
                                      'new_basket': request.session['checkout'],
                                      'total_count': count_items(request.session.get('basket', {})),
                                      'total_price': request.session['total_price'],
                                      })
    else:
        messages.warning(request, "You need to login before buying something!")
        return render(request, 'flash_page.html')



def buy(request):
    if request.user.is_authenticated:
        if len(request.session['checkout']) == 0:
            messages.warning(request, 'Your basket is empty!')
            return render(request, 'flash_page.html', {'total_count': 0})

        try:
            with transaction.atomic():
                basket = request.session.get('basket', {})
                items = Shop_Item.objects.filter(id__in=basket.keys())
                for item_shop in items:  #Проверяем, есть ли данное кол-во заказа на складе
                    if basket[str(item_shop.id)] > item_shop.stock:
                        messages.error(request, "You try to buy more {} than we have in stock, sorry".format(item_shop.name))
                        return render(request, 'flash_page.html')
                #Сохраняем сам заказ
                user_order = UsersAndOrders(user_id = request.user.id,
                                      order_date=datetime.datetime.now(),
                                      comment = 'No comment',
                                      total_sum = request.session['total_price'],
                                      )
                user_order.save()
                #Сохраняем позиции в заказе
                current_order_id = user_order.pk  #Take this saved order number
                for checkouts in request.session['checkout']:
                    detail_order = Orders(order_id = current_order_id,
                                        item_id = checkouts['id'],
                                        item_name = checkouts['item'],
                                        price = checkouts['price'],
                                        total_count = checkouts['count'],
                                        ordered_date = datetime.datetime.now()
                                        )
                    item_stock = Shop_Item.objects.get(id = checkouts['id'])
                    item_stock.stock = item_shop.stock - basket[str(item_shop.id)]  #Обновляем сток по товару в позиции
                    detail_order.save()
                    item_stock.save()

                messages.success(request, "Order id: {} saved!".format(current_order_id))
                messages.success(request, "Thanks for buying in the SHOP!")
                del request.session['total_price']
                del request.session['basket']
                del request.session['checkout']
                return render(request, 'flash_page.html')

        except IntegrityError as e:
            messages.warning(request, "Order was not saved properly! Contact Ded Moroz {}".format(e))
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







