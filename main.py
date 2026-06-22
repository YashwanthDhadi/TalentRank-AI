"""Application entry point for generating a ranked submission."""

from src.pipeline.submission_generator import SubmissionGenerator


def main() -> None:
    """Generate the submission artifact using default configuration."""
    generator = SubmissionGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
