# AI Workflow Assistant

A small and reproducible AI workflow assistant demo for organizing meeting notes, customer feedback, and project communication into structured outputs.

This repository is intentionally lightweight. It focuses on a simple agent-style workflow: task detection, information extraction, validation, and structured output.

## Problem

In daily work, a lot of time is spent reading unstructured text and turning it into clear summaries, action items, deadlines, risks, and reply drafts. The task is repetitive and easy to get wrong when important details are hidden in long notes or chat messages.

## Workflow

```text
Raw user input
  ↓
1. Intent Detection
  ↓
2. Information Extraction
  ↓
3. Validation
  ↓
4. Structured Output
```

## Supported Scenarios

- Meeting summary
- Customer feedback analysis
- Project requirement整理

## Quick Start

```bash
python main.py examples/meeting.txt
```

## Example Output

```text
[1/4] Detecting task type...
Task type: Meeting Summary

[2/4] Extracting key information...
Found: topic, decisions, owners, deadlines, risks

[3/4] Validating output...
Warning: backend API fields are not confirmed

[4/4] Generating structured summary...

Meeting Topic:
登录页改版与支付流程优化

Key Decisions:
- 本周优先完成登录页文案修改
- 支付流程需要补充异常提示
- 后端接口字段仍需确认

Action Items:
- 张三：完成登录页文案修改，本周五前
- 李四：补充支付失败提示，下周二前

Risks:
- 后端接口字段尚未最终确认，可能影响前端联调
```

## Project Structure

```text
.
├── README.md
├── main.py
├── requirements.txt
└── examples
    ├── meeting.txt
    └── customer_feedback.txt
```

## Agent-style Design

The demo does not generate the final answer in one step. It breaks the process into smaller stages:

1. Detect what kind of task the input belongs to.
2. Extract task-specific fields.
3. Validate whether important information is missing or risky.
4. Generate a clean structured result.

In a real LLM-based version, the extraction and validation steps can be replaced by model calls, and the output can be connected to tools such as spreadsheets, Notion, Feishu, or project management software.

## Roadmap

- Add LLM API integration
- Support Markdown and CSV export
- Add task sync to external tools
- Improve multi-turn context handling
- Add more detailed feedback classification
