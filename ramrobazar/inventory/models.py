from io import BytesIO
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from PIL import Image
from ramrobazar.account.models import User


class Category(MPTTModel):
    name = models.CharField(
        max_length=100,
        null=False,
        blank=False,
        verbose_name=_("category name"),
        help_text=_("format: required, max_length=100"),
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        blank=False,
        editable=False,
        verbose_name=_("category url"),
        help_text=_("format: required, letters, numbers, underscore or hyphen"),
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.SET_NULL,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_("parent category"),
        help_text=_("format: not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("brand name"),
        help_text=_("format: required, unique, max-100"),
    )

    def __str__(self):
        return self.name


class Item(models.Model):
    # web_id = models.CharField(max_length=50, unique=True, verbose_name=_("item web id"), help_text=_("format: required, unique"))
    slug = models.SlugField(
        max_length=255,
        null=False,
        blank=False,
        editable=False,
        verbose_name=_("item url"),
        help_text=_("format: required, letters, numbers, underscore or hyphen"),
    )
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        verbose_name=_("item name"),
        help_text=_("format: required, max_length=250"),
    )
    seller = models.ForeignKey(User, related_name="item", on_delete=models.CASCADE)
    description = models.TextField(
        verbose_name=_("item description"), help_text=_("format: required")
    )
    category = TreeManyToManyField(Category)
    is_visible = models.BooleanField(
        default=True,
        verbose_name=_("item visibility"),
        help_text=_("format: true->product is visiible"),
    )
    is_blocked = models.BooleanField(
        default=False,
        verbose_name=_("item blocked"),
        help_text=_("format: true->product is blocked"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_("date item was created"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("date item was last updated"),
        help_text=_("format: Y-m-d H:M:S"),
    )
    users_wishlist = models.ManyToManyField(
        User, related_name="user_wishlist", blank=True
    )
    reported_by = models.ManyToManyField(User, related_name="reported_item", blank=True)
    brand = models.ForeignKey(
        Brand,
        related_name="brand_products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    show_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name=_("Cost of Product shown on the site."),
        help_text=_("format: max price = 99999.99"),
    )
    sold_times = models.IntegerField(
        null=False, default=0, verbose_name=_("sold times")
    )
    location = models.TextField(
        null=True, blank=True, verbose_name=_("available locations")
    )

    def __str__(self):
        return self.name


class Media(models.Model):
    """Model representing images of items."""

    item = models.ForeignKey(
        Item, null=True, blank=True, related_name="media", on_delete=models.PROTECT
    )
    image = models.ImageField(
        default="default_item.jpg",
        upload_to="items",
        null=False,
        blank=False,
        verbose_name=_("item image"),
        help_text=_("format: required, default-default_product.png"),
    )
    alt_text = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_("alternative text"),
        help_text=_("format: required, max-255"),
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=_("default/main image"),
        help_text=_("format: default=false, true=default/main image"),
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def save(self, *args, **kwargs):
        """Adjust the size of image uploaded to 500*500 pixels if it is greater than that before uploading to cloudinary"""

        super().save(*args, **kwargs)
        if storage.exists(self.image.name):
            img_read = storage.open(self.image.name, "r")
            img = Image.open(img_read)
            img_buffer = BytesIO()
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size, Image.ANTIALIAS)
                img.save(img_buffer, img.format)
                img.show()
                self.image.save(self.image.name, ContentFile(img_buffer.getvalue()))
            img_read.close()

    def __str__(self):
        if self.image:
            return self.item.name
        else:
            return "No product or service associated with this image was found"


class SoldStatus(models.Model):
    """Model representing the sold status of an item."""

    is_sold = models.BooleanField(
        default=False,
        verbose_name=_("is the item sold?"),
        help_text=_("format: default=false, true=item is sold"),
    )
    buyer = models.ForeignKey(
        User, related_name="+", on_delete=models.SET_NULL, null=True
    )
    item = models.OneToOneField(
        Item, related_name="sold_status", on_delete=models.CASCADE
    )
    buyer_status = models.BooleanField(
        default=False,
        verbose_name=_("bought by buyer"),
        help_text=_("format: default=false, true=buyer confirms buying"),
    )
    seller_status = models.BooleanField(
        default=False,
        verbose_name=_("sold by seller"),
        help_text=_("format: default=false, true=seller confirms selling"),
    )
    sold_price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name=_("Price at which the item was sold."),
        help_text=_("format: max price = 99999.99"),
        null=True,
    )
    sold_units = models.IntegerField(
        default=0,
        blank=False,
        help_text=_("number of units/times sold to buyer"),
        null=True,
    )
    date_sold = models.DateField(
        blank=False,
        verbose_name=_("date sold"),
        help_text=_("date when item was sold"),
        null=True,
    )

    class Meta:
        verbose_name = _("Sold Status")
        verbose_name_plural = _("Sold Status")

    def __str__(self):
        return f"{self.item.name}: Sold: {self.is_sold}"


class Comment(MPTTModel):
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="comments", null=True, blank=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_commented = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name=_("date commented")
    )
    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="comment_children",
        null=True,
        blank=True,
        verbose_name=_("parent comment"),
        help_text=_("format: not required"),
    )

    @property
    def children(self):
        """returns all the children of a comment"""

        return Comment.objects.filter(parent=self).order_by("-date_commented").all()

    @property
    def is_parent(self):
        """returns True if a comment has no parent i.e. the coment is the parent"""

        if self.parent is None:
            return True
        return False

    class Meta:
        ordering = ["-date_commented"]

    def __str__(self):
        return 'Comment "{}" by "{}"'.format(self.content, self.author)
