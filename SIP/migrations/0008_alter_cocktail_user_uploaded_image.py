# Generated by Django 4.2.6 on 2023-11-19 12:33

import SIP.models.cocktail
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SIP', '0007_alter_cocktail_user_uploaded_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cocktail',
            name='user_uploaded_image',
            field=models.FileField(blank=True, null=True, upload_to='user_image/', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'pdf']), SIP.models.cocktail.validate_file_extension]),
        ),
    ]
