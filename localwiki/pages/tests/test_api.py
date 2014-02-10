import json

from django.contrib.auth.models import User, Group
from django.conf import settings

from rest_framework import status
from rest_framework.authtoken.models import Token

from main.api.test import APITestCase
from regions.models import Region

from .. models import Page


class PageAPITests(APITestCase):
    def setUp(self):
        super(PageAPITests, self).setUp()

        # Create the edit user and add it to the authenticated group
        self.edit_user = User(
            username="edituser", email="edituser@example.org", password="fakepassword")
        self.edit_user.save()
        all_group, created = Group.objects.get_or_create(name=settings.USERS_DEFAULT_GROUP)
        self.edit_user.groups.add(all_group)
        self.edit_user.save()

        self.sf_region = Region(full_name='San Francisco', slug='sf')
        self.sf_region.save()

        p = Page(region=self.sf_region)
        p.content = '<p>Dolores Park here</p>'
        p.name = 'Dolores Park'
        p.save()
        self.dolores_park = p

        p = Page(region=self.sf_region)
        p.content = '<p>Duboce Park here</p>'
        p.name = 'Duboce Park'
        p.save()
        self.duboce_park = p

    def test_basic_page_list(self):
        response = self.client.get('/api/pages/')
        jresp = json.loads(response.content)
        self.assertEqual(len(jresp['results']), 2)

    def test_basic_page_detail(self):
        response = self.client.get('/api/pages/?slug=dolores%20park')
        jresp = json.loads(response.content)
        self.assertEqual(len(jresp['results']), 1)
        self.assertEqual(jresp['results'][0]['name'], 'Dolores Park')

    def test_basic_page_post(self):
        self.client.force_authenticate(user=self.edit_user)

        data = {'name': 'Test Page', 'content': '<p>hi</p>', 'region': 'http://testserver/api/regions/%s/' % (self.sf_region.id)}
        resp = self.client.post('/api/pages/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_page_post_with_tags(self):
        self.client.force_authenticate(user=self.edit_user)

        data = {'name': 'Test Page with tags', 'content': '<p>hi with tags</p>',
                'tags': ['park', 'fun'],
                'region': 'http://testserver/api/regions/%s/' % (self.sf_region.id)}
        resp = self.client.post('/api/pages/', data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        jresp = json.loads(resp.content)
        self.assertEqual(set(jresp['tags']), set(['park', 'fun']))