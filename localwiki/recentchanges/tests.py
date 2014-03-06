"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from .utils import take_n_from


class TakeNFromTests(TestCase):
    def setUp(self):
        self.pages = ['front page', 'duboce park', 'cows on fire', 'farts', 'more cows', 'duboce park', 'hi']
        self.pages = sorted(self.pages, reverse=True)
        self.maps = ['front page map', 'corn', 'holy', 'apple']
        self.maps = sorted(self.maps, reverse=True)
        self.files = ['front page', 'duboce park whoa', 'aaaaaaaaaaaaaaa', 'aaaa', 'aaa']
        self.files = sorted(self.files, reverse=True)

    def test_basic_take(self):
        ls = ((self.pages, 0), (self.maps, 0), (self.files, 0))

        all_sorted = sorted(self.pages + self.maps + self.files, reverse=True)

        items, indexes = take_n_from(ls, 3)
        self.assertEqual(items, all_sorted[:3])
        self.assertEqual(indexes, [2, 1, 0])

    def test_take_general(self):
        ls = ((self.pages, 0), (self.maps, 0), (self.files, 0))

        all_sorted = sorted(self.pages + self.maps + self.files, reverse=True)

        for i in range(0, len(all_sorted)):
            items, indexes = take_n_from(ls, i)
            self.assertEqual(items, all_sorted[:i])

    def test_take_more_than_left(self):
        ls = ((self.pages, 0), (self.maps, 0), (self.files, 0))

        all_sorted = sorted(self.pages + self.maps + self.files, reverse=True)

        items, indexes = take_n_from(ls, len(all_sorted) + 1)
        self.assertEqual(len(items), len(all_sorted))
