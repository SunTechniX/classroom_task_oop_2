#!/usr/bin/env python3
import json
import subprocess
import sys
import os
import ast
import base64

def run_test(command, input_str, expected, method, timeout=5):
    try:
        proc = subprocess.run(
            command,
            input=input_str,
            text=True,
            capture_output=True,
            timeout=timeout,
            shell=True
        )
        actual = proc.stdout.strip()
        stderr = proc.stderr
        if method == "exact":
            passed = actual == expected
        elif method == "contains":
            passed = expected in actual
        else:
            passed = False
        score = 1 if passed else 0
        output = actual
        if stderr and not passed:
            output += f"\nSTDERR: {stderr}"
        return {
            "name": "",
            "status": "pass" if passed else "fail",
            "score": score,
            "max_score": 1,
            "output": output
        }
    except subprocess.TimeoutExpired:
        return {"name": "", "status": "fail", "score": 0, "max_score": 1, "output": f"Timeout >{timeout}s"}
    except Exception as e:
        return {"name": "", "status": "fail", "score": 0, "max_score": 1, "output": f"Error: {e}"}

# === AST АНАЛИЗ ===
def check_task_01_structure(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return False, "Синтаксическая ошибка"
    
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    funcs = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef)}
    
    errors = []
    if 'Notifier' not in classes:
        errors.append("Нет класса Notifier")
    else:
        methods = [m.name for m in classes['Notifier'].body if isinstance(m, ast.FunctionDef)]
        if 'send' not in methods:
            errors.append("Нет send в Notifier")
    
    for cls in ['EmailNotifier', 'SMSNotifier', 'PushNotifier']:
        if cls not in classes:
            errors.append(f"Нет {cls}")
    
    if 'notify_all' not in funcs:
        errors.append("Нет функции notify_all")
    
    return len(errors) == 0, "; ".join(errors) if errors else "OK"

def check_task_02_structure(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
    except:
        return False, "Синтаксическая ошибка"
    
    classes = {n.name: n for n in tree.body if isinstance(n, ast.ClassDef)}
    errors = []
    
    if 'Animal' not in classes:
        errors.append("Нет Animal")
    else:
        methods = [m.name for m in classes['Animal'].body if isinstance(m, ast.FunctionDef)]
        if '__init__' not in methods:
            errors.append("Нет __init__ в Animal")
        if 'speak' not in methods:
            errors.append("Нет speak в Animal")
        if 'about_me' not in methods:
            errors.append("Нет about_me в Animal")
    
    for cls in ['Dog', 'Cat']:
        if cls not in classes:
            errors.append(f"Нет {cls}")
        else:
            node = classes[cls]
            methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
            if '__init__' in methods or 'about_me' in methods:
                errors.append(f"В {cls} не должно быть __init__/about_me")
            if 'speak' not in methods:
                errors.append(f"Нет speak в {cls}")
    
    return len(errors) == 0, "; ".join(errors) if errors else "OK"

def main():
    if len(sys.argv) != 2:
        print("Usage: run_task_tests.py <task_id>")
        sys.exit(1)
    
    task_id = sys.argv[1]
    with open(".github/tasks.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    task = next((t for t in config["tasks"] if t["id"] == task_id), None)
    if not task:
        print(f"Task {task_id} not found")
        sys.exit(1)
    
    file_path = task["file"]
    max_score = task["max_score"]
    test_results = []
    
    if not os.path.exists(file_path):
        for test in task["tests"]:
            test_results.append({
                "name": test["name"],
                "status": "fail",
                "score": 0,
                "max_score": test["max_score"],
                "output": "Файл не найден"
            })
    else:
        # Проверка синтаксиса
        try:
            subprocess.run([sys.executable, "-m", "py_compile", file_path], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            for test in task["tests"]:
                test_results.append({
                    "name": test["name"],
                    "status": "fail",
                    "score": 0,
                    "max_score": test["max_score"],
                    "output": f"SyntaxError\n{e.stderr.decode()}"
                })
        else:
            # AST-анализ
            if task_id == "task_01":
                ast_ok, ast_msg = check_task_01_structure(file_path)
            elif task_id == "task_02":
                ast_ok, ast_msg = check_task_02_structure(file_path)
            else:
                ast_ok = True
            
            if not ast_ok:
                for test in task["tests"]:
                    test_results.append({
                        "name": test["name"],
                        "status": "fail",
                        "score": 0,
                        "max_score": test["max_score"],
                        "output": f"AST Error: {ast_msg}"
                    })
            else:
                command = f"{sys.executable} {file_path}"
                total_score = 0
                for test in task["tests"]:
                    res = run_test(
                        command=command,
                        input_str=test["input"],
                        expected=test["expected_output"],
                        method=test["comparison_method"],
                        timeout=5
                    )
                    res["name"] = test["name"]
                    res["max_score"] = test["max_score"]
                    res["score"] = res["score"] * test["max_score"]
                    test_results.append(res)
                    total_score += res["score"]
    
    result = {
        "score": sum(t["score"] for t in test_results),
        "max_score": max_score,
        "tests": test_results
    }
    encoded = base64.b64encode(json.dumps(result, ensure_ascii=False).encode("utf-8")).decode("utf-8")
    print(f"::set-output name=result::{encoded}")

if __name__ == "__main__":
    main()