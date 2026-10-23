"""${project_name} - A Python library."""

from ${project_name}.core import hello, add


def main() -> None:
    print(hello("World"))
    print(f"2 + 3 = {add(2, 3)}")


if __name__ == "__main__":
    main()