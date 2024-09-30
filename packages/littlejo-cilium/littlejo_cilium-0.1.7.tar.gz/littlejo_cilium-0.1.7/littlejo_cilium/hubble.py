# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['HubbleArgs', 'Hubble']

@pulumi.input_type
class HubbleArgs:
    def __init__(__self__, *,
                 relay: Optional[pulumi.Input[bool]] = None,
                 ui: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a Hubble resource.
        :param pulumi.Input[bool] relay: Deploy Hubble Relay (Default: `true`).
        :param pulumi.Input[bool] ui: Enable Hubble UI (Default: `false`).
        """
        if relay is not None:
            pulumi.set(__self__, "relay", relay)
        if ui is not None:
            pulumi.set(__self__, "ui", ui)

    @property
    @pulumi.getter
    def relay(self) -> Optional[pulumi.Input[bool]]:
        """
        Deploy Hubble Relay (Default: `true`).
        """
        return pulumi.get(self, "relay")

    @relay.setter
    def relay(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "relay", value)

    @property
    @pulumi.getter
    def ui(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable Hubble UI (Default: `false`).
        """
        return pulumi.get(self, "ui")

    @ui.setter
    def ui(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ui", value)


@pulumi.input_type
class _HubbleState:
    def __init__(__self__, *,
                 relay: Optional[pulumi.Input[bool]] = None,
                 ui: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering Hubble resources.
        :param pulumi.Input[bool] relay: Deploy Hubble Relay (Default: `true`).
        :param pulumi.Input[bool] ui: Enable Hubble UI (Default: `false`).
        """
        if relay is not None:
            pulumi.set(__self__, "relay", relay)
        if ui is not None:
            pulumi.set(__self__, "ui", ui)

    @property
    @pulumi.getter
    def relay(self) -> Optional[pulumi.Input[bool]]:
        """
        Deploy Hubble Relay (Default: `true`).
        """
        return pulumi.get(self, "relay")

    @relay.setter
    def relay(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "relay", value)

    @property
    @pulumi.getter
    def ui(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable Hubble UI (Default: `false`).
        """
        return pulumi.get(self, "ui")

    @ui.setter
    def ui(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ui", value)


class Hubble(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 relay: Optional[pulumi.Input[bool]] = None,
                 ui: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Hubble resource for Cilium. This is equivalent to cilium cli: `cilium hubble`: It manages cilium hubble

        ## Example Usage

        ```python
        import pulumi
        import littlejo_cilium as cilium

        example = cilium.Hubble("example", ui=True)
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] relay: Deploy Hubble Relay (Default: `true`).
        :param pulumi.Input[bool] ui: Enable Hubble UI (Default: `false`).
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: Optional[HubbleArgs] = None,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Hubble resource for Cilium. This is equivalent to cilium cli: `cilium hubble`: It manages cilium hubble

        ## Example Usage

        ```python
        import pulumi
        import littlejo_cilium as cilium

        example = cilium.Hubble("example", ui=True)
        ```

        :param str resource_name: The name of the resource.
        :param HubbleArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(HubbleArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 relay: Optional[pulumi.Input[bool]] = None,
                 ui: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = HubbleArgs.__new__(HubbleArgs)

            __props__.__dict__["relay"] = relay
            __props__.__dict__["ui"] = ui
        super(Hubble, __self__).__init__(
            'cilium:index/hubble:Hubble',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            relay: Optional[pulumi.Input[bool]] = None,
            ui: Optional[pulumi.Input[bool]] = None) -> 'Hubble':
        """
        Get an existing Hubble resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] relay: Deploy Hubble Relay (Default: `true`).
        :param pulumi.Input[bool] ui: Enable Hubble UI (Default: `false`).
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _HubbleState.__new__(_HubbleState)

        __props__.__dict__["relay"] = relay
        __props__.__dict__["ui"] = ui
        return Hubble(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def relay(self) -> pulumi.Output[bool]:
        """
        Deploy Hubble Relay (Default: `true`).
        """
        return pulumi.get(self, "relay")

    @property
    @pulumi.getter
    def ui(self) -> pulumi.Output[bool]:
        """
        Enable Hubble UI (Default: `false`).
        """
        return pulumi.get(self, "ui")

