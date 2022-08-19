# Generated by Django 4.0.6 on 2022-08-19 12:13

import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations

import website.contrib.code_block.blocks


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0002_contactpage"),
    ]

    operations = [
        migrations.AlterField(
            model_name="contactpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                    (
                        "rich_text",
                        wagtail.blocks.RichTextBlock(
                            features=[
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
                                "snippet-link",
                                "snippet-embed",
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
                    (
                        "image",
                        wagtail.blocks.StructBlock(
                            [
                                ("image", wagtail.images.blocks.ImageChooserBlock()),
                                (
                                    "caption",
                                    wagtail.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "document-link",
                                            "code",
                                            "strikethrough",
                                            "snippet-link",
                                        ]
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
                                    wagtail.blocks.RichTextBlock(
                                        features=[
                                            "bold",
                                            "italic",
                                            "ol",
                                            "ul",
                                            "link",
                                            "document-link",
                                            "code",
                                            "strikethrough",
                                            "snippet-link",
                                        ]
                                    ),
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
                                        features=[
                                            "bold",
                                            "italic",
                                            "link",
                                            "document-link",
                                            "code",
                                            "strikethrough",
                                            "snippet-link",
                                        ]
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
