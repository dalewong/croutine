from django.db import models
from tinymce.models import HTMLField


class User_db(models.Model):

    user_name = models.CharField(max_length=20)
    user_password = models.CharField(max_length=20)
    user_phone = models.CharField(max_length=20)
    user_email = models.CharField(max_length=20)
    user_address = HTMLField()
    #def __str__(self):
    #    return self.user_name.encode('utf-8')

    class Meta():
        db_table = 'User_db'


class Ord(models.Model):

    order_user_id = models.ForeignKey('User_db')
    order_num = models.IntegerField(default=0)
    submit_date = models.DateTimeField()
    total_price = models.DecimalField(max_digits=20,decimal_places=2)
    isPay = models.BooleanField(default=0)
    #def __str__(self):
    #    return self.order_num.encode('utf-8')

    class Meta():
        db_table = 'Ord'


class Order_detail(models.Model):

    odetail_goods_id = models.ForeignKey('Goods_info')
    odetail_goods_num = models.IntegerField(default=0)
    odetail_totalprice = models.IntegerField(default=0)
    detail_num = models.ForeignKey('Ord')

    class Meta():
        db_table = 'Order_detail'


class Goods_list(models.Model):

    goods_list_name = models.CharField(max_length=20)
    goods_list_class = models.CharField(max_length=20)
    goods_list_pic = models.ImageField(upload_to='uploads/')

    #def __str__(self):
    #    return self.goods_list_name.encode('utf-8')


    class Meta():
        db_table = 'Goods_list'


class Cart(models.Model):

    goods_num = models.IntegerField()
    user_id = models.ForeignKey('User_db')
    goods_id = models.ForeignKey('Goods_info')

    class Meta():
        db_table = 'Cart'


class Goods_info(models.Model):

    goods_name = models.CharField(max_length=20)
    goods_description = HTMLField()
    goods_price = models.DecimalField(max_digits=10,decimal_places=2)
    goods_stock = models.IntegerField()
    goods_msg = HTMLField()
    goods_unit = models.CharField(max_length=20)
    goods_list_id=models.ForeignKey('Goods_list')
    goods_pic_url=models.ImageField(upload_to='uploads/')

    #def __str__(self):
    #    return self.goods_name.encode('utf-8')
    class Meta():
        db_table = 'Goods_info'



class Receiver(models.Model):

    receiver_address = HTMLField()
    receiver_name = models.CharField(max_length=20)
    receiver_phone = models.CharField(max_length=20)
    receiver_user_id = models.ForeignKey('User_db')
    receiver_email = models.CharField(max_length=20)
    
    class Meta():
        db_table = 'Receiver'
