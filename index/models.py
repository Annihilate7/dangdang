# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class TAddress(models.Model):
    order_user = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=20, blank=True, null=True)
    clear_address = models.CharField(max_length=100, blank=True, null=True)
    post_code = models.CharField(max_length=6, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_address'


class TBook(models.Model):
    book_name = models.CharField(max_length=20, blank=True, null=True)
    author = models.CharField(max_length=20, blank=True, null=True)
    press = models.CharField(max_length=20, blank=True, null=True)
    time = models.DateField(blank=True, null=True)
    edition = models.SmallIntegerField(blank=True, null=True)
    isbn = models.CharField(db_column='ISBN', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numbers = models.IntegerField(blank=True, null=True)
    pages = models.IntegerField(blank=True, null=True)
    size = models.CharField(max_length=10, blank=True, null=True)
    paper = models.CharField(max_length=10, blank=True, null=True)
    pack = models.CharField(max_length=10, blank=True, null=True)
    book_pic = models.CharField(max_length=200, blank=True, null=True)
    book_price = models.FloatField(blank=True, null=True)
    new_price = models.FloatField(blank=True, null=True)
    bool_count = models.CharField(max_length=20, blank=True, null=True)
    sell_count = models.CharField(max_length=20, blank=True, null=True)
    author_inf = models.CharField(max_length=1000, blank=True, null=True)
    synopsis = models.CharField(max_length=1000, blank=True, null=True)
    ed_recom = models.CharField(max_length=1000, blank=True, null=True)
    con_recom = models.CharField(max_length=1000, blank=True, null=True)
    list = models.CharField(max_length=1000, blank=True, null=True)
    m_review = models.CharField(max_length=1000, blank=True, null=True)
    try_read = models.CharField(max_length=1000, blank=True, null=True)
    make_time = models.DateField(blank=True, null=True)
    impression = models.SmallIntegerField(blank=True, null=True)
    flow = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    suit = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('TCategory', models.DO_NOTHING, blank=True, null=True)

    def discount(self):
        return '%.2f' % (float(self.new_price) / float(self.book_price) * 10.00)

    class Meta:
        # managed = False
        db_table = 't_book'


class TCar(models.Model):
    count = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_car'


class TCategory(models.Model):
    class_name = models.CharField(max_length=20)
    level = models.IntegerField()
    parent_id = models.IntegerField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_category'


class TOrder(models.Model):
    order_item = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    create_time = models.DateField(blank=True, null=True)
    user = models.ForeignKey('TUser', models.DO_NOTHING, blank=True, null=True)
    address = models.ForeignKey(TAddress, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_order'


class TOrderItem(models.Model):
    count = models.CharField(max_length=20, blank=True, null=True)
    order = models.ForeignKey(TOrder, models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(TBook, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_order_item'


class TUser(models.Model):
    user_name = models.CharField(max_length=20, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 't_user'
