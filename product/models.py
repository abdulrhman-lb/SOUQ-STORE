from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify
#from django.core.urlresolvers import reverse
# Create your models here.
class Product(models.Model):
    PRDName = models.CharField(max_length=100 , verbose_name=_("Name"))
    PRDCategory = models.ForeignKey('Category' , on_delete=models.CASCADE , blank=True , null=True , verbose_name=_("Category"))
    PRDBrand = models.ForeignKey('settings.Brand' , on_delete=models.CASCADE , blank=True , null=True , verbose_name=_("Brand"))
    #PRDVariant = models.ForeignKey('settings.Variant' , on_delete=models.CASCADE)
    PRDDesc = models.TextField(verbose_name=_("Description"))
    PRDImage = models.ImageField(upload_to='product/' , verbose_name=_("Image") , blank=True , null=True)
    PRDPrice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Price"))
    PRDDiscountPrice = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Discount Price"))
    PRDCost = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Cost"))
    PRDCreated = models.DateTimeField(verbose_name=_("Created At"))

    PRDSlug = models.SlugField(blank=True , null=True , verbose_name=_("Product URL"))
    PRDISNew = models.BooleanField(default=True , verbose_name=_("New Product"))
    PRDISBestSeller = models.BooleanField(default=False , verbose_name=_("Best Saller"))

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def save(self , *arg , **kwargs):
        if not self.PRDSlug:
            self.PRDSlug = slugify(self.PRDName)
        super(Product , self).save(*arg , **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail' , kwargs={'slug' : self.PRDSlug})

    def __str__(self):
        return self.PRDName

class ProductImage(models.Model):
    PRDIProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("Product"))
    PRDIImage = models.ImageField(upload_to='product/' , verbose_name=_("Image"))

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return str(self.PRDIProduct)


class Category(models.Model):
    CATName = models.CharField(max_length=50 , verbose_name=_("Name"))
    CATParent = models.ForeignKey('self' , limit_choices_to={'CATParent__isnull':True} , on_delete=models.CASCADE , blank=True , null=True , verbose_name=_("Main Category"))
    CATDesc = models.TextField(verbose_name=_("Description"))
    CATImg = models.ImageField(upload_to='category/' , verbose_name=_("Image"))

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return str(self.CATName)


class Product_Alternative(models.Model):
    PALTProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='main_prduct' , verbose_name=_("Product"))
    PALTAlternatives = models.ManyToManyField(Product , related_name='alternative_prducts' , verbose_name=_("Alternations"))

    class Meta:
        verbose_name = _('Product Alternative')
        verbose_name_plural = _('Product Alternatives')

    def __str__(self):
        return str(self.PALTProduct)


class Product_Accessories(models.Model):
    PACCProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='mainAccessory_prduct' , verbose_name=_("Product"))
    PACCAccessories = models.ManyToManyField(Product , related_name='accessories_prducts' , verbose_name=_("Accessories"))

    class Meta:
        verbose_name = _('Product Accessory')
        verbose_name_plural = _('Product Accessories')

    def __str__(self):
        return str(self.PACCProduct)
