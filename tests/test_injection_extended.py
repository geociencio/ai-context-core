import ast
from ai_context_core.analyzer.visitors.injection import InjectionChecker


def test_subprocess_shell_true():
    checker = InjectionChecker()
    issues = []
    code = "import subprocess; subprocess.run('ls', shell=True)"
    tree = ast.parse(code)
    for node in ast.walk(tree):
        checker.check(node, issues)

    assert any(
        "subprocess.run" in i["pattern"] and "shell=True" in i["description"]
        for i in issues
    )


def test_sql_injection_variants():
    checker = InjectionChecker()

    # f-string
    issues = []
    tree = ast.parse("db.execute(f'SELECT * FROM users WHERE id={id}')")
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert any("SQL Injection (f-string)" in i["pattern"] for i in issues)

    # .format()
    issues = []
    tree = ast.parse("db.execute('SELECT * FROM users WHERE id={}'.format(id))")
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert any("SQL Injection (.format)" in i["pattern"] for i in issues)

    # % operator
    issues = []
    tree = ast.parse("db.execute('SELECT * FROM users WHERE id=%s' % id)")
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert any("SQL Injection (%)" in i["pattern"] for i in issues)


def test_fstring_sql_heuristic():
    checker = InjectionChecker()
    issues = []
    # f-string SQL outside execute()
    tree = ast.parse("query = f'SELECT * FROM {table}'")
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert any("f-string SQL" in i["pattern"] for i in issues)


def test_sql_execute_no_args():
    checker = InjectionChecker()
    issues = []
    # Coverage for line 62: if not node.args: return
    tree = ast.parse("db.execute()")
    for node in ast.walk(tree):
        checker.check(node, issues)
    assert len(issues) == 0
