from django import template

register = template.Library()

@register.filter
def filter_by(queryset, field_value):
    """
    Filters a queryset by field and value
    Usage: {{ queryset|filter_by:"role:admin" }}
    """
    try:
        field_name, value = field_value.split(':', 1)
        
        # Handle boolean values
        if value.lower() == 'true':
            value = True
        elif value.lower() == 'false':
            value = False
            
        return queryset.filter(**{field_name: value})
    except ValueError:
        return queryset
    
@register.filter
def subtract(value, arg):
    """
    Subtracts the arg from the value
    Usage: {{ value|subtract:arg }}
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value