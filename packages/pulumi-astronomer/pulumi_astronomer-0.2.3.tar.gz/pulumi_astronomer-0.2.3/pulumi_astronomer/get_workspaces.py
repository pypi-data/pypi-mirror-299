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
    'GetWorkspacesResult',
    'AwaitableGetWorkspacesResult',
    'get_workspaces',
    'get_workspaces_output',
]

@pulumi.output_type
class GetWorkspacesResult:
    """
    A collection of values returned by getWorkspaces.
    """
    def __init__(__self__, id=None, names=None, workspace_ids=None, workspaces=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if workspace_ids and not isinstance(workspace_ids, list):
            raise TypeError("Expected argument 'workspace_ids' to be a list")
        pulumi.set(__self__, "workspace_ids", workspace_ids)
        if workspaces and not isinstance(workspaces, list):
            raise TypeError("Expected argument 'workspaces' to be a list")
        pulumi.set(__self__, "workspaces", workspaces)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def names(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="workspaceIds")
    def workspace_ids(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "workspace_ids")

    @property
    @pulumi.getter
    def workspaces(self) -> Sequence['outputs.GetWorkspacesWorkspaceResult']:
        return pulumi.get(self, "workspaces")


class AwaitableGetWorkspacesResult(GetWorkspacesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkspacesResult(
            id=self.id,
            names=self.names,
            workspace_ids=self.workspace_ids,
            workspaces=self.workspaces)


def get_workspaces(names: Optional[Sequence[str]] = None,
                   workspace_ids: Optional[Sequence[str]] = None,
                   opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkspacesResult:
    """
    Workspaces data source

    ## Example Usage

    ```python
    import pulumi
    import pulumi_astronomer as astronomer

    example_workspaces_workspaces = astronomer.get_workspaces()
    example_workspaces_filter_by_workspace_ids = astronomer.get_workspaces(workspace_ids=[
        "clozc036j01to01jrlgvueo8t",
        "clozc036j01to01jrlgvueo81",
    ])
    example_workspaces_filter_by_names = astronomer.get_workspaces(names=[
        "my first workspace",
        "my second workspace",
    ])
    pulumi.export("exampleWorkspaces", example_workspaces_workspaces)
    ```
    """
    __args__ = dict()
    __args__['names'] = names
    __args__['workspaceIds'] = workspace_ids
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('astronomer:index/getWorkspaces:getWorkspaces', __args__, opts=opts, typ=GetWorkspacesResult).value

    return AwaitableGetWorkspacesResult(
        id=pulumi.get(__ret__, 'id'),
        names=pulumi.get(__ret__, 'names'),
        workspace_ids=pulumi.get(__ret__, 'workspace_ids'),
        workspaces=pulumi.get(__ret__, 'workspaces'))


@_utilities.lift_output_func(get_workspaces)
def get_workspaces_output(names: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                          workspace_ids: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkspacesResult]:
    """
    Workspaces data source

    ## Example Usage

    ```python
    import pulumi
    import pulumi_astronomer as astronomer

    example_workspaces_workspaces = astronomer.get_workspaces()
    example_workspaces_filter_by_workspace_ids = astronomer.get_workspaces(workspace_ids=[
        "clozc036j01to01jrlgvueo8t",
        "clozc036j01to01jrlgvueo81",
    ])
    example_workspaces_filter_by_names = astronomer.get_workspaces(names=[
        "my first workspace",
        "my second workspace",
    ])
    pulumi.export("exampleWorkspaces", example_workspaces_workspaces)
    ```
    """
    ...
