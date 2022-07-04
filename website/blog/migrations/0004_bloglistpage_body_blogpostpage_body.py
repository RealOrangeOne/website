# Generated by Django 4.0.5 on 2022-06-26 17:35

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0003_blogpostpage_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="bloglistpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    ("rich_text", wagtail.blocks.RichTextBlock()),
                    (
                        "lorem",
                        wagtail.blocks.StructBlock(
                            [("paragraphs", wagtail.blocks.IntegerBlock(min_value=1))]
                        ),
                    ),
                    ("html", wagtail.blocks.RawHTMLBlock()),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
        migrations.AddField(
            model_name="blogpostpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    ("rich_text", wagtail.blocks.RichTextBlock()),
                    (
                        "lorem",
                        wagtail.blocks.StructBlock(
                            [("paragraphs", wagtail.blocks.IntegerBlock(min_value=1))]
                        ),
                    ),
                    ("html", wagtail.blocks.RawHTMLBlock()),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]