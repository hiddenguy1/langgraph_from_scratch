from __future__ import annotations

from typing import Any, Dict

from bank_marketing_graph.state import GraphState
from bank_marketing_graph.tools.chart_tool import generate_chart_with_a10001
from bank_marketing_graph.tools.data_sources import external_search, query_group_customer, query_single_customer
from bank_marketing_graph.tools.workflows import run_report_workflow


def _build_guidance() -> str:
    return "你还可以继续说：查询某集团信息，或生成该企业短报告。"


def dispatch_node(state: GraphState) -> Dict[str, Any]:
    intent = state.get("intent", "unknown_or_clarify")
    slots = dict(state.get("slots") or {})
    org_name = slots.get("org_name") or state.get("context_memory", {}).get("last_org_name")
    tool_trace = list(state.get("tool_trace") or [])

    if intent == "query_single_customer":
        result = query_single_customer(org_name or "")
        tool_trace.append("A04-01/A04-02/A04-03")
        if result.get("found"):
            answer = f"已查询单客 {result['org_name']}：已返回基础、财务和存量信息（mock）。"
        else:
            fallback = external_search(state.get("user_text", ""))
            tool_trace.append("web_fallback")
            answer = f"库内未命中，已尝试外网兜底：{fallback.get('message')}"
            result = fallback
        return {"tool_result": result, "tool_trace": tool_trace, "final_answer": f"{answer} {_build_guidance()}"}

    if intent == "query_group_customer":
        result = query_group_customer(org_name or "")
        tool_trace.append("A04-04/A04-05")
        if result.get("found"):
            answer = f"已查询集团 {result['org_name']}：已返回集团画像、子公司分布与存量信息（mock）。"
        else:
            fallback = external_search(state.get("user_text", ""))
            tool_trace.append("web_fallback")
            answer = f"库内未命中，已尝试外网兜底：{fallback.get('message')}"
            result = fallback
        return {"tool_result": result, "tool_trace": tool_trace, "final_answer": f"{answer} {_build_guidance()}"}

    if intent in {
        "generate_report_long",
        "generate_report_short",
        "generate_report_talking_points",
        "generate_report_other",
    }:
        report_result = run_report_workflow(
            report_type=slots.get("report_type"),
            workflow_id=slots.get("workflow_id"),
            org_name=org_name,
        )
        tool_trace.append(report_result.get("workflow_id", "workflow_unknown"))

        chart_result = None
        if slots.get("report_type") in {"short", "talking_points"}:
            chart_result = generate_chart_with_a10001(subject=org_name or "目标企业")
            tool_trace.append("A100-01")

        answer = report_result.get("message", "报告生成完成。")
        if chart_result:
            answer += " 已自动补充图表配置。"

        merged_result = {"report": report_result, "chart": chart_result}
        return {"tool_result": merged_result, "tool_trace": tool_trace, "final_answer": f"{answer} {_build_guidance()}"}

    if intent == "generate_chart":
        chart = generate_chart_with_a10001(subject=org_name or "目标企业")
        tool_trace.append("A100-01")
        return {
            "tool_result": chart,
            "tool_trace": tool_trace,
            "final_answer": f"{chart.get('message')} 你也可以继续让我基于图表生成短报告。",
        }

    if intent == "chitchat_guided":
        return {
            "final_answer": "我在的。除了闲聊，我还可以直接帮你查企业、生成一户一策报告或图表。你可以先给我一个公司名。",
            "tool_result": {},
            "tool_trace": tool_trace,
        }

    return {
        "final_answer": "我还不确定你的目标。你可以说“查询XX公司”或“生成XX公司短报告”。",
        "tool_result": {},
        "tool_trace": tool_trace,
    }
