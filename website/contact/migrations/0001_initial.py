# Generated by Django 4.0.6 on 2022-09-04 14:44

import django.core.validators
import django.db.models.deletion
import wagtail.blocks
import wagtail.contrib.typed_table_block.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks
import wagtail.search.index
import wagtailmetadata.models
from django.db import migrations, models

import website.contrib.code_block.blocks


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("wagtailcore", "0069_log_entry_jsonfield"),
        ("images", "0001_initial"),
        ("unsplash", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OnlineAccount",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=64, unique=True)),
                ("url", models.URLField()),
                ("username", models.CharField(max_length=64)),
                (
                    "icon",
                    models.CharField(
                        blank=True,
                        max_length=64,
                        validators=[
                            django.core.validators.RegexValidator("[a-z-\\\\s]")
                        ],
                    ),
                ),
            ],
            bases=(models.Model, wagtail.search.index.Indexed),
        ),
        migrations.CreateModel(
            name="ContactPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("subtitle", wagtail.fields.RichTextField(blank=True)),
                (
                    "body",
                    wagtail.fields.StreamField(
                        [
                            ("embed", wagtail.embeds.blocks.EmbedBlock()),
                            ("rich_text", wagtail.blocks.RichTextBlock()),
                            (
                                "lorem",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "paragraphs",
                                            wagtail.blocks.IntegerBlock(min_value=1),
                                        )
                                    ]
                                ),
                            ),
                            ("html", wagtail.blocks.RawHTMLBlock()),
                            (
                                "image",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "image",
                                            wagtail.images.blocks.ImageChooserBlock(),
                                        ),
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
                                        (
                                            "always_show_header",
                                            wagtail.blocks.BooleanBlock(default=False),
                                        ),
                                    ]
                                ),
                            ),
                            (
                                "tangent",
                                wagtail.blocks.StructBlock(
                                    [
                                        (
                                            "name",
                                            wagtail.blocks.CharBlock(max_length=64),
                                        ),
                                        (
                                            "content",
                                            wagtail.blocks.RichTextBlock(
                                                editor="simple"
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
                                            wagtail.blocks.RichTextBlock(
                                                editor="plain"
                                            ),
                                        ),
                                        ("numeric", wagtail.blocks.FloatBlock()),
                                        ("text", wagtail.blocks.CharBlock()),
                                    ]
                                ),
                            ),
                        ],
                        blank=True,
                        use_json_field=True,
                    ),
                ),
                (
                    "hero_image",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="images.customimage",
                    ),
                ),
                (
                    "hero_unsplash_photo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="unsplash.unsplashphoto",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("wagtailcore.page", wagtailmetadata.models.MetadataMixin),
        ),
    ]
