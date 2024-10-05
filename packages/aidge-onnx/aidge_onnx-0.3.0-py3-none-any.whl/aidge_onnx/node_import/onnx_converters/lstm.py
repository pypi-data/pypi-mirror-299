"""
Copyright (c) 2023 CEA-List

This program and the accompanying materials are made available under the
terms of the Eclipse Public License 2.0 which is available at
http://www.eclipse.org/legal/epl-2.0.

SPDX-License-Identifier: EPL-2.0
"""
from typing import List, Tuple

import aidge_core
import onnx

from aidge_onnx.node_import import auto_register_import

from aidge_core import Log
from aidge_onnx.utils import warn_unsupported_attr

@auto_register_import("lstm")
def import_lstm(onnx_node:onnx.NodeProto, input_nodes:List[Tuple[aidge_core.Node, int]], opset=None) -> aidge_core.Node:
    """
    :param onnx_node: ONNX node to convert
    :type onnx_node: onnx.NodeProto
    :param input_nodes: List of Aidge nodes which constitute the input of the current node
    :type input_nodes: List[aidge_core.Node]
    :param opset: Indicate opset version of the ONNX model, default=None
    :type opset: int, optional
    """
    node_name = onnx_node.name if onnx_node.name else onnx_node.output[0]
    onnx_attrs = {attr.name : attr for attr in onnx_node.attribute}

    if 'direction' in onnx_attrs:
        if onnx_attrs['direction'].s == b'forward':
            del onnx_attrs['direction']
        else:
            warn_unsupported_attr("direction","lstm",opset,onnx_attrs['direction'].s)
            return None

    if 'hidden_size' in onnx_attrs:
        hidden_channels = onnx_attrs['hidden_size'].i
        del onnx_attrs['hidden_size']

    if 'input_forget' in onnx_attrs:
        if onnx_attrs['input_forget'].i == 0:
            del onnx_attrs['input_forget']
        else:
            warn_unsupported_attr("input_forget","lstm",opset,onnx_attrs['input_forget'].i)
            return None

    if len(onnx_attrs) > 0:
        Log.warn(f"Warning: unsupported attribute(s): {onnx_attrs.keys()} for operator 'lstm' with opset {opset}.\nThis node will be filled by a GenericOperator.")
        return None

    #seq_length = input_nodes[0][0].get_operator().get_output(input_nodes[0][1]).dims()[0]
    in_channels = input_nodes[1][0].get_operator().get_output(input_nodes[1][1]).dims()[-1]

    # Current Aidge LSTM meta operator does take separate weights and bias for every FC operator
    # But ONNX LSTM takes a concatenated tensor for input, output, forget and cell state gates
    # We therefore create a new meta operator wrapping Aidge LSTM and Slices operations
    lstm = aidge_core.LSTM(in_channels=in_channels, hidden_channels=hidden_channels, seq_length=0, nobias=False, name=node_name)

    # Add a Pop operator at the input to make scheduling work
    pop = aidge_core.Pop()
    pop.add_child(lstm, 0, 0)

    # Weights slicing
    w = aidge_core.Identity()
    wi_slice = aidge_core.Slice(starts=[0], ends=[1], axes=[0])
    wi_slice.add_child(lstm, 0, 1)
    wo_slice = aidge_core.Slice(starts=[1], ends=[2], axes=[0])
    wo_slice.add_child(lstm, 0, 2)
    wf_slice = aidge_core.Slice(starts=[2], ends=[3], axes=[0])
    wf_slice.add_child(lstm, 0, 3)
    wc_slice = aidge_core.Slice(starts=[3], ends=[4], axes=[0])
    wc_slice.add_child(lstm, 0, 4)
    w.add_child(wi_slice, 0, 0)
    w.add_child(wo_slice, 0, 0)
    w.add_child(wf_slice, 0, 0)
    w.add_child(wc_slice, 0, 0)

    # Recurrent weights slicing
    r = aidge_core.Identity()
    ri_slice = aidge_core.Slice(starts=[0], ends=[1], axes=[0])
    ri_slice.add_child(lstm, 0, 5)
    ro_slice = aidge_core.Slice(starts=[1], ends=[2], axes=[0])
    ro_slice.add_child(lstm, 0, 6)
    rf_slice = aidge_core.Slice(starts=[2], ends=[3], axes=[0])
    rf_slice.add_child(lstm, 0, 7)
    rc_slice = aidge_core.Slice(starts=[3], ends=[4], axes=[0])
    rc_slice.add_child(lstm, 0, 8)
    r.add_child(ri_slice, 0, 0)
    r.add_child(ro_slice, 0, 0)
    r.add_child(rf_slice, 0, 0)
    r.add_child(rc_slice, 0, 0)

    # Bias slicing
    b = aidge_core.Identity()
    bwi_slice = aidge_core.Slice(starts=[0], ends=[1], axes=[0])
    bwi_slice.add_child(lstm, 0, 9)
    bwo_slice = aidge_core.Slice(starts=[1], ends=[2], axes=[0])
    bwo_slice.add_child(lstm, 0, 10)
    bwf_slice = aidge_core.Slice(starts=[2], ends=[3], axes=[0])
    bwf_slice.add_child(lstm, 0, 11)
    bwc_slice = aidge_core.Slice(starts=[3], ends=[4], axes=[0])
    bwc_slice.add_child(lstm, 0, 12)
    bri_slice = aidge_core.Slice(starts=[4], ends=[5], axes=[0])
    bri_slice.add_child(lstm, 0, 13)
    bro_slice = aidge_core.Slice(starts=[5], ends=[6], axes=[0])
    bro_slice.add_child(lstm, 0, 14)
    brf_slice = aidge_core.Slice(starts=[6], ends=[7], axes=[0])
    brf_slice.add_child(lstm, 0, 15)
    brc_slice = aidge_core.Slice(starts=[7], ends=[8], axes=[0])
    brc_slice.add_child(lstm, 0, 16)
    b.add_child(bwi_slice, 0, 0)
    b.add_child(bwo_slice, 0, 0)
    b.add_child(bwf_slice, 0, 0)
    b.add_child(bwc_slice, 0, 0)
    b.add_child(bri_slice, 0, 0)
    b.add_child(bro_slice, 0, 0)
    b.add_child(brf_slice, 0, 0)
    b.add_child(brc_slice, 0, 0)

    # Create the graph for the ONNX LSTM meta operator with correct input/output ordering
    graph = aidge_core.get_connected_graph_view(lstm)
    graph.set_ordered_inputs([[pop, 0], [w, 0], [r, 0], [b, 0], [None, 0], [lstm, 17], [lstm, 18]])
    graph.set_ordered_outputs([[None, 0], [lstm, 0], [lstm, 1]])

    my_node = aidge_core.meta_operator("LSTM_ONNX", graph, name=node_name)
    Log.notice(f"- {node_name} ({onnx_node.op_type})")
    return my_node
