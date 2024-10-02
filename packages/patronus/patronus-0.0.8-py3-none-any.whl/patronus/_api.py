import datetime
import logging
import typing

import pydantic

from ._base_api import BaseAPIClient, UnrecoverableAPIError, APIError, RPMLimitError

log = logging.getLogger(__name__)


class Account(pydantic.BaseModel):
    id: str
    name: str


class WhoAmIAPIKey(pydantic.BaseModel):
    id: str
    account: Account


class WhoAmICaller(pydantic.BaseModel):
    api_key: WhoAmIAPIKey


class WhoAmIResponse(pydantic.BaseModel):
    caller: WhoAmICaller


class Evaluator(pydantic.BaseModel):
    id: str
    name: str
    evaluator_family: str | None
    aliases: list[str] | None


class ListEvaluatorsResponse(pydantic.BaseModel):
    evaluators: list[Evaluator]


class Project(pydantic.BaseModel):
    id: str
    name: str


class CreateProjectRequest(pydantic.BaseModel):
    name: str


class Experiment(pydantic.BaseModel):
    project_id: str
    id: str
    name: str


class CreateExperimentRequest(pydantic.BaseModel):
    project_id: str
    name: str


class CreateExperimentResponse(pydantic.BaseModel):
    experiment: Experiment


class EvaluateEvaluator(pydantic.BaseModel):
    evaluator: str
    profile_name: str | None = None
    explain_strategy: str = "always"


class EvaluateRequest(pydantic.BaseModel):
    # Currently we support calls with only one evaluator.
    # One of the reasons is that we support "smart" retires on failures
    # And it wouldn't be possible
    evaluators: list[EvaluateEvaluator] = pydantic.Field(min_length=1, max_length=1)
    evaluated_model_system_prompt: str | None = None
    evaluated_model_retrieved_context: list[str] | None = None
    evaluated_model_input: str | None = None
    evaluated_model_output: str | None = None
    evaluated_model_gold_answer: str | None = None
    experiment_id: str
    capture: str = "all"
    dataset_id: str | None = None
    dataset_sample_id: int | None = None
    tags: dict[str, str] | None = None


class EvaluationResultAdditionalInfo(pydantic.BaseModel):
    positions: list | None
    extra: dict | None
    confidence_interval: dict | None


class EvaluationResult(pydantic.BaseModel):
    id: str
    project_id: str
    experiment_id: str
    created_at: pydantic.AwareDatetime
    evaluator_id: str
    evaluated_model_system_prompt: str | None
    evaluated_model_retrieved_context: list[str] | None
    evaluated_model_input: str | None
    evaluated_model_output: str | None
    evaluated_model_gold_answer: str | None
    pass_: bool | None = pydantic.Field(alias="pass")
    score_raw: float | None
    additional_info: EvaluationResultAdditionalInfo
    explanation: str | None
    evaluation_duration: datetime.timedelta | None
    explanation_duration: datetime.timedelta | None
    evaluator_family: str
    evaluator_profile_public_id: str
    dataset_id: str | None
    dataset_sample_id: int | None
    tags: dict[str, str] | None


class EvaluateResult(pydantic.BaseModel):
    evaluator_id: str
    profile_name: str
    status: str
    error_message: str | None
    evaluation_result: EvaluationResult | None


class EvaluateResponse(pydantic.BaseModel):
    results: list[EvaluateResult]


class ExportEvaluationResult(pydantic.BaseModel):
    experiment_id: str
    evaluator_id: str
    profile_name: str | None = None
    evaluated_model_system_prompt: str | None = None
    evaluated_model_retrieved_context: list[str] | None = None
    evaluated_model_input: str | None = None
    evaluated_model_output: str | None = None
    evaluated_model_gold_answer: str | None = None
    pass_: bool | None = pydantic.Field(alias="pass_", serialization_alias="pass")
    score_raw: float | None
    evaluation_duration: datetime.timedelta | None = None
    evaluated_model_name: str | None = None
    evaluated_model_provider: str | None = None
    evaluated_model_params: dict[str, str | int | float] | None = None
    evaluated_model_selected_model: str | None = None
    dataset_id: str | None = None
    dataset_sample_id: int | None = None
    tags: dict[str, str] | None = None


