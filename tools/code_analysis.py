#!/usr/bin/env python3
import subprocess
import os

def analyze_task_file(filename):
    if not os.path.exists(filename):
        return None
    results = {'file': filename, 'exists': True, 'pylint_score': 0, 'flake8_errors': 0, 'ruff_errors': 0, 'syntax_ok': False}
    try:
        subprocess.run(['python3', '-m', 'py_compile', filename], capture_output=True, check=True)
        results['syntax_ok'] = True
    except:
        results['syntax_ok'] = False
    try:
        pylint_result = subprocess.run(['pylint', filename, '--exit-zero', '--score=yes'], capture_output=True, text=True, timeout=10)
        for line in pylint_result.stdout.split('\n'):
            if 'rated at' in line:
                score = line.split('rated at ')[1].split('/')[0]
                results['pylint_score'] = float(score)
                break
    except:
        pass
    try:
        flake8_result = subprocess.run(['flake8', filename], capture_output=True, text=True)
        results['flake8_output'] = flake8_result.stdout
        results['flake8_errors'] = len(flake8_result.stdout.strip().split('\n')) if flake8_result.stdout.strip() else 0
    except:
        pass
    try:
        ruff_result = subprocess.run(['ruff', 'check', filename, '--exit-zero', '--output-format', 'text'], capture_output=True, text=True)
        lines = ruff_result.stdout.split('\n')
        error_count = sum(1 for line in lines if filename in line and ':' in line and len(line.split(':')) >= 4)
        results['ruff_errors'] = error_count
        results['ruff_details'] = [l for l in lines if filename in l][:10]
    except:
        pass
    return results

def analysis():
    task_files = ['task_01.py', 'task_02.py']
    print("## 🔍 ДЕТАЛЬНЫЙ АНАЛИЗ КАЧЕСТВА КОДА")
    print("### Используются линтеры: PyLint, Flake8, Ruff\n")
    print("| Задача | Файл | Синтаксис | PyLint | Flake8 | Ruff | Статус |")
    print("|--------|------|-----------|--------|--------|------|--------|")
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        if result is None:
            print(f"| Задача {i} | `{task_file}` | ❌ | - | - | - | ❌ Не сдано |")
            continue
        status = "❌ Синтаксис" if not result['syntax_ok'] else ("✅ Отлично" if result['pylint_score'] >= 9.0 and result['flake8_errors'] == 0 and result['ruff_errors'] == 0 else ("⚠️ Средне" if result['pylint_score'] >= 7.0 else "❌ Ошибки"))
        print(f"| Задача {i} | `{task_file}` | {'✅' if result['syntax_ok'] else '❌'} | {result['pylint_score']:.1f}/10 | {result['flake8_errors']} | {result['ruff_errors']} | {status} |")
    print("\n---\n")
    for i, task_file in enumerate(task_files, 1):
        result = analyze_task_file(task_file)
        if result is None:
            print(f"### ⚠️ Задача {i}: Файл `{task_file}` не найден\nСтудент еще не сдал эту задачу.\n\n---\n")
            continue
        print(f"### 📄 Задача {i}: Анализ файла **{task_file}**\n")
        if not result['syntax_ok']:
            print("**❌ Синтаксис:** Ошибка в коде\n")
        print(f"**🐍 PyLint:** {result['pylint_score']:.1f}/10\n")
        if result['flake8_errors'] > 0:
            print(f"**❌ Flake8 ошибки ({result['flake8_errors']}):**\n```{result['flake8_output']}```\n")
        else:
            print("**✅ Flake8:** Нет ошибок\n")
        if result['ruff_errors'] > 0:
            print(f"**❌ Ruff ошибки ({result['ruff_errors']}):**\n```")
            for error in result['ruff_details']:
                print(error)
            print("```\n")
        else:
            print("**✅ Ruff:** Нет ошибок\n")
        print("---\n")
    print("### 💡 Рекомендации по улучшению:\n")
    print("1. **Следуйте PEP 8:** 4 пробела для отступов, максимум 79 символов в строке\n")
    print("2. **Исправьте ошибки линтеров** перед отправкой заданий\n")
    print("3. **Проверяйте свой код** на наличие синтаксических ошибок\n")
    print("*Качество кода учитывается при оценке!*")

if __name__ == "__main__":
    analysis()
