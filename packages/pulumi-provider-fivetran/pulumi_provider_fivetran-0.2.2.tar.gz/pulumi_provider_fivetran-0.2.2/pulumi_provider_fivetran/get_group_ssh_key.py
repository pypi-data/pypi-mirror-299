# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = [
    'GetGroupSshKeyResult',
    'AwaitableGetGroupSshKeyResult',
    'get_group_ssh_key',
    'get_group_ssh_key_output',
]

@pulumi.output_type
class GetGroupSshKeyResult:
    """
    A collection of values returned by getGroupSshKey.
    """
    def __init__(__self__, id=None, public_key=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if public_key and not isinstance(public_key, str):
            raise TypeError("Expected argument 'public_key' to be a str")
        pulumi.set(__self__, "public_key", public_key)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique identifier for the group within the Fivetran system.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="publicKey")
    def public_key(self) -> str:
        """
        Public key from SSH key pair associated with the group.
        """
        return pulumi.get(self, "public_key")


class AwaitableGetGroupSshKeyResult(GetGroupSshKeyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetGroupSshKeyResult(
            id=self.id,
            public_key=self.public_key)


def get_group_ssh_key(id: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetGroupSshKeyResult:
    """
    This data source returns public key from SSH key pair associated with the group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_group_public_key = fivetran.get_group_ssh_key(id="group_id")
    ```


    :param str id: The unique identifier for the group within the Fivetran system.
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getGroupSshKey:getGroupSshKey', __args__, opts=opts, typ=GetGroupSshKeyResult).value

    return AwaitableGetGroupSshKeyResult(
        id=pulumi.get(__ret__, 'id'),
        public_key=pulumi.get(__ret__, 'public_key'))


@_utilities.lift_output_func(get_group_ssh_key)
def get_group_ssh_key_output(id: Optional[pulumi.Input[str]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetGroupSshKeyResult]:
    """
    This data source returns public key from SSH key pair associated with the group.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    my_group_public_key = fivetran.get_group_ssh_key(id="group_id")
    ```


    :param str id: The unique identifier for the group within the Fivetran system.
    """
    ...
