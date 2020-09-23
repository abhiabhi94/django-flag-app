from django import template


register = template.Library()


@register.simple_tag(name='render_field')
def render_field(field, **kwargs):
    field.field.widget.attrs.update(kwargs)
    return field