class ExportEvaluationRequest(pydantic.BaseModel):
    evaluation_results: list[ExportEvaluationResult]


class ExportEvaluationResultPartial(pydantic.BaseModel):
    id: str
    app: str | None
    created_at: pydantic.AwareDatetime
    evaluator_id: str


class ExportEvaluationResponse(pydantic.BaseModel):
    evaluation_results: list[ExportEvaluationResultPartial]


class ListProfilesRequest(pydantic.BaseModel):
    public_id: str | None = None
    evaluator_family: str | None = None
    evaluator_id: str | None = None
    name: str | None = None
    revision: str | None = None
    get_last_revision: bool = False
    is_patronus_managed: bool | None = None
    limit: int = 1000
    offset: int = 0


class EvaluatorProfile(pydantic.BaseModel):
    public_id: str
    evaluator_family: str
    name: str
    revision: int
    config: dict[str, typing.Any] | None
    is_patronus_managed: bool
    created_at: datetime.datetime
    description: str | None


class CreateProfileRequest(pydantic.BaseModel):
    evaluator_family: str
    name: str
    config: dict[str, typing.Any]


class CreateProfileResponse(pydantic.BaseModel):
    evaluator_profile: EvaluatorProfile


class AddEvaluatorProfileRevisionRequest(pydantic.BaseModel):
    config: dict[str, typing.Any]


class AddEvaluatorProfileRevisionResponse(pydantic.BaseModel):
    evaluator_profile: EvaluatorProfile


class ListProfilesResponse(pydantic.BaseModel):
    evaluator_profiles: list[EvaluatorProfile]


class DatasetDatum(pydantic.BaseModel):
    dataset_id: str
    sid: int
    evaluated_model_system_prompt: str | None = None
    evaluated_model_retrieved_context: list[str] | None = None
    evaluated_model_input: str | None = None
    evaluated_model_output: str | None = None
    evaluated_model_gold_answer: str | None = None
    meta_evaluated_model_name: str | None = None
    meta_evaluated_model_provider: str | None = None
    meta_evaluated_model_selected_model: str | None = None
    meta_evaluated_model_params: dict[str, str | int | float] | None = None


class ListDatasetData(pydantic.BaseModel):
    data: list[DatasetDatum]


