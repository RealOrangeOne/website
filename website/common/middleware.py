from django_minify_html.middleware import MinifyHtmlMiddleware


class CustomMinifyHtmlMiddleware(MinifyHtmlMiddleware):
    minify_args = {
        "do_not_minify_doctype": True,
        "ensure_spec_compliant_unquoted_attribute_values": True,
        "keep_spaces_between_attributes": True,
    }
