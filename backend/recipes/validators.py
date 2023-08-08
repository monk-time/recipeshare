from django.core import validators
from django.utils.deconstruct import deconstructible


@deconstructible
class HEXColorValidator(validators.RegexValidator):
    regex = r'^#[0-9a-fA-F]{6}\Z'
    message = (
        'HEX-цвет должен начинаться с # и содержать '
        'шесть цифр и/или букв a-f/A-F'
    )
