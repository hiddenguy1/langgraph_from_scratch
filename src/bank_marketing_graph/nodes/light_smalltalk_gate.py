from __future__ import annotations

from typing import Any, Dict

from bank_marketing_graph.state import GraphState


_GREETING = {"你好", "您好", "hi", "hello", "嗨"}
_IDENTITY = {"你是谁", "你是干嘛的", "你能做什么", "你会什么"}
_THANKS = {"谢谢", "感谢", "thanks", "thx"}
_BYE = {"再见", "拜拜", "bye"}
_TASK_HINT_KEYWORDS = {
    "公司",
    "集团",
    "查询",
    "报告",
    "图表",
    "workflow",
    "单客",
    "谈资",
    "短报告",
    "长报告",
}


def _match_smalltalk(text: str) -> str | None:
    if text in _GREETING or text.startswith(("你好", "您好", "嗨", "hi", "hello")):
        return "greeting"
    if text in _IDENTITY or "你是谁" in text or "你能做什么" in text:
        return "identity"
    if text in _THANKS or "谢谢" in text or "感谢" in text:
        return "thanks"
    if text in _BYE or text.startswith(("再见", "拜拜", "bye")):
        return "bye"
    return None


def light_smalltalk_gate_node(state: GraphState) -> Dict[str, Any]:
    normalized = state.get("normalized_text", "")
    has_task_signal = any(k in normalized for k in _TASK_HINT_KEYWORDS)
    smalltalk_type = _match_smalltalk(normalized)

    if smalltalk_type and not has_task_signal:
        if smalltalk_type == "identity":
            answer = "我是对公营销助手，可以帮你查企业信息、生成一户一策报告、产出图表。你可以先说“查询XX公司”。"
        elif smalltalk_type == "thanks":
            answer = "不客气。你可以告诉我企业名称，我先帮你查单客或集团信息。"
        elif smalltalk_type == "bye":
            answer = "好的，随时找我。下次你可以直接说“生成某公司短报告”。"
        else:
            answer = "你好，我可以帮你做对公营销相关的数据查询、报告生成和图表生成。你可以先输入一个公司名。"

        return {
            "intent": "chitchat_guided",
            "confidence": 0.99,
            "reason": "smalltalk_fastpath",
            "next_node": "end_fastpath",
            "fallback_triggered": False,
            "final_answer": answer,
        }

    return {
        "next_node": "rule_router",
    }
