from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from ramrobazar.account.models import User


class Category(MPTTModel):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_("category name"), help_text=_("format: required, max_length=100"))
    slug = models.SlugField(max_length=150, null=False, blank=False, verbose_name=_("category url"), help_text=_("format: required, letters, numbers, underscore or hyphen"))
    parent = TreeForeignKey("self", on_delete=models.PROTECT, related_name="children", null=True, blank=True, verbose_name=_("parent category"), help_text=_("format: not required"))

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')
    
    def __str__(self):
        return self.name


class Product(models.Model):
    web_id = models.CharField(max_length=50, unique=True, verbose_name=_("product web id"), help_text=_("format: required, unique"))
    slug = models.SlugField(max_length=255, null=False, blank=False, verbose_name=_("product url"), help_text=_("format: required, letters, numbers, underscore or hyphen"))
    name = models.CharField(max_length=250, null=False, blank=False, verbose_name=_("product name"), help_text=_("format: required, max_length=250"))
    description = models.TextField(verbose_name=_("product description"), help_text=_("format: required"))
    category = TreeManyToManyField(Category)
    is_visible = models.BooleanField(default=True, verbose_name=_("product visibility"), help_text=_("format: true->product is visiible"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date product created"), help_text=_("format: Y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date product last updated"), help_text=_("format: Y-m-d H:M:S"))

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("type of product"), help_text=_("format: required, unique, max-100"))

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("brand name"), help_text=_("format: required, unique, max-100"))

    def __str__(self):
        return self.name


# class ProductAttributeValue(models.Model):
#     pass


class ProductAttribute(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_("product attribute description"), help_text=_("format: required, unique, max-100"))
    description = models.TextField(verbose_name=_("product attribute description"), help_text=_("format: required"))

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, related_name="product_attribute", on_delete=models.PROTECT)
    attribute_value = models.CharField(max_length=100, verbose_name=_("attribute value"), help_text=_("format: required, max-100"))

    def __str__(self):
        return f"{self.product_attribute.name} : {self.attribute_value}"


class ProductInventory(models.Model):
    product_type = models.ForeignKey(ProductType, related_name="product_type", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT)
    brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.PROTECT)
    attribute_value = models.ManyToManyField(ProductAttributeValue, related_name="product_attribute_values")
    sold = models.BooleanField(default=False, verbose_name=_("product sold"), help_text=_("format: default=false, true=product is sold"))
    # attribute_values = models.ManyToManyField(ProductAttributeValue, related_name="product_attribute_values", through="ProductAttributeValues")
    is_visible = models.BooleanField(default=True, verbose_name=_("product visibility"), help_text=_("format: true->product is visiible"))
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name=_("Cost of Product"), help_text=_("format: max price = 99999.99"))
    error_messages = {
        "name": { "max_length" : _("the price must be between 0 and 99999.99") }
    }
    weight = models.FloatField(verbose_name=_("product weight"), help_text=_("format: in grams"))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_("date subproduct created"), help_text=_("format: Y-m-d H:M:S"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("date subproduct last updated"), help_text=_("format: Y-m-d H:M:S"))

    def __str__(self):
        return self.product.name


#Product Image Table
class Media(models.Model):
    product_inventory = models.ForeignKey(ProductInventory, related_name="media_product_inventory", on_delete=models.PROTECT)
    image = models.ImageField(default='default_product.jpg', upload_to='products', null=False, blank=False, verbose_name=_("product image"), help_text=_("format: required, default-default_product.png"))
    alt_text = models.CharField(max_length=255, verbose_name=_("alternative text"), help_text=_("format: required, max-255"))
    is_feature = models.BooleanField(default=False, verbose_name=_("product default/main image"), help_text=_("format: default=false, true=default/main image"))

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")
    
    def __str__(self):
        return self.product_inventory.product.name


class Stock(models.Model):
    product_inventory = models.OneToOneField(ProductInventory, related_name="product_inventory", on_delete=models.PROTECT)
    available_units = models.IntegerField(default=0, verbose_name=_("units/qty of stock"), help_text=_("format: required, default-0"))
    sold_units =  models.IntegerField(default=0, verbose_name=_("units sold"), help_text=_("format: required, default-0"))


# class SoldStatusConnection(models.Model):
#     buyer = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)
#     seller = models.ForeignKey(User, related_name="+", on_delete=models.CASCADE)


class SoldStatus(models.Model):
    buyer = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    seller = models.ForeignKey(User, related_name="+", on_delete=models.PROTECT)
    # connection = models.ForeignKey(SoldStatusConnection, on_delete=models.CASCADE)
    product_inventory = models.ForeignKey(ProductInventory, related_name="sold_status", on_delete=models.PROTECT)
    buyer_status = models.BooleanField(default=False, verbose_name=_("bought by buyer"), help_text=_("format: default=false, true=buyer confirms buying"))
    seller_status = models.BooleanField(default=False, verbose_name=_("sold by seller"), help_text=_("format: default=false, true=seller confirms selling"))

    def __str__(self):
        return f"Buyer Status: {self.buyer_status} : Seller Status: {self.seller_status}"
