from django.db import models
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen, with_bbl
from datasets.utils.validation_filters import is_null
from django.conf import settings
from django.dispatch import receiver
from datasets import models as ds
from django.db.models import Count, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from core.tasks import async_download_and_update

import os
import csv
import logging
from datetime import datetime, timezone
from django.utils.timezone import make_aware

from datasets.utils import dates
logger = logging.getLogger('app')


class AcrisRealLegal(BaseDatasetModel, models.Model):
    API_ID = '8h5j-fqxa'
    download_endpoint = 'https://data.cityofnewyork.us/api/views/8h5j-fqxa/rows.csv?accessType=DOWNLOAD'
    QUERY_DATE_KEY = 'documentid__docdate'  # date is on the acrisrealmaster record

    class Meta:
        indexes = [
            models.Index(fields=['bbl', 'documentid']),
            models.Index(fields=['documentid', 'bbl']),

        ]

    key = models.TextField(primary_key=True, blank=False, null=False)
    documentid = models.ForeignKey('AcrisRealMaster', db_column='documentid', db_constraint=False,
                                   on_delete=models.SET_NULL, null=True, blank=True)
    bbl = models.ForeignKey('Property', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=True)
    recordtype = models.TextField(blank=True, null=True)
    borough = models.SmallIntegerField(blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    lot = models.IntegerField(blank=True, null=True)
    easement = models.BooleanField(blank=True, null=True)
    partiallot = models.TextField(blank=True, null=True)
    airrights = models.BooleanField(blank=True, null=True)
    subterraneanrights = models.BooleanField(blank=True, null=True)
    propertytype = models.TextField(blank=True, null=True)
    streetnumber = models.TextField(blank=True, null=True)
    streetname = models.TextField(blank=True, null=True)
    unit = models.TextField(blank=True, null=True)
    goodthroughdate = models.DateField(blank=True, null=True)

    slim_query_fields = ["bbl", "documentid"]

    @classmethod
    def create_async_update_worker(self, endpoint=None, file_name=None):
        async_download_and_update.delay(
            self.get_dataset().id, endpoint=endpoint, file_name=file_name)

    @classmethod
    def download(self, endpoint=None, file_name=None):
        return self.download_file(self.download_endpoint, file_name=file_name)

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['documentid']):
                continue

            # add primary key
            row['key'] = "{}-{}".format(row['documentid'], row['bbl'])
            yield row

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(with_bbl(from_csv_file_to_gen(file_path, update), allow_blank=True))

    @classmethod
    def split_seed_or_update_self(self, **kwargs):
        logger.info("Seeding/Updating {}", self.__name__)
        return self.seed_with_single(delete_file=True, **kwargs)

    @classmethod
    def seed_or_update_self(self, **kwargs):
        logger.info("Seeding/Updating {}", self.__name__)
        if settings.TESTING:
            self.seed_with_single(**kwargs)
        else:
            self.async_concurrent_seed(**kwargs)

    @classmethod
    def annotate_properties(self):
        count = 0
        records = []
        logger.debug('annotating properties for: {}'.format(self.__name__))

        last30 = dates.get_last_month_since_api_update(
            self.get_dataset(), string=False)
        lastyear = dates.get_last_year(string=False)
        last3years = dates.get_last3years(string=False)

        last30_subquery = Subquery(self.objects.filter(bbl=OuterRef('bbl'), documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES,
                                                       documentid__docdate__gte=last30).values('bbl').annotate(count=Count('bbl')).values('count'))

        lastyear_subquery = Subquery(self.objects.filter(bbl=OuterRef(
            'bbl'), documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, documentid__docdate__gte=lastyear).values('bbl').annotate(count=Count('bbl')).values('count'))

        last3years_subquery = Subquery(self.objects
                                       .filter(bbl=OuterRef('bbl'), documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, documentid__docdate__gte=last3years).values('bbl')
                                       .annotate(count=Count('bbl'))
                                       .values('count')
                                       )
        latestprice = Subquery(self.objects.filter(bbl=OuterRef('bbl'), documentid__docdate__isnull=False, documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES).order_by(
            '-documentid__docdate').values('documentid__docamount')[:1])
        latestsaledate = Subquery(self.objects.filter(bbl=OuterRef('bbl'), documentid__docdate__isnull=False,
                                                      documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES).order_by(
            '-documentid__docdate').values('documentid__docdate')[:1])

        ds.PropertyAnnotation.objects.update(acrisrealmasters_last30=Coalesce(last30_subquery, 0), acrisrealmasters_lastyear=Coalesce(lastyear_subquery, 0),
                                             acrisrealmasters_last3years=Coalesce(last3years_subquery, 0), latestsaleprice=latestprice, latestsaledate=latestsaledate, acrisrealmasters_lastupdated=make_aware(datetime.now()))

    def __str__(self):
        return self.key


@receiver(models.signals.post_save, sender=AcrisRealLegal)
def annotate_property_on_save(sender, instance, created, **kwargs):
    if created == True:
        try:

            last30 = dates.get_last_month_since_api_update(
                ds.AcrisRealLegal.get_dataset(), string=False)
            lastyear = dates.get_last_year(string=False)
            last3years = dates.get_last3years(string=False)

            annotation = instance.bbl.propertyannotation
            annotation.acrisrealmasters_last30 = Coalesce(annotation.bbl.acrisreallegal_set.filter(
                documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, documentid__docdate__gte=last30).count(), 0)

            annotation.acrisrealmasters_lastyear = Coalesce(annotation.bbl.acrisreallegal_set.filter(
                documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, documentid__docdate__gte=lastyear).count(), 0)

            annotation.acrisrealmasters_last3years = Coalesce(annotation.bbl.acrisreallegal_set.filter(
                documentid__doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, documentid__docdate__gte=last3years).count(), 0)

            annotation.latestsaleprice = ds.AcrisRealMaster.objects.filter(documentid__in=annotation.bbl.acrisreallegal_set.values(
                'documentid'), doctype__in=ds.AcrisRealMaster.SALE_DOC_TYPES, docdate__isnull=False).latest('docdate').docamount

            annotation.save()
        except Exception as e:
            print(e)
            return
