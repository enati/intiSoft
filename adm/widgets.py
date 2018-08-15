from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe
from django.forms import widgets
from django.conf import settings

class RelatedFieldWidgetCanAdd(widgets.Select):

    class Media:
        js = (
            'intiSoft/js/MyRelatedObjectLookups.js',
        )

    def __init__(self, related_model, add_related_url=None, view_related_url=None, *args, **kw):
        super(RelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        self.actions = []

        # Be careful that here "reverse" is not allowed
        if add_related_url:
            self.actions.append('add')
            self.add_related_url = add_related_url

        if view_related_url:
            self.actions.append('view')
            self.view_related_url = view_related_url

    def render(self, name, value, *args, **kwargs):
        output = ''

        if 'add' in self.actions:
            self.add_related_url = reverse(self.add_related_url)
            output = [super(RelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
            output.append(u'<a href="%s?_popup=1" class="add-another input-group-addon" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> '
                          % (self.add_related_url, name))
            output.append(u'<img src="%sadmin/img/icon-addlink.svg" width="15" height="15" alt="%s"/></a>'
                          % (settings.STATIC_URL, ('Crear')))

        if 'view' in self.actions:
            self.view_related_url = reverse(self.view_related_url, args={'1'}).replace('1', '__fk__')
            output.append(
                u'<a data-href-template=%s?_popup=1 class="change-related input-group-addon" id="change_id_%s" onclick="return showAddAnotherPopup(this);"> '
                % (self.view_related_url, name))
            output.append(u'<img src="%sadmin/img/search.svg" width="15" height="15" alt="%s"/></a>'
                          % (settings.STATIC_URL, ('Ver')))

        return mark_safe(u''.join(output))


class NestedRelatedFieldWidgetCanAdd(widgets.Select):

    class Media:
        js = (
            'intiSoft/js/MyRelatedObjectLookups.js',
        )

    def __init__(self, parent_model, related_model, add_related_url=None, view_related_url=None, *args, **kw):
        super(NestedRelatedFieldWidgetCanAdd, self).__init__(*args, **kw)

        self.actions = []

        # Be careful that here "reverse" is not allowed
        if add_related_url:
            self.actions.append('add')
            self.add_related_url = add_related_url

        if view_related_url:
            self.actions.append('view')
            self.view_related_url = view_related_url

    def render(self, name, value, *args, **kwargs):
        output = ''

        if 'add' in self.actions:
            self.add_related_url = reverse(self.add_related_url)
            output = [super(NestedRelatedFieldWidgetCanAdd, self).render(name, value, *args, **kwargs)]
            output.append(u'<a data-href-template="%s?parent_id=__fk__&_popup=1" class="add-another input-group-addon" id="add_id_%s" onclick="return showRelatedObjectPopup(this);"> '
                          % (self.add_related_url, name))
            output.append(u'<img src="%sadmin/img/icon-addlink.svg" width="15" height="15" alt="%s"/></a>'
                          % (settings.STATIC_URL, ('Crear')))

        if 'view' in self.actions:
            self.view_related_url = reverse(self.view_related_url, args={'1'}).replace('1', '__fk__')
            output.append(
                u'<a data-href-template=%s?_popup=1 class="change-related input-group-addon" id="change_id_%s" onclick="return showRelatedObjectPopup(this);"> '
                % (self.view_related_url, name))
            output.append(u'<img src="%sadmin/img/search.svg" width="15" height="15" alt="%s"/></a>'
                          % (settings.STATIC_URL, ('Ver')))

        return mark_safe(u''.join(output))