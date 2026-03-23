from __future__ import annotations

from typing import Any, Dict

from bank_marketing_graph.state import GraphState


def confirm_node(state: GraphState) -> Dict[str, Any]:
    intent = state.get("intent", "unknown_or_clarify")
    slots = dict(state.get("slots") or {})

    if intent == "generate_report_other" and not slots.get("report_type"):
        return {
            "clarify_question": "你希望生成哪类报告？可选：一户一策长报告、短报告、谈资报告，或指定 workflow-xx。",
            "final_answer": "在生成前我需要先确认报告类型：长报告 / 短报告 / 谈资报告 / workflow-xx。",
            "next_node": "end_confirm",
            "reason": "confirm:missing_report_type",
        }

    if intent == "unknown_or_clarify":
        return {
            "clarify_question": "请告诉我你的目标：查询企业信息、生成报告，还是生成图表？",
            "final_answer": "我可以帮你做三类任务：查询企业信息、生成报告、生成图表。你可以直接说“查询XX公司”开始。",
            "next_node": "end_confirm",
            "reason": "confirm:unknown_intent",
        }

    return {"next_node": "dispatch"}
