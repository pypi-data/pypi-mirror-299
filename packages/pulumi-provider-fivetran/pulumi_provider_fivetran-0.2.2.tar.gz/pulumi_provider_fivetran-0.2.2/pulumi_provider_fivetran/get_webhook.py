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
    'GetWebhookResult',
    'AwaitableGetWebhookResult',
    'get_webhook',
    'get_webhook_output',
]

@pulumi.output_type
class GetWebhookResult:
    """
    A collection of values returned by getWebhook.
    """
    def __init__(__self__, active=None, created_at=None, created_by=None, events=None, group_id=None, id=None, run_tests=None, secret=None, type=None, url=None):
        if active and not isinstance(active, bool):
            raise TypeError("Expected argument 'active' to be a bool")
        pulumi.set(__self__, "active", active)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if created_by and not isinstance(created_by, str):
            raise TypeError("Expected argument 'created_by' to be a str")
        pulumi.set(__self__, "created_by", created_by)
        if events and not isinstance(events, list):
            raise TypeError("Expected argument 'events' to be a list")
        pulumi.set(__self__, "events", events)
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        pulumi.set(__self__, "group_id", group_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if run_tests and not isinstance(run_tests, bool):
            raise TypeError("Expected argument 'run_tests' to be a bool")
        pulumi.set(__self__, "run_tests", run_tests)
        if secret and not isinstance(secret, str):
            raise TypeError("Expected argument 'secret' to be a str")
        pulumi.set(__self__, "secret", secret)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if url and not isinstance(url, str):
            raise TypeError("Expected argument 'url' to be a str")
        pulumi.set(__self__, "url", url)

    @property
    @pulumi.getter
    def active(self) -> bool:
        """
        Boolean, if set to true, webhooks are immediately sent in response to events
        """
        return pulumi.get(self, "active")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        The webhook creation timestamp
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> str:
        """
        The ID of the user who created the webhook.
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter
    def events(self) -> Sequence[str]:
        """
        The array of event types
        """
        return pulumi.get(self, "events")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> str:
        """
        The group ID
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The webhook ID
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="runTests")
    def run_tests(self) -> bool:
        """
        Specifies whether the setup tests should be run
        """
        return pulumi.get(self, "run_tests")

    @property
    @pulumi.getter
    def secret(self) -> str:
        """
        The secret string used for payload signing and masked in the response.
        """
        return pulumi.get(self, "secret")

    @property
    @pulumi.getter
    def type(self) -> str:
        """
        The webhook type (group, account)
        """
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def url(self) -> str:
        """
        Your webhooks URL endpoint for your application
        """
        return pulumi.get(self, "url")


class AwaitableGetWebhookResult(GetWebhookResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWebhookResult(
            active=self.active,
            created_at=self.created_at,
            created_by=self.created_by,
            events=self.events,
            group_id=self.group_id,
            id=self.id,
            run_tests=self.run_tests,
            secret=self.secret,
            type=self.type,
            url=self.url)


def get_webhook(id: Optional[str] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWebhookResult:
    """
    This data source returns a webhook object.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    webhook = fivetran.get_webhook(id="webhook_id")
    ```


    :param str id: The webhook ID
    """
    __args__ = dict()
    __args__['id'] = id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('fivetran:index/getWebhook:getWebhook', __args__, opts=opts, typ=GetWebhookResult).value

    return AwaitableGetWebhookResult(
        active=pulumi.get(__ret__, 'active'),
        created_at=pulumi.get(__ret__, 'created_at'),
        created_by=pulumi.get(__ret__, 'created_by'),
        events=pulumi.get(__ret__, 'events'),
        group_id=pulumi.get(__ret__, 'group_id'),
        id=pulumi.get(__ret__, 'id'),
        run_tests=pulumi.get(__ret__, 'run_tests'),
        secret=pulumi.get(__ret__, 'secret'),
        type=pulumi.get(__ret__, 'type'),
        url=pulumi.get(__ret__, 'url'))


@_utilities.lift_output_func(get_webhook)
def get_webhook_output(id: Optional[pulumi.Input[str]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWebhookResult]:
    """
    This data source returns a webhook object.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_fivetran as fivetran

    webhook = fivetran.get_webhook(id="webhook_id")
    ```


    :param str id: The webhook ID
    """
    ...
