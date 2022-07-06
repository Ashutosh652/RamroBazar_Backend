from io import BytesIO
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from PIL import Image
from ramrobazar.account.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("category name"), help_text=_("format: required, max_length=100"))
    slug = models.SlugField(max_length=150, null=False, blank=False, verbose_name=_("category url"), help_text=_("format: required, letters, numbers, underscore or hyphen"))
    parent = TreeForeignKey("self", on_delete=models.SET_NULL, related_name="children", null=True, blank=True, verbose_name=_("parent category"), help_text=_("format: not required"))

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("brand name"), help_text=_("format: required, unique, max-100"))

    def __str__(self):
        return self.name


class Item(models.Model):
    web_id = models.CharField(max_length=50, unique=True, verbose_name=_("item web id"), help_text=_("format: required, unique"))
    slug = models.SlugField(max_length=255, null=False, blank=False, verbose_name=_("item url"), help_text=_("format: required, letters, numbers, underscore or hyphen"))
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("item name"), help_text=_("format: required, max_length=250"))
    seller = models.ForeignKey(User, related_name="item", on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_("item description"), help_text=_("format: required"))
    category = TreeManyToManyField(Category)
    is_visible = models.BooleanField(default=True, verbose_name=_("item visibility"), help_text=_("format: true->product is visiible"))
    is_blocked = models.BooleanField(default=False, verbose_name=_("item blocked"), help_text=_("format: true->product is blocked"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date item was created"), help_text=_("format: Y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date item was last updated"), help_text=_("format: Y-m-d H:M:S"))
    # is_product = models.BooleanField(default=True, verbose_name=_("Is this product?"), help_text=_("format: true->product, false->service"))
    # product = models.OneToOneField(Product, related_name='product', on_delete=models.CASCADE)
    # service = models.OneToOneField(Service, related_name='service', on_delete=models.CASCADE)
    users_wishlist = models.ManyToManyField(User, related_name='user_wishlist', blank=True)
    reported_by = models.ManyToManyField(User, related_name='reported_item', blank=True)
    brand = models.ForeignKey(Brand, related_name="brand_products", on_delete=models.SET_NULL, null=True, blank=True)
    show_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Cost of Product shown on the site."), help_text=_("format: max price = 99999.99"))
    sold_times = models.IntegerField(null=False, default=0, verbose_name=_("sold times"))
    location = models.TextField(null=True, blank=True, verbose_name=_("available locations"))

    def __str__(self):
        return self.name


# class Product(models.Model):
#     brand = models.ForeignKey(Brand, related_name="brand_products", on_delete=models.PROTECT)
#     show_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Cost of Product shown on the site."), help_text=_("format: max price = 99999.99"))
#     available_units = models.IntegerField(null=False, default=0, verbose_name=_("available units"))
#     sold_units = models.IntegerField(null=False, default=0, verbose_name=_("sold units"))
#     product_or_service = models.OneToOneField(ProductOrService, related_name='product', on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.product_or_service.name


# class Service(models.Model):
#     price_min = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2, verbose_name=_("Minimum Cost of Service"), help_text=_("format: max price = 99999.99"))
#     price_max = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2, verbose_name=_("Maximum Cost of Service"), help_text=_("format: max price = 99999.99"))
#     no_sold_times = models.IntegerField(null=False, default=0, verbose_name=_("No. of times service is sold"))
#     available_date_start = models.DateField(null=True, blank=True, verbose_name=_("service start date"), help_text=_("date when service starts. can be null."))
#     available_date_end = models.DateField(null=True, blank=True, verbose_name=_("service end date"), help_text=_("date when service ends. can be null."))
#     available_time_start = models.TimeField(null=True, blank=True, verbose_name=_("service start time"), help_text=_("time when service starts. can be null."))
#     available_time_end = models.TimeField(null=True, blank=True, verbose_name=_("service end time"), help_text=_("time when service ends. can be null."))
#     location = models.TextField(null=True, blank=True, verbose_name=_("available locations"))
#     product_or_service = models.OneToOneField(ProductOrService, related_name='service', on_delete=models.CASCADE, null=True)

#     def __str__(self):
#         return self.product_or_service.name


# class ProductType(models.Model):
#     name = models.CharField(max_length=100, unique=True, verbose_name=_("type of product"), help_text=_("format: required, unique, max-100"))

#     def __str__(self):
#         return self.name


# class ProductAttributeValue(models.Model):
#     pass


# class ProductAttribute(models.Model):
#     name = models.CharField(max_length=100, unique=True, verbose_name=_("product attribute title"), help_text=_("format: required, unique, max-100"))
#     description = models.TextField(verbose_name=_("product attribute description"), help_text=_("format: required"))

#     def __str__(self):
#         return self.name


# class ProductAttributeValue(models.Model):
#     product_attribute = models.ForeignKey(ProductAttribute, related_name="product_attribute", on_delete=models.PROTECT)
#     attribute_value = models.CharField(max_length=100, verbose_name=_("attribute value"), help_text=_("format: required, max-100"))

#     def __str__(self):
#         return f"{self.product_attribute.name} : {self.attribute_value}"


# class ProductInventory(models.Model):
#     product_type = models.ForeignKey(ProductType, related_name="product_type", on_delete=models.PROTECT)
#     product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
#     brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.PROTECT)
#     attribute_value = models.ManyToManyField(ProductAttributeValue, related_name="product_attribute_values")
#     sold = models.BooleanField(default=False, verbose_name=_("product sold"), help_text=_("format: default=false, true=product is sold"))
#     # attribute_values = models.ManyToManyField(ProductAttributeValue, related_name="product_attribute_values", through="ProductAttributeValues")
#     is_visible = models.BooleanField(default=True, verbose_name=_("product visibility"), help_text=_("format: true->product is visiible"))
#     price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Cost of Product"), help_text=_("format: max price = 99999.99"))
#     error_messages = {
#         "name": { "max_length" : _("the price must be between 0 and 99999.99") }
#     }
#     weight = models.FloatField(verbose_name=_("product weight"), help_text=_("format: in grams"))
#     created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date subproduct created"), help_text=_("format: Y-m-d H:M:S"))
#     updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date subproduct last updated"), help_text=_("format: Y-m-d H:M:S"))

#     class Meta:
#         verbose_name = _('product inventory')
#         verbose_name_plural = _('product inventory')

#     def __str__(self):
#         return self.product.name


#Product Image Table
class Media(models.Model):
    item = models.ForeignKey(Item, null=True, blank=True, related_name="media", on_delete=models.PROTECT)
    image = models.ImageField(default='default_item.jpg', upload_to='items', null=False, blank=False, verbose_name=_("item image"), help_text=_("format: required, default-default_product.png"))
    alt_text = models.CharField(max_length=255, verbose_name=_("alternative text"), help_text=_("format: required, max-255"))
    is_feature = models.BooleanField(default=False, verbose_name=_("default/main image"), help_text=_("format: default=false, true=default/main image"))

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if storage.exists(self.image.name):
            img_read = storage.open(self.image.name, "r")
            img = Image.open(img_read)
            img_buffer = BytesIO()
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size, Image.ANTIALIAS)
                img.save(img_buffer, img.format)
                img.show()
                self.image.save(self.image.name, ContentFile(img_buffer.getvalue()))
            img_read.close()
    
    def __str__(self):
        if self.image:
            return self.item.name
        else:
            return 'No product or service associated with this image was found'


# class Stock(models.Model):
#     product_inventory = models.OneToOneField(ProductInventory, related_name="product_inventory", on_delete=models.PROTECT)
#     available_units = models.IntegerField(default=0, verbose_name=_("units/qty of stock"), help_text=_("format: required, default-0"))
#     sold_units =  models.IntegerField(default=0, verbose_name=_("units sold"), help_text=_("format: required, default-0"))

#     def __str__(self):
#         return self.product_inventory.product.name


# class SoldStatusConnection(models.Model):
#     buyer = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
#     seller = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)


# class ProductSoldStatus(models.Model):
#     buyer = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
#     # seller = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
#     # connection = models.ForeignKey(SoldStatusConnection, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, related_name="sold_status", on_delete=models.PROTECT)
#     buyer_status = models.BooleanField(default=False, verbose_name=_("bought by buyer"), help_text=_("format: default=false, true=buyer confirms buying"))
#     seller_status = models.BooleanField(default=False, verbose_name=_("sold by seller"), help_text=_("format: default=false, true=seller confirms selling"))
#     sold_units = models.IntegerField(null=False, default=0, blank=False, help_text=_("number of units sold to buyer"))

#     def __str__(self):
#         return f"{self.product.name}: Buyer Status: {self.buyer_status} : Seller Status: {self.seller_status}"
    
#     class Meta:
#         verbose_name = _('product sold status')
#         verbose_name_plural = _('product sold status')


# class ServiceSoldStatus(models.Model):
#     buyer = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
#     # seller = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
#     # connection = models.ForeignKey(SoldStatusConnection, on_delete=models.CASCADE)
#     service = models.ForeignKey(Service, related_name="sold_status", on_delete=models.PROTECT)
#     buyer_status = models.BooleanField(default=False, verbose_name=_("bought by buyer"), help_text=_("format: default=false, true=buyer confirms buying"))
#     seller_status = models.BooleanField(default=False, verbose_name=_("sold by seller"), help_text=_("format: default=false, true=seller confirms selling"))
#     no_sold_times = models.IntegerField(null=False, default=0, blank=False, help_text=_("number of times buyer bought the service"))

#     def __str__(self):
#         return f"{self.service.name}: Buyer Status: {self.buyer_status} : Seller Status: {self.seller_status}"
    
#     class Meta:
#         verbose_name = _('service sold status')
#         verbose_name_plural = _('service sold status')


class SoldStatus(models.Model):
    is_sold = models.BooleanField(default=False, verbose_name=_("is the item sold?"), help_text=_("format: default=false, true=item is sold"))
    buyer = models.ForeignKey(User, related_name="+", on_delete=models.SET_NULL, null=True)
    item = models.OneToOneField(Item, related_name="sold_status", on_delete=models.CASCADE)
    buyer_status = models.BooleanField(default=False, verbose_name=_("bought by buyer"), help_text=_("format: default=false, true=buyer confirms buying"))
    seller_status = models.BooleanField(default=False, verbose_name=_("sold by seller"), help_text=_("format: default=false, true=seller confirms selling"))
    sold_price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Price at which the item was sold."), help_text=_("format: max price = 99999.99"), null=True)
    sold_units = models.IntegerField(default=0, blank=False, help_text=_("number of units/times sold to buyer"), null=True)
    date_sold = models.DateField(blank=False, verbose_name=_("date sold"), help_text=_("date when item was sold"), null=True)

    def __str__(self):
        return f"{self.item.name}: Buyer Status: {self.buyer_status} : Seller Status: {self.seller_status}"


class Comment(MPTTModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date commented"))
	# likes = models.ManyToManyField(User, blank=True, related_name='comment_likes')
	# dislikes = models.ManyToManyField(User, blank=True, related_name='comment_dislikes')
    # parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="comment_children", null=True, blank=True, verbose_name=_("parent comment"), help_text=_("format: not required"))

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-date_commented').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False

    class Meta:
        ordering = ['-date_commented']

    def __str__(self):
        return 'Comment "{}" by "{}"'.format(self.content, self.author)


# class WishList(models.Model):
#     product = models.ManyToManyField(Product, null=True, blank=True, related_name='+')
#     service = models.ManyToManyField(Service, null=True, blank=True, related_name='+')
#     # user = models.ForeignKey(User, blank=True, null=False, on_delete=models.CASCADE, related_name='want_to_buy')
#     date_added = models.DateField()

#     # def __str__(self):
#     #     return f'Want to buy of {self.user}'
