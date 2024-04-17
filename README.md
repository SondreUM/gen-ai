# Generative AI - course project

> UiT The Arctic University of Norway\
> FYS-3810 Generativ AI 24V Individual special curriculum - Master's degree

## Table of contents

- [Generative AI - course project](#generative-ai---course-project)
  - [Table of contents](#table-of-contents)
  - [Project description](#project-description)
    - [Project activity](#project-activity)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Project structure](#project-structure)
    - [Models](#models)
  - [Disclaimer](#disclaimer)

## Project description

An OSINT (Open Source INTelligence) tool that creates a report about  a chosen organization, company or individual.

The tool can extract information with the following targets

- Person
- Organization/Company
- Person in a organization or company

The data is then used to generate a report containing information about the target.
The report may contain the following information:

- Location/Address
- Contact information
- Social media accounts
- Recent activities

### Project activity

![Alt](https://repobeats.axiom.co/api/embed/b16fb7d94a73f0f71a96f0dd343a6c7cf0ea409f.svg "Repobeats analytics image")

## Installation

Clone the repository in cli or download the zip file from the github repository.

```bash
git clone git@github.com:SondreUM/gen-ai.git
```

To run the project, you need to have `python3` and `python3-pip` installed on your system.
Then, you can install the project dependencies by running the following commands:

```bash
pip install -r requirements.txt
```

Because of the size of some of the dependencies, we recommend using a virtual environment to install the them.
Creating a virtual environment should be done before installing dependencies.
You can create a virtual environment by running the following commands:

```bash
# creates the virtual environment
python3 -m venv venv
# activates the virtual environment
source venv/bin/activate
```

Deleting the virtual environment folder will uninstall all dependencies from the project.

## Usage

The project requires a gpt api key to be provided as plain text in the `src/api_key.txt` file.
The key can be obtained from <https://beta.openai.com/signup/>

To run the project, you can run the following command:

```bash
python src/main.py
```

---

## Project structure

> Crawler+APIs -> Filtering layer -> Extractor/reduce model -> tmp-dump -> Generator model (LLM) -> Report

TODO: insert UML diagram

### Models

TODO

## Disclaimer

This project is for educational purposes only. The authors do not take any responsibility for the use of this project.
