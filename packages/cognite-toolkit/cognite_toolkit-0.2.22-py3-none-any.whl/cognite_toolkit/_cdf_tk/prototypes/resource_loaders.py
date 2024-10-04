from __future__ import annotations

import io
from collections.abc import Hashable, Iterable
from functools import lru_cache
from pathlib import Path
from typing import Any, final

import pandas as pd
from cognite.client.data_classes import (
    Asset,
    AssetList,
    AssetWrite,
    AssetWriteList,
    ThreeDModel,
    ThreeDModelList,
    ThreeDModelUpdate,
    ThreeDModelWrite,
    ThreeDModelWriteList,
    capabilities,
)
from cognite.client.data_classes.capabilities import Capability
from cognite.client.exceptions import CogniteAPIError, CogniteNotFoundError
from cognite.client.utils.useful_types import SequenceNotStr

from cognite_toolkit._cdf_tk._parameters import ParameterSpec, ParameterSpecSet
from cognite_toolkit._cdf_tk.loaders._base_loaders import ResourceContainerLoader, ResourceLoader
from cognite_toolkit._cdf_tk.loaders._resource_loaders import DataSetsLoader, LabelLoader
from cognite_toolkit._cdf_tk.utils import CDFToolConfig, load_yaml_inject_variables


@final
class AssetLoader(ResourceLoader[str, AssetWrite, Asset, AssetWriteList, AssetList]):
    folder_name = "assets"
    filename_pattern = r"^.*\.Asset$"  # Matches all yaml files whose stem ends with '.Asset'.
    filetypes = frozenset({"yaml", "yml", "csv", "parquet"})
    resource_cls = Asset
    resource_write_cls = AssetWrite
    list_cls = AssetList
    list_write_cls = AssetWriteList
    kind = "Asset"
    dependencies = frozenset({DataSetsLoader, LabelLoader})
    _doc_url = "Assets/operation/createAssets"

    @classmethod
    def get_id(cls, item: Asset | AssetWrite | dict) -> str:
        if isinstance(item, dict):
            return item["externalId"]
        if not item.external_id:
            raise KeyError("Asset must have external_id")
        return item.external_id

    @classmethod
    def get_required_capability(cls, items: AssetWriteList) -> Capability | list[Capability]:
        if not items:
            return []
        data_set_ids = {item.data_set_id for item in items if item.data_set_id}
        scope = (
            capabilities.AssetsAcl.Scope.DataSet(list(data_set_ids))
            if data_set_ids
            else capabilities.AssetsAcl.Scope.All()
        )

        return capabilities.AssetsAcl(
            [capabilities.AssetsAcl.Action.Read, capabilities.AssetsAcl.Action.Write],
            scope,  # type: ignore[arg-type]
        )

    def create(self, items: AssetWriteList) -> AssetList:
        return self.client.assets.create(items)

    def retrieve(self, ids: SequenceNotStr[str]) -> AssetList:
        return self.client.assets.retrieve_multiple(external_ids=ids, ignore_unknown_ids=True)

    def update(self, items: AssetWriteList) -> AssetList:
        return self.client.assets.update(items)

    def delete(self, ids: SequenceNotStr[str]) -> int:
        try:
            self.client.assets.delete(external_id=ids)
        except (CogniteAPIError, CogniteNotFoundError) as e:
            non_existing = set(e.failed or [])
            if existing := [id_ for id_ in ids if id_ not in non_existing]:
                self.client.assets.delete(external_id=existing)
            return len(existing)
        else:
            return len(ids)

    def iterate(self) -> Iterable[Asset]:
        return iter(self.client.assets)

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        # Added by toolkit
        spec.add(ParameterSpec(("dataSetExternalId",), frozenset({"str"}), is_required=False, _is_nullable=False))

        # Should not be used, used for parentExternalId instead
        spec.discard(ParameterSpec(("parentId",), frozenset({"int"}), is_required=False, _is_nullable=False))
        return spec

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        """Returns all items that this item requires.

        For example, a TimeSeries requires a DataSet, so this method would return the
        DatasetLoader and identifier of that dataset.
        """
        if "dataSetExternalId" in item:
            yield DataSetsLoader, item["dataSetExternalId"]
        for label in item.get("labels", []):
            if isinstance(label, dict):
                yield LabelLoader, label["externalId"]
            elif isinstance(label, str):
                yield LabelLoader, label
        if "parentExternalId" in item:
            yield cls, item["parentExternalId"]

    def load_resource(self, filepath: Path, ToolGlobals: CDFToolConfig, skip_validation: bool) -> AssetWriteList:
        resources: list[dict[str, Any]]
        if filepath.suffix in {".yaml", ".yml"}:
            raw = load_yaml_inject_variables(filepath, ToolGlobals.environment_variables())
            resources = [raw] if isinstance(raw, list) else raw  # type: ignore[assignment, list-item]
        elif filepath.suffix == ".csv" or filepath.suffix == ".parquet":
            if filepath.suffix == ".csv":
                # The replacement is used to ensure that we read exactly the same file on Windows and Linux
                file_content = filepath.read_bytes().replace(b"\r\n", b"\n").decode("utf-8")
                data = pd.read_csv(io.StringIO(file_content))
            else:
                data = pd.read_parquet(filepath)
            data.replace(pd.NA, None, inplace=True)
            data.replace("", None, inplace=True)
            resources = data.to_dict(orient="records")
        else:
            raise ValueError(f"Unsupported file type: {filepath.suffix}")

        for resource in resources:
            # Unpack metadata keys from table formats (e.g. csv, parquet)
            metadata: dict = resource.get("metadata", {})
            for key, value in list(resource.items()):
                if key.startswith("metadata."):
                    if value not in {None, float("nan")} and str(value) not in {"", " ", "nan", "null", "none"}:
                        metadata[key.removeprefix("metadata.")] = str(value)
                    del resource[key]
            if metadata:
                resource["metadata"] = metadata
            if "labels" in resource and isinstance(resource["labels"], str):
                resource["labels"] = [
                    label.strip() for label in resource["labels"].removeprefix("[").removesuffix("]").split(",")
                ]

            if resource.get("dataSetExternalId") is not None:
                ds_external_id = resource.pop("dataSetExternalId")
                resource["dataSetId"] = ToolGlobals.verify_dataset(
                    ds_external_id, skip_validation, action="replace dataSetExternalId with dataSetId in assets"
                )
        return AssetWriteList.load(resources)

    def _are_equal(
        self, local: AssetWrite, cdf_resource: Asset, return_dumped: bool = False
    ) -> bool | tuple[bool, dict[str, Any], dict[str, Any]]:
        local_dumped = local.dump()
        cdf_dumped = cdf_resource.as_write().dump()
        # Dry run
        if local_dumped.get("dataSetId") == -1 and "dataSetId" in cdf_dumped:
            local_dumped["dataSetId"] = cdf_dumped["dataSetId"]
        if (
            all(s == -1 for s in local_dumped.get("securityCategories", []))
            and "securityCategories" in cdf_dumped
            and len(cdf_dumped["securityCategories"]) == len(local_dumped.get("securityCategories", []))
        ):
            local_dumped["securityCategories"] = cdf_dumped["securityCategories"]

        return self._return_are_equal(local_dumped, cdf_dumped, return_dumped)


