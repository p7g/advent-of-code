def get_input(split_lines=False, line_transform=None):
    import inspect
    from pathlib import Path

    last_frame = inspect.stack()[1]
    module = inspect.getmodule(last_frame[0])
    input_path = Path(module.__file__).parent / "input.txt"
    with open(input_path, "r") as f:
        content = f.read().strip()
        if split_lines:
            content = content.splitlines()
        if line_transform is not None:
            content = [line_transform(line) for line in content]
        return content
