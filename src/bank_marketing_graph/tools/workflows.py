from __future__ import annotations

from typing import Any, Dict


_REPORT_WORKFLOW_MAP = {
    "long": "workflow-01",
    "short": "workflow-02",
    "talking_points": "workflow-03",
}


def run_report_workflow(report_type: str | None, workflow_id: str | None, org_name: str | None) -> Dict[str, Any]:
    resolved_workflow = workflow_id or _REPORT_WORKFLOW_MAP.get(report_type or "")
    if not resolved_workflow:
        return {
            "ok": False,
            "message": "无法确定报告工作流，请先确认报告类型或指定 workflow-xx。",
        }

    return {
        "ok": True,
        "workflow_id": resolved_workflow,
        "report_type": report_type or "other",
        "org_name": org_name,
        "report_id": f"mock-{resolved_workflow}-{(org_name or 'unknown')}",
        "message": f"已调用 {resolved_workflow} 生成报告（mock）。",
    }
