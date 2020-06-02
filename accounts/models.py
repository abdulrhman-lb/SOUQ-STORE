from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import datetime
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User , verbose_name=_("User") , on_delete=models.CASCADE)
    slug = models.SlugField(blank=True , null=True , verbose_name=_("Profile URL"))
    image = models.ImageField(upload_to="profile_img", verbose_name=_("image") , blank=True , null=True)
    country = CountryField()
    address = models.CharField(max_length=100)
    join_date = models.DateTimeField(verbose_name=_("join date"), default=datetime.datetime.now)

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')

    def get_absolute_url(self):
        return reverse('accounts:Profile' , kwargs={'slug' : self.slug})

    def __str__(self):
        return '%s' %(self.user)

    def save(self , *arg , **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(Profile , self).save(*arg , **kwargs)

def create_profile(sender , **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile , sender=User)


