from django.db import models
from django.utils import timezone

from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen, with_bbl
from datasets.utils.validation_filters import is_null
import logging
import datetime
logger = logging.getLogger('app')


# Update process: Manual
# Update strategy: Overwrite
#
# Combine all borough files downloaded from DOF into single CSV file
# https://www1.nyc.gov/site/finance/benefits/benefits-j51.page
# upload file through admin, then update

class SubsidyJ51(BaseDatasetModel, models.Model):
    bbl = models.ForeignKey('Property', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=False)
    borough = models.SmallIntegerField(blank=True, null=True)
    neighborhood = models.TextField(blank=True, null=True)
    buildingclasscategory = models.TextField(blank=True, null=True)
    taxclassatpresent = models.TextField(blank=True, null=True)
    block = models.IntegerField(blank=True, null=True)
    lot = models.IntegerField(blank=True, null=True)
    buildingclassatpresent = models.TextField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    zipcode = models.TextField(blank=True, null=True)
    residentialunits = models.SmallIntegerField(blank=True, null=True)
    commercialunits = models.SmallIntegerField(blank=True, null=True)
    totalunits = models.SmallIntegerField(blank=True, null=True)
    landsquarefeet = models.IntegerField(blank=True, null=True)
    grosssquarefeet = models.IntegerField(blank=True, null=True)
    yearbuilt = models.SmallIntegerField(db_index=True, blank=True, null=True)

    @classmethod
    def pre_validation_filters(self, gen_rows):
        return gen_rows

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(with_bbl(from_csv_file_to_gen(file_path, update)))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        return self.bulk_seed(**kwargs, overwrite=True)

    def __str__(self):
        return str(self.id)