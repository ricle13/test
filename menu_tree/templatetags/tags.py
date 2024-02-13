from django import template
from django.urls import reverse, NoReverseMatch
from menu_tree.models import MenuItem
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag(takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    menu_items = MenuItem.objects.filter(menu_name=menu_name).select_related('parent').order_by('parent__id', 'order', 'id')

    def build_menu_tree(items):
        tree = {}
        for item in items:
            item.url_resolved = item.url
            try:
                item.url_resolved = reverse(item.url)
            except NoReverseMatch:
                pass
            item.is_active = request.path == item.url_resolved
            tree.setdefault(item.parent_id, []).append(item)
        return tree

    menu_tree = build_menu_tree(menu_items)

    def render_menu(items, parent=None):
        menu_html = ''
        for item in items.get(parent, []):
            children_html = render_menu(items, item.id)
            is_expanded = item.is_active or any(child.is_active for child in items.get(item.id, []))
            menu_html += f'<li class="{"active" if is_expanded else ""}"><a href="{item.url_resolved}">{item.name}</a>{children_html}</li>'
        if menu_html:
            menu_html = f'<ul class={"sub-menu" if parent else ""}>{menu_html}</ul>'
        return menu_html

    return mark_safe(render_menu(menu_tree))