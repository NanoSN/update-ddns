#! /usr/bin/env python

import requests
import socket
import settings

URL_TEMPLATE = ('http://dynupdate.no-ip.com/nic/update?hostname=%(host)s&'
                'myip=%(ip)s')


def get_public_ip():
    '''Returns the public ip for this computer.
    '''
    ip = requests.get('http://httpbin.org/ip')
    return ip.json()['origin']


def update_host_ip(username, password, ip, host):
    '''Updates the noip.com ip mapping for the given host.
    '''
    url = URL_TEMPLATE % {'host': host, 'ip': ip}
    r = requests.get(url, auth=(username, password))
    return (r.status_code, r.text)


def need_update(host):
    return get_public_ip() != socket.gethostbyname(host)

if __name__ == '__main__':
    if need_update(settings.HOSTNAME):
        r = update_host_ip(username=settings.USERNAME,
                           password=settings.PASSWORD,
                           host=settings.HOSTNAME,
                           ip=get_public_ip())

        print r
    else:
        print('Already up to date. Nothing to do.')
