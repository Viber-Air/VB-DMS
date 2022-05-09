from statistics import fmean, stdev, variance
from django.contrib.auth.models import User
from django.utils import timezone
from djongo import models


# Create your models here.

class Module(models.Model):
    module_num  = models.CharField(max_length=100, unique=True, primary_key=True)
    module_type = models.CharField(max_length=100)
    asset       = models.CharField(max_length=100)
    sensor_type = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.module_num}'

class Measure(models.Model):
    name  = models.CharField(max_length=100)
    value = models.FloatField()
    class Meta:
        abstract = True


class RawData(models.Model):
    #module       = models.ForeignKey('Module', on_delete=models.CASCADE)
    temperature = models.FloatField()
    voltage     = models.FloatField()
    description = models.CharField(max_length=100, blank=True)
    measures    = models.ArrayField(model_container=Measure, blank=True)
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
    raw_data            = models.ArrayReferenceField(to=RawData)

    def save(self, *args, **kwargs):
        #setting fields with editable=False
        times = [measure['timestamp'] for measure in self.rawdata]
        values = [measure['value'] for measure in self.rawdata]

        self.starting_timestamp = min(times)
        self.ending_timestamp   = max(times)
        #TODO normalization
        self.batch_mean = fmean(values)
        self.batch_std = stdev(values)
        #TODO other batch analysis
        #TODO rolling mean
        #TODO freq and time_freq analysis
        return super().save(*args, **kwargs)