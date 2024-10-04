# Copyright 2023 Cognite AS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

from collections.abc import Hashable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import final

from cognite.client.data_classes import (
    Workflow,
    WorkflowList,
    WorkflowUpsert,
    WorkflowUpsertList,
    WorkflowVersion,
    WorkflowVersionId,
    WorkflowVersionList,
    WorkflowVersionUpsert,
    WorkflowVersionUpsertList,
)
from cognite.client.data_classes.capabilities import (
    Capability,
    WorkflowOrchestrationAcl,
)
from cognite.client.exceptions import CogniteNotFoundError
from cognite.client.utils.useful_types import SequenceNotStr
from rich import print

from cognite_toolkit._cdf_tk._parameters import ANY_INT, ANY_STR, ParameterSpec, ParameterSpecSet
from cognite_toolkit._cdf_tk.exceptions import (
    ToolkitRequiredValueError,
)
from cognite_toolkit._cdf_tk.loaders._base_loaders import ResourceLoader
from cognite_toolkit._cdf_tk.utils import (
    CDFToolConfig,
    load_yaml_inject_variables,
)

from .auth_loaders import GroupAllScopedLoader
from .function_loaders import FunctionLoader
from .transformation_loaders import TransformationLoader


@final
class WorkflowLoader(ResourceLoader[str, WorkflowUpsert, Workflow, WorkflowUpsertList, WorkflowList]):
    folder_name = "workflows"
    filename_pattern = r"^.*Workflow$"
    resource_cls = Workflow
    resource_write_cls = WorkflowUpsert
    list_cls = WorkflowList
    list_write_cls = WorkflowUpsertList
    kind = "Workflow"
    dependencies = frozenset(
        {
            GroupAllScopedLoader,
            TransformationLoader,
            FunctionLoader,
        }
    )
    _doc_base_url = "https://api-docs.cognite.com/20230101-beta/tag/"
    _doc_url = "Workflows/operation/CreateOrUpdateWorkflow"

    @classmethod
    def get_required_capability(cls, items: WorkflowUpsertList) -> Capability | list[Capability]:
        if not items:
            return []
        return WorkflowOrchestrationAcl(
            [WorkflowOrchestrationAcl.Action.Read, WorkflowOrchestrationAcl.Action.Write],
            WorkflowOrchestrationAcl.Scope.All(),
        )

    @classmethod
    def get_id(cls, item: Workflow | WorkflowUpsert | dict) -> str:
        if isinstance(item, dict):
            return item["externalId"]
        if item.external_id is None:
            raise ToolkitRequiredValueError("Workflow must have external_id set.")
        return item.external_id

    def load_resource(self, filepath: Path, ToolGlobals: CDFToolConfig, skip_validation: bool) -> WorkflowUpsertList:
        resource = load_yaml_inject_variables(filepath, {})

        workflows = [resource] if isinstance(resource, dict) else resource
        return WorkflowUpsertList.load(workflows)

    def retrieve(self, ids: SequenceNotStr[str]) -> WorkflowList:
        workflows = []
        for ext_id in ids:
            workflow = self.client.workflows.retrieve(external_id=ext_id)
            if workflow:
                workflows.append(workflow)
        return WorkflowList(workflows)

    def _upsert(self, items: WorkflowUpsert | WorkflowUpsertList) -> WorkflowList:
        upserts = [items] if isinstance(items, WorkflowUpsert) else items
        return WorkflowList([self.client.workflows.upsert(upsert) for upsert in upserts])

    def create(self, items: WorkflowUpsert | WorkflowUpsertList) -> WorkflowList:
        return self._upsert(items)

    def update(self, items: WorkflowUpsertList) -> WorkflowList:
        return self._upsert(items)

    def delete(self, ids: SequenceNotStr[str]) -> int:
        successes = 0
        for id_ in ids:
            try:
                self.client.workflows.delete(external_id=id_)
            except CogniteNotFoundError:
                print(f"  [bold yellow]WARNING:[/] Workflow {id_} does not exist, skipping delete.")
            else:
                successes += 1
        return successes

    def iterate(self) -> Iterable[Workflow]:
        return self.client.workflows.list(limit=-1)


