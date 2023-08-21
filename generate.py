import logging
from pathlib import Path

from jinja2 import Template

BASE_IMAGES = ["alpine", "buster", "bullseye", "slim"]
PYTHON_VERSIONS = [
    "3.7",
    "3.7.12",
    "3.7.13",
    "3.7.14",
    "3.7.15",
    "3.7.16",
    "3.7.17",
    "3.8",
    "3.8.12",
    "3.8.13",
    "3.8.14",
    "3.8.15",
    "3.8.16",
    "3.8.17",
    "3.9",
    "3.9.9",
    "3.9.10",
    "3.9.11",
    "3.9.12",
    "3.9.13",
    "3.9.14",
    "3.9.15",
    "3.9.16",
    "3.9.17",
    "3.10",
    "3.10.0",
    "3.10.1",
    "3.10.2",
    "3.10.3",
    "3.10.4",
    "3.10.5",
    "3.10.6",
    "3.10.7",
    "3.10.8",
    "3.10.9",
    "3.10.10",
    "3.10.11",
    "3.10.12",
    "3.11",
    "3.11.0",
    "3.11.1",
    "3.11.2",
    "3.11.3",
    "3.11.4",
]
POETRY_VERSION = "1.6.1"

logging.basicConfig(
    level="INFO", format="%(levelname)s:%(name)s:%(lineno)d:%(message)s"
)
logger = logging.getLogger(__name__)


def generate_dockerfiles():
    for base_image in BASE_IMAGES:
        for python_version in PYTHON_VERSIONS:
            with open(Path.cwd() / "templates" / f"{base_image}.j2", "r") as f:
                logger.info(
                    "Generating Dockerfile for "
                    f"{base_image}:{python_version}:{POETRY_VERSION}"
                )
                template = Template(f.read()).render(
                    python_version=python_version, poetry_version=POETRY_VERSION
                )

                output_file = Path(
                    Path.cwd() / "docker" / base_image / python_version / "Dockerfile"
                )
                output_file.parent.mkdir(exist_ok=True, parents=True)

                with open(output_file, "w") as f:
                    f.write(f"{template}\n")


if __name__ == "__main__":
    generate_dockerfiles()
