from typing import TYPE_CHECKING
from typing import Optional
from typing import Self

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta
from scipy import stats

from experiments.utils import calculate_expiry_date
from experiments.utils import generate_unique_token

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


def get_experience_level_description(level_id: int) -> str:
    for x in EXPERIENCE_LEVELS:
        if x[0] == level_id:
            return x[1]
    return "Unknown"


def get_experience_level_id(level_description: str) -> int:
    for x in EXPERIENCE_LEVELS:
        if x[1] == level_description:
            return x[0]
    return 0


class Observation(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    correct_sample = models.CharField(max_length=1, choices=SAMPLE_NAMES)
    experiment = models.ForeignKey(
        "Experiment",
        on_delete=models.CASCADE,
        related_name="observations",
    )  # type: ignore

    if TYPE_CHECKING:
        experiment: "Experiment"
        response: "ObservationResponse"
        observation_token: "ObservationToken"

    class Meta(TypedModelMeta):
        pass


class ObservationResponse(models.Model):
    id = models.AutoField(primary_key=True)
    experiment = models.ForeignKey(
        "Experiment",
        on_delete=models.CASCADE,
        related_name="observation_responses",
    )
    experience_level = models.IntegerField(choices=EXPERIENCE_LEVELS)
    chosen_sample = models.CharField(max_length=1, choices=SAMPLE_NAMES)
    response_date = models.DateTimeField(auto_now_add=True)
    observation = models.OneToOneField(
        "Observation",
        on_delete=models.CASCADE,
        related_name="response",
    )

    class Meta(TypedModelMeta):
        pass

    @property
    def is_correct(self) -> Optional[bool]:
        if self.observation.correct_sample == self.chosen_sample:
            return True
        return False


class ObservationToken(models.Model):
    id = models.AutoField(primary_key=True)
    token = models.CharField(max_length=32)
    expiry_date = models.DateTimeField()
    observation = models.OneToOneField(
        "Observation", on_delete=models.CASCADE, related_name="observation_token"
    )

    @classmethod
    def create_token_for_observation(cls, observation_id: int) -> Self:
        observation = Observation.objects.get(id=observation_id)
        token = generate_unique_token()
        expiry_date = calculate_expiry_date()
        return cls.objects.create(
            token=token,
            expiry_date=expiry_date,
            observation=observation,
        )

    @classmethod
    def get_observation_for_token(cls, token: str) -> Observation:
        return cls.objects.get(token=token).observation

    def refresh_token(self) -> Self:
        self.expiry_date = calculate_expiry_date()
        self.save()
        return self


class Experiment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    date_started = models.DateField()
    date_ended = models.DateField()

    if TYPE_CHECKING:
        observations = RelatedManager["Observation"]()
        observation_responses = RelatedManager["ObservationResponse"]()

    class Meta(TypedModelMeta):
        pass

    def __str__(self):
        return f"{self.name} ({self.date_started}, # samples: {self.sample_size})"

    @property
    def sample_size(self) -> int:
        return self.observations.count()

    @property
    def p_value(self) -> float:
        n_samples = float(self.sample_size)
        if n_samples < 1:
            return 1.0
        # expected 1/3 of the time to be correct
        expected_correct = n_samples / 3
        # expected 2/3 of the time to be incorrect
        expected_incorrect = expected_correct * 2

        # number of correct observations
        observed_correct = len(
            [1 for x in self.observation_responses.all() if x.is_correct]
        )
        observed_incorrect = n_samples - observed_correct

        correct_x2 = (abs(observed_correct - expected_correct) ** 2) / expected_correct
        incorrect_x2 = (
            abs(observed_incorrect - expected_incorrect) ** 2
        ) / expected_incorrect

        x2 = correct_x2 + incorrect_x2

        return float(1 - stats.chi2.cdf(x2, 1))
