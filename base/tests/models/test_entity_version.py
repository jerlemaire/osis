##############################################################################
#
# OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from django.test import TestCase
from django.utils import timezone
import factory
import factory.fuzzy
import datetime
from base.models import entity_version
from base.tests.factories.entity import EntityFactory
from base.tests.factories.entity_version import EntityVersionFactory


class EntityVersionTest(TestCase):

    def setUp(self):
        self.entities = [EntityFactory() for x in range(3)]
        self.parent = EntityFactory()
        self.start_date = datetime.date(2015, 1, 1)
        self.end_date = datetime.date(2015, 12, 31)
        self.date_in_2015 = factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                    datetime.date(2015, 12, 30)).fuzz()
        self.date_in_2017 = factory.fuzzy.FuzzyDate(datetime.date(2017, 1, 1),
                                                    datetime.date(2017, 12, 30)).fuzz()

        self.entity_versions = [EntityVersionFactory(
                                entity=self.entities[x],
                                acronym="ENTITY_V_"+str(x),
                                title="This is the entity version "+str(x),
                                entity_type="FACULTY",
                                parent=self.parent,
                                start_date=self.start_date,
                                end_date=self.end_date
                                )
                                for x in range(3)]
        self.parent_entity_version = EntityVersionFactory(
                                        entity=self.parent,
                                        acronym="ENTITY_PARENT",
                                        title="This is the entity parent version",
                                        entity_type="SECTOR",
                                        start_date=self.start_date,
                                        end_date=self.end_date
                                        )

    def test_create_entity_version_same_entity_same_dates(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                entity=self.entities[0],
                start_date=self.start_date,
                end_date=self.end_date
                )

    def test_create_entity_version_same_entity_overlapping_dates_end_date_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                entity=self.entities[0],
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                   datetime.date(2014, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                 datetime.date(2015, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_entity_overlapping_dates_start_date_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                entity=self.entities[0],
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                   datetime.date(2015, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2016, 1, 1),
                                                 datetime.date(2020, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_entity_overlapping_dates_both_dates_out(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                entity=self.entities[0],
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                   datetime.date(2014, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2016, 1, 1),
                                                 datetime.date(2020, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_entity_overlapping_dates_both_dates_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                entity=self.entities[0],
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                   datetime.date(2015, 6, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 7, 1),
                                                 datetime.date(2015, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_acronym_overlapping_dates_end_date_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                acronym=self.entity_versions[0].acronym,
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                   datetime.date(2014, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                 datetime.date(2015, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_acronym_overlapping_dates_start_date_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                acronym=self.entity_versions[0].acronym,
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                   datetime.date(2015, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2016, 1, 1),
                                                 datetime.date(2020, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_acronym_overlapping_dates_both_dates_out(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                acronym=self.entity_versions[0].acronym,
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                   datetime.date(2014, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2016, 1, 1),
                                                 datetime.date(2020, 12, 30)).fuzz()
                )

    def test_create_entity_version_same_acronym_overlapping_dates_both_dates_in(self):
        with self.assertRaisesMessage(AttributeError, 'EntityVersion invalid parameters'):
            EntityVersionFactory(
                acronym=self.entity_versions[0].acronym,
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                                   datetime.date(2015, 6, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2015, 7, 1),
                                                 datetime.date(2015, 12, 30)).fuzz()
                )

    def test_find_entity_version(self):
        search_date = factory.fuzzy.FuzzyDate(datetime.date(2015, 1, 1),
                                              datetime.date(2015, 12, 30)).fuzz()
        self.assertEqual(entity_version.find("ENTITY_V_0", search_date), self.entity_versions[0])
        self.assertEqual(entity_version.find("ENTITY_V_1", search_date), self.entity_versions[1])
        self.assertEqual(entity_version.find("NOT_EXISTING_ENTITY", search_date), None)

    def test_search_matching_entity_version(self):
        self.assertCountEqual(
            entity_version.search(
                entity=self.entities[0].id,
                acronym="ENTITY_V_0",
                title="This is the entity version 0",
                entity_type="FACULTY",
                start_date=self.start_date,
                end_date=self.end_date
            ),
            [self.entity_versions[0]]
        )

    def test_search_not_matching_entity_versions(self):
        self.assertCountEqual(
            entity_version.search(
                entity=self.entities[0].id,
                acronym="FNVABAB",
                title="There is no version matching this search",
                entity_type="FACULTY",
                start_date=self.start_date,
                end_date=self.end_date
            ),
            []
        )

        self.assertCountEqual(
            entity_version.search(
                entity=self.entities[0].id,
                acronym="ENTITY_V_0",
                title="This is the entity version 0",
                entity_type="FACULTY",
                start_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                   datetime.date(2014, 12, 30)).fuzz(),
                end_date=factory.fuzzy.FuzzyDate(datetime.date(2010, 1, 1),
                                                 datetime.date(2014, 12, 30)).fuzz(),
            ),
            []
        )

    def test_version_direct_children_in_dates(self):
        self.assertCountEqual(self.parent_entity_version.find_direct_children(date=self.date_in_2015),
                              [self.entity_versions[x] for x in range(3)])
        self.assertEqual(self.parent_entity_version.count_direct_children(date=self.date_in_2015), 3)

    def test_version_direct_children_out_dates(self):
        self.assertCountEqual(self.parent_entity_version.find_direct_children(date=self.date_in_2017),
                              [])
        self.assertEqual(self.parent_entity_version.count_direct_children(date=self.date_in_2017), 0)

    def test_version_direct_children_with_null_end(self):
        for version in self.entity_versions:
            version.end_date = None
            version.save()
            self.assertIsNone(version.end_date)
        self.parent_entity_version.end_date = None
        self.parent_entity_version.save()

        self.assertCountEqual(self.parent_entity_version.find_direct_children(date=self.date_in_2015),
                              [self.entity_versions[x] for x in range(3)])
        self.assertEqual(self.parent_entity_version.count_direct_children(date=self.date_in_2015), 3)

        self.assertCountEqual(self.parent_entity_version.find_direct_children(date=self.date_in_2017),
                              [self.entity_versions[x] for x in range(3)])
        self.assertEqual(self.parent_entity_version.count_direct_children(date=self.date_in_2017), 3)

    def test_version_get_parent(self):
        for child in self.entity_versions:
            self.assertEqual(child.get_parent_version(date=self.date_in_2015), self.parent_entity_version)
            self.assertEqual(child.get_parent_version(date=self.date_in_2017), None)
