from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model

from experiments.models import Experiment
from experiments.models import Observation


# Register your models here.
@admin.register(Experiment)
class ExperimentAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date_started",
        "date_ended",
        "n_observations",
        "p_value",
    )
    list_filter = ["date_started"]
    search_fields = ["name", "description"]

    def p_value(self, experiment: Experiment) -> str:
        return f"{experiment.p_value:.3f}"

    def n_observations(self, experiment: Experiment) -> str:
        return f"{experiment.sample_size}"

    def save_model(self, request, obj: Experiment, form, change):
        super().save_model(request, obj, form, change)
        if change:
            change_message = f"{obj.name} - {obj.date_started}"
            LogEntry.objects.create(
                user=request.user,
                content_type=get_content_type_for_model(obj),
                object_id=obj.id,
                action_flag=2,
                change_message=change_message,
                object_repr=obj.__str__()[:200],
            )


@admin.register(Observation)
class ObservationAdmin(admin.ModelAdmin):
    readonly_fields = ("experiment",)
