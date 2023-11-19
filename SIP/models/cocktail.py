from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
import magic

FILE_SIZE_LIMIT = 5 # in MB
SIZE_VALIDATOR = FILE_SIZE_LIMIT * 1024 * 1024
RESTRIC_FILE_TYPES = ['png', 'jpg', 'pdf']

ext_validator = FileExtensionValidator(RESTRIC_FILE_TYPES)

#  https://stackoverflow.com/questions/2472422/django-file-upload-size-limit
def file_size(file):
    if file.size > SIZE_VALIDATOR:
        raise ValidationError(f'File too large. Size should not exceed {FILE_SIZE_LIMIT} MiB.')

#  https://stackoverflow.com/questions/3648421/only-accept-a-certain-file-type-in-filefield-server-side
def validate_file_extension(file):
    accept = ['image/jpeg', 'image/png', 'application/pdf']
    file_mime_type = magic.from_buffer(file.read(1024), mime=True)
    print(file_mime_type)
    if file_mime_type not in accept:
        raise ValidationError('Unsupported file type.')


class Cocktail(models.Model):
    CREATE_BY = (
        ('o', 'Official'),
        ('u', 'Unofficial')
    )
    name = models.CharField(max_length=255)
    alternate_name = models.CharField(max_length=255, blank=True, null=True)
    cocktail_tag = models.CharField(max_length=1, choices=CREATE_BY)  # 'o' for official, 'u' for unofficial
    tags = models.ManyToManyField('SIP.Tag', blank=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    glass = models.CharField(max_length=255)
    instructions = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField('SIP.Ingredient', through='SIP.CocktailIngredient', blank=True)
    image = models.URLField(max_length=255, blank=True, null=True)
    image_source = models.URLField(max_length=255, blank=True, null=True)
    image_attribution = models.CharField(max_length=255, blank=True, null=True)
    date_modified = models.DateTimeField(default=timezone.now, null=True)
    user_uploaded_image = models.FileField(upload_to='user_image/', validators=[ext_validator, file_size, validate_file_extension], blank=True, null=True)

    def __str__(self):
        return self.name

# class Favorite(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
#     cocktail = models.ForeignKey('SIP.Cocktail', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.user} likes {self.cocktail}'
