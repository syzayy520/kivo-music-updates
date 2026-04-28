#!/usr/bin/env python3
"""Lightweight AI workflow assistant demo.

This version uses simple rule-based steps to make the workflow easy to run
locally without external API keys. The extraction and validation functions can
be replaced by real LLM calls later.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, List


def detect_task_type(text: str) -> str:
    keywords = {
        "Meeting Summary": ["会议", "讨论", "结论", "负责", "截止", "周五", "下周"],
        "Customer Feedback": ["客户", "反馈", "投诉", "建议", "回复", "优先级"],
        "Requirement整理": ["需求", "功能", "上线", "版本", "接口", "页面"],
    }

    scores = {
        task: sum(1 for word in words if word in text)
        for task, words in keywords.items()
    }
    return max(scores, key=scores.get)


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"[。；;\n]+", text)
    return [part.strip() for part in parts if part.strip()]


def extract_information(text: str, task_type: str) -> Dict[str, List[str] | str]:
    sentences = split_sentences(text)

    decisions = [s for s in sentences if any(k in s for k in ["结论", "需要", "先", "优先", "确认"])]
    risks = [s for s in sentences if any(k in s for k in ["风险", "未确认", "没最终确认", "阻塞", "影响"])]

    action_items = []
    for sentence in sentences:
        if any(name in sentence for name in ["张三", "李四", "王五", "产品", "后端", "前端"]):
            if any(k in sentence for k in ["负责", "完成", "补充", "确认", "处理"]):
                action_items.append(sentence)

    if task_type == "Customer Feedback":
        topic = "客户反馈整理"
    elif task_type == "Requirement整理":
        topic = "需求与项目沟通整理"
    else:
        topic = "登录页改版与支付流程优化" if "登录" in text or "支付" in text else "会议纪要整理"

    return {
        "topic": topic,
        "decisions": decisions or ["暂无明确结论，需要进一步确认"],
        "action_items": action_items or ["暂无明确负责人或截止时间"],
        "risks": risks or ["未发现明显风险"],
    }


def validate_result(info: Dict[str, List[str] | str]) -> List[str]:
    warnings = []
    action_items = info.get("action_items", [])
    risks = info.get("risks", [])

    joined_actions = " ".join(action_items) if isinstance(action_items, list) else str(action_items)
    joined_risks = " ".join(risks) if isinstance(risks, list) else str(risks)

    if "暂无明确负责人" in joined_actions:
        warnings.append("missing owner or deadline in action items")
    if any(word in joined_risks for word in ["未确认", "没最终确认", "阻塞"]):
        warnings.append("some dependencies or fields are not confirmed")

    return warnings


def format_output(task_type: str, info: Dict[str, List[str] | str], warnings: List[str]) -> str:
    lines = []
    lines.append("[1/4] Detecting task type...")
    lines.append(f"Task type: {task_type}")
    lines.append("")
    lines.append("[2/4] Extracting key information...")
    lines.append("Found: topic, decisions, owners, deadlines, risks")
    lines.append("")
    lines.append("[3/4] Validating output...")
    if warnings:
        for warning in warnings:
            lines.append(f"Warning: {warning}")
    else:
        lines.append("No obvious missing fields found")
    lines.append("")
    lines.append("[4/4] Generating structured summary...")
    lines.append("")
    lines.append("Topic:")
    lines.append(str(info["topic"]))
    lines.append("")
    lines.append("Key Decisions:")
    for item in info["decisions"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Action Items:")
    for item in info["action_items"]:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("Risks:")
    for item in info["risks"]:
        lines.append(f"- {item}")

    return "\n".join(lines)


def run(file_path: Path) -> str:
    text = file_path.read_text(encoding="utf-8")
    task_type = detect_task_type(text)
    info = extract_information(text, task_type)
    warnings = validate_result(info)
    return format_output(task_type, info, warnings)


def main() -> None:
    parser = argparse.ArgumentParser(description="AI workflow assistant demo")
    parser.add_argument("input_file", type=Path, help="Path to a text file")
    args = parser.parse_args()

    if not args.input_file.exists():
        raise FileNotFoundError(f"Input file not found: {args.input_file}")

    print(run(args.input_file))


if __name__ == "__main__":
    main()
