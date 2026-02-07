import ast
import sys
from ai_context_core.analyzer.complexity_visitor import ComplexityVisitor

def check_file(path):
    with open(path, "r") as f:
        content = f.read()
    
    tree = ast.parse(content)
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            visitor = ComplexityVisitor()
            visitor.visit(node)
            print(f"Function {node.name}: {visitor.complexity}")

if __name__ == "__main__":
    check_file(sys.argv[1])
