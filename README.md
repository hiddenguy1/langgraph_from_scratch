# 对公营销意图路由项目交接文档

## 1. 项目目标（当前共识）

基于 LangGraph 搭建一个对公营销助手的意图路由中枢，第一阶段重点覆盖：

- 数据查询（单客/集团）
- 报告生成（长报告/短报告/谈资报告/其他 workflow）
- 图表生成（A100-01）
- 闲聊引导（可闲聊，但持续引导到业务任务）
- 未知意图澄清（避免乱猜）

同时明确要求：简单对话（如“你好”“你是谁”）要走快通道，不进入重推理流程。

---

## 2. 已完成实现（代码已落地）

### 2.1 目录结构

- `src/bank_marketing_graph/state.py`
- `src/bank_marketing_graph/graph.py`
- `src/bank_marketing_graph/nodes/normalize.py`
- `src/bank_marketing_graph/nodes/light_smalltalk_gate.py`
- `src/bank_marketing_graph/nodes/rule_router.py`
- `src/bank_marketing_graph/nodes/llm_router_mock.py`
- `src/bank_marketing_graph/nodes/confirm.py`
- `src/bank_marketing_graph/nodes/dispatch.py`
- `src/bank_marketing_graph/tools/data_sources.py`
- `src/bank_marketing_graph/tools/workflows.py`
- `src/bank_marketing_graph/tools/chart_tool.py`
- `scripts/chat_demo.py`
- `tests/test_smalltalk_fastpath.py`
- `tests/test_intent_routing.py`
- `tests/test_report_confirmation.py`

### 2.2 当前图流程

`normalize -> light_smalltalk_gate -> rule_router -> (llm_router_mock/confirm/dispatch) -> END`

核心设计：

- fast path：轻问候、身份、感谢、再见直接返回
- hybrid 路由：规则优先，低置信/不确定走 mock LLM
- confirm：报告类型不明确时先追问
- dispatch：统一调用查询/报告/图表工具占位

### 2.3 当前意图集合（10类）

- `query_single_customer`
- `query_group_customer`
- `query_external_search`
- `generate_report_long`
- `generate_report_short`
- `generate_report_talking_points`
- `generate_report_other`
- `generate_chart`
- `chitchat_guided`
- `unknown_or_clarify`

---

## 3. 对话中确认过的关键业务信息

### 3.1 数据查询能力边界

- 单客相关：`A04-01`~`A04-03`
- 集团相关：`A04-04`~`A04-05`
- 库内无结果时：外网兜底
- 再无结果：明确返回“找不到信息”

### 3.2 报告工作流

- `workflow-01`：一户一策长报告
- `workflow-02`：一户一策短报告
- `workflow-03`：一户一策谈资报告
- 后续将扩展 `workflow-04`、`workflow-05` ...

约束：用户说“生成报告”但没说类型，必须先确认类型再执行。

### 3.3 图表能力

- 调用 `A100-01` 图表助手
- 输出支持 ECharts / AntV Infographic 渲染
- 当前设计中：短报告、谈资报告可自动补图表

---

## 4. 已发现并修复的问题

### 4.1 运行命令问题（Windows）

- `python3` 在当前 Windows 环境下不可用
- 文件名误输为 `chatdemo.py`，实际是 `chat_demo.py`

建议运行方式（项目根目录）：

```powershell
conda activate langchain_basic
$env:PYTHONPATH=".\src"
python .\scripts\chat_demo.py
```

### 4.2 意图误判问题

问题现象：`帮我查询一下腾讯的财务信息` 被误判为闲聊。

已修复点：

- 放宽轻问候匹配（支持“你好啊”等口语）
- 增强企业名抽取（支持“腾讯”这类无后缀简称）
- LLM fallback 遇到查询信号优先走查询，不默认闲聊

---

## 5. 当前验证状态

- 测试通过：`8 passed`
- 已覆盖：
  - fast path 命中
  - 单客/集团查询路由
  - 报告确认逻辑
  - 查询简称不落入闲聊

运行测试：

```powershell
conda activate langchain_basic
cd D:\pingan\projects\langgraph_from_scratch
$env:PYTHONPATH=".\src"
python -m pytest -q
```

---

## 6. 后续可继续做什么（按优先级）

### P0（建议先做）

1. 接入真实工具 API（替换 mock）  
   - A04-01~A04-05 真实查询  
   - workflow-01/02/03 真实调用  
   - A100-01 真实图表生成
2. 增加错误处理与重试策略  
   - 网络超时、接口限流、空结果、参数缺失
3. 增加会话记忆策略  
   - 最近企业名、最近报告类型、最近图表主题复用

### P1（效果提升）

1. 加 Embedding 路由层（规则 -> embedding -> LLM -> confirm）  
2. 建立意图样本库与阈值调优  
3. 打通日志观测（命中率、fallback率、澄清率）

### P2（进阶）

1. 训练 BERT 意图分类器（10类）  
2. 引入简称归一化（“腾讯” -> 多候选企业并二次确认）  
3. 增加自动评测集（离线回放+混淆矩阵）

---

## 7. 下一台电脑继续开发时建议步骤

1. 拉取项目代码
2. 创建并激活 Conda 环境 `langchain_basic`
3. 安装依赖（推荐）

```powershell
pip install -e .
pip install pytest
```

4. 运行测试确保一致性
5. 运行 `scripts/chat_demo.py` 做对话验证
6. 再开始替换 mock 工具为真实接口

---

## 8. 备注

- 当前版本是“可运行、可扩展”的 V1 骨架，重点在路由与编排而非真实数据连接。
- 若后续接入生产，建议优先补全：鉴权、审计日志、敏感信息脱敏、异常告警。
