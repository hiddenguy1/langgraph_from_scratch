from __future__ import annotations

import re
from typing import Any, Dict

from bank_marketing_graph.state import GraphState


_ORG_SUFFIX = r"(?:公司|集团|股份有限公司|有限责任公司)"
_NOISE_TOKENS = {
    "一下",
    "一下子",
    "一下下",
    "帮我",
    "请",
    "请问",
    "一下哈",
    "一下呢",
}


def _extract_org_name(text: str) -> str | None:
    match = re.search(rf"([\u4e00-\u9fa5A-Za-z0-9\-]{{2,40}}{_ORG_SUFFIX})", text)
    if match:
        return match.group(1)

    # Fallback for short organization aliases like "腾讯" without explicit suffix.
    patterns = [
        r"(?:查询|查|看看|了解|分析|帮我查|帮我查询|查询一下|查一下)([\u4e00-\u9fa5A-Za-z0-9\-]{2,20})(?:的|财务|信息|情况|数据)?",
        r"(?:关于|针对)([\u4e00-\u9fa5A-Za-z0-9\-]{2,20})(?:的|财务|信息|情况|数据)?",
    ]
    for pattern in patterns:
        short_match = re.search(pattern, text)
        if short_match:
            candidate = short_match.group(1).strip("，。！？,.!?:： ")
            if candidate and candidate not in _NOISE_TOKENS:
                return candidate

    return None


def normalize_node(state: GraphState) -> Dict[str, Any]:
    raw = (state.get("user_text") or "").strip()
    normalized = re.sub(r"\s+", "", raw).lower()
    org_name = _extract_org_name(raw)

    slots = dict(state.get("slots") or {})
    if org_name:
        slots["org_name"] = org_name
        slots["entity_type"] = "group" if "集团" in org_name else "single"

    context = dict(state.get("context_memory") or {})
    if org_name:
        context["last_org_name"] = org_name

    return {
        "normalized_text": normalized,
        "slots": slots,
        "context_memory": context,
        "route_policy": "hybrid_rule_first",
        "retry_count": state.get("retry_count", 0),
        "tool_trace": list(state.get("tool_trace") or []),
    }
