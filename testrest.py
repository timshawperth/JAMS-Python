#! /usr/bin/env python3
import requests
import json
import jamswrapper.auth as Auth
import jamswrapper.job as Job
import jamswrapper.elements


def main():
    host = 'replace with hostname or ip address of JAMS Web server'
    user = 'user name to connect as'
    password = 'password for user'

    auth = Auth.Auth(host, user, password)

    auth.login()


    job = Job.Job(auth,'\\Samples\\Sleep60')

    print('Job is: {}. Description is {}'.format(job.get('jobName'), job.get('description')))

    resource = jamswrapper.elements.ResourceTemplate(auth)

    resource.quantity_required(1)
    resource.resource('Test_Resource_2')

    job.add_element(resource)

    schedule = jamswrapper.elements.ScheduleTemplate(auth)
    schedule.scheduled_date('weekdays')
# Time in a schedule is seconds since midnight    
    schedule.scheduled_time(25200)
    job.add_element(schedule)
    job.update()

if __name__ == '__main__':
    main()
