def count_items(cart):
    i = 0
    for key in cart:
        i += cart[key]
    return i
