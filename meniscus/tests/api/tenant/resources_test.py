from datetime import datetime
from meniscus.api.tenant.resources import *

from mock import MagicMock

import falcon
import unittest


def suite():
    suite = unittest.TestSuite()
    suite.addTest(WhenFormattingResponses())

    return suite


class WhenTestingVersionResources(unittest.TestCase):

    def test_getting_versrions(self):
        req = MagicMock()
        resp = MagicMock()
        
        resource = VersionResource()
        resource.on_get(req, resp)

        self.assertEqual(falcon.HTTP_200, resp.status)


class WhenFormattingResponses(unittest.TestCase):

    def test_format_tenant(self):
        tenant_proxy = {'id': 'identification',
                        'tenant_id': 'tenant id',
                        'should_never': 'see_mee'}

        formatted_tenant = format_tenant(tenant_proxy)

        self.assertEqual(formatted_tenant['id'], 'identification')

        self.assertEqual(formatted_tenant['tenant_id'], 'tenant id')

        self.assertFalse('should_never' in formatted_tenant)

    def test_format_event_producers(self):
        event_producer = {'name': 'Formatted Apache Log',
                          'pattern': 'apache_cee',
                          'should_never': 'see_mee'}

        formatted_event_producer = format_event_producer(
            event_producer)

        self.assertEqual(
            formatted_event_producer['name'], 'Formatted Apache Log')

        self.assertEqual(
            formatted_event_producer['pattern'], 'apache_cee')

        self.assertFalse('should_never' in formatted_event_producer)

    def test_format_host_profile(self):
        profile = {'id': 'profile id',
                   'name': 'profile name',
                   'superfluous': 'junk',
                   'event_producers': [{'name': 'Formatted Apache Log1',
                                        'pattern': 'apache_cee1'},
                                       {'name': 'Formatted Apache Log2',
                                        'pattern': 'apache_cee2'},
                                       {'name': 'Formatted Apache Log3',
                                        'pattern': 'apache_cee3',
                                        'superfluous': 'junk'}]}

        formatted_profile = format_host_profile(profile)

        self.assertEquals(formatted_profile['id'], 'profile id')

        self.assertEquals(formatted_profile['name'], 'profile name')

        self.assertFalse('superfluous' in formatted_profile)

        self.assertEqual(formatted_profile['event_producers'], [
            {'name': 'Formatted Apache Log1', 'pattern': 'apache_cee1'},
            {'name': 'Formatted Apache Log2', 'pattern': 'apache_cee2'},
            {'name': 'Formatted Apache Log3', 'pattern': 'apache_cee3'}])

    def test_format_host_profiles(self):
        profiles = [{'id': 'id0',
                     'name': 'profile0',
                     'superfluous': 'junk0',
                     'event_producers': [{'name': 'Formatted Apache Log01',
                                          'pattern': 'apache_cee01'},
                                         {'name': 'Formatted Apache Log02',
                                          'pattern': 'apache_cee02'},
                                         {'name': 'Formatted Apache Log03',
                                          'pattern': 'apache_cee03',
                                         'superfluous': 'junk'}]},
                    {'id': 'id1',
                     'name': 'profile1',
                     'superfluous': 'junk1',
                     'event_producers': [{'name': 'Formatted Apache Log11',
                                          'pattern': 'apache_cee11'},
                                         {'name': 'Formatted Apache Log12',
                                          'pattern': 'apache_cee12'},
                                         {'name': 'Formatted Apache Log13',
                                          'pattern': 'apache_cee13',
                                          'superfluous': 'junk'}]},
                    {'id': 'id2',
                     'name': 'profile2',
                     'superfluous': 'junk2',
                     'event_producers': [{'name': 'Formatted Apache Log21',
                                          'pattern': 'apache_cee21'},
                                         {'name': 'Formatted Apache Log22',
                                          'pattern': 'apache_cee22'},
                                         {'name': 'Formatted Apache Log23',
                                          'pattern': 'apache_cee23',
                                          'superfluous': 'junk'}]}]

        formatted_profiles = format_host_profiles(profiles)

        for formatted_profile in formatted_profiles:
            self.assertTrue('id' in formatted_profile)
            self.assertTrue('name' in formatted_profile)
            self.assertFalse('superfluous' in formatted_profile)
            self.assertTrue('event_producers' in formatted_profile)
            for event_producer in formatted_profile['event_producers']:
                self.assertTrue('name' in event_producer)
                self.assertTrue('pattern' in event_producer)
                self.assertFalse('superfluous' in event_producer)

    def test_format_host(self):
        host = {'id': 'host_id00',
                'hostname': 'host_name00',
                'ip_address': 'ip_address00',
                'superfluous': 'junk',
                'profile': {'id': 'profile id',
                            'name': 'profile name',
                            'superfluous': 'junk',
                            'event_producers': [
                                {'name': 'Formatted Apache Log1',
                                 'pattern': 'apache_cee1'},
                                {'name': 'Formatted Apache Log2',
                                 'pattern': 'apache_cee2'},
                                {'name': 'Formatted Apache Log3',
                                 'pattern': 'apache_cee3',
                                 'superfluous': 'junk'}]}}

        formatted_host = format_host(host)

        self.assertEquals(formatted_host['id'], 'host_id00')

        self.assertEquals(formatted_host['hostname'], 'host_name00')

        self.assertEquals(formatted_host['ip_address'], 'ip_address00')

        self.assertFalse('superfluous' in formatted_host)

        self.assertEquals(formatted_host['profile']['id'], 'profile id')

        self.assertEquals(formatted_host['profile']['name'], 'profile name')

        for event_producer in formatted_host['profile']['event_producers']:
            self.assertTrue('name' in event_producer)
            self.assertTrue('pattern' in event_producer)
            self.assertFalse('superfluous' in event_producer)

    def test_format_hosts(self):
        hosts = [{'id': 'host_id00',
                  'hostname': 'host_name00',
                  'ip_address': 'ip_address00',
                  'superfluous': 'junk',
                  'profile': {'id': 'profile id',
                              'name': 'profile name',
                              'superfluous': 'junk',
                              'event_producers': [
                                {'name': 'Formatted Apache Log1',
                                 'pattern': 'apache_cee1'},
                                {'name': 'Formatted Apache Log2',
                                 'pattern': 'apache_cee2'},
                                {'name': 'Formatted Apache Log3',
                                 'pattern': 'apache_cee3',
                                 'superfluous': 'junk'}]}},
                 {'id': 'host_id01',
                  'hostname': 'host_name01',
                  'ip_address': 'ip_address01',
                  'superfluous': 'junk',
                  'profile': {'id': 'profile id',
                              'name': 'profile name',
                              'superfluous': 'junk',
                              'event_producers': [
                                  {'name': 'Formatted Apache Log1',
                                   'pattern': 'apache_cee1'},
                                  {'name': 'Formatted Apache Log2',
                                   'pattern': 'apache_cee2'},
                                  {'name': 'Formatted Apache Log3',
                                   'pattern': 'apache_cee3',
                                   'superfluous': 'junk'}]}},
                 {'id': 'host_id02',
                  'hostname': 'host_name02',
                  'ip_address': 'ip_address02',
                  'superfluous': 'junk',
                  'profile': {'id': 'profile id',
                              'name': 'profile name',
                              'superfluous': 'junk',
                              'event_producers': [
                                  {'name': 'Formatted Apache Log1',
                                   'pattern': 'apache_cee1'},
                                  {'name': 'Formatted Apache Log2',
                                   'pattern': 'apache_cee2'},
                                  {'name': 'Formatted Apache Log3',
                                   'pattern': 'apache_cee3',
                                   'superfluous': 'junk'}]}}]

        formatted_hosts = format_hosts(hosts)

        for formatted_host in formatted_hosts:
            self.assertTrue('id' in formatted_host)
            self.assertTrue('hostname' in formatted_host)
            self.assertTrue('ip_address' in formatted_host)
            self.assertFalse('superfluous' in formatted_host)
            self.assertTrue('id' in formatted_host['profile'])
            self.assertTrue('name' in formatted_host['profile'])
            self.assertFalse('superfluous' in formatted_host['profile'])


if __name__ == '__main__':
    unittest.main()
