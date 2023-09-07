from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404
from ninja import ModelSchema
from ninja import NinjaAPI
from ninja import Schema

from experiments.models import Experiment
from experiments.models import Observation
from experiments.models import ObservationResponse
from experiments.models import ObservationToken
from experiments.models import get_experience_level_description
from experiments.models import get_experience_level_id

api = NinjaAPI(title="Triangler")


# common schemas
class JustId(Schema):
    id: int


class Success(Schema):
    success: bool


# experiment schemas
class ExperimentIn(ModelSchema):
    class Config:
        model = Experiment
        model_fields = [
            "name",
            "description",
            "date_started",
            "date_ended",
        ]


class ExperimentOut(ModelSchema):
    sample_size: int
    p_value: float

    class Config:
        model = Experiment
        model_fields = [
            "id",
            "name",
            "description",
            "date_started",
            "date_ended",
        ]


@api.get("/experiments", tags=["Experiments"], response=list[ExperimentOut])
def get_all_experiments(request: HttpRequest) -> list[ExperimentOut]:
    """Gets all experiments defined in this application."""
    return [
        ExperimentOut(
            id=x.id,
            name=x.name,
            description=x.description,
            date_started=x.date_started,
            date_ended=x.date_ended,
            sample_size=x.sample_size,
            p_value=x.p_value,
        )
        for x in Experiment.objects.all()
    ]


@api.get("/experiments/{experiment_id}", tags=["Experiments"], response=ExperimentOut)
def get_experiment_by_id(request: HttpRequest, experiment_id: int) -> ExperimentOut:
    """Get a specific experiemnt by its experiment ID."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return ExperimentOut(
        id=experiment.id,
        name=experiment.name,
        description=experiment.description,
        date_started=experiment.date_started,
        date_ended=experiment.date_ended,
        sample_size=experiment.sample_size,
        p_value=experiment.p_value,
    )


@api.post("/experiments", tags=["Experiments"], response=JustId)
def create_experiment(request: HttpRequest, payload: ExperimentIn) -> JustId:
    """Creates a new experiment with the supplied payload, returns the experiment id."""
    experiment = Experiment.objects.create(**payload.dict())
    return JustId(id=experiment.id)


@api.put("/experiments/{experiment_id}", tags=["Experiments"], response=Success)
def update_experiment(
    request: HttpRequest, experiment_id: int, payload: ExperimentIn
) -> Success:
    """Updates the experiment with `experiment id`, using supplied payload"""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    for attr, value in payload.dict().items():
        setattr(experiment, attr, value)
    experiment.save()
    return Success(success=True)


@api.delete("/experiments/{experiment_id}", tags=["Experiments"], response=Success)
def delete_experiment(request: HttpRequest, experiment_id: int) -> Success:
    """Deletes the experiment with a matching id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    experiment.delete()
    return Success(success=True)


# Observations
class ObservationIn(ModelSchema):
    class Config:
        model = Observation
        model_fields = [
            "correct_sample",
        ]


class ObservationOut(ModelSchema):
    token: str

    class Config:
        model = Observation
        model_fields = [
            "id",
            "created_at",
            "correct_sample",
        ]


@api.get(
    "/experiments/{experiment_id}/observations",
    tags=["Observations"],
    response=list[ObservationOut],
)
def get_all_observations(
    request: HttpRequest, experiment_id: int
) -> list[ObservationOut]:
    """Gets all observations defined for provided experiment id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return [
        ObservationOut(
            id=x.id,
            created_at=x.created_at,
            correct_sample=x.correct_sample,
            experiment=x.experiment,
            token=x.observation_token.token,
        )
        for x in experiment.observations.all()
    ]


@api.get(
    "/experiments/{experiment_id}/observations/{observation_id}",
    tags=["Observations"],
    response=ObservationOut,
)
def get_observation_by_id(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> ObservationOut:
    """Get a specific observation by its experiment id and observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(experiment.observations, id=observation_id)
    return ObservationOut(
        id=observation.id,
        created_at=observation.created_at,
        correct_sample=observation.correct_sample,
        experiment=observation.experiment,
        token=observation.observation_token.token,
    )


