from django.template import Library
register=Library()

@register.filter
def get_item(list,val):
	return list[val]