@final
class ThreeDModelLoader(
    ResourceContainerLoader[str, ThreeDModelWrite, ThreeDModel, ThreeDModelWriteList, ThreeDModelList]
):
    folder_name = "3dmodels"
    filename_pattern = r"^.*\.3DModel$"  # Matches all yaml files whose stem ends with '.3DModel'.
    resource_cls = ThreeDModel
    resource_write_cls = ThreeDModelWrite
    list_cls = ThreeDModelList
    list_write_cls = ThreeDModelWriteList
    kind = "3DModel"
    dependencies = frozenset({DataSetsLoader})
    _doc_url = "3D-Models/operation/create3DModels"
    item_name = "revisions"

    @classmethod
    def get_id(cls, item: ThreeDModel | ThreeDModelWrite | dict) -> str:
        if isinstance(item, dict):
            return item["name"]
        if not item.name:
            raise KeyError("3DModel must have name")
        return item.name

    @classmethod
    def get_required_capability(cls, items: ThreeDModelWriteList | None) -> Capability | list[Capability]:
        if not items and items is not None:
            return []
        data_set_ids = {item.data_set_id for item in items or [] if item.data_set_id}
        scope = (
            capabilities.ThreeDAcl.Scope.DataSet(list(data_set_ids))
            if data_set_ids
            else capabilities.ThreeDAcl.Scope.All()
        )

        return capabilities.ThreeDAcl(
            [
                capabilities.ThreeDAcl.Action.Read,
                capabilities.ThreeDAcl.Action.Create,
                capabilities.ThreeDAcl.Action.Update,
                capabilities.ThreeDAcl.Action.Delete,
            ],
            scope,  # type: ignore[arg-type]
        )

    def create(self, items: ThreeDModelWriteList) -> ThreeDModelList:
        created = ThreeDModelList([])
        for item in items:
            new_item = self.client.three_d.models.create(**item.dump(camel_case=False))
            created.append(new_item)
        return created

    def retrieve(self, ids: SequenceNotStr[str]) -> ThreeDModelList:
        output = ThreeDModelList([])
        to_find = set(ids)
        for model in self.client.three_d.models:
            if model.name in to_find:
                output.append(model)
                to_find.remove(model.name)
                if not to_find:
                    break
        return output

    def update(self, items: ThreeDModelWriteList) -> ThreeDModelList:
        found = self.retrieve([item.name for item in items])
        id_by_name = {model.name: model.id for model in found}
        # 3D Model does not have an external identifier, only internal.
        # Thus, we cannot use the ThreeDModelWrite object to update the model,
        # instead we convert it to a ThreeDModelUpdate object.
        updates = []
        for item in items:
            if id_ := id_by_name.get(item.name):
                update = ThreeDModelUpdate(id=id_)
                if item.metadata:
                    update.metadata.set(item.metadata)
                if item.data_set_id:
                    update.data_set_id.set(item.data_set_id)
                # We cannot change the name of a 3D model as we use it as the identifier
                # Note this is expected
                updates.append(update)
        return self.client.three_d.models.update(updates)

    def delete(self, ids: SequenceNotStr[str]) -> int:
        models = self.retrieve(ids)
        self.client.three_d.models.delete(models.as_ids())
        return len(models)

    def iterate(self) -> Iterable[ThreeDModel]:
        return iter(self.client.three_d.models)

    def drop_data(self, ids: SequenceNotStr[str]) -> int:
        models = self.retrieve(ids)
        count = 0
        for model in models:
            revisions = self.client.three_d.revisions.list(model_id=model.id)
            self.client.three_d.revisions.delete(model_id=model.id, id=revisions.as_ids())
            count += len(revisions)
        return count

    def count(self, ids: SequenceNotStr[str]) -> int:
        models = self.retrieve(ids)
        count = 0
        for model in models:
            revisions = self.client.three_d.revisions.list(model_id=model.id)
            count += len(revisions)
        return count

    @classmethod
    @lru_cache(maxsize=1)
    def get_write_cls_parameter_spec(cls) -> ParameterSpecSet:
        spec = super().get_write_cls_parameter_spec()
        # Added by toolkit
        spec.add(ParameterSpec(("dataSetExternalId",), frozenset({"str"}), is_required=False, _is_nullable=False))

        # Should not be used, used for dataSetExternalId instead
        spec.discard(ParameterSpec(("dataSetId",), frozenset({"int"}), is_required=False, _is_nullable=False))
        return spec

    @classmethod
    def get_dependent_items(cls, item: dict) -> Iterable[tuple[type[ResourceLoader], Hashable]]:
        """Returns all items that this item requires.

        For example, a TimeSeries requires a DataSet, so this method would return the
        DatasetLoader and identifier of that dataset.
        """
        if "dataSetExternalId" in item:
            yield DataSetsLoader, item["dataSetExternalId"]

    def load_resource(self, filepath: Path, ToolGlobals: CDFToolConfig, skip_validation: bool) -> ThreeDModelWriteList:
        raw = load_yaml_inject_variables(filepath, ToolGlobals.environment_variables())
        resources = raw if isinstance(raw, list) else [raw]

        for resource in resources:
            if resource.get("dataSetExternalId") is not None:
                ds_external_id = resource.pop("dataSetExternalId")
                resource["dataSetId"] = ToolGlobals.verify_dataset(
                    ds_external_id, skip_validation, action="replace dataSetExternalId with dataSetId in 3D Model"
                )
        return ThreeDModelWriteList.load(resources)

    def _are_equal(
        self, local: ThreeDModelWrite, cdf_resource: ThreeDModel, return_dumped: bool = False
    ) -> bool | tuple[bool, dict[str, Any], dict[str, Any]]:
        local_dumped = local.dump()
        cdf_dumped = cdf_resource.as_write().dump()
        # Dry run
        if local_dumped.get("dataSetId") == -1 and "dataSetId" in cdf_dumped:
            local_dumped["dataSetId"] = cdf_dumped["dataSetId"]
        if not cdf_dumped.get("metadata") and not local_dumped.get("metadata"):
            cdf_dumped["metadata"] = local_dumped["metadata"] = {}
        return self._return_are_equal(local_dumped, cdf_dumped, return_dumped)
