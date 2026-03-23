from bank_marketing_graph.graph import build_graph


def test_route_single_customer_query():
    app = build_graph()
    result = app.invoke({"user_text": "查询平安科技公司的基本信息"})
    assert result["intent"] == "query_single_customer"
    assert "A04-01" in "/".join(result.get("tool_trace", []))


def test_route_group_customer_query():
    app = build_graph()
    result = app.invoke({"user_text": "帮我看下平安集团的存量合作信息"})
    assert result["intent"] == "query_group_customer"
    assert "A04-04" in "/".join(result.get("tool_trace", []))


def test_chitchat_guided_fallback():
    app = build_graph()
    result = app.invoke({"user_text": "今天心情一般"})
    assert result["intent"] in {"chitchat_guided", "unknown_or_clarify"}
    assert result.get("final_answer")


def test_query_alias_org_name_should_not_fall_to_chitchat():
    app = build_graph()
    result = app.invoke({"user_text": "帮我查询一下腾讯的财务信息"})
    assert result["intent"] in {"query_single_customer", "query_external_search"}
    assert result["intent"] != "chitchat_guided"
