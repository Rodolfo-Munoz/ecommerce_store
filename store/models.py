from django.db import models


# a many to many relationship, a Promotion that can apply to different products
# a product can be in different promotions
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # we can define the relationship in either of the classes (product or promotion)
    # and Django created the reverse relationship. It makes more sense to do it in the
    # Product class as we want to show to the client the product and all the promotions that apply to
    # that product

class Collection(models.Model):
    title = models.CharField(max_length=255)
    # we type 'Product' to solve the circular dependency
    #  the related name '+' cancels the creation of the reverse relationship in the Product class
    # as the name "collection" will clash with the existing collection field. Other option
    # is to provide an alternative name.
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')



class Product(models.Model):
    title = models.CharField(max_length=255)
    # slug helps search engines to find our products by adding it at the
    # end of the url
    slug = models.SlugField()
    description = models.TextField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)
    # we use protect on delete, as if we accidentally delete a collection the products will not be deleted
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # we use a plural here as we can have multiple promotions.
    # The related_name argument changes how the name of the field in the promotion class will appear
    # if not specified Django will use "product_set" by default
    promotions = models.ManyToManyField(Promotion)

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)




class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]

    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    # the price is also a field in Product class, but as the price can change overtime
    # it has to be recorded in the order item too
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    # auto_now_true means that this field is auto-populated when we create a new cart
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


# this is an example of a one to one relationship the child class of customer as we say a "customer has an address"
# class Address(models.Model):
#    street = models.CharField(max_length=255)
#    city = models.CharField(max_length=255)
    # the first argument is the parent class, the CASCADE indicates that if the
    # customer is deleted, then the address record is deleted as well
    # the primary key is equal to true, to prevent djanfo to create an additional pk
    # for address as we need only one address per customer.
    # We don't need to create an address field in customer class as is
    # automatically created by Django
#    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key=True)
# This class is similar to the previous one but allows the customer to have more than one address


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # To define a one-to-many relationship we use a Foreingkey field type.
    # We don't need the pk as we allow now multiple values per customer
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, )




