from django.db import models

class MenuName(models.Model):    
    name = models.CharField(max_length=128, unique=True)
    
    def __str__(self):
       return self.name  # f'{self.id}: {self.name}'

    class Meta:
        abstract = True

class MenuPrice(models.Model):
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        abstract = True

class MenuSize(models.Model):
    size = models.ForeignKey('Size', on_delete=models.CASCADE, default=1)

    class Meta:
        abstract = True


class Pizza(MenuPrice, MenuSize):
    pizza_title = models.ForeignKey('PizzaTitle', on_delete=models.CASCADE)    
    pizza_type = models.ForeignKey('PizzaType', on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = (('pizza_title', 'size', 'pizza_type'),)

    def __str__(self):
       return f'{self.pizza_type} - {self.pizza_title} ({self.size})'

class Sub(MenuPrice, MenuSize):
    name = models.ForeignKey('SubName', on_delete=models.CASCADE)    
    
    class Meta:
        unique_together = (('name', 'size'),)

    def __str__(self):
       return f'{self.name} ({self.size})'

class DinnerPlatter(MenuPrice, MenuSize):
    name = models.ForeignKey('DinnerPlatterName', on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('name', 'size'),)

    def __str__(self):
       return f'{self.name} ({self.size})'

class Pasta(MenuName, MenuPrice):
    pass
    
class Salad(MenuName, MenuPrice):
    pass   

class PizzaTitle(MenuName):    
    number_of_toppings = models.PositiveSmallIntegerField(null=True, blank=True)
    
class PizzaType(MenuName):
    pass

class DinnerPlatterName(MenuName):
    pass

class SubName(MenuName):  
    pass

class Size(MenuName):
    pass

class SubAddition(MenuName, MenuPrice):
    pass

class Topping(MenuName):
    pass
#DinnerPlatter.objects.values('name_id').annotate(price=ArrayAgg('price'))