from statistics import fmean, stdev, variance
from django.contrib.auth.models import User
from django.utils import timezone
from djongo import models


# Create your models here.

class Measure(models.Model):
    name  = models.CharField(max_length=100)
    value = models.FloatField()
    class Meta:
        abstract = True


class RawData(models.Model):
    #   Module Related
    module_num  = models.CharField(max_length=100)
    module_type = models.CharField(max_length=100)
    asset       = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=100)
    #   Data
    temperature = models.FloatField()
    voltage     = models.FloatField()
    description = models.CharField(max_length=100, blank=True)
    measures    = models.ArrayField(model_container=Measure)
    timestamp   = models.DateTimeField(default=timezone.now)


class DataBatch(models.Model):
    module_num          = models.CharField(max_length=100)
    module_type         = models.CharField(max_length=100)
    starting_timestamp  = models.DateTimeField(editable=False)
    ending_timestamp    = models.DateTimeField(editable=False)
    window_size         = models.PositiveIntegerField()
    #normalized          = models.BooleanField(editable=False)
    #normalization       = models.CharField(max_length=100)
    batch_mean          = models.FloatField(editable=False)
    batch_std           = models.FloatField(editable=False)
    #batch_rms           = models.FloatField(editable=False)
    #batch_kurtosis      = models.FloatField(editable=False)
    #batch_skewness      = models.FloatField(editable=False)
    #rolling_mean_params = models.JSONField()
    #frequency_params    = models.JSONField()
    #frequency_features  = models.JSONField(editable=False)
    #time_freq_params    = models.JSONField()
    #time_freq_features  = models.JSONField(editable=False)
    raw_data_begin      = models.ForeignKey(to=RawData, on_delete=models.CASCADE, related_name='+')
    raw_data_end        = models.ForeignKey(to=RawData, on_delete=models.CASCADE, related_name='+') 

    def save(self, *args, **kwargs):
        #setting fields with editable=False
        raw_datas = RawData.objects.filter(id__range=(self.raw_data_begin.id, self.raw_data_end.id))

        times  = [rd.timestamp for rd in raw_datas]
        values = []
        for raw_data in raw_datas:                 #<<<<< só funciona se raw_data.measures.name forem todos iguais
            for measure in raw_data.measures:
                values.append(measure['value'])

        self.starting_timestamp = min(times)
        self.ending_timestamp   = max(times)
        #TODO normalization
        self.batch_mean = fmean(values)
        self.batch_std = stdev(values)
        #TODO other batch analysis
        #TODO rolling mean
        #TODO freq and time_freq analysis
        return super().save(*args, **kwargs)