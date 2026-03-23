from bank_marketing_graph.graph import build_graph


def test_report_without_type_triggers_confirmation():
    app = build_graph()
    result = app.invoke({"user_text": "给我生成一个一户一策报告"})

    assert result["intent"] == "generate_report_other"
    assert result["next_node"] == "end_confirm"
    assert "确认报告类型" in result["final_answer"]


def test_report_short_runs_workflow_and_chart():
    app = build_graph()
    result = app.invoke({"user_text": "帮我生成平安科技公司短报告"})

    assert result["intent"] == "generate_report_short"
    assert "workflow-02" in result.get("tool_trace", [])
    assert "A100-01" in result.get("tool_trace", [])
