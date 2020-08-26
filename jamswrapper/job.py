import requests

class Job:
    def __init__(self, auth):
        self._auth = auth
        self._target = 'http://{}/jams/api/job'.format(auth.host())

    def load(self, jobname):
        q_param = {'name': jobname}
        r = requests.get(self._target, headers = self._auth.header(), params=q_param)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        else:
            self._job = r.json()

    def job(self):
        return self._job

    def add_element(self, element):
        self._job['elements'].append(element)

    def update(self):
        r = requests.put(self._target, headers = self._auth.header(), json=self._job)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

