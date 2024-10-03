from typing import Optional
from synapse.api.node_pb2 import NodeConfig, NodeType
from synapse.api.nodes.electrical_broadband_pb2 import ElectricalBroadbandConfig
from synapse.client.channel import Channel
from synapse.client.node import Node


class ElectricalBroadband(Node):
    type = NodeType.kElectricalBroadband

    def __init__(
        self,
        peripheral_id,
        channels,
        bit_width,
        sample_rate,
        gain,
        low_cutoff_hz,
        high_cutoff_hz
    ):
        self.peripheral_id = peripheral_id
        self.channels = channels
        self.bit_width = bit_width
        self.sample_rate = sample_rate
        self.gain = gain
        self.low_cutoff_hz = low_cutoff_hz
        self.high_cutoff_hz = high_cutoff_hz    

    def _to_proto(self):
        channels = [c.to_proto() for c in self.channels]
        n = NodeConfig()
        p = ElectricalBroadbandConfig(
            peripheral_id=self.peripheral_id,
            channels=channels,
            bit_width=self.bit_width,
            sample_rate=self.sample_rate,
            gain=self.gain,
            low_cutoff_hz=self.low_cutoff_hz,
            high_cutoff_hz=self.high_cutoff_hz,
        )
        n.electrical_broadband.CopyFrom(p)
        return n

    @staticmethod
    def _from_proto(proto: Optional[ElectricalBroadbandConfig]):
        if not proto:
            raise ValueError("parameter 'proto' is missing")
        if not isinstance(proto, ElectricalBroadbandConfig):
            raise ValueError("proto is not of type ElectricalBroadbandConfig")

        channels = [Channel.from_proto(c) for c in proto.channels]
        return ElectricalBroadband(
            peripheral_id=proto.peripheral_id,
            channels=channels,
            bit_width=proto.bit_width,
            sample_rate=proto.sample_rate,
            gain=proto.gain,
            low_cutoff_hz=proto.low_cutoff_hz,
            high_cutoff_hz=proto.high_cutoff_hz,
        )
