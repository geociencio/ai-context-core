"""Logic for the 'scaffold' command to generate code templates."""

import pathlib
import click

TEMPLATES = {
    "strategy": '''"""Strategy Pattern Template."""

from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self, data):
        print(f"Executing Strategy A with {data}")

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
        
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
        
    def run(self, data):
        self._strategy.execute(data)
''',
    "observer": '''"""Observer Pattern Template."""

from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Subject:
    def __init__(self):
        self._observers = []
        
    def attach(self, observer: Observer):
        self._observers.append(observer)
        
    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class ConcreteObserver(Observer):
    def update(self, message):
        print(f"Observer received: {message}")
''',
}


def run_scaffold(pattern: str, output: str = None):
    """Generate a code template for a design pattern."""
    pattern = pattern.lower()
    if pattern not in TEMPLATES:
        click.secho(
            f"❌ Unknown pattern: {pattern}. Available: {', '.join(TEMPLATES.keys())}",
            fg="red",
        )
        return

    content = TEMPLATES[pattern]
    out_file = output or f"{pattern}_pattern.py"
    path = pathlib.Path(out_file)

    if path.exists():
        if not click.confirm(f"⚠️ File {out_file} already exists. Overwrite?"):
            return

    path.write_text(content, encoding="utf-8")
    click.secho(f"✅ Scaffolded {pattern} pattern to {out_file}", fg="green")
