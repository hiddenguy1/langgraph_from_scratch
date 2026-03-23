from __future__ import annotations

from typing import Any, Dict

from bank_marketing_graph.state import GraphState


def llm_router_mock_node(state: GraphState) -> Dict[str, Any]:
    text = state.get("normalized_text", "")
    slots = dict(state.get("slots") or {})
    has_query_signal = any(k in text for k in {"查询", "查", "信息", "财务", "工商", "存量", "情况"})

    # Mock LLM fallback: use softer rules to mimic model correction.
    if "集团" in text and ("公司" in text or "信息" in text):
        return {
            "intent": "query_group_customer",
            "confidence": 0.78,
            "reason": "mock_llm:group_query",
            "next_node": "dispatch",
            "fallback_triggered": True,
            "slots": slots,
        }

    if "公司" in text and ("报告" in text or "一户一策" in text):
        if "短" in text:
            slots["report_type"] = "short"
            slots["workflow_id"] = "workflow-02"
            intent = "generate_report_short"
        elif "长" in text:
            slots["report_type"] = "long"
            slots["workflow_id"] = "workflow-01"
            intent = "generate_report_long"
        elif "谈资" in text:
            slots["report_type"] = "talking_points"
            slots["workflow_id"] = "workflow-03"
            intent = "generate_report_talking_points"
        else:
            intent = "generate_report_other"

        return {
            "intent": intent,
            "confidence": 0.72,
            "reason": "mock_llm:report_related",
            "next_node": "confirm" if intent == "generate_report_other" else "dispatch",
            "fallback_triggered": True,
            "slots": slots,
        }

    if "图" in text or "趋势" in text:
        return {
            "intent": "generate_chart",
            "confidence": 0.7,
            "reason": "mock_llm:chart_related",
            "next_node": "dispatch",
            "fallback_triggered": True,
            "slots": slots,
        }

    if has_query_signal:
        if slots.get("entity_type") == "group" or "集团" in text:
            intent = "query_group_customer"
            reason = "mock_llm:query_fallback_group"
        elif slots.get("org_name"):
            intent = "query_single_customer"
            reason = "mock_llm:query_fallback_single"
        else:
            intent = "query_external_search"
            reason = "mock_llm:query_fallback_external"
        return {
            "intent": intent,
            "confidence": 0.7,
            "reason": reason,
            "next_node": "dispatch",
            "fallback_triggered": True,
            "slots": slots,
        }

    return {
        "intent": "chitchat_guided",
        "confidence": 0.65,
        "reason": "mock_llm:default_chitchat",
        "next_node": "dispatch",
        "fallback_triggered": True,
        "slots": slots,
    }
