from unicodedata import category
from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.core.validators import RegexValidator


# Model Objects

# Product Ingoing (Collections)
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    barcode = models.IntegerField()
    category= models.CharField(max_length=500)
    perishable = models.BooleanField(default=False)
    allergens = models.CharField(max_length=500)
    weight = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    footprint = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey('Collection', on_delete=models.CASCADE, null=True)
    
    def category_list(self):
        return self.category.split(',')

# Product Outgoing (Pickups)
class ProductOut(models.Model):
    id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    barcode = models.IntegerField()
    category= models.CharField(max_length=500)
    perishable = models.BooleanField(default=False)
    allergens = models.CharField(max_length=500)
    weight = models.FloatField(default=0)
    quantity = models.IntegerField(default=1)
    footprint = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    pickup = models.ForeignKey('Pickup', on_delete=models.CASCADE, null=True)
    
    def category_list(self):
        return self.category.split(',')

# Member Data
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    addressFirstLine = models.CharField(max_length=500)
    ageGroup = models.CharField(max_length=100)
    ethnicity = models.CharField(max_length=100)
    postCode = models.CharField(max_length=100)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    email = models.EmailField(max_length=100)
    prefContact = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    isCarer = models.BooleanField(default=False)
    isMember = models.BooleanField(default=True)
    isEmployed = models.BooleanField(default=True)
    noAdults = models.IntegerField(default=0)
    noChildren = models.IntegerField(default=0)
    foodAllergies = models.CharField(max_length=300)
    prefLarder = models.ForeignKey('Larder', on_delete=models.CASCADE, null=True)
    acceptedPolicy = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    totalFoodCollected = models.FloatField(default=0)
    baselineHealthScore = models.FloatField(default=0)
    currentHealthScore = models.FloatField(default=0)

    def __str__(self):
        return self.firstName + " " + self.lastName

# Volunteer Data    
class Volunteer(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    addressFirstLine = models.CharField(max_length=500)
    postCode = models.CharField(max_length=100)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # Validators should be a list
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    isAdmin = models.BooleanField(default=False)
    age = models.IntegerField(default=0)
    prefLarder = models.ForeignKey('Larder', on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.firstName + " " + self.lastName

# Supplier Data    
class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    addressFirstLine = models.CharField(max_length=500)
    postCode = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name + " " + self.addressFirstLine

# Larder Data
class Larder(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    addressFirstLine = models.CharField(max_length=500)
    postCode = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Updating the list of products at a specific larder
class Update(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    larder = models.ForeignKey(Larder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "member:" + str(self.member) + "larder:" + str(self.larder) + "product:" + str(self.product) + "created_at:" + str(self.created_at) + "time:" + str(self.time)

#(Ingoing) Collection is when a volunteer collects products from a supplier to be stored in a larder
class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    larder = models.ForeignKey(Larder, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.volunteer.firstName + " | " + self.supplier.name + " " + self.supplier.addressFirstLine + " -> " + self.larder.name + " | " + str(self.created_at)

# (Outgoing) Pickup is when a member picks up products from a larder
class Pickup(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    larder = models.ForeignKey(Larder, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.volunteer.firstName + " | " + self.larder.name + " -> " + self.member.lastName + " | " + str(self.created_at)


