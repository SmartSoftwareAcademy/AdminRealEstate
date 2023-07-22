from django import template

register = template.Library()

@register.filter
def multiply_html_element(num, html_element):
    return html_element * int(num)