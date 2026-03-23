from bank_marketing_graph.graph import build_graph


def test_smalltalk_hello_uses_fastpath():
    app = build_graph()
    result = app.invoke({"user_text": "你好"})

    assert result["intent"] == "chitchat_guided"
    assert result["reason"] == "smalltalk_fastpath"
    assert result["next_node"] == "end_fastpath"
    assert "查询" in result["final_answer"] or "公司" in result["final_answer"]


def test_smalltalk_variant_hello_uses_fastpath():
    app = build_graph()
    result = app.invoke({"user_text": "你好啊"})

    assert result["intent"] == "chitchat_guided"
    assert result["reason"] == "smalltalk_fastpath"
    assert result["next_node"] == "end_fastpath"
