import random
from datetime import datetime

from django.test import TestCase

from experiments.models import EXPERIENCE_LEVELS
from experiments.models import SAMPLE_NAMES
from experiments.models import Experiment
from experiments.models import Observation

N_SAMPLES = 60
N_CORRECT = 20
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
            choice = random.choice(["B", "C"])
            if i < N_CORRECT:
                choice = "A"
            Observation.objects.create(
                experiment=self.experiment,
                experience_level=random.choice(EXPERIENCE_LEVELS)[0],
                chosen_sample=choice,
            )

    def test_calculate_p_value(self) -> None:
        """ensure that the calculated P-value is the expected value"""
        p_value = self.experiment.calculate_p_value
        self.assertGreaterEqual(p_value, 0.05)
