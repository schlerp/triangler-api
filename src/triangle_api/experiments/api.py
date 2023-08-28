from datetime import datetime
from typing import Literal
from typing import Optional

from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja import Schema

from experiments.models import Experiment
from experiments.models import Observation

api = NinjaAPI(title="Triangler")


# common schemas
class JustId(Schema):
    id: int


class Success(Schema):
    success: bool


# Experiemnts
class ExperimentIn(Schema):
    name: str
    description: Optional[str]
    date_started: datetime
    date_ended: Optional[datetime]
    correct_sample: Literal["A", "B", "C"]


class ExperimentOut(ExperimentIn):
    id: int


@api.get("/experiments")
def get_all_experiments(request: HttpRequest) -> list[ExperimentOut]:
    return Experiment.objects.all()  # type: ignore


@api.get("/experiments/{experiment_id}")
def get_experiment_by_id(request: HttpRequest, experiment_id: int) -> ExperimentOut:
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return experiment  # type: ignore


@api.post("/experiments")
def create_experiment(request: HttpRequest, payload: ExperimentIn) -> JustId:
    experiment = Experiment.objects.create(**payload.dict())
    return JustId(id=experiment.id)


@api.put("/experiments/{experiment_id}")
def update_experiment(
    request: HttpRequest, experiment_id: int, payload: ExperimentIn
) -> Success:
    experiment = get_object_or_404(Experiment, id=experiment_id)
    for attr, value in payload.dict().items():
        setattr(experiment, attr, value)
    experiment.save()
    return Success(success=True)


@api.delete("/experiments/{experiment_id}")
def delete_experiment(request: HttpRequest, experiment_id: int) -> Success:
    experiment = get_object_or_404(Experiment, id=experiment_id)
    experiment.delete()
    return Success(success=True)


# Observations
class ObservationIn(Schema):
    experiment: int
    experience_level: int
    chosen_sample: Literal["A", "B", "C"]
    observation_date: datetime


class ObservationOut(ObservationIn):
    id: int


@api.get("/observation")
def get_all_observations(request: HttpRequest) -> list[ObservationOut]:
    return Observation.objects.all()  # type: ignore


@api.get("/observation/{observation_id}")
def get_observation_by_id(request: HttpRequest, observation_id: int) -> ObservationOut:
    observation = get_object_or_404(Experiment, id=observation_id)
    return observation  # type: ignore


@api.post("/observation")
def create_observation(request: HttpRequest, payload: ExperimentIn) -> JustId:
    observation = Experiment.objects.create(**payload.dict())
    return JustId(id=observation.id)


@api.put("/observation/{observation_id}")
def update_observation(
    request: HttpRequest, observation_id: int, payload: ExperimentIn
) -> Success:
    observation = get_object_or_404(Experiment, id=observation_id)
    for attr, value in payload.dict().items():
        setattr(observation, attr, value)
    observation.save()
    return Success(success=True)


@api.delete("/observation/{observation_id}")
def delete_observation(request: HttpRequest, observation_id: int) -> Success:
    experiment = get_object_or_404(Experiment, id=observation_id)
    experiment.delete()
    return Success(success=True)
