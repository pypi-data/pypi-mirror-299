# # GitAdmin

A Python command-line tool for managing GitHub repositories. This tool allows users to list repositories, manage visibility, and retrieve issue summaries from their GitHub account.

## Features

- **List Repositories**: Retrieve a list of your GitHub repositories, including their visibility status.
- **Manage Repository Visibility**: Change the visibility of your repositories (e.g., from public to private).
- **Get Issue Summaries**: Summarize open issues across your repositories.

## Installation

You can install the tool using `pip` once it is distributed:

```bash
pip install GitAdmin
```

## Setup
Before using the tool, run the setup command to configure your GitHub username and token
```bash
GitAdmin setup
```
This command will:
- prompt for your github token (repo is the only access it needs) and your username
- Store this within a local yaml file

## Usage
### list
```bash
GitAdmin list
```
returns a list of your repositories and their visibility
### visibility
```bash
GitAdmin visibility --repo <repositoryname> --visibility <public|private>
```
use to change visibility of given repo
### issues
```bash
GitAdmin issues --repo <repository name>
```
Fetches issues in given repository
