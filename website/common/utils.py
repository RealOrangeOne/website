from wagtail.models import get_page_models as get_wagtail_page_models, Page

def get_page_models():
    page_models = get_wagtail_page_models().copy()
    page_models.remove(Page)
    return page_models
