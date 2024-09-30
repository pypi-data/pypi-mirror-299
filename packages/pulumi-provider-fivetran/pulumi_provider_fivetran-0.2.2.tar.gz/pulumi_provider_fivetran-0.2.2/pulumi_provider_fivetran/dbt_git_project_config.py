# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['DbtGitProjectConfigArgs', 'DbtGitProjectConfig']

@pulumi.input_type
class DbtGitProjectConfigArgs:
    def __init__(__self__, *,
                 project_id: pulumi.Input[str],
                 ensure_readiness: Optional[pulumi.Input[bool]] = None,
                 folder_path: Optional[pulumi.Input[str]] = None,
                 git_branch: Optional[pulumi.Input[str]] = None,
                 git_remote_url: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a DbtGitProjectConfig resource.
        :param pulumi.Input[str] project_id: The unique identifier for the dbt Project within the Fivetran system.
        :param pulumi.Input[bool] ensure_readiness: Should resource wait for project to finish initialization. Default value: false.
        :param pulumi.Input[str] folder_path: Folder in Git repo with your dbt project.
        :param pulumi.Input[str] git_branch: Git branch.
        :param pulumi.Input[str] git_remote_url: Git remote URL with your dbt project.
        """
        pulumi.set(__self__, "project_id", project_id)
        if ensure_readiness is not None:
            pulumi.set(__self__, "ensure_readiness", ensure_readiness)
        if folder_path is not None:
            pulumi.set(__self__, "folder_path", folder_path)
        if git_branch is not None:
            pulumi.set(__self__, "git_branch", git_branch)
        if git_remote_url is not None:
            pulumi.set(__self__, "git_remote_url", git_remote_url)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Input[str]:
        """
        The unique identifier for the dbt Project within the Fivetran system.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "project_id", value)

    @property
    @pulumi.getter(name="ensureReadiness")
    def ensure_readiness(self) -> Optional[pulumi.Input[bool]]:
        """
        Should resource wait for project to finish initialization. Default value: false.
        """
        return pulumi.get(self, "ensure_readiness")

    @ensure_readiness.setter
    def ensure_readiness(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ensure_readiness", value)

    @property
    @pulumi.getter(name="folderPath")
    def folder_path(self) -> Optional[pulumi.Input[str]]:
        """
        Folder in Git repo with your dbt project.
        """
        return pulumi.get(self, "folder_path")

    @folder_path.setter
    def folder_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder_path", value)

    @property
    @pulumi.getter(name="gitBranch")
    def git_branch(self) -> Optional[pulumi.Input[str]]:
        """
        Git branch.
        """
        return pulumi.get(self, "git_branch")

    @git_branch.setter
    def git_branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "git_branch", value)

    @property
    @pulumi.getter(name="gitRemoteUrl")
    def git_remote_url(self) -> Optional[pulumi.Input[str]]:
        """
        Git remote URL with your dbt project.
        """
        return pulumi.get(self, "git_remote_url")

    @git_remote_url.setter
    def git_remote_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "git_remote_url", value)


