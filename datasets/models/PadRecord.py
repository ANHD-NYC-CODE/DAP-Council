from django.db import models, transaction
from django.db.models import Q
from core import models as c
from datasets import models as ds
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from datasets.utils.validation_filters import is_null, exceeds_char_length
from core.utils.transform import from_csv_file_to_gen, with_bbl
from django.contrib.postgres.search import SearchVector, SearchVectorField
from core.tasks import async_create_update
from core.utils.address import clean_number_and_streets
from django.conf import settings
import re
import logging

logger = logging.getLogger('app')

# Update process: Manual
# Update strategy: Upsert
#
# Download latest
# https://data.cityofnewyork.us/City-Government/Property-Address-Directory/bc8t-ecyu
# Extract ZIP and upload bobaadr.csv file through admin, then update using bobaadr AND settng dataset = PadRecord
# ** RESOURCE INTENSIVE UPDATE ** - don't run during regular updates after 7pm
# Make sure to run this update AFTER updating the Building table w/ the same file.


class PadRecord(BaseDatasetModel, models.Model):
    key = models.TextField(primary_key=True, blank=False, null=False)
    bin = models.ForeignKey('Building', on_delete=models.SET_NULL, null=True,
                            db_column='bin', db_constraint=False)
    bbl = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True,
                            db_column='bbl', db_constraint=False)
    boro = models.TextField(blank=False, null=False)
    block = models.TextField(blank=False, null=False)
    lot = models.TextField(blank=False, null=False)
    lhnd = models.TextField(blank=False, null=False)  # low house number
    lhns = models.TextField(blank=True, null=True)
    lcontpar = models.TextField(blank=True, null=True)
    lsos = models.TextField(blank=True, null=True)
    hhnd = models.TextField(blank=False, null=False)  # high house number
    hhns = models.TextField(blank=True, null=True)
    hcontpar = models.TextField(blank=True, null=True)
    hsos = models.TextField(blank=True, null=True)
    scboro = models.TextField(blank=True, null=True)
    sc5 = models.IntegerField(blank=True, null=True)
    sclgc = models.TextField(blank=True, null=True)
    stname = models.TextField(blank=True, null=True)
    addrtype = models.TextField(blank=True, null=True)
    realb7sc = models.TextField(blank=True, null=True)
    validlgcs = models.TextField(blank=True, null=True)
    dapsflag = models.TextField(blank=True, null=True)
    naubflag = models.TextField(blank=True, null=True)
    parity = models.TextField(blank=True, null=True)
    b10sc = models.BigIntegerField(blank=True, null=True)
    segid = models.IntegerField(blank=True, null=True)
    zipcode = models.IntegerField(blank=True, null=True)
    physicalid = models.IntegerField(blank=True, null=True)

    def get_house_number(self):
        if (self.lhnd == self.hhnd):
            return self.lhnd
        elif (self.lhnd and self.hhnd):
            return "{}-{}".format(self.lhnd, self.hhnd)
        else:
            return self.lhnd

    @classmethod
    def construct_house_number(self, low, high):
        if (low == high):
            return low
        elif (low and high):
            return "{}-{}".format(low, high)
        else:
            return low

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['bin']):
                continue
            if is_null(row['lot']):
                continue
            if is_null(row['block']):
                continue
            if is_null(row['hhnd']):
                continue
            if is_null(row['lhnd']):
                continue
            row['stname'] = clean_number_and_streets(
                row['stname'], False, clean_typos=False)
            row['key'] = re.sub(
                ' ', '', "{}{}-{}{}".format(row['bin'], row['lhnd'], row['hhnd'], row['stname']))
            yield row

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def annotate_buildings(self):
        logger.debug('Annotating Buildings with PAD addresses')
        with transaction.atomic():
            ds.Building.objects.update(pad_addresses='')
            count = 0
            for building in ds.Building.objects.all():
                pad_records = self.objects.filter(bin=building.bin)
                if len(pad_records):
                    pad_addresses = ','.join(["{}-{} {}".format(record.lhnd, record.hhnd, record.stname)
                                              for record in pad_records])

                    building.pad_addresses = pad_addresses
                    building.save()
                    count = count + 1
                    if count % (settings.BATCH_SIZE / 10) == 0:
                        logger.debug(
                            'Processed {} pad addresses'.format(count))
                else:
                    continue

    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(with_bbl(from_csv_file_to_gen(file_path, update), borough='boro'))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        logger.info("Seeding/Updating {}", self.__name__)
        self.bulk_seed(**kwargs, ignore_conflict=True, overwrite=True)
        self.annotate_buildings()  # add pad addresses to building model

    def __str__(self):
        return str(self.key)
