from django.db import models
from django.utils import timezone

class Shop_Item(models.Model):
    name = models.CharField(max_length=10)
    description = models.CharField(max_length=255, blank=True, null=True)
    features = models.CharField(max_length=2000, blank=True, null=True)
    price = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField()
    image_add1 = models.ImageField()
    image_add2 = models.ImageField()
    image_add3 = models.ImageField()

    class Meta:
        verbose_name = 'All shop item'

    def __str__(self):
        return self.name


class UsersAndOrders(models.Model):
    user_id = models.IntegerField()
    order_date = models.DateTimeField()
    comment = models.CharField(max_length=255, blank=True, null=True)
    total_sum = models.IntegerField()

    class Meta:
        verbose_name = 'User Order'

    def save(self, **kwargs):
        super(UsersAndOrders, self).save(**kwargs)

    def __str__(self):
        return str(self.id)


class Orders(models.Model):
    #order_id = models.IntegerField()
    item_id = models.IntegerField()
    item_name = models.CharField(max_length=10)
    total_count = models.IntegerField()
    price = models.IntegerField()
    ordered_date = models.DateTimeField()
    order = models.ForeignKey(UsersAndOrders, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Orders detail'

    def save(self, **kwargs):
        super(Orders, self).save(**kwargs)

    def __str__(self):
        return str(self.order_id)


class ShopSettings(models.Model):
    name = models.CharField(max_length=20)
    value = models.CharField(max_length=100)
    def save(self, **kwargs):
        super(ShopSettings, self).save(**kwargs)

    def __str__(self):
        return str(self.name)






