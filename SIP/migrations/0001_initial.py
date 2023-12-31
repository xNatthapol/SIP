# Generated by Django 4.2.7 on 2023-11-08 06:25

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Official",
            fields=[
                ("drink_name", models.CharField(max_length=255)),
                (
                    "alternate_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=255, null=True
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                ("glass", models.CharField(max_length=255)),
                ("instructions", models.TextField()),
                ("ingredients", models.JSONField(default=dict)),
                ("image", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "image_source",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_attribution",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_modified", models.DateTimeField()),
                ("id_drink", models.IntegerField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "sip_official_cocktails",
            },
        ),
        migrations.CreateModel(
            name="Unofficial",
            fields=[
                ("drink_name", models.CharField(max_length=255)),
                (
                    "alternate_name",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "tags",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            blank=True, max_length=255, null=True
                        ),
                        blank=True,
                        null=True,
                        size=None,
                    ),
                ),
                ("category", models.CharField(blank=True, max_length=255, null=True)),
                ("glass", models.CharField(max_length=255)),
                ("instructions", models.TextField()),
                ("ingredients", models.JSONField(default=dict)),
                ("image", models.URLField(blank=True, max_length=255, null=True)),
                (
                    "image_source",
                    models.URLField(blank=True, max_length=255, null=True),
                ),
                (
                    "image_attribution",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_modified", models.DateTimeField()),
                ("id_drink", models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                "db_table": "sip_unofficial_cocktails",
            },
        ),
        migrations.CreateModel(
            name="Star",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_drink", models.IntegerField()),
                ("tag", models.CharField(max_length=1)),
                ("score", models.IntegerField()),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "sip_star",
            },
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("id_drink", models.IntegerField()),
                ("tag", models.CharField(max_length=1)),
                ("message", models.CharField(max_length=255)),
                (
                    "reviewed_at",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "sip_review",
            },
        ),
    ]
