# Contributing to Voxera

Thank you for your interest in contributing to **voxera**.
We welcome contributions from developers, researchers, and open-source enthusiasts who want to improve the project and make it more robust and scalable.

This document provides guidelines and instructions for contributing effectively.

---

## Code of Conduct

By participating in this project, you agree to:

* Be respectful and inclusive
* Provide constructive feedback
* Maintain professional communication
* Help create a welcoming open-source environment

---

## Ways to Contribute

You can contribute in multiple ways:

* Bug fixes
* Feature development
* Documentation improvements
* Performance optimization
* Test coverage improvement
* Refactoring and code cleanup
* Reporting issues
* Suggesting new ideas

---

## Getting Started

### 1. Fork the Repository

Fork the Voxera repository to your GitHub account.

```
https://github.com/abhirajadhikary06/voxera
```

---

### 2. Clone the Repository

```
git clone https://github.com/<your-username>/voxera.git
cd voxera
```

---

### 3. Create a Virtual Environment

```
python -m venv venv
source venv/bin/activate
```

Windows:

```
venv\Scripts\activate
```

---

### 4. Install Dependencies

```
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

or

```
pip install -e .
```

---

### 5. Run Tests

```
pytest -q
```

Make sure all tests pass before making changes.

---

## Development Workflow

### Create a New Branch

```
git checkout -b feature/your-feature-name
```

or

```
git checkout -b fix/bug-name
```

---

### Make Changes

Follow project structure and coding standards.

Ensure:

* Code is clean and readable
* Functions are modular
* Proper comments are added
* Tests are updated

---

### Run Linting and Tests

```
pytest
```

Optional:

```
flake8
black .
```

---

### Commit Changes

Use meaningful commit messages.

Example:

```
feat: add audio preprocessing pipeline
fix: resolve memory leak in transcription module
docs: update installation guide
```

---

### Push Changes

```
git push origin feature/your-feature-name
```

---

### Create Pull Request

Go to GitHub and create a Pull Request.

Provide:

* Clear title
* Description of changes
* Screenshots (if applicable)
* Related issue number

---

## Pull Request Guidelines

Before submitting a PR, ensure:

* Code builds successfully
* Tests pass
* No unnecessary files included
* Proper documentation added
* Commit messages are clean
* PR description explains the change clearly

PRs will be reviewed by maintainers before merging.

---

## Issue Guidelines

When creating an issue, include:

### Bug Report

* Description
* Steps to reproduce
* Expected behavior
* Actual behavior
* Logs or screenshots
* Environment details

---

### Feature Request

* Problem statement
* Proposed solution
* Use case
* Possible implementation

---

## Project Structure Guidelines

Follow the existing structure:

```
voxera/
│
├── src/
├── tests/
├── docs/
├── examples/
├── requirements.txt
├── pyproject.toml
└── README.md
```

Keep modules organized and avoid large monolithic files.

---

## Coding Standards

* Follow PEP8
* Use type hints
* Write docstrings
* Keep functions small
* Maintain modular architecture
* Avoid hardcoded values
* Use environment variables for secrets

Example:

```
def process_audio(file_path: str) -> str:
    """Process audio and return transcription."""
```

---

## Documentation

Update documentation if:

* New feature added
* API changed
* New dependency added
* Setup process modified

Documentation should be clear and beginner-friendly.

---

## Testing Guidelines

* Write unit tests for new features
* Maintain test coverage
* Use pytest
* Avoid flaky tests
* Mock external APIs when required

Example:

```
def test_transcription():
    assert transcribe("sample.wav") is not None
```

---

## Branch Naming Convention

```
feature/audio-engine
fix/docker-build
docs/readme-update
test/api-tests
refactor/pipeline-cleanup
```

---

## Commit Message Convention

```
feat:
fix:
docs:
test:
refactor:
chore:
```

Example:

```
feat: add streaming transcription support
```

---

## Maintainers

Project maintained by:

* Abhiraj Adhikary
* Anik Chand
* Rudra Bhowmick

---

## License

By contributing to Voxera, you agree that your contributions will be licensed under the project license.

---

## Questions

If you have any questions, open an issue or start a discussion in the repository.

---

If you want, I can also create:

* ISSUE_TEMPLATE.md
* PULL_REQUEST_TEMPLATE.md
* CODE_OF_CONDUCT.md
* SECURITY.md

to make Voxera fully open-source ready.
