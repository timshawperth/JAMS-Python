import requests

class Property:
    _auth = None
    _target = None
    _properties = None

    def __init__(self, auth, property_of):
        self._auth = auth
        self._target = 'http://{}/jams/api/propertydefinition/{}'.format(auth.host(), property_of)
        r = requests.get(self._target, headers = self._auth.header())
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        else:
            self._properties = r.json()

    def property(self):
        return self._properties

    def by_name(self, property_name):
        for p in self._properties:
            if p['propertyName'] == property_name:
                return p

'''
 Use an instance of this to build a current value dict to tag onto a property as the 'currentValue'.
 Got the idea of this from: https://jaxenter.com/implement-switch-case-statement-python-138315.html
 Is tidier than an if...elif... construct.
 To add anew reference type simply add the new def and return the appropriate dict.
'''
class ValueSwitch:
    def reference_names(self, reference, value):
        method = getattr(self, reference, lambda value: 'Invalid Reference type {}'.format(reference))
        return method(value)

    def AgentReference(self, agent_name):
        return {'$type': 'MVPSI.JAMS.Models.AgentReference, JAMS.Models', 'agentName': agent_name}

    def BatchQueueReference(self, queue_name):
        return {'$type': 'MVPSI.JAMS.Models.BatchQueueReference, JAMS.Models', 'queueName': queue_name}

    def ResourceReference(self, resource_name):
        return {'$type': 'MVPSI.JAMS.ResourceReference, JAMS.Models', 'resourceName': resource_name }

    def CredentialReference(self, credential_name):
        return {'$type': 'MVPSI.JAMS.Models.CredentialReference, JAMS.Models', 'credentialName': credential_name }

    def VariableReference(self, variable_name):
        return {'$type': 'MVPSI.JAMS.Models.VariableReference, JAMS.Models', 'variableName': variable_name }


def main():
    a = ValueSwitch()
    res = a.reference_names('AgentReference', 'centos1')
    print('Data structure is: {}'.format(res))
    res1 = a.reference_names('DeltaTime', 'bad value')
    print(res1)

if __name__ == '__main__':
    main()
