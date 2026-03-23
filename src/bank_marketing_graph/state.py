from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


IntentType = Literal[
    "query_single_customer",
    "query_group_customer",
    "query_external_search",
    "generate_report_long",
    "generate_report_short",
    "generate_report_talking_points",
    "generate_report_other",
    "generate_chart",
    "chitchat_guided",
    "unknown_or_clarify",
]


class GraphState(TypedDict, total=False):
    user_text: str
    normalized_text: str
    intent: IntentType
    confidence: float
    reason: str
    slots: Dict[str, Any]
    next_node: str
    route_policy: str
    fallback_triggered: bool
    retry_count: int
    error_type: Optional[str]
    clarify_question: Optional[str]
    context_memory: Dict[str, Any]
    tool_trace: List[str]
    tool_result: Dict[str, Any]
    final_answer: str
