from __future__ import annotations

import re
from typing import Any, Dict

from bank_marketing_graph.state import GraphState


def _contains_any(text: str, keywords: set[str]) -> bool:
    return any(word in text for word in keywords)


def rule_router_node(state: GraphState) -> Dict[str, Any]:
    text = state.get("normalized_text", "")
    slots = dict(state.get("slots") or {})

    query_kw = {"查询", "查", "看看", "信息", "工商", "财务", "存量"}
    chart_kw = {"图表", "图", "趋势", "echarts", "antv"}
    report_kw = {"报告", "一户一策", "workflow"}

    if _contains_any(text, chart_kw):
        return {
            "intent": "generate_chart",
            "confidence": 0.9,
            "reason": "rule:chart_keyword",
            "next_node": "dispatch",
            "slots": slots,
            "fallback_triggered": False,
        }

    if _contains_any(text, report_kw):
        if "长报告" in text or "workflow-01" in text:
            slots["report_type"] = "long"
            slots["workflow_id"] = "workflow-01"
            intent = "generate_report_long"
            next_node = "dispatch"
            confidence = 0.95
            reason = "rule:long_report"
        elif "短报告" in text or "workflow-02" in text:
            slots["report_type"] = "short"
            slots["workflow_id"] = "workflow-02"
            intent = "generate_report_short"
            next_node = "dispatch"
            confidence = 0.95
            reason = "rule:short_report"
        elif "谈资" in text or "workflow-03" in text:
            slots["report_type"] = "talking_points"
            slots["workflow_id"] = "workflow-03"
            intent = "generate_report_talking_points"
            next_node = "dispatch"
            confidence = 0.95
            reason = "rule:talking_points_report"
        else:
            custom_match = re.search(r"workflow-(\d+)", text)
            if custom_match:
                slots["report_type"] = "other"
                slots["workflow_id"] = f"workflow-{custom_match.group(1)}"
                intent = "generate_report_other"
                next_node = "dispatch"
                confidence = 0.9
                reason = "rule:custom_workflow_report"
            else:
                intent = "generate_report_other"
                next_node = "confirm"
                confidence = 0.75
                reason = "rule:report_needs_confirmation"

        return {
            "intent": intent,
            "confidence": confidence,
            "reason": reason,
            "next_node": next_node,
            "slots": slots,
            "fallback_triggered": False,
        }

    if _contains_any(text, query_kw):
        entity_type = slots.get("entity_type")
        if "集团" in text or entity_type == "group":
            return {
                "intent": "query_group_customer",
                "confidence": 0.92,
                "reason": "rule:group_query",
                "next_node": "dispatch",
                "slots": slots,
                "fallback_triggered": False,
            }
        if "公司" in text or "单客" in text or entity_type == "single":
            return {
                "intent": "query_single_customer",
                "confidence": 0.92,
                "reason": "rule:single_query",
                "next_node": "dispatch",
                "slots": slots,
                "fallback_triggered": False,
            }
        return {
            "intent": "query_external_search",
            "confidence": 0.6,
            "reason": "rule:query_but_no_entity",
            "next_node": "llm_router_mock",
            "slots": slots,
            "fallback_triggered": False,
        }

    if not text:
        return {
            "intent": "unknown_or_clarify",
            "confidence": 0.2,
            "reason": "rule:empty_input",
            "next_node": "confirm",
            "slots": slots,
            "fallback_triggered": False,
        }

    return {
        "intent": "unknown_or_clarify",
        "confidence": 0.45,
        "reason": "rule:low_confidence_fallback",
        "next_node": "llm_router_mock",
        "slots": slots,
        "fallback_triggered": False,
    }
