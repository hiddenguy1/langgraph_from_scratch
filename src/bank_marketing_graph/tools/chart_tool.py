from __future__ import annotations

from typing import Any, Dict


def generate_chart_with_a10001(subject: str, chart_type: str = "line", renderer: str = "echarts") -> Dict[str, Any]:
    return {
        "ok": True,
        "tool_id": "A100-01",
        "renderer": renderer,
        "chart_type": chart_type,
        "subject": subject or "未指定主题",
        "payload": {
            "title": f"{subject or '企业'}趋势图（mock）",
            "xAxis": ["Q1", "Q2", "Q3", "Q4"],
            "series": [12, 16, 19, 25],
        },
        "message": "已生成可渲染图表配置（mock）。",
    }
