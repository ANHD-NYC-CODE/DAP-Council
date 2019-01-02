from django.contrib import admin
from django.conf import settings
from django.db.models import Count
from django.http import HttpResponseRedirect
from core.models import Dataset, DataFile, Update
from app.admin.mixins import admin_changelist_link, admin_link
from core.tasks import async_download_file


class DatasetAdmin(admin.ModelAdmin):
    def response_change(self, request, obj):
        if "_download-file" in request.POST:
            worker = async_download_file.delay(obj.id)
            self.message_user(
                request, "This file is now downloading with worker {}. Please view monitor the status in Flower. {}".format(worker.id, settings.FLOWER_URL))
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)

    @admin_changelist_link('datafile_set', ('DataFiles'), query_string=lambda c: 'dataset={}'.format(c.pk))
    def datafiles_link(self, updates):
        return ('View DateFiles')

    @admin_changelist_link('update_set', ('Updates'), query_string=lambda c: 'dataset={}'.format(c.pk))
    def updates_link(self, updates):
        return ('View Updates')

    def data_files_count(self, inst):
        return inst.datafile_set.count()

    def updates_count(self, inst):
        return inst.update_set.count()

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['name', 'model_name', 'download_endpoint',
                    'updates_count', 'updates_link', 'data_files_count', 'datafiles_link']
    Dataset.objects.prefetch_related('update')
    Dataset.objects.prefetch_related('datafile')
    ordering = ['name']
    actions = []


class DataFileAdmin(admin.ModelAdmin):
    @admin_link('dataset', ('Dataset'), query_string=lambda c: 'id={}'.format(c.dataset.pk))
    def dataset_link(self, dataset):
        return dataset

    def has_delete_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    list_display = ['id', 'dataset_link', 'uploaded_date', 'file']
    ordering = ['-uploaded_date']
    actions = []


class UpdateAdmin(admin.ModelAdmin):
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    @admin_link('dataset', ('Dataset'), query_string=lambda c: 'id={}'.format(c.dataset.pk))
    def dataset_link(self, dataset):
        return dataset

    @admin_link('file', ('File'), query_string=lambda c: 'id={}'.format(c.file.pk))
    def file_link(self, datafile):
        return datafile.file.name

    @admin_link('task_result', ('Task Result'))
    def task_result_link(self, task_result):
        return task_result.status

    list_display = ['id', 'dataset_link', 'model_name', 'file_link',
                    'rows_updated', 'rows_created', 'created_date', 'completed_date',  'task_id', 'task_result_link']

    list_select_related = (
        'task_result',
    )

    ordering = ['-created_date']
    actions = []


admin.site.register(Dataset, DatasetAdmin)
admin.site.register(DataFile, DataFileAdmin)
admin.site.register(Update, UpdateAdmin)
