# Generated by Django 4.1.9 on 2023-06-02 12:36

from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_alter_blogpostcollectionlistpage_body_and_more"),
    ]

    operations = [TrigramExtension()]
