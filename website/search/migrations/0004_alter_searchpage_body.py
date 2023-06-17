# Generated by Django 4.1.8 on 2023-04-19 20:19

import wagtail.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations

import website.contrib.code_block.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("search", "0003_alter_searchpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="searchpage",
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
                    (
                        "image",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "caption",
                                    wagtail.blocks.RichTextBlock(
                                        editor="plain", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "code",
                        wagtail.blocks.StructBlock(
                            [
                                (
                                    "filename",
                                    wagtail.blocks.CharBlock(
                                        max_length=128, required=False
                                    ),
                                ),
                                (
                                    "language",
                                    wagtail.blocks.ChoiceBlock(
                                        choices=website.contrib.code_block.blocks.get_language_choices
                                    ),
                                ),
                                ("source", wagtail.blocks.TextBlock()),
                            ]
                        ),
                    ),
                    (
                        "tangent",
                        wagtail.blocks.StructBlock(
                            [
                                ("name", wagtail.blocks.CharBlock(max_length=64)),
                                (
                                    "content",
                                    wagtail.blocks.RichTextBlock(editor="simple"),
                                ),
                            ]
                        ),
                    ),
                    (
                        "mermaid",
                        wagtail.blocks.StructBlock(
                            [
                                ("source", wagtail.blocks.TextBlock()),
                                (
                                    "caption",
                                    wagtail.blocks.RichTextBlock(
                                        editor="plain", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                    (
                        "table",
                        wagtail.contrib.typed_table_block.blocks.TypedTableBlock(
                            [
                                (
                                    "rich_text",
                                    wagtail.blocks.RichTextBlock(editor="plain"),
                                ),
                                ("numeric", wagtail.blocks.FloatBlock()),
                                ("text", wagtail.blocks.CharBlock()),
                            ]
                        ),
                    ),
                    (
                        "iframe",
                        wagtail.blocks.StructBlock(
                            [
                                ("url", wagtail.blocks.URLBlock()),
                                (
                                    "caption",
                                    wagtail.blocks.RichTextBlock(
                                        editor="plain", required=False
                                    ),
                                ),
                            ]
                        ),
                    ),
                ],
                blank=True,
                use_json_field=True,
            ),
        ),
    ]
