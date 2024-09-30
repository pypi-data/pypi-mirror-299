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
    'GetUsersResult',
    'AwaitableGetUsersResult',
    'get_users',
    'get_users_output',
]

@pulumi.output_type
class GetUsersResult:
    """
    A collection of values returned by getUsers.
    """
    def __init__(__self__, id=None, users=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if users and not isinstance(users, list):
            raise TypeError("Expected argument 'users' to be a list")
        pulumi.set(__self__, "users", users)

    @property
    @pulumi.getter
    def id(self) -> Optional[str]:
        """
        The ID of this resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def users(self) -> Optional[Sequence['outputs.GetUsersUserResult']]:
        return pulumi.get(self, "users")


class AwaitableGetUsersResult(GetUsersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetUsersResult(
            id=self.id,
            users=self.users)


def get_users(id: Optional[str] = None,
              users: Optional[Sequence[Union['GetUsersUserArgs', 'GetUsersUserArgsDict']]] = None,
              opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetUsersResult:
    """
    This data source returns a list of all users within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    users = fivetran.get_users()
    ```


    :param str id: The ID of this resource.
    """
    __args__ = dict()
    __args__['id'] = id
    __args__['users'] = users
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getUsers:getUsers', __args__, opts=opts, typ=GetUsersResult).value

    return AwaitableGetUsersResult(
        id=pulumi.get(__ret__, 'id'),
        users=pulumi.get(__ret__, 'users'))


@_utilities.lift_output_func(get_users)
def get_users_output(id: Optional[pulumi.Input[Optional[str]]] = None,
                     users: Optional[pulumi.Input[Optional[Sequence[Union['GetUsersUserArgs', 'GetUsersUserArgsDict']]]]] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetUsersResult]:
    """
    This data source returns a list of all users within your Fivetran account.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    users = fivetran.get_users()
    ```


    :param str id: The ID of this resource.
    """
    ...
