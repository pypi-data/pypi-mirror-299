from asyncio import create_task, as_completed
from typing import List, Coroutine, Type

from pydantic import BaseModel

from gravybox.exceptions import DataUnavailable
from gravybox.protocol import Condition, UpstreamCallParadigms


def merge_dicts_and_trim_nones(first: dict, second: dict):
    trimmed_first = {}
    for key, value in first.items():
        if isinstance(value, str):
            if len(value) > 0:
                trimmed_first[key] = value
        elif value is not None:
            trimmed_first[key] = value
    trimmed_second = {}
    for key, value in second.items():
        if isinstance(value, str):
            if len(value) > 0:
                trimmed_second[key] = value
        elif value is not None:
            trimmed_second[key] = value
    result = trimmed_first | trimmed_second
    return result


def all_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is None:
            return False
    return True


def no_fields_populated(instance: BaseModel):
    for key, value in instance.model_dump().items():
        if value is not None:
            return False
    return True


def all_upstream_calls_were_data_unavailable(failure_conditions, upstream_call_count):
    if len(failure_conditions) != upstream_call_count:
        return False
    for condition in failure_conditions:
        if condition != Condition.data_unavailable:
            return False
    return True


class UpstreamCentrifuge:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.tasks = [create_task(upstream_call) for upstream_call in upstream_calls]
        self.result_model = result_model

    async def activate(self):
        final_result = self.result_model()
        failure_conditions = []
        for upstream_call_wrapper in as_completed(self.tasks):
            upstream_result = await upstream_call_wrapper
            if isinstance(upstream_result, Condition):
                failure_conditions.append(upstream_result)
            else:
                final_result_dict = merge_dicts_and_trim_nones(final_result.model_dump(), upstream_result.model_dump())
                final_result = self.result_model.model_validate(final_result_dict)
                if all_fields_populated(final_result):
                    break
        for task in self.tasks:
            if not task.done():
                task.cancel()
        if all_upstream_calls_were_data_unavailable(failure_conditions, len(self.tasks)):
            raise DataUnavailable()
        else:
            return final_result


class UpstreamSequencer:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.upstream_calls = upstream_calls
        self.result_model = result_model

    async def activate(self):
        final_result = self.result_model()
        failure_conditions = []
        for upstream_call_wrapper in self.upstream_calls:
            upstream_result = await upstream_call_wrapper
            if isinstance(upstream_result, Condition):
                failure_conditions.append(upstream_result)
            else:
                final_result_dict = merge_dicts_and_trim_nones(final_result.model_dump(), upstream_result.model_dump())
                final_result = self.result_model.model_validate(final_result_dict)
                if all_fields_populated(final_result):
                    break
        if all_upstream_calls_were_data_unavailable(failure_conditions, len(self.upstream_calls)):
            raise DataUnavailable()
        else:
            return final_result


class UpstreamShortCircuit:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel]):
        self.upstream_calls = upstream_calls
        self.result_model = result_model

    async def activate(self):
        failure_conditions = []
        for upstream_call_wrapper in self.upstream_calls:
            upstream_result = await upstream_call_wrapper
            if isinstance(upstream_result, Condition):
                failure_conditions.append(upstream_result)
            else:
                return upstream_result
        if all_upstream_calls_were_data_unavailable(failure_conditions, len(self.upstream_calls)):
            raise DataUnavailable()
        else:
            return self.result_model()


class UpstreamCaller:
    def __init__(self, upstream_calls: List[Coroutine], result_model: Type[BaseModel], paradigm: UpstreamCallParadigms):
        if paradigm == UpstreamCallParadigms.sequential:
            self.upstream_caller = UpstreamSequencer(upstream_calls, result_model)
        elif paradigm == UpstreamCallParadigms.simultaneous:
            self.upstream_caller = UpstreamCentrifuge(upstream_calls, result_model)
        elif paradigm == UpstreamCallParadigms.short_circuit:
            self.upstream_caller = UpstreamShortCircuit(upstream_calls, result_model)
        else:
            raise ValueError("invalid upstream call paradigm")

    async def activate(self):
        return await self.upstream_caller.activate()
