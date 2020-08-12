# external class imports
from nacl.signing import VerifyKey
from typing import List

from syft.core.common.message import (
    ImmediateSyftMessageWithoutReply,
    ImmediateSyftMessageWithReply,
    SignedMessage,
)

from .....decorators import syft_decorator
from ...abstract.node import AbstractNode
from .node_service import (
    ImmediateNodeServiceWithoutReply,
    ImmediateNodeServiceWithReply,
    SignedNodeServiceWithReply,
)

from .auth import service_auth


class MessageWithoutReplyForwardingService(ImmediateNodeServiceWithoutReply):
    @service_auth(existing_users_only=True)
    @syft_decorator(typechecking=True)
    def process(
        self, node: AbstractNode, msg: ImmediateSyftMessageWithoutReply, verify_key: VerifyKey
    ) -> None:
        addr = msg.address
        print(addr.vm.id)
        if addr.vm is not None and addr.vm.id in node.store:
            # TODO: don't return .data - instead have storableObject's parameters actually
            #  be on the object.
            return node.store[addr.vm.id].data.send_immediate_msg_without_reply(msg=msg)

        if addr.device is not None and addr.device.id in node.store:

            return node.store[addr.device.id].data.send_immediate_msg_without_reply(
                msg=msg
            )

        if addr.domain is not None and addr.domain.id in node.store:
            return node.store[addr.domain.id].data.send_immediate_msg_without_reply(
                msg=msg
            )

        if addr.network is not None and addr.network.id in node.store:
            return node.store[addr.network.id].data.send_immediate_msg_without_reply(
                msg=msg
            )

        raise Exception(
            "Address unknown - cannot forward old_message. Throwing it away."
        )

    @staticmethod
    @syft_decorator(typechecking=True)
    def message_handler_types() -> List[type]:
        return [ImmediateSyftMessageWithoutReply]


class MessageWithReplyForwardingService(ImmediateNodeServiceWithReply):
    @syft_decorator(typechecking=True)
    def process(
        self, node: AbstractNode, msg: ImmediateSyftMessageWithReply, verify_key: VerifyKey
    ) -> ImmediateSyftMessageWithoutReply:

        addr = msg.address
        pri_addr = addr.pri_address
        pub_addr = addr.pub_address

        if pri_addr.vm is not None and node.store.has_object(pri_addr.vm):
            return node.store.get_object(pri_addr.vm).send_immediate_msg_with_reply(
                msg=msg
            )

        if pri_addr.device is not None and node.store.has_object(pri_addr.device):
            return node.store.get_object(pri_addr.device).send_immediate_msg_with_reply(
                msg=msg
            )

        if pub_addr.domain is not None and node.store.has_object(pub_addr.domain):
            return node.store.get_object(pub_addr.domain).send_immediate_msg_with_reply(
                msg=msg
            )

        if pub_addr.network is not None and node.store.has_object(pub_addr.network):
            return node.store.get_object(
                pub_addr.network
            ).send_immediate_msg_with_reply(msg=msg)

        raise Exception(
            "Address unknown - cannot forward old_message. Throwing it away."
        )


class SignedMessageWithReplyForwardingService(SignedNodeServiceWithReply):
    @syft_decorator(typechecking=True)
    def process(self, node: AbstractNode, msg: SignedMessage, verify_key: VerifyKey) -> SignedMessage:

        addr = msg.address
        pri_addr = addr.pri_address
        pub_addr = addr.pub_address

        if pri_addr.vm is not None and node.store.has_object(pri_addr.vm):
            return node.store.get_object(pri_addr.vm).send_signed_msg_with_reply(
                msg=msg
            )

        if pri_addr.device is not None and node.store.has_object(pri_addr.device):
            return node.store.get_object(pri_addr.device).send_signed_msg_with_reply(
                msg=msg
            )

        if pub_addr.domain is not None and node.store.has_object(pub_addr.domain):
            return node.store.get_object(pub_addr.domain).send_signed_msg_with_reply(
                msg=msg
            )

        if pub_addr.network is not None and node.store.has_object(pub_addr.network):
            return node.store.get_object(pub_addr.network).send_signed_msg_with_reply(
                msg=msg
            )

        raise Exception(
            "Address unknown - cannot forward old_message. Throwing it away."
        )

    @staticmethod
    @syft_decorator(typechecking=True)
    def message_handler_types() -> List[type]:
        return [ImmediateSyftMessageWithReply]
