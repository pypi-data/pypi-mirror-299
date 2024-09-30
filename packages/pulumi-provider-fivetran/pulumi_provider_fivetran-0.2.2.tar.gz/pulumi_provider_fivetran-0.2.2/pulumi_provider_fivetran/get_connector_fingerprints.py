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
    'GetConnectorFingerprintsResult',
    'AwaitableGetConnectorFingerprintsResult',
    'get_connector_fingerprints',
    'get_connector_fingerprints_output',
]

@pulumi.output_type
class GetConnectorFingerprintsResult:
    """
    A collection of values returned by getConnectorFingerprints.
    """
    def __init__(__self__, connector_id=None, fingerprints=None, id=None):
        if connector_id and not isinstance(connector_id, str):
            raise TypeError("Expected argument 'connector_id' to be a str")
        pulumi.set(__self__, "connector_id", connector_id)
        if fingerprints and not isinstance(fingerprints, list):
            raise TypeError("Expected argument 'fingerprints' to be a list")
        pulumi.set(__self__, "fingerprints", fingerprints)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter(name="connectorId")
    def connector_id(self) -> str:
        """
        The unique identifier for the target connection within the Fivetran system.
        """
        return pulumi.get(self, "connector_id")

    @property
    @pulumi.getter
    def fingerprints(self) -> Optional[Sequence['outputs.GetConnectorFingerprintsFingerprintResult']]:
        return pulumi.get(self, "fingerprints")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The unique identifier for the resource. Equal to target connection id.
        """
        return pulumi.get(self, "id")


class AwaitableGetConnectorFingerprintsResult(GetConnectorFingerprintsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetConnectorFingerprintsResult(
            connector_id=self.connector_id,
            fingerprints=self.fingerprints,
            id=self.id)


def get_connector_fingerprints(fingerprints: Optional[Sequence[Union['GetConnectorFingerprintsFingerprintArgs', 'GetConnectorFingerprintsFingerprintArgsDict']]] = None,
                               id: Optional[str] = None,
                               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetConnectorFingerprintsResult:
    """
    This data source returns a list of SSH fingerprints approved for specified connector.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    connector_fingerprints = fivetran.get_connector_fingerprints(id="connector_id")
    ```


    :param str id: The unique identifier for the resource. Equal to target connection id.
    """
    __args__ = dict()
    __args__['fingerprints'] = fingerprints
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getConnectorFingerprints:getConnectorFingerprints', __args__, opts=opts, typ=GetConnectorFingerprintsResult).value

    return AwaitableGetConnectorFingerprintsResult(
        connector_id=pulumi.get(__ret__, 'connector_id'),
        fingerprints=pulumi.get(__ret__, 'fingerprints'),
        id=pulumi.get(__ret__, 'id'))


@_utilities.lift_output_func(get_connector_fingerprints)
def get_connector_fingerprints_output(fingerprints: Optional[pulumi.Input[Optional[Sequence[Union['GetConnectorFingerprintsFingerprintArgs', 'GetConnectorFingerprintsFingerprintArgsDict']]]]] = None,
                                      id: Optional[pulumi.Input[str]] = None,
                                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetConnectorFingerprintsResult]:
    """
    This data source returns a list of SSH fingerprints approved for specified connector.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    connector_fingerprints = fivetran.get_connector_fingerprints(id="connector_id")
    ```


    :param str id: The unique identifier for the resource. Equal to target connection id.
    """
    ...
