#!/usr/bin/env python3
import os
import sys
import base64
import json
from datetime import datetime

def decode_result(encoded):
    if not encoded or encoded in ("null", "undefined", ""):
        return {"score": 0, "max_score": 0}
    try:
        decoded = base64.b64decode(encoded).decode("utf-8")
        return json.loads(decoded)
    except:
        return {"score": 0, "max_score": 0}

def main():
    with open(".github/tasks.json", "r", encoding="utf-8") as f:
        tasks = {t["id"]: t for t in json.load(f)["tasks"]}
    
    task_ids = ["task_01", "task_02"]
    total_score = 0
    max_total = 0
    lines = []
    
    for task_id in task_ids:
        encoded = os.environ.get(f"{task_id.upper()}_RESULT")
        res = decode_result(encoded)
        score = res.get("score", 0)
        max_score = tasks[task_id]["max_score"]
        name = tasks[task_id]["name"]
        total_score += score
        max_total += max_score
        status = "✅" if score == max_score else ("⚠️" if score > 0 else "❌")
        lines.append(f"| **{name}** | {score} | {max_score} | {status} |")
    
    percentage = int(100 * total_score / max_total) if max_total else 0
    report = []
    report.append("## 📊 ИТОГОВЫЙ ОТЧЕТ ПО ВСЕМ ЗАДАНИЯМ")
    report.append("### 📈 Сводная таблица")
    report.append("| Задание | Баллы | Максимум | Статус |")
    report.append("|---------|-------|----------|--------|")
    report.extend(lines)
    report.append(f"| **ВСЕГО** | **{total_score}** | **{max_total}** | **{percentage}%** |")
    report.append("\n### 📁 Найденные файлы:\n")
    for task_id in task_ids:
        f = tasks[task_id]["file"]
        exists = "✅" if os.path.exists(f) else "❌"
        report.append(f"{exists} **{f}** - {'найден' if exists == '✅' else 'не найден'}")
    report.append(f"\n### 🏆 Итоговая оценка: **{total_score} / {max_total}**\n")
    if total_score == max_total:
        report.append("🎉 **ПОЗДРАВЛЯЕМ! Все задачи выполнены на 100%!**")
    else:
        report.append("💡 **Есть что улучшить! Смотри детали тестов.**")
    report.append(f"\n**GitHub Classroom: {total_score}/{max_total} баллов**")
    report.append(f"\n*Автоматическая проверка завершена* • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY", "/dev/stdout")
    with open(summary_file, "w") as f:
        f.write("\n".join(report))

if __name__ == "__main__":
    main()