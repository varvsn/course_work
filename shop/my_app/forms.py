from django import forms
from my_app.models import Shop_Item
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Shop_Form(forms.ModelForm):
    class Meta:
        model = Shop_Item
        fields = (
            'name',
            'description',
            'price',
            'image',
            'created_date',
        )


class RegistrationForm(UserCreationForm):  #Add additional field - email, to built-in Django registration form
    email = forms.EmailField(required=True)  #See UserCreationForm in Django auth - forms

    def __init__(self, *args, **kwargs):  #Переопределяем класс, чтобы убрать тупорылые хелп-тесты
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user


class PerPageSelectForm(forms.Form):
    def __init__(self,request,*args,**kwargs):
        super (PerPageSelectForm,self).__init__(*args,**kwargs)
        CHOICES = (('6', '6'),('12', '12'),('999', 'All'))
        self.fields['item_per_page'] = forms.CharField(
                                                       initial = request.session.get('item_per_page', 6),
                                                       widget=forms.Select(
                                                                           choices=CHOICES,
                                                                           attrs={'class': 'custom-select', 
                                                                                  'onchange': 'this.form.submit()'
                                                                                 }
                                                                          )
                                                      )
