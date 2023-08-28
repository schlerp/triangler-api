import random
from datetime import datetime

from django.test import TestCase

from experiments.models import EXPERIENCE_LEVELS
from experiments.models import SAMPLE_NAMES
from experiments.models import Experiment
from experiments.models import Observation

N_SAMPLES = 60
CORRECT_ANSWER = SAMPLE_NAMES[0][0]


class ExperimentTestCase(TestCase):
    def setUp(self) -> None:
        self.experiment: Experiment = Experiment.objects.create(
            name="Test Experiment",
            description="A test experiement to test experiments.",
            date_started=datetime.now().date(),
            date_ended=datetime.now().date(),
            correct_sample=CORRECT_ANSWER,
        )

        # create the observations
        for i in range(N_SAMPLES):
            choice = random.choice(["A", "B", "C"])
            Observation.objects.create(
                experiment=self.experiment,
                experience_level=random.choice(EXPERIENCE_LEVELS)[0],
                chosen_sample=choice,
            )

    def test_sample_size(self) -> None:
        self.assertEqual(self.experiment.sample_size, N_SAMPLES)
