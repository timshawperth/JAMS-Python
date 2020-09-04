import requests

class Job:
    _job = None

    def __init__(self, auth, jobname=None):
        self._auth = auth
        self._target = 'http://{}/jams/api/job'.format(auth.host())
        if jobname != None:
            self.load(jobname)

    def load(self, jobname):
        q_param = {'name': jobname}
        r = requests.get(self._target, headers = self._auth.header(), params=q_param)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        else:
            self._job = r.json()
#            return self._job

    def get(self, attr):
        return self._job[attr]

    def add_element(self, element):
        if self._job == None:
            raise Exception('No job available to add element to')
        self._job['elements'].append(element.template())

    def update(self):
        if self._job == None:
            raise Exception('No job available to update')
        r = requests.put(self._target, headers = self._auth.header(), json=self._job)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

