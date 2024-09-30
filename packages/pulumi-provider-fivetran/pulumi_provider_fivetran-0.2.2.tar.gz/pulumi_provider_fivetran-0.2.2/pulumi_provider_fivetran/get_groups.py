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
    'GetGroupsResult',
    'AwaitableGetGroupsResult',
    'get_groups',
    'get_groups_output',
]

@pulumi.output_type
class GetGroupsResult:
    """
    A collection of values returned by getGroups.
    """
    def __init__(__self__, groups=None, id=None):
        if groups and not isinstance(groups, list):
            raise TypeError("Expected argument 'groups' to be a list")
        pulumi.set(__self__, "groups", groups)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def groups(self) -> Optional[Sequence['outputs.GetGroupsGroupResult']]:
        return pulumi.get(self, "groups")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The ID of this resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetGroupsResult(GetGroupsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupsResult(
            groups=self.groups,
            id=self.id)


def get_groups(groups: Optional[Sequence[Union['GetGroupsGroupArgs', 'GetGroupsGroupArgsDict']]] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupsResult:
    """
    This data source returns a list of all groups within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    all = fivetran.get_groups()
    ```
    """
    __args__ = dict()
    __args__['groups'] = groups
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getGroups:getGroups', __args__, opts=opts, typ=GetGroupsResult).value

    return AwaitableGetGroupsResult(
        groups=pulumi.get(__ret__, 'groups'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_groups)
def get_groups_output(groups: Optional[pulumi.Input[Optional[Sequence[Union['GetGroupsGroupArgs', 'GetGroupsGroupArgsDict']]]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupsResult]:
    """
    This data source returns a list of all groups within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    all = fivetran.get_groups()
    ```
    """
    ...
