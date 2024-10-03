# scystream-sdk

## Installation

You can install the package via pip once it's published:

```bash
pip install scystream-sdk
```

## Usage

```python3
from scystream.sdk.core import entrypoint, get_entrypoints
from scystream.sdk.scheduler import schedule_task, run_scheduler


@entrypoint
def example_task():
    print("Executing example_task...")

@entrypoint
def another_task(task_name):
    print(f"Executing another_task with task name: {task_name}")

def main():
    print("Registered entrypoints:")
    for name, func in get_entrypoints().items():
        print(f" - {name}: {func}")
    schedule_task(5, example_task)
    schedule_task(10, another_task, "ScheduledTask")
    run_scheduler()


if __name__ == "__main__":
    main()
```
