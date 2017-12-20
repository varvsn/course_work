from my_app.models import ShopSettings

def getsettings(request):
    s = ShopSettings.objects.values('name', 'value') #Grab settings from db
    settings = {}
    for i in s:
        settings[i['name']] = i['value']

    return {'settings': settings}