class API(BaseAPIClient):
    async def whoami(self) -> WhoAmIResponse:
        resp = await self.call("GET", "/v1/whoami", response_cls=WhoAmIResponse)
        resp.raise_for_status()
        return resp.data

    async def create_project(self, request: CreateProjectRequest) -> Project:
        resp = await self.call("POST", "/v1/projects", body=request, response_cls=Project)
        resp.raise_for_status()
        return resp.data

    async def create_experiment(self, request: CreateExperimentRequest) -> Experiment:
        resp = await self.call("POST", "/v1/experiments", body=request, response_cls=CreateExperimentResponse)
        resp.raise_for_status()
        return resp.data.experiment

    async def evaluate(self, request: EvaluateRequest) -> EvaluateResponse:
        resp = await self.call("POST", "/v1/evaluate", body=request, response_cls=EvaluateResponse)

        # We set defaults in case ratelimits headers were not returned. It may happen in case of an error response,
        # or in rare cases like proxy stripping response headers.
        # The defaults are selected to proceed and fallback to standard retry mechanism.
        rpm_limit = try_int(resp.response.headers.get("x-ratelimit-rpm-limit-requests"), -1)
        rpm_remaining = try_int(resp.response.headers.get("x-ratelimit-rpm-remaining-requests"), 1)
        monthly_limit = try_int(resp.response.headers.get("x-ratelimit-monthly-limit-requests"), -1)
        monthly_remaining = try_int(resp.response.headers.get("x-ratelimit-monthly-remaining-requests"), 1)

        if resp.response.is_error:
            if resp.response.status_code == 429 and monthly_remaining <= 0:
                raise UnrecoverableAPIError(
                    f"Monthly evaluation {monthly_limit!r} limit hit",
                    response=resp.response,
                )
            if resp.response.status_code == 429 and rpm_remaining <= 0:
                wait_for_s = None
                try:
                    val: str = resp.response.headers.get("date")
                    response_date = datetime.datetime.strptime(val, "%a, %d %b %Y %H:%M:%S %Z")
                    wait_for_s = 60 - response_date.second
                except Exception as err:  # noqa
                    log.debug(
                        "Failed to extract RPM period from the response; "
                        f"'date' header value {resp.response.headers.get('date')!r}: "
                        f"{err}"
                    )
                    pass
                raise RPMLimitError(
                    limit=rpm_limit,
                    wait_for_s=wait_for_s,
                    response=resp.response,
                )
            # Generally, we assume that any 4xx error (excluding 429) is a user error
            # And repeated calls won't be successful.
            # 429 is an exception, but it should be handled above,
            # and if it's not then it should be handled as recoverable error.
            # It may not be handled above in rare cases - e.g. header is stripped by a proxy.
            if resp.response.status_code != 429 and resp.response.status_code < 500:
                raise UnrecoverableAPIError(
                    f"Response with unexpected status code: {resp.response.status_code}",
                    response=resp.response,
                )
            raise APIError(
                f"Response with unexpected status code: {resp.response.status_code}",
                response=resp.response,
            )

        for res in resp.data.results:
            if res.status == "validation_error":
                raise UnrecoverableAPIError("", response=resp.response)
            if res.status != "success":
                raise APIError(f"evaluation failed with status {res.status!r} and message {res.error_message!r}'")

        return resp.data

    async def export_evaluations(self, request: ExportEvaluationRequest) -> ExportEvaluationResponse:
        resp = await self.call(
            "POST",
            "/v1/evaluation-results/batch",
            body=request,
            response_cls=ExportEvaluationResponse,
        )
        resp.raise_for_status()
        return resp.data

    async def list_evaluators(self) -> list[Evaluator]:
        resp = await self.call("GET", "/v1/evaluators", response_cls=ListEvaluatorsResponse)
        resp.raise_for_status()
        return resp.data.evaluators

    async def create_profile(self, request: CreateProfileRequest) -> CreateProfileResponse:
        resp = await self.call("POST", "/v1/evaluator-profiles", body=request, response_cls=CreateProfileResponse)
        resp.raise_for_status()
        return resp.data

    async def add_evaluator_profile_revision(
        self, evaluator_profile_id, request: AddEvaluatorProfileRevisionRequest
    ) -> AddEvaluatorProfileRevisionResponse:
        resp = await self.call(
            "POST",
            f"/v1/evaluator-profiles/{evaluator_profile_id}/revision",
            body=request,
            response_cls=AddEvaluatorProfileRevisionResponse,
        )
        resp.raise_for_status()
        return resp.data

    async def list_profiles(self, request: ListProfilesRequest) -> ListProfilesResponse:
        params = request.model_dump(exclude_none=True)
        resp = await self.call(
            "GET",
            "/v1/evaluator-profiles",
            params=params,
            response_cls=ListProfilesResponse,
        )
        resp.raise_for_status()
        return resp.data

    async def list_dataset_data(self, dataset_id: str) -> ListDatasetData:
        resp = await self.call("GET", f"/v1/datasets/{dataset_id}/data", response_cls=ListDatasetData)
        resp.raise_for_status()
        return resp.data


def try_int(v, default: int) -> int:
    if not v:
        return default
    try:
        return int(v)
    except ValueError:
        return default
