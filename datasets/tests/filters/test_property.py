from django.test import TestCase
from django.urls import include, path
from rest_framework.test import APITestCase, URLPatternsTestCase
from app.tests.base_test import BaseTest
import datetime
from datasets import models as ds

import logging
logging.disable(logging.CRITICAL)


class PropertyFilterTests(BaseTest, TestCase):
    urlpatterns = [
        path('', include('datasets.urls')),
    ]

    def tearDown(self):
        self.clean_tests()

    def test_yearbuilt_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=2000)
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1900)

        query = '/properties/?yearbuilt__gte=1950'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_legalclassb_units(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=2000)
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1900)
        hpdbuilding1 = self.hpdbuildingrecord_factory(
            property=property1, legalclassb=1)

        query = '/properties/?propertyannotation__legalclassb__gte=1'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_managementprogram(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=2000)
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1900)
        hpdbuilding1 = self.hpdbuildingrecord_factory(
            property=property1, managementprogram="7A")

        # Positive
        query = '/properties/?propertyannotation__managementprogram=7A'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_community_field(self):
        cd = self.community_factory(id=101)
        property1 = self.property_factory(bbl=1, cd=cd)
        property2 = self.property_factory(bbl=2)

        query = '/properties/?cd=101'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_zipcode_field(self):
        zipcode = self.zipcode_factory(id=11111)
        property1 = self.property_factory(bbl=1, zipcode=zipcode)
        property2 = self.property_factory(bbl=2)

        query = '/properties/?zipcode=11111'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_stateassembly_field(self):
        stateassembly = self.state_assembly_factory(id=10)
        property1 = self.property_factory(bbl=1, stateassembly=stateassembly)
        property2 = self.property_factory(bbl=2)

        query = '/properties/?stateassembly=10'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_statesenate_field(self):
        statesenate = self.state_senate_factory(id=20)
        property1 = self.property_factory(bbl=1, statesenate=statesenate)
        property2 = self.property_factory(bbl=2)

        query = '/properties/?statesenate=20'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_bbls_field(self):
        property1 = self.property_factory(bbl=1)
        property2 = self.property_factory(bbl=2)
        property3 = self.property_factory(bbl=3)

        query = '/properties/?bbls=1,2'
        response = self.client.get(query, format="json")
        content = response.data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(content[1]['bbl'], '2')

    def test_hpdviolations_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(10):
            self.hpdviolation_factory(property=property1)

        for i in range(5):
            self.hpdviolation_factory(property=property2)

        query = '/properties/?hpdviolations__gte=10'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_hpdviolationsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2017-01-01")

        for i in range(1):
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")

        query = '/properties/?hpdviolations__start=2018-01-01&hpdviolations__end=2019-01-01&hpdviolations__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_dobviolationsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")

        for i in range(5):
            self.dobviolation_factory(
                property=property1, issuedate="2017-01-01")

        for i in range(1):
            self.dobviolation_factory(
                property=property2, issuedate="2018-01-01")

        query = '/properties/?dobviolations__start=2018-01-01&dobviolations__end=2019-01-01&dobviolations__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_ecbviolationsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.ecbviolation_factory(
                property=property1, issuedate="2018-01-01")

        for i in range(5):
            self.ecbviolation_factory(
                property=property1, issuedate="2017-01-01")

        for i in range(1):
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")

        query = '/properties/?ecbviolations__start=2018-01-01&ecbviolations__end=2019-01-01&ecbviolations__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_hpdcomplaintsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.hpdcomplaint_factory(
                property=property1, receiveddate="2018-01-01")

        for i in range(5):
            self.hpdcomplaint_factory(
                property=property1, receiveddate="2017-01-01")

        for i in range(1):
            self.hpdcomplaint_factory(
                property=property2, receiveddate="2018-01-01")

        query = '/properties/?hpdcomplaints__start=2018-01-01&hpdcomplaints__end=2019-01-01&hpdcomplaints__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_dobcomplaintsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.dobcomplaint_factory(
                property=property1, dateentered="2018-01-01")

        for i in range(5):
            self.dobcomplaint_factory(
                property=property1, dateentered="2017-01-01")

        for i in range(1):
            self.dobcomplaint_factory(
                property=property2, dateentered="2018-01-01")

        query = '/properties/?dobcomplaints__start=2018-01-01&dobcomplaints__end=2019-01-01&dobcomplaints__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_evictionsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.eviction_factory(property=property1,
                                  executeddate="2018-01-01")

        for i in range(5):
            self.eviction_factory(property=property1,
                                  executeddate="2017-01-01")

        for i in range(1):
            self.eviction_factory(property=property2,
                                  executeddate="2018-01-01")

        query = '/properties/?evictions__start=2018-01-01&evictions__end=2019-01-01&evictions__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_dobissuedpermitsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.dobissuedpermit_factory(
                property=property1, issuedate="2018-01-01")

        for i in range(5):
            self.dobissuedpermit_factory(
                property=property1, issuedate="2017-01-01")

        for i in range(1):
            self.dobissuedpermit_factory(
                property=property2, issuedate="2018-01-01")

        query = '/properties/?dobissuedpermits__start=2018-01-01&dobissuedpermits__end=2019-01-01&dobissuedpermits__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_dobfiledpermitsdates_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)

        for i in range(5):
            self.dobfiledpermit_factory(
                property=property1, datefiled="2018-01-01")

        for i in range(5):
            self.dobfiledpermit_factory(
                property=property1, datefiled="2017-01-01")

        for i in range(1):
            self.dobfiledpermit_factory(
                property=property2, datefiled="2018-01-01")

        query = '/properties/?dobfiledpermits__start=2018-01-01&dobfiledpermits__end=2019-01-01&dobfiledpermits__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_rsunitslost_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)
        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2017=1)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2017=5)

        query = '/properties/?rsunitslost__start=2007&rsunitslost__end=2017&rsunitslost__gte=0.9'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_rsunitslost_field_2(self):
        # With only a start year in url
        # Use the taxbills version year # as latest year to search (default is 2017)
        dataset = self.dataset_factory(name="RentStabilizationRecord")
        file = self.datafile_factory(dataset=dataset, version="2018")

        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)
        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2018=1)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2018=5)

        query = '/properties/?rsunitslost__gte=0.9&rsunitslost__start=2007'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_rsunitslost_field_3(self):
        dataset = self.dataset_factory(name="RentStabilizationRecord")
        file = self.datafile_factory(dataset=dataset, version="2018")

        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)
        property3 = self.property_factory(bbl=3, council=council)
        property4 = self.property_factory(bbl=4, council=council)
        property5 = self.property_factory(bbl=5, council=council)

        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2018=1)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2018=5)
        self.rentstabilizationrecord_factory(
            property=property3, uc2007=10, uc2018=10)
        self.rentstabilizationrecord_factory(
            property=property4, uc2007=0, uc2018=11)
        self.rentstabilizationrecord_factory(
            property=property5, uc2007=10, uc2018=0)

        query = '/properties/?rsunitslost__gte=0.9&rsunitslost__start=2007'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(content[1]['bbl'], '5')

    def test_rsunitslost_field_4(self):
        dataset = self.dataset_factory(name="RentStabilizationRecord")
        file = self.datafile_factory(dataset=dataset, version="2018")

        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)
        property3 = self.property_factory(bbl=3, council=council)
        property4 = self.property_factory(bbl=4, council=council)
        property5 = self.property_factory(bbl=5, council=council)

        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2018=1)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2018=5)
        self.rentstabilizationrecord_factory(
            property=property3, uc2007=10, uc2018=10)
        self.rentstabilizationrecord_factory(
            property=property4, uc2007=0, uc2018=11)
        self.rentstabilizationrecord_factory(
            property=property5, uc2007=10, uc2018=0)

        query = '/properties/?rsunitslost__exact=0&rsunitslost__start=2007'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)  # number has somehow gone up
        self.assertEqual(content[0]['bbl'], '3')
        self.assertEqual(content[1]['bbl'], '4')

    def test_acrisrealmasteramount_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(bbl=1, council=council)
        property2 = self.property_factory(bbl=2, council=council)
        property3 = self.property_factory(bbl=3, council=council)
        acrismaster1 = self.acrismaster_factory(
            docamount=10, docdate="2018-01-01", doctype="DEED")
        acrismaster2 = self.acrismaster_factory(
            docamount=1, docdate="2018-01-01", doctype="DEED")
        acrismaster3 = self.acrismaster_factory(
            docamount=10, docdate="2018-01-01", doctype="RPTT")
        self.acrisreallegal_factory(master=acrismaster1, property=property1)
        self.acrisreallegal_factory(master=acrismaster2, property=property2)
        self.acrisreallegal_factory(master=acrismaster3, property=property3)

        query = '/properties/?acrisrealmasteramounts__start=2017-01-01&acrisrealmasteramounts__end=2018-01-01&acrisrealmasteramounts__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_acrisrealmasters_field(self):
        council = self.council_factory(id=1)
        # 5 in range
        property1 = self.property_factory(bbl=1, council=council)
        # only 1
        property2 = self.property_factory(bbl=2, council=council)
        # dates out of range
        property3 = self.property_factory(bbl=3, council=council)
        acrismaster2 = self.acrismaster_factory(
            docamount=1, docdate="2018-01-01")
        self.acrisreallegal_factory(master=acrismaster2, property=property2)

        # wrong doctype but all in range
        property4 = self.property_factory(bbl=4, council=council)

        for i in range(5):
            am = self.acrismaster_factory(doctype="DEED", docdate="2018-01-01")
            self.acrisreallegal_factory(master=am, property=property1)

        for i in range(5):
            am = self.acrismaster_factory(doctype="DEED", docdate="2010-01-01")
            self.acrisreallegal_factory(master=am, property=property3)

        for i in range(5):
            am = self.acrismaster_factory(
                doctype="hello", docdate="2018-01-01")
            self.acrisreallegal_factory(master=am, property=property4)

        # 5 sales between 2017-2018
        query = '/properties/?acrisrealmasters__start=2017-01-01&acrisrealmasters__end=2018-01-01&acrisrealmasters__gte=5'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_dobissuedpermits_field(self):
        council = self.council_factory(id=1)
        # 10 in range
        property1 = self.property_factory(bbl=1, council=council)
        # 10 out of range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(10):
            self.dobissuedpermit_factory(
                property=property1, issuedate="2018-01-01")

        for i in range(10):
            self.dobissuedpermit_factory(
                property=property2, issuedate="2010-01-01")

        for i in range(5):
            self.dobissuedpermit_factory(
                property=property3, issuedate="2018-01-01")

        # 10 permits between 2017-2018
        query = '/properties/?dobissuedpermits__start=2017-01-01&dobissuedpermits__end=2018-01-01&dobissuedpermits__gte=10'
        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_eviction_field(self):
        council = self.council_factory(id=1)
        # 10 in range
        property1 = self.property_factory(bbl=1, council=council)
        # 10 out of range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(10):
            self.eviction_factory(property=property1,
                                  executeddate="2018-01-01")

        for i in range(10):
            self.eviction_factory(property=property2,
                                  executeddate="2010-01-01")

        for i in range(5):
            self.eviction_factory(property=property3,
                                  executeddate="2018-01-01")

        # 10 permits between 2017-2018
        query = '/properties/?evictions__start=2017-01-01&evictions__end=2018-01-01&evictions__gte=10'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_taxlien_field(self):
        council = self.council_factory(id=1)
        # has tax lien in 2018
        property1 = self.property_factory(bbl=1, council=council)
        # has tax lien in 2017
        property2 = self.property_factory(bbl=2, council=council)
        # has no tax liens
        property3 = self.property_factory(bbl=3, council=council)

        self.taxlien_factory(property=property1, year="2018")
        self.taxlien_factory(property=property2, year="2017")

        # any buildings with tax liens in 2018
        query = '/properties/?taxlien=2018'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_subsidy_field(self):
        council = self.council_factory(id=1)
        # has lihtc ending 2018
        property1 = self.property_factory(bbl=1, council=council)
        # has j-51 ending 2018
        property2 = self.property_factory(bbl=2, council=council)
        # has lihtc ending 2025
        property3 = self.property_factory(bbl=3, council=council)

        self.coredata_factory(property=property1,
                              enddate="2018-01-01", programname="lihtc")
        self.coredata_factory(property=property1, enddate="2018-01-01",
                              programname="lihtc")  # duplicate which should get filtered out
        self.coredata_factory(property=property2,
                              enddate="2018-01-01", programname="j-51")
        self.coredata_factory(property=property3,
                              enddate="2025-01-01", programname="lihtc")

        # any lihtc buildings ending 2018
        query = '/properties/?subsidyprograms__programname=lihtc&coresubsidyrecord__enddate__lte=2018-01-01'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_subsidy_field_multiple_programs(self):
        council = self.council_factory(id=1)
        # * has lihtc ending 2018
        property1 = self.property_factory(bbl=1, council=council)
        # * has j-51 ending 2018
        property2 = self.property_factory(bbl=2, council=council)
        # has lihtc ending 2025
        property3 = self.property_factory(bbl=3, council=council)
        # has 421-a ending 2018
        property4 = self.property_factory(bbl=4, council=council)

        self.coredata_factory(property=property1,
                              enddate="2018-01-01", programname="lihtc")
        self.coredata_factory(property=property2,
                              enddate="2018-01-01", programname="j-51")
        self.coredata_factory(property=property3,
                              enddate="2025-01-01", programname="lihtc")
        self.coredata_factory(property=property4,
                              enddate="2018-01-01", programname="421-a")

        # any lihtc buildings ending 2018
        query = '/properties/?subsidyprograms__programname__any=lihtc,j-51&coresubsidyrecord__enddate__lte=2018-01-01'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(content[1]['bbl'], '2')


