from django.test import TestCase
from app.tests.base_test import BaseTest
from core import models as c_models

from datasets import models as ds

import logging
logging.disable(logging.CRITICAL)


class AddressRecordTests(BaseTest, TestCase):
    def tearDown(self):
        self.clean_tests()

    def test_seed_addresssearch(self):
        dataset = c_models.Dataset.objects.create(name='Building', model_name='Building')
        file = c_models.DataFile.objects.create(file=self.get_file(
            'mock_buildings_1.csv'), dataset=dataset)

        property = self.property_factory(bbl="1000010010", address="123 Fake Street", borough="MN", zipcode="99999")
        property2 = self.property_factory(bbl="1000010011", address="1-20 Real Street", borough="MN", zipcode="99999")
        property3 = self.property_factory(bbl="1000010012", address="100a Fake Street", borough="MN", zipcode="99999")

        ds.AddressRecord.build_table(file_path=file.file.path, overwrite=True)

        self.assertEqual(ds.AddressRecord.objects.count(), 15)
        address1 = ds.AddressRecord.objects.get(
            number="1", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(address1.buildingstreet, 'Fake Street')
        self.assertEqual(address1.buildingnumber, '1')
        self.assertEqual(address1.propertyaddress, property.address)

        self.assertEqual(bool(address1), True)
        address2 = ds.AddressRecord.objects.get(
            number="1a", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address2), True)
        self.assertEqual(address2.buildingstreet, 'Fake Street')
        self.assertEqual(address2.buildingnumber, '1a')
        self.assertEqual(address2.propertyaddress, property.address)

        address3 = ds.AddressRecord.objects.get(
            number="1", street="Real Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address3), True)
        address4 = ds.AddressRecord.objects.get(
            number="3", street="Real Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address4), True)
        address5 = ds.AddressRecord.objects.get(
            number="5", street="Real Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address5), True)
        doubles = ds.AddressRecord.objects.filter(
            number="1-10", street="Real Street", borough="Manhattan", zipcode="99999")
        address6 = doubles[0]
        self.assertEqual(bool(address6), True)
        address7 = doubles[1]
        self.assertEqual(bool(address7), True)
        address8 = ds.AddressRecord.objects.get(
            number="1-20", street="Real Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address8), True)
        address9 = ds.AddressRecord.objects.get(
            number="1-22", street="Real Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address9), True)
        address10 = ds.AddressRecord.objects.get(
            number="10 1/2", street="Half Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address10), True)
        address11 = ds.AddressRecord.objects.get(
            number="123", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address11), True)

        # skips property 2 due to key contstraint

        address12 = ds.AddressRecord.objects.get(
            number="100a", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address12), True)
        self.assertEqual(address12.buildingstreet, None)
        self.assertEqual(address12.buildingnumber, None)
        self.assertEqual(address12.propertyaddress, property3.address)

        address13 = ds.AddressRecord.objects.get(
            number="10-01", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address13), True)

        import pdb
        pdb.set_trace()
        address14 = ds.AddressRecord.objects.get(
            number="10-03", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address14), True)

        address15 = ds.AddressRecord.objects.get(
            number="10-05", street="Fake Street", borough="Manhattan", zipcode="99999")
        self.assertEqual(bool(address15), True)

    def test_seed_addresssearch_update(self):
        dataset = c_models.Dataset.objects.create(name='Building', model_name='Building')
        file = c_models.DataFile.objects.create(file=self.get_file(
            'mock_buildings_2.csv'), dataset=dataset)

        property = self.property_factory(bbl="1000010010")
        # no range, number
        building1 = self.building_factory(bin=1, lhnd="1", hhnd="1", stname="Fake Street",
                                          boro="1", zipcode="99999", property=property)

        ds.AddressRecord.build_table(file_path=file.file.path, overwrite=True)
        file2 = c_models.DataFile.objects.create(file=self.get_file(
            'mock_buildings_2_diff.csv'), dataset=dataset)
        building2 = self.building_factory(bin=2, lhnd="1", hhnd="1", stname="Real Street",
                                          boro="1", zipcode="99999", property=property)

        ds.AddressRecord.build_table(file_path=file2.file.path, overwrite=True)

        self.assertEqual(ds.AddressRecord.objects.count(), 2)
