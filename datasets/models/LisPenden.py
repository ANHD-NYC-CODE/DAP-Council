from django.db import models
from datasets.utils.BaseDatasetModel import BaseDatasetModel
from core.utils.transform import from_csv_file_to_gen, with_bbl
from datasets.utils.validation_filters import is_null
from datasets.utils import dates
from django.db.models import Count, OuterRef, Q, Subquery
from django.db.models.functions import Coalesce
from datetime import datetime, timezone
from django.utils.timezone import make_aware

import logging
from datasets import models as ds
from django.db.models import Q

logger = logging.getLogger('app')

# Instructions:
# 1) merge all boroughs into single file - lp_lispendens_<month><year>.csv - use these headers: KEY,BBL,ENTEREDDATE,ZIP,BC,FILEDDATE,INDEX,DEBTOR,CR,ATTORNEY,Third Party,SAT DATE,SAT TYPE,DISP 2) upload file to app 3) update


class LisPenden(BaseDatasetModel, models.Model):
    QUERY_DATE_KEY = 'fileddate'
    RECENT_DATE_PINNED = True
    REQUIRES_AUTHENTICATION = True

    class Meta:
        indexes = [
            models.Index(fields=['bbl', '-fileddate']),
            models.Index(fields=['-fileddate']),
        ]

    key = models.TextField(primary_key=True, blank=False, null=False)
    bbl = models.ForeignKey('Property', db_column='bbl', db_constraint=False,
                            on_delete=models.SET_NULL, null=True, blank=False)
    entereddate = models.DateField(db_index=True, blank=True, null=True)
    zip = models.IntegerField(blank=True, null=True)
    bc = models.TextField(blank=True, null=True)
    fileddate = models.DateField(db_index=True, blank=True, null=True)
    index = models.TextField(blank=True, null=True)
    debtor = models.TextField(blank=True, null=True)
    cr = models.TextField(blank=True, null=True)
    attorney = models.TextField(blank=True, null=True)
    thirdparty = models.TextField(blank=True, null=True)
    satdate = models.DateField(db_index=True, blank=True, null=True)
    sattype = models.TextField(blank=True, null=True)
    disp = models.TextField(blank=True, null=True)
    type = models.TextField(blank=True, null=True)
    source = models.TextField(blank=True, null=True)

    LISPENDEN_TYPES = {
        'foreclosure': 'foreclosure'
    }

    slim_query_fields = ["key", "bbl", "fileddate"]

    @classmethod
    def pre_validation_filters(self, gen_rows):
        for row in gen_rows:
            if is_null(row['key']):
                continue
            yield row

    def has_bank_creditor(self):
        if not self.cr:
            return False
        creditor_list = ('MORTGAGE', 'AMRO', 'BANC', 'BANK', 'CAPITAL', 'CHASE MAN',
                         'CREDIT',
                         'EQUITIES',
                         'FARGO',
                         'FEDERAL SB',
                         'FINAN',
                         'FSB',
                         'FUNDING',
                         'HOLDING',
                         'INVEST',
                         'LEND',
                         'LOAN',
                         'MORGAN CHASE',
                         'M & T CORP',
                         'S & L',
                         'SAVING',
                         'TRUST',)  # from coredata script

        return any(x in self.cr.upper() for x in creditor_list)

    @classmethod
    def mark_foreclosure_with_creditor(self):
        for lispenden in self.objects.filter(~Q(type=self.LISPENDEN_TYPES['foreclosure'])):
            if lispenden.has_bank_creditor():

                lispenden.type = self.LISPENDEN_TYPES['foreclosure']
                lispenden.save()

    # trims down new update files to preserve memory
    # uses original header values
    @classmethod
    def update_set_filter(self, csv_reader, headers):
        return csv_reader

    @classmethod
    def transform_self(self, file_path, update=None):
        return self.pre_validation_filters(from_csv_file_to_gen(file_path, update))

    @classmethod
    def seed_or_update_self(self, **kwargs):
        logger.info("Seeding/Updating {}", self.__name__)
        self.seed_with_upsert(**kwargs)
        logger.debug('marking foreclosures by creditor for {}', self.__name__)
        self.mark_foreclosure_with_creditor()
        # TODO: Create a Foreclosure record for all lispendens marked with foreeclosures

        # TODO: move this into a Dataset public class method
        dataset = self.get_dataset()
        dataset.api_last_updated = datetime.today()
        dataset.save()

    def __str__(self):
        return str(self.key)
