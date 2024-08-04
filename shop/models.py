from django.db import models
from django.core.exceptions import ValidationError

def validate_prohibited_words(value):
    prohibited_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
    for word in prohibited_words:
        if word in value.lower():
            raise ValidationError(f'Нельзя использовать слово "{word}" в названии или описании.')

class Product(models.Model):
    name = models.CharField(max_length=255, validators=[validate_prohibited_words])
    description = models.TextField(validators=[validate_prohibited_words])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    @property
    def active_version(self):
        return self.versions.filter(is_active=True).first()

class Version(models.Model):
    product = models.ForeignKey(Product, related_name='versions', on_delete=models.CASCADE)
    version_number = models.CharField(max_length=10)
    version_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            Version.objects.filter(product=self.product, is_active=True).update(is_active=False)
        super().save(*args, **kwargs)
