# Codara Code Review and Diagnostics Tool

This script assists in AI code review and diagnosis by using tailored AI models to intelligently provide suggestions and improvements. Purchase a subscription at [codara.io](https://codara.io)

## Subscribe to use this tool: [codara.io](https://codara.io)
### These prices directly help us with the AI costs related to running the model

| Plan      | Price    | Description                                                                                                                | Link                                                                                                    |
|-----------|----------|----------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
| Basic     | $4/month | - 14 day free trial<br/> - unlimited reviews<br/> - diagnostic feature<br/> - review unstaged code<br/> - locally saved reviews | [Free Trial](https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-2YR33470WV105614YMXX5QQI) |

[//]: # (| Pro       | $30/month | Access to all basic features plus more.      | [Sign Up]&#40;#&#41;    |)

[//]: # (| Ultimate  | $60/month | All features from Pro, plus premium support. | [Sign Up]&#40;#&#41;    |)


## Features

- Review the code differences between two branches in a Git repository.
- Review unstaged code diffs.
- Generate a formatted review file with a timestamp and the branch commit hash.
- Diagnose code issues directly in the terminal by providing the command to debug.

## Prerequisites

- Python 3.6 or later.
- Git must be installed and configured on the system where the script is executed.

## Installation

```bash
pip install codara
```

## Help and Documentation
```bash
codara --help
```

## Login 
### an active subscription is required to use this tool: [codara.io](https://codara.io)
#### register or login with the below command using the same email used to purchase your subscription
```bash
codara --login
```

## Usage

To use the AI review feature run the following command:

```bash
codara review --unstaged
```
or the short version (shorthands available for all commands)
```bash
codara review -u
```

or review between two branches like a pull request

```bash
codara review --target <target_branch>
```

get help
```bash
codara review --help
```

To use the AI diagnostic feature run the following command:

```bash
codara diagnose "<command-producing-error>"
```
get help
```bash
codara diagnose --help
```

## Output

The AI reviewer will create a new file in the `reviews` directory with the review output. The file will be named using the source and target branch names, their respective commit hashes, and a timestamp.

The AI diagnostics will create a new file in the `diagnostics` directory with the diagnostic output. The file will be named using the command provided and a timestamp.

Example review filename: `feature-branch_abc123_to_main_def456_2023-11-15_23-31-56.txt`

Example diagnostic filename: `diagnose_command_2023-11-15_23-31-56.txt`
