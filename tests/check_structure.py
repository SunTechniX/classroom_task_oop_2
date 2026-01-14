import ast
import sys
import argparse

def check_task_1(tree):
    errors = []
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}

    if 'Notifier' not in classes:
        errors.append("Отсутствует класс Notifier")
    else:
        methods = [n.name for n in classes['Notifier'].body if isinstance(n, ast.FunctionDef)]
        if 'send' not in methods:
            errors.append("В Notifier нет метода send")

    for cls in ['EmailNotifier', 'SMSNotifier', 'PushNotifier']:
        if cls not in classes:
            errors.append(f"Отсутствует класс {cls}")

    if 'notify_all' not in functions:
        errors.append("Отсутствует функция notify_all")
    
    return errors

def check_task_2(tree):
    errors = []
    classes = {node.name: node for node in tree.body if isinstance(node, ast.ClassDef)}

    if 'Animal' not in classes:
        errors.append("Отсутствует класс Animal")
    else:
        animal = classes['Animal']
        methods = [n.name for n in animal.body if isinstance(n, ast.FunctionDef)]
        if '__init__' not in methods:
            errors.append("В Animal нет __init__")
        if 'speak' not in methods:
            errors.append("В Animal нет speak")
        if 'about_me' not in methods:
            errors.append("В Animal нет about_me")

    for cls in ['Dog', 'Cat']:
        if cls not in classes:
            errors.append(f"Отсутствует класс {cls}")
        else:
            node = classes[cls]
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            init_methods = [n for n in methods if n == '__init__']
            about_me_methods = [n for n in methods if n == 'about_me']
            if init_methods:
                errors.append(f"В {cls} не должно быть __init__")
            if about_me_methods:
                errors.append(f"В {cls} не должно быть about_me")
            if 'speak' not in methods:
                errors.append(f"В {cls} нет метода speak")
    
    return errors

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--task', type=int, required=True)
    args = parser.parse_args()

    with open(args.filename, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())

    if args.task == 1:
        errors = check_task_1(tree)
    elif args.task == 2:
        errors = check_task_2(tree)
    else:
        print("Поддерживаются только --task 1 или --task 2")
        sys.exit(1)

    if errors:
        print(f"Ошибки в {args.filename}:")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print(f"✅ {args.filename}: структура корректна")

if __name__ == "__main__":
    main()
