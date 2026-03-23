from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from bank_marketing_graph.nodes.confirm import confirm_node
from bank_marketing_graph.nodes.dispatch import dispatch_node
from bank_marketing_graph.nodes.light_smalltalk_gate import light_smalltalk_gate_node
from bank_marketing_graph.nodes.llm_router_mock import llm_router_mock_node
from bank_marketing_graph.nodes.normalize import normalize_node
from bank_marketing_graph.nodes.rule_router import rule_router_node
from bank_marketing_graph.state import GraphState


def _route_after_smalltalk(state: GraphState) -> str:
    return "end" if state.get("next_node") == "end_fastpath" else "rule_router"


def _route_after_rule(state: GraphState) -> str:
    next_node = state.get("next_node")
    if next_node == "llm_router_mock":
        return "llm_router_mock"
    if next_node == "confirm":
        return "confirm"
    return "dispatch"


def _route_after_llm(state: GraphState) -> str:
    return "confirm" if state.get("next_node") == "confirm" else "dispatch"


def _route_after_confirm(state: GraphState) -> str:
    return "end" if state.get("next_node") == "end_confirm" else "dispatch"


def build_graph():
    graph = StateGraph(GraphState)

    graph.add_node("normalize", normalize_node)
    graph.add_node("light_smalltalk_gate", light_smalltalk_gate_node)
    graph.add_node("rule_router", rule_router_node)
    graph.add_node("llm_router_mock", llm_router_mock_node)
    graph.add_node("confirm", confirm_node)
    graph.add_node("dispatch", dispatch_node)

    graph.add_edge(START, "normalize")
    graph.add_edge("normalize", "light_smalltalk_gate")

    graph.add_conditional_edges(
        "light_smalltalk_gate",
        _route_after_smalltalk,
        {
            "rule_router": "rule_router",
            "end": END,
        },
    )
    graph.add_conditional_edges(
        "rule_router",
        _route_after_rule,
        {
            "llm_router_mock": "llm_router_mock",
            "confirm": "confirm",
            "dispatch": "dispatch",
        },
    )
    graph.add_conditional_edges(
        "llm_router_mock",
        _route_after_llm,
        {
            "confirm": "confirm",
            "dispatch": "dispatch",
        },
    )
    graph.add_conditional_edges(
        "confirm",
        _route_after_confirm,
        {
            "dispatch": "dispatch",
            "end": END,
        },
    )
    graph.add_edge("dispatch", END)

    return graph.compile()
