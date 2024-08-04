from django import forms
from django.core.exceptions import ValidationError
from .models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description']

    def clean_name(self):
        name = self.cleaned_data['name']
        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise ValidationError(f"Запрещенное слово в названии: {word}")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise ValidationError(f"Запрещенное слово в описании: {word}")
        return description


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = ['product', 'version_name', 'is_active']

    def clean_is_active(self):
        is_active = self.cleaned_data.get('is_active')
        product = self.cleaned_data.get('product')

        if is_active and product.versions.filter(is_active=True).exists():
            raise forms.ValidationError('У этого продукта уже есть активная версия.')

        return is_active
