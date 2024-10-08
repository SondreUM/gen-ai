# Generative AI - course project

> ⚠️ This project is now archived and will not be maintained. ⚠️\
> You are free to fork the project and continue development according to the license.
>
> This project is a proof of concept, and is not intended for production use.

> Part of the course:\
> FYS-3810 Generativ AI 24V Individual special curriculum - Master's degree\
> UiT The Arctic University of Norway

## Table of contents

- [Generative AI - course project](#generative-ai---course-project)
  - [Table of contents](#table-of-contents)
  - [Project description](#project-description)
    - [Project activity](#project-activity)
  - [Installation](#installation)
    - [API keys](#api-keys)
      - [Optional keys](#optional-keys)
  - [Usage](#usage)
  - [Project structure](#project-structure)
  - [Disclaimer](#disclaimer)

## Project description

An OSINT (Open Source INTelligence) tool that creates a report about a chosen organization, company or individual.

The tool can extract information with the following targets

- Company
- Organization

More targets may be added in the future.
Other targets may work, but are not guaranteed or supported.

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

To run the project, you need to have `python3` version 3.10 or newer, and `python3-pip` installed on your system.
Then, you can install the project dependencies by running the following command:

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

### API keys

The project requires a gpt api key to be provided as plain text in the `src/keys/gpt_key.txt` file.
The key can be obtained from <https://beta.openai.com/signup/>

#### Optional keys

- `src/keys/1881_key.txt` - 1881.no API key

## Usage

To run the project, you can run the following command:

```bash
python3 src/processing.py -e <insert entity>
```

---

## Project structure

![UML diagram](docs/img/uml_bck.png "UML diagram")

## Disclaimer

This project is for educational purposes only. The authors do not take any responsibility for the use of this project.