@pulumi.input_type
class _DbtGitProjectConfigState:
    def __init__(__self__, *,
                 ensure_readiness: Optional[pulumi.Input[bool]] = None,
                 folder_path: Optional[pulumi.Input[str]] = None,
                 git_branch: Optional[pulumi.Input[str]] = None,
                 git_remote_url: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering DbtGitProjectConfig resources.
        :param pulumi.Input[bool] ensure_readiness: Should resource wait for project to finish initialization. Default value: false.
        :param pulumi.Input[str] folder_path: Folder in Git repo with your dbt project.
        :param pulumi.Input[str] git_branch: Git branch.
        :param pulumi.Input[str] git_remote_url: Git remote URL with your dbt project.
        :param pulumi.Input[str] project_id: The unique identifier for the dbt Project within the Fivetran system.
        """
        if ensure_readiness is not None:
            pulumi.set(__self__, "ensure_readiness", ensure_readiness)
        if folder_path is not None:
            pulumi.set(__self__, "folder_path", folder_path)
        if git_branch is not None:
            pulumi.set(__self__, "git_branch", git_branch)
        if git_remote_url is not None:
            pulumi.set(__self__, "git_remote_url", git_remote_url)
        if project_id is not None:
            pulumi.set(__self__, "project_id", project_id)

    @property
    @pulumi.getter(name="ensureReadiness")
    def ensure_readiness(self) -> Optional[pulumi.Input[bool]]:
        """
        Should resource wait for project to finish initialization. Default value: false.
        """
        return pulumi.get(self, "ensure_readiness")

    @ensure_readiness.setter
    def ensure_readiness(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ensure_readiness", value)

    @property
    @pulumi.getter(name="folderPath")
    def folder_path(self) -> Optional[pulumi.Input[str]]:
        """
        Folder in Git repo with your dbt project.
        """
        return pulumi.get(self, "folder_path")

    @folder_path.setter
    def folder_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "folder_path", value)

    @property
    @pulumi.getter(name="gitBranch")
    def git_branch(self) -> Optional[pulumi.Input[str]]:
        """
        Git branch.
        """
        return pulumi.get(self, "git_branch")

    @git_branch.setter
    def git_branch(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "git_branch", value)

    @property
    @pulumi.getter(name="gitRemoteUrl")
    def git_remote_url(self) -> Optional[pulumi.Input[str]]:
        """
        Git remote URL with your dbt project.
        """
        return pulumi.get(self, "git_remote_url")

    @git_remote_url.setter
    def git_remote_url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "git_remote_url", value)

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> Optional[pulumi.Input[str]]:
        """
        The unique identifier for the dbt Project within the Fivetran system.
        """
        return pulumi.get(self, "project_id")

    @project_id.setter
    def project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project_id", value)


class DbtGitProjectConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ensure_readiness: Optional[pulumi.Input[bool]] = None,
                 folder_path: Optional[pulumi.Input[str]] = None,
                 git_branch: Optional[pulumi.Input[str]] = None,
                 git_remote_url: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Resource is in ALPHA state.

        This resource allows you to add and manage dbt Git Projects Configs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_provider_fivetran as fivetran

        git_project_config = fivetran.DbtGitProjectConfig("gitProjectConfig",
            folder_path="/dbt/project/folder/path",
            git_branch="main",
            git_remote_url="your_git_remote_url",
            project_id="project_id")
        ```

        ## Import

        1. To import an existing `fivetran_dbt_git_project_config` resource into your Terraform state, you need to get **Dbt Project ID** via API call `GET https://api.fivetran.com/v1/dbt/projects` to retrieve available projects.

        2. Fetch project details for particular `project-id` using `GET https://api.fivetran.com/v1/dbt/projects/{project-id}` to ensure that this is the project you want to import.

        3. Define an empty resource in your `.tf` configuration:

        hcl

        resource "fivetran_dbt_git_project_config" "my_imported_fivetran_dbt_git_project_config" {

        }

        4. Run the `pulumi import` command:

        ```sh
        $ pulumi import fivetran:index/dbtGitProjectConfig:DbtGitProjectConfig my_imported_fivetran_dbt_git_project_config {Dbt Project ID}
        ```

        4. Use the `terraform state show` command to get the values from the state:

        terraform state show 'fivetran_dbt_git_project_config.my_imported_fivetran_dbt_git_project_config'

        5. Copy the values and paste them to your `.tf` configuration.

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] ensure_readiness: Should resource wait for project to finish initialization. Default value: false.
        :param pulumi.Input[str] folder_path: Folder in Git repo with your dbt project.
        :param pulumi.Input[str] git_branch: Git branch.
        :param pulumi.Input[str] git_remote_url: Git remote URL with your dbt project.
        :param pulumi.Input[str] project_id: The unique identifier for the dbt Project within the Fivetran system.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: DbtGitProjectConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource is in ALPHA state.

        This resource allows you to add and manage dbt Git Projects Configs.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_provider_fivetran as fivetran

        git_project_config = fivetran.DbtGitProjectConfig("gitProjectConfig",
            folder_path="/dbt/project/folder/path",
            git_branch="main",
            git_remote_url="your_git_remote_url",
            project_id="project_id")
        ```

        ## Import

        1. To import an existing `fivetran_dbt_git_project_config` resource into your Terraform state, you need to get **Dbt Project ID** via API call `GET https://api.fivetran.com/v1/dbt/projects` to retrieve available projects.

        2. Fetch project details for particular `project-id` using `GET https://api.fivetran.com/v1/dbt/projects/{project-id}` to ensure that this is the project you want to import.

        3. Define an empty resource in your `.tf` configuration:

        hcl

        resource "fivetran_dbt_git_project_config" "my_imported_fivetran_dbt_git_project_config" {

        }

        4. Run the `pulumi import` command:

        ```sh
        $ pulumi import fivetran:index/dbtGitProjectConfig:DbtGitProjectConfig my_imported_fivetran_dbt_git_project_config {Dbt Project ID}
        ```

        4. Use the `terraform state show` command to get the values from the state:

        terraform state show 'fivetran_dbt_git_project_config.my_imported_fivetran_dbt_git_project_config'

        5. Copy the values and paste them to your `.tf` configuration.

        :param str resource_name: The name of the resource.
        :param DbtGitProjectConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(DbtGitProjectConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 ensure_readiness: Optional[pulumi.Input[bool]] = None,
                 folder_path: Optional[pulumi.Input[str]] = None,
                 git_branch: Optional[pulumi.Input[str]] = None,
                 git_remote_url: Optional[pulumi.Input[str]] = None,
                 project_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = DbtGitProjectConfigArgs.__new__(DbtGitProjectConfigArgs)

            __props__.__dict__["ensure_readiness"] = ensure_readiness
            __props__.__dict__["folder_path"] = folder_path
            __props__.__dict__["git_branch"] = git_branch
            __props__.__dict__["git_remote_url"] = git_remote_url
            if project_id is None and not opts.urn:
                raise TypeError("Missing required property 'project_id'")
            __props__.__dict__["project_id"] = project_id
        super(DbtGitProjectConfig, __self__).__init__(
            'fivetran:index/dbtGitProjectConfig:DbtGitProjectConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            ensure_readiness: Optional[pulumi.Input[bool]] = None,
            folder_path: Optional[pulumi.Input[str]] = None,
            git_branch: Optional[pulumi.Input[str]] = None,
            git_remote_url: Optional[pulumi.Input[str]] = None,
            project_id: Optional[pulumi.Input[str]] = None) -> 'DbtGitProjectConfig':
        """
        Get an existing DbtGitProjectConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] ensure_readiness: Should resource wait for project to finish initialization. Default value: false.
        :param pulumi.Input[str] folder_path: Folder in Git repo with your dbt project.
        :param pulumi.Input[str] git_branch: Git branch.
        :param pulumi.Input[str] git_remote_url: Git remote URL with your dbt project.
        :param pulumi.Input[str] project_id: The unique identifier for the dbt Project within the Fivetran system.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _DbtGitProjectConfigState.__new__(_DbtGitProjectConfigState)

        __props__.__dict__["ensure_readiness"] = ensure_readiness
        __props__.__dict__["folder_path"] = folder_path
        __props__.__dict__["git_branch"] = git_branch
        __props__.__dict__["git_remote_url"] = git_remote_url
        __props__.__dict__["project_id"] = project_id
        return DbtGitProjectConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="ensureReadiness")
    def ensure_readiness(self) -> pulumi.Output[bool]:
        """
        Should resource wait for project to finish initialization. Default value: false.
        """
        return pulumi.get(self, "ensure_readiness")

    @property
    @pulumi.getter(name="folderPath")
    def folder_path(self) -> pulumi.Output[Optional[str]]:
        """
        Folder in Git repo with your dbt project.
        """
        return pulumi.get(self, "folder_path")

    @property
    @pulumi.getter(name="gitBranch")
    def git_branch(self) -> pulumi.Output[Optional[str]]:
        """
        Git branch.
        """
        return pulumi.get(self, "git_branch")

    @property
    @pulumi.getter(name="gitRemoteUrl")
    def git_remote_url(self) -> pulumi.Output[Optional[str]]:
        """
        Git remote URL with your dbt project.
        """
        return pulumi.get(self, "git_remote_url")

    @property
    @pulumi.getter(name="projectId")
    def project_id(self) -> pulumi.Output[str]:
        """
        The unique identifier for the dbt Project within the Fivetran system.
        """
        return pulumi.get(self, "project_id")

