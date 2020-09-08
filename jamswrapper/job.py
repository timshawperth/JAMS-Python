import requests

class Job:
    _auth = None
    _target = None
    _job = None
    _newjob = {'jobName':'', 'parentFolderName':'', 'description':'', 'methodName':''}

    def __init__(self, auth, jobname,  parent_folder_name=None, method_name=None, desc=''):
        if jobname == None:
            raise 'Must supply a job name'

        self._auth = auth
        self._target = 'http://{}/jams/api/job'.format(auth.host())

        if parent_folder_name == None and method_name == None:
            self.load(jobname)
        else:
            self._newjob['jobName'] = jobname
            self._newjob['parentFolderName'] = parent_folder_name
            self._newjob['methodName'] = method_name
            self._newjob['description'] = desc
            self._create()

    def _create(self):
        r = requests.post(self._target, headers=self._auth.header(), json=self._newjob)
        # A 201 is a successful result of creatnig a job
        if r.status_code != 201:
            r.raise_for_status()
        else:
            self.load(self._newjob['jobName'])

    def load(self, jobname):
        q_param = {'name': jobname}
        r = requests.get(self._target, headers=self._auth.header(), params=q_param)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()
        else:
            self._job = r.json()

    def get(self, attr):
        return self._job[attr]

    def add_element(self, element):
        if self._job == None:
            raise Exception('No job available to add element to')
        self._job['elements'].append(element.template())

    def update(self):
        if self._job == None:
            raise Exception('No job available to update')
        r = requests.put(self._target, headers=self._auth.header(), json=self._job)
        if r.status_code != requests.codes.ok:
            r.raise_for_status()

