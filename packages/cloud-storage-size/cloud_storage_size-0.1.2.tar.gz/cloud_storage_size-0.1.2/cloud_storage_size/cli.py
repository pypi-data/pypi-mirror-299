import fire
from .rclone import size


def main():
    fire.Fire(size)


if __name__ == "__main__":
    main()