class PropertyAdvancedFilterTests(BaseTest, TestCase):
    def tearDown(self):
        self.clean_tests()

    def test_single_all_condition(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=2000)
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1900)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2017-01-01")

        for i in range(1):
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019
        query = '/properties/?q=*condition_0=AND+filter_0=hpdviolations__count__gte=5,hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_single_all_condition_single_field(self):
        council = self.council_factory(id=1)
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=2000)
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1900)
        property3 = self.property_factory(
            bbl=3, council=council, yearbuilt=1900)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")

        for i in range(5):
            self.hpdviolation_factory(
                property=property2, approveddate="2017-01-01")

        for i in range(1):
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")

        # properties with 5 HPD violations any date
        query = '/properties/?q=*condition_0=AND+filter_0=hpdviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(content[1]['bbl'], '2')

    def test_single_any_condition(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 DOB violations not in range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 DOB Violations in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2018-01-01")

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2017-01-01")
            self.dobviolation_factory(
                property=property2, issuedate="2017-01-01")

        for i in range(1):
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019 OR 5 DOB violations b/t 2018-2019
        # query = '/properties/?q=condition_0=OR+group_0A=hpdviolation__approveddate__gte=2018-01-01,hpdviolation__approveddate__lte=2019-01-01,hpdviolation__count__gte=5+group_0B=dobviolation__issuedate__gte=2018-01-01,dobviolation__issuedate__lte=2019-01-01,dobviolation__count__gte=5'
        query = '/properties/?q=*condition_0=OR+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '3' for d in content), True)

    def test_single_all_condition_multi_groups(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations and 5 DOB Violations in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 DOB violations in range, no HPD Violations in range
        property2 = self.property_factory(bbl=2, council=council)
        # 5HPD Violations and 5 DOB Violations in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2018-01-01")

        for i in range(5):
            self.dobviolation_factory(
                property=property2, issuedate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019 AND 5 DOB violations b/t 2018-2019
        # query = '/properties/?q=condition_0=AND+group_0A=hpdviolation__approveddate__gte=2018-01-01,hpdviolation__approveddate__lte=2019-01-01,hpdviolation__count__gte=5+group_0B=dobviolation__issuedate__gte=2018-01-01,dobviolation__issuedate__lte=2019-01-01,dobviolation__count__gte=5'
        query = '/properties/?q=*condition_0=AND+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+filter_0=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '3' for d in content), True)

    def test_multiple_condition_multi_groups_1(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations and 5 DOB Violations in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 HPD Violations and 5 ECB Violations in range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 HPD Violations in range
        property3 = self.property_factory(bbl=3, council=council)
        # 5 DOB Violations in range
        property4 = self.property_factory(bbl=4, council=council)
        # 5 ECB Violations in range and 5 DOB Violations in range
        property5 = self.property_factory(bbl=5, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property5, issuedate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_multiple_condition_multi_groups_2(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations and 5 DOB Violations in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 HPD Violations and 5 ECB Violations in range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 HPD Violations in range
        property3 = self.property_factory(bbl=3, council=council)
        # 5 DOB Violations in range
        property4 = self.property_factory(bbl=4, council=council)
        # 5 ECB Violations in range and 5 DOB Violations in range
        property5 = self.property_factory(bbl=5, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property5, issuedate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019 OR (5 DOB violations b/t 2018-2019 AND 5 ECB violations b/t 2018-2019)
        query = '/properties/?q=*condition_0=OR+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=AND+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+group_1B=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 4)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)
        self.assertEqual(any(d['bbl'] == '3' for d in content), True)
        self.assertEqual(any(d['bbl'] == '5' for d in content), True)

    def test_multiple_condition_multi_groups_3(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations and 5 DOB Violations in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 HPD Violations and 5 ECB Violations in range AND 5 HPD Complaints
        property2 = self.property_factory(bbl=2, council=council)
        # 5 HPD Violations in range
        property3 = self.property_factory(bbl=3, council=council)
        # 5 DOB Violations
        property4 = self.property_factory(bbl=4, council=council)
        # 5 HPD Violations and 5 ECB Violations in range
        property5 = self.property_factory(bbl=5, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdcomplaint_factory(
                property=property2, receiveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property5, issuedate="2018-01-01")

        # properties with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR (5 ECB violations b/t 2018-2019 AND 5 HPD Complaints b/t 2018-2019))

        query = '/properties/?q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=condition_2+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+*condition_2=AND+filter_2=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5+group_2A=hpdcomplaints__receiveddate__gte=2018-01-01,hpdcomplaints__receiveddate__lte=2019-01-01,hpdcomplaints__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_multiple_condition_multi_groups_4(self):
        council = self.council_factory(id=1)
        # 5 HPD Violations and 5 HPD Complaints in range
        property1 = self.property_factory(bbl=1, council=council)
        # 5 DOB Violations and 5 ECB Violations in range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 HPD Violations in range and 5 HPD Complaints NOT in range
        property3 = self.property_factory(bbl=3, council=council)
        # 5 DOB Violations in range
        property4 = self.property_factory(bbl=4, council=council)
        # 5 DOB Violations in range and 5 ECB violations NOT in range
        property5 = self.property_factory(bbl=5, council=council)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.hpdcomplaint_factory(
                property=property1, receiveddate="2018-01-01")
            self.dobviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.hpdcomplaint_factory(
                property=property3, receiveddate="2016-01-01")

            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property5, issuedate="2016-01-01")

        # properties with either (5 HPD violations b/t 2018- 2019 AND 5 HPD complaints b/t 2018-2019) OR (5 DOB violations b/t 2018-2019 AND 5 ECB violations b/t 2018-2019)
        # query = '/properties/?q=condition_0=OR+group_0a=*condition_1+group_0b=*condition_2+condition_1=AND+group_1a=hpdviolation__approveddate__gte=2018-01-01,hpdviolation__approveddate__lte=2019-01-01,hpdviolation__count__gte=5+group_1b=hpdcomplaint__receiveddate__gte=2018-01-01,hpdcomplaint__receiveddate__lte=2019-01-01,hpdcomplaint__count__gte=5+condition_2=AND+group_2a=dobviolation__issuedate__gte=2018-01-01,dobviolation__issuedate__lte=2019-01-01,dobviolation__count__gte=5+group_2b=ecbviolation__issuedate__gte=2018-01-01,ecbviolation__issuedate__lte=2019-01-01,ecbviolation__count__gte=5'

        query = '/properties/?q=*condition_0=OR+filter_0=condition_1+filter_0=condition_2+*condition_1=AND+filter_1=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+filter_1=hpdcomplaints__receiveddate__gte=2018-01-01,hpdcomplaints__receiveddate__lte=2019-01-01,hpdcomplaints__count__gte=5+*condition_2=AND+filter_2=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_2=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_rentstabilization_rules(self):
        council = self.council_factory(id=1)
        # loses 90% between 2007 - 2017
        property1 = self.property_factory(bbl=1, council=council)
        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2017=1)
        # loses 50% between 2007 - 2017
        property2 = self.property_factory(bbl=2, council=council)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2017=5)
        # loses 10% between 2007 - 2017
        property3 = self.property_factory(bbl=3, council=council)
        self.rentstabilizationrecord_factory(
            property=property3, uc2007=10, uc2017=9)
        # loses 0% between 2007 - 2017
        property4 = self.property_factory(bbl=4, council=council)
        self.rentstabilizationrecord_factory(
            property=property4, uc2007=10, uc2017=10)

        # properties that lost over 50% of rent stabilized units between 2007 and 2017
        query = '/properties/?q=*condition_0=AND+filter_0=rentstabilizationrecords__year__gte=2007,rentstabilizationrecords__year__gte=2017,rentstabilizationrecords__percent__gte=0.5'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_acrisamount_rules(self):
        council = self.council_factory(id=1)

        # sold for $10 in date range
        acrismaster1 = self.acrismaster_factory(
            documentid="a", doctype="DEED", docamount=10, docdate="2018-01-01")
        property1 = self.property_factory(bbl=1, council=council)
        self.acrisreallegal_factory(property=property1, master=acrismaster1)

        # sold for $1 in date range
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=1, docdate="2018-01-01")
        property2 = self.property_factory(bbl=2, council=council)
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # sold for $10 out of date range
        acrismaster3 = self.acrismaster_factory(
            documentid="c", doctype="DEED", docamount=10, docdate="2011-01-01")
        property3 = self.property_factory(bbl=3, council=council)
        self.acrisreallegal_factory(property=property3, master=acrismaster3)

        # tax document for $10 in date range
        acrismaster4 = self.acrismaster_factory(
            documentid="d", doctype="RPTT", docamount=10, docdate="2017-01-01")
        property4 = self.property_factory(bbl=4, council=council)
        self.acrisreallegal_factory(property=property4, master=acrismaster4)

        # properties that sold for over $5 between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=acrisreallegals__documentid__docdate__gte=2017-01-01,acrisreallegals__documentid__docdate__lte=2018-01-01,acrisreallegals__documentid__docamount__gte=5'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_acrisamount_rules_2(self):
        council = self.council_factory(id=1)

        # sold for $10 in date range
        acrismaster1 = self.acrismaster_factory(
            documentid="a", doctype="DEED", docamount=10, docdate="2018-01-01")
        property1 = self.property_factory(bbl=1, council=council)
        self.acrisreallegal_factory(property=property1, master=acrismaster1)

        # sold for $1 in date range
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=1, docdate="2018-01-01")
        property2 = self.property_factory(bbl=2, council=council)
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # sold for $10 out of date range
        acrismaster3 = self.acrismaster_factory(
            documentid="c", doctype="DEED", docamount=10, docdate="2011-01-01")
        property3 = self.property_factory(bbl=3, council=council)
        self.acrisreallegal_factory(property=property3, master=acrismaster3)

        # tax document for $10 in date range
        acrismaster4 = self.acrismaster_factory(
            documentid="d", doctype="RPTT", docamount=10, docdate="2017-01-01")
        property4 = self.property_factory(bbl=4, council=council)
        self.acrisreallegal_factory(property=property4, master=acrismaster4)

        # only hpd violations
        property5 = self.property_factory(bbl=5, council=council)

        for i in range(5):
            # self.hpdviolation_factory(property=property1, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")

        # properties that sold for over $5 between 2017-2018 OR +5 hpd violations
        query = '/properties/?q=*condition_0=OR+filter_0=acrisreallegals__documentid__docdate__gte=2017-01-01,acrisreallegals__documentid__docdate__lte=2018-01-01,acrisreallegals__documentid__docamount__gte=5+filter_1=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(content), 2)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(content[1]['bbl'], '5')

    def test_acrissales_rules(self):
        council = self.council_factory(id=1)

        # sold 5 times in date range
        property1 = self.property_factory(bbl=1, council=council)
        for i in range(5):
            am = self.acrismaster_factory(
                doctype="DEED", docamount=10, docdate="2018-01-01")
            self.acrisreallegal_factory(property=property1, master=am)

        # sold 1 time in date range
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=1, docdate="2018-01-01")
        property2 = self.property_factory(bbl=2, council=council)
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # properties with 5 sales between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=acrisreallegals__documentid__docdate__gte=2017-01-01,acrisreallegals__documentid__docdate__lte=2018-01-01,acrisreallegals__documentid__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_acrissales_rules_with_annotation(self):
        self.create_annotated_datasets(datetime.datetime.now())
        council = self.council_factory(id=1)

        # sold 5 times in date range
        property1 = self.property_factory(bbl=1, council=council)
        for i in range(5):
            am = self.acrismaster_factory(
                doctype="DEED", docamount=10, docdate="2018-01-01")
            self.acrisreallegal_factory(property=property1, master=am)

        # sold 1 time in date range
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=1, docdate="2018-01-01")
        property2 = self.property_factory(bbl=2, council=council)
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # properties with 5 sales between 2017-2018
        query = '/properties/?summary=true&summary-type=short-annotated&q=*condition_0=AND+filter_0=acrisreallegals__documentid__docdate__gte=2017-01-01,acrisreallegals__documentid__docdate__lte=2018-01-01,acrisreallegals__documentid__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')
        self.assertEqual(
            content[0]['acrisrealmasters__01/01/2017-01/01/2018'], 5)

    def test_acriscombined_rules(self):
        council = self.council_factory(id=1)

        # sold 5 times in date range, once with price
        property1 = self.property_factory(bbl=1, council=council)
        for i in range(5):
            am = self.acrismaster_factory(
                doctype="DEED", docamount=1, docdate="2018-01-01")
            self.acrisreallegal_factory(property=property1, master=am)
        am = self.acrismaster_factory(
            doctype="DEED", docamount=10, docdate="2018-01-01")
        self.acrisreallegal_factory(property=property1, master=am)

        # sold 1 time in date range with price
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=10, docdate="2018-01-01")
        property2 = self.property_factory(bbl=2, council=council)
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # sold 5 times with price, out of date range
        property3 = self.property_factory(bbl=3, council=council)
        for i in range(5):
            am3 = self.acrismaster_factory(
                doctype="DEED", docamount=10, docdate="2011-01-01")
            self.acrisreallegal_factory(property=property3, master=am3)

        # sold 5 times in date range, not with price
        property4 = self.property_factory(bbl=4, council=council)
        for i in range(5):
            am4 = self.acrismaster_factory(
                doctype="DEED", docamount=1, docdate="2018-01-01")
            self.acrisreallegal_factory(property=property4, master=am4)

        # sold 5 times not in date range, not with price, and 1 time in date range with price
        property5 = self.property_factory(bbl=5, council=council)
        for i in range(5):
            am = self.acrismaster_factory(
                doctype="DEED", docamount=1, docdate="2011-01-01")
            self.acrisreallegal_factory(property=property5, master=am)
        am = self.acrismaster_factory(
            doctype="DEED", docamount=10, docdate="2018-01-01")
        self.acrisreallegal_factory(property=property5, master=am)

        # properties with 5 sales between 2017-2018 and sold for over $5 between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=acrisreallegals__documentid__count__gte=5,acrisreallegals__documentid__docdate__gte=2018-01-01+filter_1=acrisreallegals__documentid__docamount__gte=10,acrisreallegals__documentid__docdate__gte=2018-01-01'
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_permitissuedjoined_rules(self):
        council = self.council_factory(id=1)
        # 10 in range
        property1 = self.property_factory(bbl=1, council=council)
        # 10 out of range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(10):
            self.dobissuedpermit_factory(
                property=property1, issuedate="2018-01-01")

        for i in range(10):
            self.dobissuedpermit_factory(
                property=property2, issuedate="2010-01-01")

        for i in range(5):
            self.dobissuedpermit_factory(
                property=property3, issuedate="2018-01-01")

        # 10 permits between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=dobissuedpermits__issuedate__gte=2017-01-01,dobissuedpermits__issuedate__lte=2018-01-01,dobissuedpermits__count__gte=10'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_filedpermit_rules(self):
        council = self.council_factory(id=1)
        # 10 in range
        property1 = self.property_factory(bbl=1, council=council)
        # 10 out of range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(10):
            self.dobfiledpermit_factory(
                property=property1, datefiled="2018-01-01")

        for i in range(10):
            self.dobfiledpermit_factory(
                property=property2, datefiled="2010-01-01")

        for i in range(5):
            self.dobfiledpermit_factory(
                property=property3, datefiled="2018-01-01")

        # 10 permits between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=dobfiledpermits__datefiled__gte=2017-01-01,dobfiledpermits__datefiled__lte=2018-01-01,dobfiledpermits__count__gte=10'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_eviction_rules(self):
        council = self.council_factory(id=1)
        # 10 in range
        property1 = self.property_factory(bbl=1, council=council)
        # 10 out of range
        property2 = self.property_factory(bbl=2, council=council)
        # 5 in range
        property3 = self.property_factory(bbl=3, council=council)

        for i in range(10):
            self.eviction_factory(property=property1,
                                  executeddate="2018-01-01")

        for i in range(10):
            self.eviction_factory(property=property2,
                                  executeddate="2010-01-01")

        for i in range(5):
            self.eviction_factory(property=property3,
                                  executeddate="2018-01-01")

        # 10 permits between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=evictions__executeddate__gte=2017-01-01,evictions__executeddate__lte=2018-01-01,evictions__count__gte=10'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_foreclosure_rules_authorized(self):
        council = self.council_factory(id=1)
        # has lihtc ending 2018
        property1 = self.property_factory(bbl=1, council=council)
        # has j-51 ending 2018
        property2 = self.property_factory(bbl=2, council=council)
        # has lihtc ending 2025
        property3 = self.property_factory(bbl=3, council=council)

        self.lispenden_factory(property=property1, fileddate='2017-01-01',
                               type=ds.LisPenden.LISPENDEN_TYPES['foreclosure'])
        self.lispenden_factory(property=property2, fileddate='2018-01-01')
        self.lispenden_factory(property=property3, fileddate='2016-01-01',
                               type=ds.LisPenden.LISPENDEN_TYPES['foreclosure'])

        # any properties with >= 1 foreclosures since ending 2017
        query = '/properties/?q=*condition_0=AND+filter_0=lispendens__count__gte=1,lispendens__fileddate__gte=2017-01-01,lispendens__type=foreclosure'
        token = self.get_access_token()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_foreclosure_rules_unauthorized(self):
        council = self.council_factory(id=1)
        # has lihtc ending 2018
        property1 = self.property_factory(bbl=1, council=council)
        # has j-51 ending 2018
        property2 = self.property_factory(bbl=2, council=council)
        # has lihtc ending 2025
        property3 = self.property_factory(bbl=3, council=council)

        self.lispenden_factory(property=property1, fileddate='2017-01-01',
                               type=ds.LisPenden.LISPENDEN_TYPES['foreclosure'])
        self.lispenden_factory(property=property2, fileddate='2018-01-01')
        self.lispenden_factory(property=property3, fileddate='2016-01-01',
                               type=ds.LisPenden.LISPENDEN_TYPES['foreclosure'])

        # any properties with >= 1 foreclosures since ending 2017
        query = '/properties/?q=*condition_0=AND+filter_0=lispendens__count__gte=1,lispendens__fileddate__gte=2017-01-01,lispenden__type=foreclosure'
        response = self.client.get(query, format="json")

        self.assertEqual(response.status_code, 401)

    def test_taxlien_rules(self):
        # has tax lien
        property1 = self.property_factory(bbl=1)
        # does not have tax lien
        property2 = self.property_factory(bbl=2)

        self.taxlien_factory(property=property1)

        # 10 permits between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=taxliens__count__gte=1'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_conh_rules(self):
        # has tax lien
        property1 = self.property_factory(bbl=1)
        # does not have tax lien
        property2 = self.property_factory(bbl=2)

        self.conhrecord_factory(property=property1)

        # 10 permits between 2017-2018
        query = '/properties/?q=*condition_0=AND+filter_0=conhrecords__count__gte=1'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]['bbl'], '1')

    def test_council_with_housingtype_with_q_1(self):
        council = self.council_factory(id=1)
        council2 = self.council_factory(id=2)
        # full match
        property1 = self.property_factory(bbl=1, council=council, unitsres=4)
        # full match
        property2 = self.property_factory(bbl=2, council=council, unitsres=4)
        # correct council, correct housing type, not filter match
        property3 = self.property_factory(bbl=3, council=council, unitsres=4)
        # correct council, wrong housing type, filter match
        property4 = self.property_factory(bbl=4, council=council, unitsres=6)
        # wrong council, otherwise complete match
        property5 = self.property_factory(bbl=5, council=council2, unitsres=4)
        # wrong council, housing type only match
        property6 = self.property_factory(bbl=6, council=council2, unitsres=4)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2016-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property6, issuedate="2018-01-01")

        # properties in council 1 with small homes and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?format=json&council=1&housingtype=sh&unitsres__lte=4&q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        # json response
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_council_with_housingtype_with_q_2(self):
        council = self.council_factory(id=1)
        council2 = self.council_factory(id=2)
        # full match
        property1 = self.property_factory(bbl=1, council=council)
        self.coredata_factory(property=property1, programname="j-51")

        # full match
        property2 = self.property_factory(bbl=2, council=council)
        self.coredata_factory(property=property2, programname="j-51")

        # correct council, correct housing type, not filter match
        property3 = self.property_factory(bbl=3, council=council)
        self.coredata_factory(property=property3, programname="j-51")

        # correct council, wrong housing type, filter match
        property4 = self.property_factory(bbl=4, council=council)
        self.coredata_factory(property=property4, programname="421a")

        # wrong council, otherwise complete match
        property5 = self.property_factory(bbl=5, council=council2)
        self.coredata_factory(property=property5, programname="j-51")

        # wrong council, housing type only match
        property6 = self.property_factory(bbl=6, council=council2)
        self.coredata_factory(property=property6, programname="j-51")

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2016-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property6, issuedate="2018-01-01")

        # properties in council 1 with rent regulated j-51 and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?council=1&housingtype=rr&subsidyprograms__programname=j-51&q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_council_with_housingtype_with_q_3(self):
        council = self.council_factory(id=1)
        council2 = self.council_factory(id=2)
        # full match
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2017=1)
        # council match, no housing type match
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2017=10)
        # council match, housing type match, no record match
        property3 = self.property_factory(
            bbl=3, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property3, uc2007=10, uc2017=1)
        # council match, no housing type match
        property4 = self.property_factory(bbl=4, council=council)

        # no council match, housing type match, record match
        property5 = self.property_factory(
            bbl=5, council=council2, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property5, uc2007=10, uc2017=1)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")

        # properties in council 1 with rent regulated j-51 and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?council=1&housingtype=rs&rsunitslost__gte=0.5&rsunitslost__start=2007&q=*condition_0=AND+filter_0=hpdviolations__count__gte=5,hpdviolations__approveddate__gte=2018-01-01'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)

    def test_council_with_housingtype_with_q_4(self):
        council = self.council_factory(id=1)
        council2 = self.council_factory(id=2)

        # full match
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property1, uc2007=10, uc2017=1)
        # council match, no housing type match
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property2, uc2007=10, uc2017=10)
        # council match, housing type match, no record match
        property3 = self.property_factory(
            bbl=3, council=council, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property3, uc2007=10, uc2017=1)
        # council match, no housing type match
        property4 = self.property_factory(bbl=4, council=council)

        # no council match, housing type match, record match
        property5 = self.property_factory(
            bbl=5, council=council2, yearbuilt=1950)
        self.rentstabilizationrecord_factory(
            property=property5, uc2007=10, uc2017=1)

        # sold for $10 in date range
        acrismaster1 = self.acrismaster_factory(
            documentid="a", doctype="DEED", docamount=10, docdate="2018-01-01")
        self.acrisreallegal_factory(property=property1, master=acrismaster1)

        # sold for $1 in date range
        acrismaster2 = self.acrismaster_factory(
            documentid="b", doctype="DEED", docamount=1, docdate="2018-01-01")
        self.acrisreallegal_factory(property=property2, master=acrismaster2)

        # sold for $10 out of date range
        acrismaster3 = self.acrismaster_factory(
            documentid="c", doctype="DEED", docamount=10, docdate="2011-01-01")
        self.acrisreallegal_factory(property=property3, master=acrismaster3)

        # tax document for $10 in date range
        acrismaster4 = self.acrismaster_factory(
            documentid="d", doctype="RPTT", docamount=10, docdate="2017-01-01")
        self.acrisreallegal_factory(property=property4, master=acrismaster4)

        # sold for $10 in date range
        acrismaster5 = self.acrismaster_factory(
            documentid="e", doctype="DEED", docamount=10, docdate="2018-01-01")
        self.acrisreallegal_factory(property=property5, master=acrismaster5)

        # properties in council 1 lost 50% rs units and sold for at least $5 betwen 2017-2018
        query = '/properties/?council=1&housingtype=rs&rsunitslost__gte=0.5&rsunitslost__start=2007&q=*condition_0=AND+filter_0=acrisreallegals__documentid__docdate__gte=2017-01-01,acrisreallegals__documentid__docdate__lte=2018-01-01,acrisreallegals__documentid__docamount__gte=5'

        response = self.client.get(query, format="json")

        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)

    def test_council_with_housingtype_with_q_5(self):
        council = self.council_factory(id=1)
        council2 = self.council_factory(id=2)
        # full match
        property1 = self.property_factory(
            bbl=1, council=council, yearbuilt=1950)
        self.coredata_factory(
            property=property1, enddate="2018-01-01", programname="421a Affordable")
        # council match, no housing type match, record match
        property2 = self.property_factory(
            bbl=2, council=council, yearbuilt=1950)
        # council match, no housing type match on program, record match
        property3 = self.property_factory(
            bbl=3, council=council, yearbuilt=1950)
        self.coredata_factory(property=property3,
                              enddate="2018-01-01", programname="LIHCT")
        # council match, housing type match, no record match
        property4 = self.property_factory(
            bbl=4, council=council, yearbuilt=1950)
        self.coredata_factory(
            property=property4, enddate="2018-01-01", programname="421a Affordable")

        # no council match, housing type match, record match
        property5 = self.property_factory(
            bbl=5, council=council2, yearbuilt=1950)
        self.coredata_factory(
            property=property5, enddate="2018-01-01", programname="421a Affordable")

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")

        # properties in council 1 with rent regulated j-51 and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?council=1&housingtype=rr&subsidyprograms__programname__any=421a+Affordable&q=*condition_0=AND+filter_0=hpdviolations__count__gte=5,hpdviolations__approveddate__gte=2018-01-01'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 1)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)

    def test_zipcode_with_housingtype_with_q_1(self):
        zipcode = self.zipcode_factory(id=1)
        zipcode2 = self.zipcode_factory(id=2)
        # full match
        property1 = self.property_factory(bbl=1, zipcode=zipcode, unitsres=4)
        # full match
        property2 = self.property_factory(bbl=2, zipcode=zipcode, unitsres=4)
        # correct zipcode, correct housing type, not filter match
        property3 = self.property_factory(bbl=3, zipcode=zipcode, unitsres=4)
        # correct zipcode, wrong housing type, filter match
        property4 = self.property_factory(bbl=4, zipcode=zipcode, unitsres=6)
        # wrong zipcode, otherwise complete match
        property5 = self.property_factory(bbl=5, zipcode=zipcode2, unitsres=4)
        # wrong zipcode, housing type only match
        property6 = self.property_factory(bbl=6, zipcode=zipcode2, unitsres=4)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2016-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property6, issuedate="2018-01-01")

        # properties in zipcode 1 with small homes and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?format=json&zipcode=1&housingtype=sh&unitsres__lte=4&q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        # json response
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_stateassembly_with_housingtype_with_q_1(self):
        stateassembly = self.state_assembly_factory(id=1)
        stateassembly2 = self.state_assembly_factory(id=2)
        # full match
        property1 = self.property_factory(
            bbl=1, stateassembly=stateassembly, unitsres=4)
        # full match
        property2 = self.property_factory(
            bbl=2, stateassembly=stateassembly, unitsres=4)
        # correct stateassembly, correct housing type, not filter match
        property3 = self.property_factory(
            bbl=3, stateassembly=stateassembly, unitsres=4)
        # correct stateassembly, wrong housing type, filter match
        property4 = self.property_factory(
            bbl=4, stateassembly=stateassembly, unitsres=6)
        # wrong stateassembly, otherwise complete match
        property5 = self.property_factory(
            bbl=5, stateassembly=stateassembly2, unitsres=4)
        # wrong stateassembly, housing type only match
        property6 = self.property_factory(
            bbl=6, stateassembly=stateassembly2, unitsres=4)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2016-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property6, issuedate="2018-01-01")

        # properties in stateassembly 1 with small homes and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?format=json&stateassembly=1&housingtype=sh&unitsres__lte=4&q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        # json response
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_statesenate_with_housingtype_with_q_1(self):
        statesenate = self.state_senate_factory(id=1)
        statesenate2 = self.state_senate_factory(id=2)
        # full match
        property1 = self.property_factory(
            bbl=1, statesenate=statesenate, unitsres=4)
        # full match
        property2 = self.property_factory(
            bbl=2, statesenate=statesenate, unitsres=4)
        # correct statesenate, correct housing type, not filter match
        property3 = self.property_factory(
            bbl=3, statesenate=statesenate, unitsres=4)
        # correct statesenate, wrong housing type, filter match
        property4 = self.property_factory(
            bbl=4, statesenate=statesenate, unitsres=6)
        # wrong statesenate, otherwise complete match
        property5 = self.property_factory(
            bbl=5, statesenate=statesenate2, unitsres=4)
        # wrong statesenate, housing type only match
        property6 = self.property_factory(
            bbl=6, statesenate=statesenate2, unitsres=4)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property1, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2018-01-01")
            self.ecbviolation_factory(
                property=property2, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property3, issuedate="2016-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property4, issuedate="2018-01-01")
            self.hpdviolation_factory(
                property=property5, approveddate="2018-01-01")
            self.dobviolation_factory(
                property=property5, issuedate="2018-01-01")
            self.ecbviolation_factory(
                property=property6, issuedate="2018-01-01")

        # properties in statesenate 1 with small homes and with 5 HPD violations b/t 2018- 2019 AND (5 DOB violations b/t 2018-2019 OR 5 ECB violations b/t 2018-2019)
        query = '/properties/?format=json&statesenate=1&housingtype=sh&unitsres__lte=4&q=*condition_0=AND+filter_0=condition_1+filter_0=hpdviolations__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5+*condition_1=OR+filter_1=dobviolations__issuedate__gte=2018-01-01,dobviolations__issuedate__lte=2019-01-01,dobviolations__count__gte=5+filter_1=ecbviolations__issuedate__gte=2018-01-01,ecbviolations__issuedate__lte=2019-01-01,ecbviolations__count__gte=5'

        response = self.client.get(query, format="json")
        # json response
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)

    def test_validations_1(self):
        # Unknown / misspelled datasets
        query = '/properties/?q=*condition_0=AND+filter_0=fakedataset__approveddate__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5'
        response = self.client.get(query, format="json")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            '"fakedataset" is not a valid dataset.' in response.data['detail'], True)

    def test_validations_2(self):
        # incorrect conditions types
        query = '/properties/?q=*condition_0=BOR+filter_0='
        response = self.client.get(query, format="json")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            '"BOR" is not a valid condition type.' in response.data['detail'], True)

    def test_validations_3(self):
        # no filters on the condition
        query = '/properties/?q=*condition_0=AND+fir_0='
        response = self.client.get(query, format="json")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            'Condition 0 has no filters' in response.data['detail'], True)

    def test_validations_4(self):
        # invalid field on the dataset filter
        query = '/properties/?q=*condition_0=AND+filter_0=hpdviolations__badfield__gte=2018-01-01,hpdviolations__approveddate__lte=2019-01-01,hpdviolations__count__gte=5'
        response = self.client.get(query, format="json")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(
            'Field "badfield" is not valid for dataset "HPDViolation"' in response.data['detail'], True)

    def test_duplicate_dataset_1_OR(self):
        # 5 HPD Violations in range 1
        property1 = self.property_factory(bbl=1)
        # 5 HPD violations in range 2
        property2 = self.property_factory(bbl=2)

        # 1 HPD violation in range 1
        property3 = self.property_factory(bbl=3)

        # 5 HPD Violations not in range
        property4 = self.property_factory(bbl=4)

        for i in range(5):
            self.hpdviolation_factory(
                property=property1, approveddate="2018-01-01")
            self.hpdviolation_factory(
                property=property2, approveddate="2008-01-01")
            self.hpdviolation_factory(
                property=property4, approveddate="2015-01-01")

        for i in range(1):
            self.hpdviolation_factory(
                property=property3, approveddate="2018-01-01")

        # 5 HPD Violations after 2018 OR 5 HPD Violations before 2010
        query = '/properties/?q=*condition_0=OR+filter_0=hpdviolations__count__gte=5,hpdviolations__approveddate__gte=2018-01-01+filter_1=hpdviolations__count__gte=5,hpdviolations__approveddate__lte=2010-01-01'

        response = self.client.get(query, format="json")
        content = response.data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(content), 2)
        self.assertEqual(any(d['bbl'] == '1' for d in content), True)
        self.assertEqual(any(d['bbl'] == '2' for d in content), True)
