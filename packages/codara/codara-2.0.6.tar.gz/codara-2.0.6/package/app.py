#!/usr/bin/env python3
import os
import sys
import argparse
from package.git_utils import get_code_diff, get_current_git_branch
from package.auth import login
from package.review import review_code, review_file_path
from package.auth import access_token_expired, get_new_access_token
from package.user import check_user_subscription_status, check_if_user_exists_or_create
from package.token_utils import decode_token, get_codararc_value
from package.version import version
from package.diagnose import get_diagnostic_output, diagnose_code, diagnose_file_path


def handle_diagnose_command(command):
    output = get_diagnostic_output(command)
    diagnosis = diagnose_code(output)
    if diagnosis:
        print('\n')
        print(diagnosis)
        print('\n')
        diagnosis_file = diagnose_file_path(command)
        with open(diagnosis_file, "w") as file:
            file.write("Review:\n")
            file.write(diagnosis)
        print(f"Review saved to {diagnosis_file}")


def handle_review_command(args):
    repo_dir = args.dir
    source_branch = args.source
    target_branch = args.target
    unstaged = args.unstaged

    if unstaged and (source_branch or target_branch):
        print("Cannot use the --unstaged flag with --source or --target.")
        sys.exit(1)

    if not source_branch:
        source_branch = get_current_git_branch(repo_dir)
        if not source_branch:
            sys.exit(1)

    if not os.path.isdir(repo_dir):
        print(f"Repository directory does not exist: {repo_dir}")
        sys.exit(1)

    try:
        code_diff = get_code_diff(repo_dir, source_branch, target_branch, unstaged)
        if not code_diff:
            print("No differences found.")
            return

        review = review_code(code_diff)
        if review:
            print('\n')
            print(review)
            print('\n')
            review_file = review_file_path(source_branch, target_branch, repo_dir, unstaged)
            with open(review_file, "w") as file:
                file.write("Review:\n")
                file.write(review)
            print(f"Review saved to {review_file}")
    except Exception as e:
        print(f"Error reviewing code: {e}")


def run_app(args):
    if args.command == 'diagnose':
        handle_diagnose_command(args.diagnose_command)
        return

    if args.command == 'review':
        handle_review_command(args)


def check_subscription():
    id_token = decode_token(get_codararc_value('id_token'))
    return check_user_subscription_status(id_token.get('email'))


def parser_args(parser):
    # Explicitly add the help flag
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-l', '--login', action='store_true',
                        help='login to your codara account')
    parser.add_argument('-v', '--version', action='version', version=f'version {version}',
                        help='Show the version of the program and exit.')


def review_parser_args(parser):
    # Define other arguments with detailed help
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    parser.add_argument('-t', '--target',
                        help='REQUIRED: Name of the target branch to compare with the source branch.')
    parser.add_argument('-d', '--dir', default='.',
                        help='OPTIONAL: Path to the repository directory.\n'
                             'Defaults to current directory if not specified.')
    parser.add_argument('-s', '--source', help='OPTIONAL: Name of the source branch to compare.')
    parser.add_argument('-u', '--unstaged', action='store_true',
                        help='OPTIONAL: Review unstaged changes. Cannot be used with --source or --target.')


def if_no_args(parser):
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=f"AI Code Automation Tools: Review code differences. Diagnose code errors and issues.\nLogin to your Codara account to get started. A subscription is required to use this tool.\n\nCode Review:\n\n'codara review -t main' \n\nDiagnose code:\n\n'codara diagnose '<command-producing-error>''\n\nPurchase a subscription plan at https://codara.io",
        add_help=False,  # Disable automatic help to customize
        formatter_class=argparse.RawTextHelpFormatter  # For better formatting of help text
    )

    # Create a subparsers object
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Create a subparser for the 'review' command
    review_parser = subparsers.add_parser('review', add_help=False, description=f"Code Review Automation Tool\n\nThis tool automates the process of reviewing code differences between two branches in a git repository using AI. \nLogin to your Codara account to get started. A subscription is required to use this tool.\n\nBasic usage 'codara review -t main' \n\nThis starts a review of the current branch you're on and main.\nChanges must be committed before running, if you want to run a review on a branch with unstaged commits you can do \n\n'codara review --unstaged' or 'codara review -u' \n\nPurchase a subscription plan at https://codara.io", formatter_class=argparse.RawTextHelpFormatter)
    review_parser_args(review_parser)  # Add the existing arguments to the review subparser

    # Create a subparser for the 'diagnose' command
    diagnose_parser = subparsers.add_parser('diagnose', add_help=False, description=f"Code Diagnosis Automation Tool\n\nThis tool automates the process of diagnosing code errors using AI. \nLogin to your Codara account to get started. A subscription is required to use this tool.\n\nBasic usage 'codara diagnose '<command>'' \n\nThis starts a diagnosis of the command you provide. Keep in mind, the command needs to be wrapped in strings.\n\nPurchase a subscription plan at https://codara.io", formatter_class=argparse.RawTextHelpFormatter)
    diagnose_parser.add_argument('diagnose_command', help='Command for diagnosis')
    diagnose_parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit.')

    parser_args(parser)
    if_no_args(parser)
    args = parser.parse_args()

    if args.login:
        login()
        check_if_user_exists_or_create()
    else:
        if access_token_expired():
            try:
                get_new_access_token()
            except Exception as e:
                print(f"There was an error with authentication, please login: {e}")
                sys.exit(1)
        if not check_subscription():
            print("No active subscription found, please purchase a subscription plan, https://codara.io")
            sys.exit(1)
        else:
            run_app(args)


if __name__ == "__main__":
    main()
