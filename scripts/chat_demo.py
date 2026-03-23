from __future__ import annotations

from bank_marketing_graph.graph import build_graph


def main() -> None:
    app = build_graph()
    memory = {}

    print("对公营销助手（输入 quit 退出）")
    while True:
        user_text = input("\n你: ").strip()
        if user_text.lower() in {"quit", "exit"}:
            print("助手: 再见。")
            break

        result = app.invoke(
            {
                "user_text": user_text,
                "context_memory": memory,
            }
        )
        memory = result.get("context_memory", memory)
        print(f"助手: {result.get('final_answer', '收到。')}")
        print(
            "meta:",
            {
                "intent": result.get("intent"),
                "confidence": result.get("confidence"),
                "next_node": result.get("next_node"),
                "tool_trace": result.get("tool_trace"),
            },
        )


if __name__ == "__main__":
    main()
