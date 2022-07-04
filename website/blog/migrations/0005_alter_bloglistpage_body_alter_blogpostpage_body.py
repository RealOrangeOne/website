# Generated by Django 4.0.5 on 2022-06-27 18:57

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0004_bloglistpage_body_blogpostpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloglistpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    (
                        "rich_text",
                        wagtail.blocks.RichTextBlock(
                            features=[
                                "h1",
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                                "code",
                                "strikethrough",
                            ]
                        ),
                    ),
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
        migrations.AlterField(
            model_name="blogpostpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    (
                        "rich_text",
                        wagtail.blocks.RichTextBlock(
                            features=[
                                "h1",
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "link",
                                "document-link",
                                "code",
                                "strikethrough",
                            ]
                        ),
                    ),
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