from django.db import models
from django.contrib.auth.models import User

class MenuName(models.Model):    
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
       return self.name

    class Meta:
        abstract = True

class MenuPrice(models.Model):
    price_large = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_small = models.DecimalField(max_digits=6, decimal_places=2, null=True)

    class Meta:
        abstract = True
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)   
    item = models.ForeignKey('MenuItem', on_delete=models.CASCADE)
    #tops = models.ManyToManyField('Topping', blank=True)
    #adds = models.ManyToManyField('SubAddition', blank=True)
    adds = models.ManyToManyField('Addition', blank=True)

    def __str__(self):
       return f'{self.user}: {self.item}'


class MenuItem(MenuPrice):
    item_type = models.ForeignKey('ItemType', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    number_of_toppings = models.PositiveSmallIntegerField(null=True, blank=True)  
    
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

class AddType(MenuName):
    pass

class ItemType(MenuName):
    pass

class Pizza(MenuPrice):
    name = models.CharField(max_length=128)
    number_of_toppings = models.PositiveSmallIntegerField(null=True, blank=True)   
    pizza_type = models.ForeignKey('PizzaType', on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = (('name', 'pizza_type'),)

    def __str__(self):
       return f'{self.pizza_type} - {self.name}'

class Sub(MenuName, MenuPrice):
    pass

class DinnerPlatter(MenuName, MenuPrice):
    pass

class Pasta(MenuName, MenuPrice):
    pass
    
class Salad(MenuName, MenuPrice):
    pass   
    
class PizzaType(MenuName):
    pass

class SubAddition(MenuName, MenuPrice):
    pass

class Topping(MenuName):
    pass
