#! /usr/bin/env python3
import requests
import json

class Auth:
    def __init__(self, target, username, password):
        self.host = 'http://{}/jams/api/authentication/login'.format(target)
        self.username = username
        self.password = password
        self.auth_request = {'username':self.username, 'password':self.password}

    def login(self):
        r = requests.post(self.host, data = self.auth_request)
        self.auth_response = r.json()


class Job:
    def __init__(self, target, access_token):
        self.host = 'http://{}/jams/api/job'.format(target)
        self.header = {'Authorization': 'bearer {}'.format(access_token)}

    def load(self, jobname):
        q_param = {'name': jobname}
        r = requests.get(self.host, headers = self.header, params=q_param)
        self.job = r.json()

    def add_element(self, element):
        self.job['elements'].append(element)

    def update(self):
        r = requests.put(self.host, headers = self.header, json=self.job)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

class ElementTemplate:
    def __init__(self, target, access_token):
        self.host = 'http://{}/jams/api/element/properties'.format(target)
        self.header = {'Authorization': 'bearer {}'.format(access_token)}

    def load(self, template):
        self.host = '{}/{}'.format(self.host, template)
        r = requests.get(self.host, headers = self.header)
        self.template = r.json()

    def property(self, property):
        for p in self.template['properties']:
            if p['propertyName'] == property:
                return p
        return null


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


def main():
    auth = Auth('10.1.1.33', 'tim.shaw', '1Lamentations2:13')

    auth.login()

    access_token = auth.auth_response['access_token']

    job = Job('10.1.1.33', access_token)
    job.load('\\Samples\\Sleep60')

    print('Job is: {}. Description is {}'.format(job.job['jobName'], job.job['description']))

    template = ResourceTemplate('10.1.1.33', access_token)
    template.load('ResourceRequirement')

    q_test = template.quantity_required(1)
    r_test = template.resource('Test_Resource_2')

    job.add_element(template.template)
    print(json.dumps(job.job, indent=4))
    job.update()

if __name__ == '__main__':
    main()
