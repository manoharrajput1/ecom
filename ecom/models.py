from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    category = models.CharField(max_length=50, default=None)
    subcategory = models.CharField(max_length=70,default=None)
    price = models.IntegerField()
    product_image = models.ImageField(upload_to='images')
    brand = models.CharField(max_length=70)
    processor = models.CharField(max_length=50, default=None)
    quantity = models.IntegerField(default=0)
    

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.product_image.url
        except:
            url = ''
        return url


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address