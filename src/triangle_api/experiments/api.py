from datetime import datetime
from typing import Literal
from typing import Optional

from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from ninja import Schema

from experiments.models import Experiment

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


@api.get("/experiments", tags=["Experiments"])
def get_all_experiments(request: HttpRequest) -> list[ExperimentOut]:
    """Gets all experiments defined in this application."""
    return Experiment.objects.all()  # type: ignore


@api.get("/experiments/{experiment_id}", tags=["Experiments"])
def get_experiment_by_id(request: HttpRequest, experiment_id: int) -> ExperimentOut:
    """Get a specific experiemnt by its experiment ID."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return experiment  # type: ignore


@api.post("/experiments", tags=["Experiments"])
def create_experiment(request: HttpRequest, payload: ExperimentIn) -> JustId:
    """Creates a new experiment with the supplied payload, returns the experiment id."""
    experiment = Experiment.objects.create(**payload.dict())
    return JustId(id=experiment.id)


@api.put("/experiments/{experiment_id}", tags=["Experiments"])
def update_experiment(
    request: HttpRequest, experiment_id: int, payload: ExperimentIn
) -> Success:
    """Updates the experiment with `experiment id`, using supplied payload"""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    for attr, value in payload.dict().items():
        setattr(experiment, attr, value)
    experiment.save()
    return Success(success=True)


@api.delete("/experiments/{experiment_id}", tags=["Experiments"])
def delete_experiment(request: HttpRequest, experiment_id: int) -> Success:
    """Deletes the experiment with a matching id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    experiment.delete()
    return Success(success=True)


# Observations
class ObservationIn(Schema):
    experience_level: int
    chosen_sample: Literal["A", "B", "C"]
    observation_date: datetime


class ObservationOut(ObservationIn):
    id: int
    experiment: int


@api.get("/experiments/{experiment_id}/observations", tags=["Observations"])
def get_all_observations(
    request: HttpRequest, experiment_id: int
) -> list[ObservationOut]:
    """Gets all observations defined for provided experiment id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return experiment.observations.all()  # type: ignore


@api.get(
    "/experiments/{experiment_id}/observations/{observation_id}", tags=["Observations"]
)
def get_observation_by_id(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> ObservationOut:
    """Get a specific observation by its experiment id and observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(experiment.observations, id=observation_id)
    return observation  # type: ignore


@api.post("/experiments/{experiment_id}/observation", tags=["Observations"])
def create_observation(
    request: HttpRequest, experiment_id: int, payload: ObservationIn
) -> JustId:
    """Creates a new observation with the supplied payload, returns the observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = experiment.observations.create(**payload.dict())
    return JustId(id=observation.id)


@api.put(
    "/experiments/{experiment_id}/observation/{observation_id}", tags=["Observations"]
)
def update_observation(
    request: HttpRequest,
    experiment_id: int,
    observation_id: int,
    payload: ObservationIn,
) -> Success:
    """Updates the observation on experiment, using supplied payload"""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(experiment.observations, id=observation_id)
    for attr, value in payload.dict().items():
        setattr(observation, attr, value)
    observation.save()
    return Success(success=True)


@api.delete(
    "/experiments/{experiment_id}/observation/{observation_id}", tags=["Observations"]
)
def delete_observation(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> Success:
    """Deletes the observation on provided experiment with a matching id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(experiment.observations, id=observation_id)
    observation.delete()
    return Success(success=True)
