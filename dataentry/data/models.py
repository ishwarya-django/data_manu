from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager




class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
       
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, username, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
        )
      
        user.is_active = True
   
        user.save(using=self._db)
        return user



class User(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    # required
    date_joined     = models.DateTimeField(auto_now_add=True)
    last_login      = models.DateTimeField(auto_now_add=True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=False)
    is_superadmin        = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


STATUS_CHOICES= (
    ('profit', 'profit'),
    ('loss', 'loss'),
    
    )


class Makeproduct(models.Model):
    product_name=models.CharField(max_length=100)
    sell_price=models.DecimalField(max_digits = 8,decimal_places = 2,default=0)
    makeproduct_price=models.DecimalField(max_digits = 8,decimal_places = 2, default=0)
    status_makeproduct= models.CharField(choices=STATUS_CHOICES,max_length=100, null=True,blank=True)
    pro_loss_makeproduct=models.DecimalField(max_digits = 8,decimal_places = 2,default=0)
    # product form shop
    price_pro_fromshop=models.DecimalField(max_digits = 8,decimal_places = 2,default=0)
    status_purchaseproduct= models.CharField(choices=STATUS_CHOICES,max_length=100, null=True,blank=True)
    pro_loss_purchaseproduct=models.DecimalField(max_digits = 8,decimal_places = 2,default=0)
    is_active=models.BooleanField(default=True)
    def __str__(self):
        return f"{self.product_name}"

class Expense_Product(models.Model):
    org_product=models.ForeignKey(Makeproduct,on_delete=models.CASCADE,null=True,blank=True)
    product=models.CharField(max_length=100,null=True,blank=True)
    price=models.DecimalField(max_digits = 8,decimal_places = 2,null=True, blank=True)

    def __str__(self):
        return f"{self.org_product.product_name}"

class Purchase_product(models.Model):
    org_product=models.ForeignKey(Makeproduct,on_delete=models.CASCADE,null=True,blank=True)
    price_pro_fromshop=models.DecimalField(max_digits = 8,decimal_places = 2,null=True, blank=True)
    status= models.CharField(choices=STATUS_CHOICES,max_length=100, null=True,blank=True)

    def __str__(self):
        return f"{self.org_product.product_name}"

class Add_Expense(models.Model):
    product=models.CharField(max_length=100,null=True,blank=True)
    price=models.DecimalField(max_digits = 8,decimal_places = 2,default=0)
    def __str__(self):
        return f"{self.product}"