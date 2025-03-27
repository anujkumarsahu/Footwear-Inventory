# templatetags/check_permissions.py
from django import template

register = template.Library()

def get_menu_structure(context):
    """Safely retrieve the menu structure from the session."""
    request = context.get('request')
    if request is None:
        return {}

    menu_structure = request.session.get('menu_structure', {})
    if not isinstance(menu_structure, dict):
        return {}

    return menu_structure

@register.simple_tag(takes_context=True)
def check_action_permission(context, menu_name, action):
    """
    Optimized permission check with improved error handling and efficient logic.
    """
    menu_structure = get_menu_structure(context)

    try:
        return any(
            child_menu.get('action_permissions', {}).get(action, False)
            for parent_menu in menu_structure.values()
            if isinstance(parent_menu, dict)
            for child_menu in parent_menu.get('children', [])
            if isinstance(child_menu, dict) and child_menu.get('name') == menu_name
        )
    except Exception:   
        return False

# Example Usage in Template
# {% load check_permissions %}
# {% if check_action_permission 'Users' 'is_save' %}
#     <a href="/dashboard/add/">Add New Item</a>
# {% endif %}
