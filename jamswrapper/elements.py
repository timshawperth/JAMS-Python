import requests

class ElementTemplate:
    def __init__(self, auth):
        self._auth = auth
        self._host = 'http://{}/jams/api/element/properties'.format(auth.host())

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
    def quantity_required(self, qty):
        res =  ElementTemplate.property(self, 'QuantityRequired')
        res['currentValue'] = qty
        return res

    def resource(self, res_name):
        res = ElementTemplate.property(self, 'Resource')
        r1 = res['defaultValue'].copy()
        r1['resourceName'] = res_name
        res['currentValue'] = r1
        return res

