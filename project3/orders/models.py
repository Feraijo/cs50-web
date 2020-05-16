from django.db import models
from django.contrib.auth.models import User

class MenuType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    purchases = models.ManyToManyField('Purchase')
    finished = models.BooleanField(default=False)

    def __str__(self):
       return f'{self.user}: {self.purchases.count()} items'

class PendingPurchasesManager(models.Manager):
    use_for_related_fields = True
    def pp(self):
        qs = super().get_queryset()
        qs = qs.filter(pending=True)
        return qs

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="purchases")   
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    adds = models.ManyToManyField('Addition', blank=True, related_name="purchases")
    pending = models.BooleanField(default=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    notes = models.CharField(max_length=256, null=True, blank=True)
    amount = models.PositiveSmallIntegerField(null=True, blank=True, default=1)    

    objects = PendingPurchasesManager()
    #pending_objects = PendingPurchasesManager()

    class Meta:
        base_manager_name = 'objects'

    def __str__(self):
       return f'{self.item} ({self.amount})'

class MenuItem(models.Model):
    item_type = models.ForeignKey('ItemType', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    number_of_toppings = models.PositiveSmallIntegerField(null=True, blank=True)
    price_large = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_small = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    
    class Meta:
        unique_together = (('name', 'item_type'),)

    def __str__(self):
       return f'{self.item_type} - {self.name}'

class Addition(models.Model):
    add_type = models.ForeignKey('AddType', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    name = models.CharField(max_length=128)
    
    class Meta:
        unique_together = (('name', 'add_type'),)
    
    def __str__(self):
        return f'{self.add_type} - {self.name}'

class AddType(MenuType):
    parent_type = models.ManyToManyField('ItemType', related_name="add_types")

class ItemType(MenuType):
    pass

