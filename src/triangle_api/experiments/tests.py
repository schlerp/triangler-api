from datetime import datetime
import random

from django.test import TestCase
from experiments.models import SAMPLE_NAMES, Experiment, Observation
from experiments.models import Experiment
from experiments.models import SAMPLE_NAMES
from experiments.models import EXPERIENCE_LEVELS


N_SAMPLES = 60
N_CORRECT = 28
CORRECT_ANSWER = SAMPLE_NAMES[0][0]

class ExperimentTestCase(TestCase):
    def setUp(self):
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

    def test_sample_size(self):
        self.assertEqual(self.experiment.sample_size, N_SAMPLES)

    def test_calculate_p_value(self):
        """ensure that the calculated P-value is the expected value"""
        p_value = self.experiment.calculate_p_value()
        self.assertLessEqual(p_value, 0.05)
