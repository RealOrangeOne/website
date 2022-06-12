from wagtail.models import Page


class BasePage(Page):
    class Meta:
        abstract = True

    @classmethod
    @property
    def body_class(cls) -> str:
        return "page-" + cls._meta.db_table.replace("_", "-")