@api.post(
    "/experiments/{experiment_id}/observations",
    tags=["Observations"],
    response=ObservationOut,
)
def create_observation(
    request: HttpRequest, experiment_id: int, payload: ObservationIn
) -> ObservationOut:
    """Creates a new observation with the supplied payload, returns the observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = experiment.observations.create(**payload.dict())
    observation_token = ObservationToken.create_token_for_observation(observation.id)
    return ObservationOut(
        id=observation.id,
        created_at=observation.created_at,
        correct_sample=observation.correct_sample,
        experiment=observation.experiment,
        token=observation_token.token,
    )


@api.put(
    "/experiments/{experiment_id}/observations/{observation_id}",
    tags=["Observations"],
    response=Success,
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
    "/experiments/{experiment_id}/observations/{observation_id}",
    tags=["Observations"],
    response=Success,
)
def delete_observation(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> Success:
    """Deletes the observation on provided experiment with a matching id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(experiment.observations, id=observation_id)
    observation.delete()
    return Success(success=True)


# Observation Responses
class ObservationResponseIn(ModelSchema):
    experience_level: str
    token: str

    class Config:
        model = ObservationResponse
        model_fields = [
            "chosen_sample",
        ]


class ObservationResponseOut(ModelSchema):
    is_correct: bool
    experience_level: str
    observation_id: int

    class Config:
        model = ObservationResponse
        model_fields = [
            "id",
            "chosen_sample",
            "response_date",
        ]


@api.get(
    "/experiments/{experiment_id}/responses",
    tags=["Observation Responses"],
    response=list[ObservationResponseOut],
)
def get_all_observation_responses(
    request: HttpRequest, experiment_id: int
) -> list[ObservationResponseOut]:
    """Gets all observations defined for provided experiment id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    return [
        ObservationResponseOut(
            id=x.id,
            experience_level=get_experience_level_description(x.experience_level),
            chosen_sample=x.chosen_sample,
            response_date=x.response_date,
            observation_id=x.observation.id,
            is_correct=x.is_correct,
        )
        for x in experiment.observation_responses.all()
    ]


@api.get(
    "/experiments/{experiment_id}/responses/{observation_id}",
    tags=["Observation Responses"],
    response=ObservationResponseOut,
)
def get_observation_response_by_id(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> ObservationResponseOut:
    """Get a specific observation by its experiment id and observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation_response = get_object_or_404(
        experiment.observation_responses, observation__id=observation_id
    )
    return ObservationResponseOut(
        id=observation_response.id,
        experience_level=get_experience_level_description(
            observation_response.experience_level
        ),
        chosen_sample=observation_response.chosen_sample,
        response_date=observation_response.response_date,
        observation_id=observation_response.observation.id,
        is_correct=observation_response.is_correct,
    )


@api.post(
    "/experiments/{experiment_id}/responses",
    tags=["Observation Responses"],
    response=JustId,
)
def create_observation_response(
    request: HttpRequest, experiment_id: int, payload: ObservationResponseIn
) -> JustId:
    """Creates a new observation with the supplied payload, returns the observation id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)

    observation_token = get_object_or_404(ObservationToken, token=payload.token)

    observation_response_dict = {
        "chosen_sample": payload.chosen_sample,  # type: ignore
        "experience_level": get_experience_level_id(payload.experience_level),
    }
    observation_response_dict["experiment"] = experiment
    observation_response_dict["observation"] = observation_token.observation

    observation_response = experiment.observation_responses.create(
        **observation_response_dict
    )
    return JustId(id=observation_response.id)


@api.put(
    "/experiments/{experiment_id}/responses/{observation_id}",
    tags=["Observation Responses"],
    response=Success,
)
def update_observation_response(
    request: HttpRequest,
    experiment_id: int,
    observation_id: int,
    payload: ObservationResponseIn,
) -> Success:
    """Updates the observation on experiment, using supplied payload"""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(
        experiment.observation_responses, observation__id=observation_id
    )
    for attr, value in payload.dict().items():
        if attr == "experience_level":
            value = get_experience_level_id(value)
        setattr(observation, attr, value)
    observation.save()
    return Success(success=True)


@api.delete(
    "/experiments/{experiment_id}/responses/{observation_id}",
    tags=["Observation Responses"],
    response=Success,
)
def delete_observation_response(
    request: HttpRequest, experiment_id: int, observation_id: int
) -> Success:
    """Deletes the observation on provided experiment with a matching id."""
    experiment = get_object_or_404(Experiment, id=experiment_id)
    observation = get_object_or_404(
        experiment.observations, observation__id=observation_id
    )
    observation.delete()
    return Success(success=True)
