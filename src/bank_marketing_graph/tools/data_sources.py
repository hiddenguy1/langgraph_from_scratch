from __future__ import annotations

from typing import Any, Dict


def query_single_customer(org_name: str) -> Dict[str, Any]:
    if not org_name:
        return {"found": False, "message": "缺少单客名称。"}
    return {
        "found": True,
        "source": ["A04-01", "A04-02", "A04-03"],
        "org_name": org_name,
        "data": {
            "basic_profile": f"{org_name} 基本信息（mock）",
            "industrial_info": "行业分类（mock）",
            "finance": "财务信息（mock，可能为空）",
            "stock_info": "我行存量合作信息（mock）",
        },
    }


def query_group_customer(group_name: str) -> Dict[str, Any]:
    if not group_name:
        return {"found": False, "message": "缺少集团名称。"}
    return {
        "found": True,
        "source": ["A04-04", "A04-05"],
        "org_name": group_name,
        "data": {
            "group_profile": f"{group_name} 集团基本信息（mock）",
            "subsidiary_distribution": "子公司在我行合作分布（mock）",
            "group_stock_info": "集团存量产品与授信信息（mock）",
        },
    }


def external_search(query: str) -> Dict[str, Any]:
    if not query:
        return {"found": False, "source": "web", "message": "查询词为空，无法外网检索。"}
    return {
        "found": False,
        "source": "web",
        "query": query,
        "message": "当前为占位实现：可在此接入联网搜索服务；若仍无结果则返回找不到信息。",
    }
