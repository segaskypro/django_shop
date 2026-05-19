from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    # Константа с запрещёнными словами
    BANNED_WORDS = [
        'казино', 'криптовалюта', 'крипта', 'биржа',
        'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем класс 'form-field' ко всем полям формы
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-field'

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']

    def clean_name(self):
        """Проверяет, что название не содержит запрещённых слов"""
        name = self.cleaned_data.get('name')
        if name:
            name_lower = name.lower()
            for bad_word in self.BANNED_WORDS:
                if bad_word in name_lower:
                    raise forms.ValidationError(
                        f'Название содержит запрещённое слово: "{bad_word}".'
                    )
        return name

    def clean_description(self):
        """Проверяет, что описание не содержит запрещённых слов"""
        description = self.cleaned_data.get('description')
        if description:
            desc_lower = description.lower()
            for bad_word in self.BANNED_WORDS:
                if bad_word in desc_lower:
                    raise forms.ValidationError(
                        f'Описание содержит запрещённое слово: "{bad_word}".'
                    )
        return description

    def clean_price(self):
        """Проверяет, что цена не отрицательная"""
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError('Цена не может быть отрицательной.')
        return price