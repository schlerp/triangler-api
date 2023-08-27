from datetime import datetime
from typing import Literal, Optional
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI, Schema

from experiments.models import SAMPLE_NAMES, Experiment

api = NinjaAPI(title="Triangler")

class ExperimentIn(Schema):
    name: str
    description: Optional[str]
    date_started: datetime
    date_ended: Optional[datetime]
    correct_sample: Literal["A", "B", "C"]

class ExperimentOut(ExperimentIn):
    id: int
    

@api.get("/experiments")
def get_all(request) -> Experiment:
    return Experiment.objects.all()

@api.get("/experiments/{experiment_id}")
def add(request, experiment_id: int) -> Experiment:
    return get_object_or_404(Experiment, id)

@api.post("/experiments/{experiment_id}")
def add(request, experiment_id: int) -> Experiment:
    return get_object_or_404(Experiment, id)
