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
    'GetOrganizationResult',
    'AwaitableGetOrganizationResult',
    'get_organization',
    'get_organization_output',
]

@pulumi.output_type
class GetOrganizationResult:
    """
    A collection of values returned by getOrganization.
    """
    def __init__(__self__, billing_email=None, created_at=None, created_by=None, id=None, is_scim_enabled=None, name=None, payment_method=None, product=None, status=None, support_plan=None, trial_expires_at=None, updated_at=None, updated_by=None):
        if billing_email and not isinstance(billing_email, str):
            raise TypeError("Expected argument 'billing_email' to be a str")
        pulumi.set(__self__, "billing_email", billing_email)
        if created_at and not isinstance(created_at, str):
            raise TypeError("Expected argument 'created_at' to be a str")
        pulumi.set(__self__, "created_at", created_at)
        if created_by and not isinstance(created_by, dict):
            raise TypeError("Expected argument 'created_by' to be a dict")
        pulumi.set(__self__, "created_by", created_by)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if is_scim_enabled and not isinstance(is_scim_enabled, bool):
            raise TypeError("Expected argument 'is_scim_enabled' to be a bool")
        pulumi.set(__self__, "is_scim_enabled", is_scim_enabled)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if payment_method and not isinstance(payment_method, str):
            raise TypeError("Expected argument 'payment_method' to be a str")
        pulumi.set(__self__, "payment_method", payment_method)
        if product and not isinstance(product, str):
            raise TypeError("Expected argument 'product' to be a str")
        pulumi.set(__self__, "product", product)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if support_plan and not isinstance(support_plan, str):
            raise TypeError("Expected argument 'support_plan' to be a str")
        pulumi.set(__self__, "support_plan", support_plan)
        if trial_expires_at and not isinstance(trial_expires_at, str):
            raise TypeError("Expected argument 'trial_expires_at' to be a str")
        pulumi.set(__self__, "trial_expires_at", trial_expires_at)
        if updated_at and not isinstance(updated_at, str):
            raise TypeError("Expected argument 'updated_at' to be a str")
        pulumi.set(__self__, "updated_at", updated_at)
        if updated_by and not isinstance(updated_by, dict):
            raise TypeError("Expected argument 'updated_by' to be a dict")
        pulumi.set(__self__, "updated_by", updated_by)

    @property
    @pulumi.getter(name="billingEmail")
    def billing_email(self) -> str:
        """
        Organization billing email
        """
        return pulumi.get(self, "billing_email")

    @property
    @pulumi.getter(name="createdAt")
    def created_at(self) -> str:
        """
        Organization creation timestamp
        """
        return pulumi.get(self, "created_at")

    @property
    @pulumi.getter(name="createdBy")
    def created_by(self) -> 'outputs.GetOrganizationCreatedByResult':
        """
        Organization creator
        """
        return pulumi.get(self, "created_by")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        Organization identifier
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="isScimEnabled")
    def is_scim_enabled(self) -> bool:
        """
        Whether SCIM is enabled for the organization
        """
        return pulumi.get(self, "is_scim_enabled")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Organization name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="paymentMethod")
    def payment_method(self) -> str:
        """
        Organization payment method
        """
        return pulumi.get(self, "payment_method")

    @property
    @pulumi.getter
    def product(self) -> str:
        """
        Organization product type
        """
        return pulumi.get(self, "product")

    @property
    @pulumi.getter
    def status(self) -> str:
        """
        Organization status
        """
        return pulumi.get(self, "status")

    @property
    @pulumi.getter(name="supportPlan")
    def support_plan(self) -> str:
        """
        Organization support plan
        """
        return pulumi.get(self, "support_plan")

    @property
    @pulumi.getter(name="trialExpiresAt")
    def trial_expires_at(self) -> str:
        """
        Organization trial expiration timestamp
        """
        return pulumi.get(self, "trial_expires_at")

    @property
    @pulumi.getter(name="updatedAt")
    def updated_at(self) -> str:
        """
        Organization last updated timestamp
        """
        return pulumi.get(self, "updated_at")

    @property
    @pulumi.getter(name="updatedBy")
    def updated_by(self) -> 'outputs.GetOrganizationUpdatedByResult':
        """
        Organization updater
        """
        return pulumi.get(self, "updated_by")


class AwaitableGetOrganizationResult(GetOrganizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationResult(
            billing_email=self.billing_email,
            created_at=self.created_at,
            created_by=self.created_by,
            id=self.id,
            is_scim_enabled=self.is_scim_enabled,
            name=self.name,
            payment_method=self.payment_method,
            product=self.product,
            status=self.status,
            support_plan=self.support_plan,
            trial_expires_at=self.trial_expires_at,
            updated_at=self.updated_at,
            updated_by=self.updated_by)


def get_organization(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationResult:
    """
    Organization data source

    ## Example Usage

    ```python
    import pulumi
    import pulumi_astronomer as astronomer

    example_organization = astronomer.get_organization()
    pulumi.export("organization", example_organization)
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('astronomer:index/getOrganization:getOrganization', __args__, opts=opts, typ=GetOrganizationResult).value

    return AwaitableGetOrganizationResult(
        billing_email=pulumi.get(__ret__, 'billing_email'),
        created_at=pulumi.get(__ret__, 'created_at'),
        created_by=pulumi.get(__ret__, 'created_by'),
        id=pulumi.get(__ret__, 'id'),
        is_scim_enabled=pulumi.get(__ret__, 'is_scim_enabled'),
        name=pulumi.get(__ret__, 'name'),
        payment_method=pulumi.get(__ret__, 'payment_method'),
        product=pulumi.get(__ret__, 'product'),
        status=pulumi.get(__ret__, 'status'),
        support_plan=pulumi.get(__ret__, 'support_plan'),
        trial_expires_at=pulumi.get(__ret__, 'trial_expires_at'),
        updated_at=pulumi.get(__ret__, 'updated_at'),
        updated_by=pulumi.get(__ret__, 'updated_by'))


@_utilities.lift_output_func(get_organization)
def get_organization_output(opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetOrganizationResult]:
    """
    Organization data source

    ## Example Usage

    ```python
    import pulumi
    import pulumi_astronomer as astronomer

    example_organization = astronomer.get_organization()
    pulumi.export("organization", example_organization)
    ```
    """
    ...
