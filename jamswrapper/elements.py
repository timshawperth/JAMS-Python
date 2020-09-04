import requests

class ElementTemplate:
    def __init__(self, auth):
        self._auth = auth
        self._host = 'http://{}/jams/api/element/properties'.format(auth.host())
        self._template = None

    def load(self, template):
        self._host = '{}/{}'.format(self._host, template)
        r = requests.get(self._host, headers = self._auth.header())
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        self._template = r.json()

    def template(self):
        return self._template

    def property(self, property):
        for p in self._template['properties']:
            if p['propertyName'] == property:
                return p
        return None


class ResourceTemplate(ElementTemplate):
    def __init__(self, auth):
        super(ResourceTemplate, self).__init__(auth)
        ElementTemplate.load(self,'ResourceRequirement')

    def quantity_required(self, qty):
        res =  ElementTemplate.property(self, 'QuantityRequired')
        res['currentValue'] = qty

    def resource(self, res_name):
        res = ElementTemplate.property(self, 'Resource')
        tmp = res['defaultValue'].copy()
        tmp['resourceName'] = res_name
        res['currentValue'] = tmp

class ScheduleTemplate(ElementTemplate):
    def __init__(self, auth):
        super(ScheduleTemplate, self).__init__(auth)
        ElementTemplate.load(self,'ScheduleTrigger')

    def scheduled_date(self, datestring):
        res = ElementTemplate.property(self, 'ScheduledDate')
        res['currentValue'] = datestring

    def scheduled_time(self, time_string):
        res = ElementTemplate.property(self, 'ScheduledTime')
        tmp = res['defaultValue'].copy()
        tmp['totalSeconds'] = time_string
        res['currentValue'] = tmp
