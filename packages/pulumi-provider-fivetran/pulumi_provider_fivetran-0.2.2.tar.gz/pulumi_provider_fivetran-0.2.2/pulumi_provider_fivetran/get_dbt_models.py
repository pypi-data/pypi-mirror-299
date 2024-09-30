# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetDbtModelsResult',
    'AwaitableGetDbtModelsResult',
    'get_dbt_models',
    'get_dbt_models_output',
]

@pulumi.output_type
class GetDbtModelsResult:
    """
    A collection of values returned by getDbtModels.
    """
    def __init__(__self__, id=None, models=None, project_id=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if models and not isinstance(models, list):
            raise TypeError("Expected argument 'models' to be a list")
        pulumi.set(__self__, "models", models)
        if project_id and not isinstance(project_id, str):
            raise TypeError("Expected argument 'project_id' to be a str")
        pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of this datasource (equals to `project_id`).
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def models(self) -> Optional[Sequence['outputs.GetDbtModelsModelResult']]:
        return pulumi.get(self, "models")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> str:
        """
        The unique identifier for the dbt Project within the Fivetran system.
        """
        return pulumi.get(self, "project_id")


class AwaitableGetDbtModelsResult(GetDbtModelsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDbtModelsResult(
            id=self.id,
            models=self.models,
            project_id=self.project_id)


def get_dbt_models(models: Optional[Sequence[Union['GetDbtModelsModelArgs', 'GetDbtModelsModelArgsDict']]] = None,
                   project_id: Optional[str] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDbtModelsResult:
    """
    This data source returns a list of all dbt Models available for specified dbt Project id.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_models = fivetran.get_dbt_models(project_id="project_id")
    ```


    :param str project_id: The unique identifier for the dbt Project within the Fivetran system.
    """
    __args__ = dict()
    __args__['models'] = models
    __args__['projectId'] = project_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getDbtModels:getDbtModels', __args__, opts=opts, typ=GetDbtModelsResult).value

    return AwaitableGetDbtModelsResult(
        id=pulumi.get(__ret__, 'id'),
        models=pulumi.get(__ret__, 'models'),
        project_id=pulumi.get(__ret__, 'project_id'))


@_utilities.lift_output_func(get_dbt_models)
def get_dbt_models_output(models: Optional[pulumi.Input[Optional[Sequence[Union['GetDbtModelsModelArgs', 'GetDbtModelsModelArgsDict']]]]] = None,
                          project_id: Optional[pulumi.Input[str]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDbtModelsResult]:
    """
    This data source returns a list of all dbt Models available for specified dbt Project id.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_models = fivetran.get_dbt_models(project_id="project_id")
    ```


    :param str project_id: The unique identifier for the dbt Project within the Fivetran system.
    """
    ...
