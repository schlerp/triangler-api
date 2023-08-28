from typing import TYPE_CHECKING

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta
from scipy import stats

if TYPE_CHECKING:
    from django.db.models.manager import RelatedManager

SAMPLE_NAMES = [
    ("A", "Sample A"),
    ("B", "Sample B"),
    ("C", "Sample C"),
]

EXPERIENCE_LEVELS = [
    (0, "Non Beer Drinker"),
    (1, "General Beer Drinker"),
    (2, "Craft Enthusiast"),
    (3, "Homebrewer"),
    (4, "BJCP (training)"),
    (5, "BJCP (Recognized or higher)"),
]


# Create your models here.
class Observation(models.Model):
    id = models.AutoField(primary_key=True)
    experiment = models.ForeignKey(
        "Experiment", on_delete=models.CASCADE, related_name="observations"
    )
    experience_level = models.IntegerField(choices=EXPERIENCE_LEVELS)
    chosen_sample = models.CharField(max_length=1, choices=SAMPLE_NAMES)
    observation_date = models.DateTimeField(auto_now_add=True)

    class Meta(TypedModelMeta):
        pass


class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    date_started = models.DateField()
    date_ended = models.DateField()
    correct_sample = models.CharField(max_length=1, choices=SAMPLE_NAMES)

    if TYPE_CHECKING:
        observations = RelatedManager["Observation"]()

    class Meta(TypedModelMeta):
        pass

    def __str__(self):
        return f"{self.name} ({self.date_started}, # samples: {self.sample_size})"

    @property
    def sample_size(self) -> int:
        return self.observations.count()

    @property
    def calculate_p_value(self) -> float:
        n_samples = float(self.sample_size)

        # expected 1/3 of the time to be correct
        expected_correct = n_samples / 3
        # expected 2/3 of the time to be incorrect
        expected_incorrect = expected_correct * 2

        # number of correct observations
        observed_correct = self.observations.filter(
            chosen_sample=self.correct_sample
        ).count()
        observed_incorrect = n_samples - observed_correct

        correct_x2 = (abs(observed_correct - expected_correct) ** 2) / expected_correct
        incorrect_x2 = (
            abs(observed_incorrect - expected_incorrect) ** 2
        ) / expected_incorrect

        x2 = correct_x2 + incorrect_x2

        return float(1 - stats.chi2.cdf(x2, 1))