@final
class WorkflowVersionLoader(
    ResourceLoader[
        WorkflowVersionId, WorkflowVersionUpsert, WorkflowVersion, WorkflowVersionUpsertList, WorkflowVersionList
    ]
):
    folder_name = "workflows"
    filename_pattern = r"^.*WorkflowVersion$"
    resource_cls = WorkflowVersion
    resource_write_cls = WorkflowVersionUpsert
    list_cls = WorkflowVersionList
    list_write_cls = WorkflowVersionUpsertList
    kind = "WorkflowVersion"
    dependencies = frozenset({WorkflowLoader})

    _doc_base_url = "https://api-docs.cognite.com/20230101-beta/tag/"
    _doc_url = "Workflow-versions/operation/CreateOrUpdateWorkflowVersion"

    @property
    def display_name(self) -> str:
        return "workflow.versions"

    @classmethod
    def get_required_capability(cls, items: WorkflowVersionUpsertList) -> Capability | list[Capability]:
        if not items:
            return []
        return WorkflowOrchestrationAcl(
            [WorkflowOrchestrationAcl.Action.Read, WorkflowOrchestrationAcl.Action.Write],
            WorkflowOrchestrationAcl.Scope.All(),
        )

    @classmethod
    def get_id(cls, item: WorkflowVersion | WorkflowVersionUpsert | dict) -> WorkflowVersionId:
        if isinstance(item, dict):
            if missing := tuple(k for k in {"workflowExternalId", "version"} if k not in item):
                # We need to raise a KeyError with all missing keys to get the correct error message.
                raise KeyError(*missing)
            return WorkflowVersionId(item["workflowExternalId"], item["version"])
        return item.as_id()

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        if "workflowExternalId" in item:
            yield WorkflowLoader, item["workflowExternalId"]

    def load_resource(
        self, filepath: Path, ToolGlobals: CDFToolConfig, skip_validation: bool
    ) -> WorkflowVersionUpsertList:
        resource = load_yaml_inject_variables(filepath, {})

        workflowversions = [resource] if isinstance(resource, dict) else resource
        return WorkflowVersionUpsertList.load(workflowversions)

    def retrieve(self, ids: SequenceNotStr[WorkflowVersionId]) -> WorkflowVersionList:
        return self.client.workflows.versions.list(list(ids))

    def _upsert(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        return WorkflowVersionList([self.client.workflows.versions.upsert(item) for item in items])

    def create(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        upserted = []
        for item in items:
            upserted.append(self.client.workflows.versions.upsert(item))
        return WorkflowVersionList(upserted)

    def update(self, items: WorkflowVersionUpsertList) -> WorkflowVersionList:
        updated = []
        for item in items:
            updated.append(self.client.workflows.versions.upsert(item))
        return WorkflowVersionList(updated)

    def delete(self, ids: SequenceNotStr[WorkflowVersionId]) -> int:
        successes = 0
        for id in ids:
            try:
                self.client.workflows.versions.delete(id)
            except CogniteNotFoundError:
                print(f"  [bold yellow]WARNING:[/] WorkflowVersion {id} does not exist, skipping delete.")
            else:
                successes += 1
        return successes

    def iterate(self) -> Iterable[WorkflowVersion]:
        return self.client.workflows.versions.list(limit=-1)

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        # The Parameter class in the SDK class WorkflowVersion implementation is deviating from the API.
        # So we need to modify the spec to match the API.
        parameter_path = ("workflowDefinition", "tasks", ANY_INT, "parameters")
        length = len(parameter_path)
        for item in spec:
            if len(item.path) >= length + 1 and item.path[:length] == parameter_path[:length]:
                # Add extra ANY_STR layer
                # The spec class is immutable, so we use this trick to modify it.
                object.__setattr__(item, "path", item.path[:length] + (ANY_STR,) + item.path[length:])
        spec.add(ParameterSpec((*parameter_path, ANY_STR), frozenset({"dict"}), is_required=True, _is_nullable=False))
        # The depends on is implemented as a list of string in the SDK, but in the API spec it
        # is a list of objects with one 'externalId' field.
        spec.add(
            ParameterSpec(
                ("workflowDefinition", "tasks", ANY_INT, "dependsOn", ANY_INT, "externalId"),
                frozenset({"str"}),
                is_required=False,
                _is_nullable=False,
            )
        )
        spec.add(
            ParameterSpec(
                ("workflowDefinition", "tasks", ANY_INT, "type"),
                frozenset({"str"}),
                is_required=True,
                _is_nullable=False,
            )
        )
        return spec
