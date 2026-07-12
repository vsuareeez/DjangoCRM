from django import template

register = template.Library()


@register.filter
def tint(pk):
    """{{ record.pk|tint }} → a/b/c/d (tinte del avatar según el id)."""
    return 'abcd'[pk % 4]


@register.filter
def initials(value):
    """Iniciales para el avatar: acepta un Record o un nombre completo."""
    if hasattr(value, 'first_name'):
        nombre = f"{value.first_name} {value.last_name}".strip()
    else:
        nombre = str(value).strip()
    partes = nombre.split()
    if not partes:
        return '?'
    return (partes[0][:1] + (partes[-1][:1] if len(partes) > 1 else '')).upper()
