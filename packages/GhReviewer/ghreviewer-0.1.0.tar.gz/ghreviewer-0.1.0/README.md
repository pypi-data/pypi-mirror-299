# A tool for systematically reviewing Github repositories

This application provides a graphical interface to systematically review GitHub repositories based on specified search queries. Users can view repository details, including the description and README, and mark repositories for inclusion or exclusion along with any motivation for why.

Getting Started

Follow these instructions to get the application running on your local machine.
Prerequisites

Make sure you have the following installed:

- Python 3.6+
- pip
- GitHub Personal Access Token (for API access)

Installation

1. Clone the repository:
```bash
git clone https://github.com/jonmest/GhReviewer.git
cd GhReviewer
```

2. Install dependencies: The dependencies are listed in requirements.txt. Install them by running:

```bash
pip install -r requirements.txt
```

3. Run the application: To start the application, run:

```bash
python github_review_app.py --token <your-github-token>
```
You can also pass in a CSV file and enable masked mode as options:

```bash
python github_review_app.py --token <your-github-token> --csv path/to/repositories.csv --masked
```

Alternatively:
```bash
python setup.py sdist bdist_wheel
pip install .
```

Usage

- Navigating repositories: Use the "Next" and "Previous" buttons to move through repositories.
- Include/Exclude: Click the "Include" or "Exclude" button to mark repositories. You can add comments to each repository.
- Save progress: The review progress, including the inclusion status and comments, will be saved to the specified CSV file.
- Masked mode: If masked mode is enabled, the application will hide repository names and images to allow anonymous reviewing.

Command-line options

```bash
usage: python my_script.py [--token GITHUB_TOKEN] [--csv CSV_FILE] [--masked]

--token      GitHub Personal Access Token (required)
--csv        CSV file path to load (optional)
--masked     Enable masked mode to hide repository names and images (optional)
```
Example Usage

```bash
python github_review_app.py --token abcdef12345 --csv repos.csv --masked
```

## License
Usage of this code is forbidden unless explicit permission is provided by the author.