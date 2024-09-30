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

__all__ = [
    'GetDbtProjectsResult',
    'AwaitableGetDbtProjectsResult',
    'get_dbt_projects',
    'get_dbt_projects_output',
]

@pulumi.output_type
class GetDbtProjectsResult:
    """
    A collection of values returned by getDbtProjects.
    """
    def __init__(__self__, id=None, projects=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if projects and not isinstance(projects, list):
            raise TypeError("Expected argument 'projects' to be a list")
        pulumi.set(__self__, "projects", projects)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def projects(self) -> Sequence['outputs.GetDbtProjectsProjectResult']:
        return pulumi.get(self, "projects")


class AwaitableGetDbtProjectsResult(GetDbtProjectsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDbtProjectsResult(
            id=self.id,
            projects=self.projects)


def get_dbt_projects(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDbtProjectsResult:
    """
    This data source returns a list of all dbt Projects within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_projects = fivetran.get_dbt_projects()
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getDbtProjects:getDbtProjects', __args__, opts=opts, typ=GetDbtProjectsResult).value

    return AwaitableGetDbtProjectsResult(
        id=pulumi.get(__ret__, 'id'),
        projects=pulumi.get(__ret__, 'projects'))


@_utilities.lift_output_func(get_dbt_projects)
def get_dbt_projects_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDbtProjectsResult]:
    """
    This data source returns a list of all dbt Projects within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_projects = fivetran.get_dbt_projects()
    ```
    """
    ...
