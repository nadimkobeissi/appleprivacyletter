#!/usr/bin/env python3
import os
import json
import re
import sys

NO_RESPONSE_TEXT = "_No response_"
DEFAULT_AFFIL = "Individual"
DEFAULT_URL = os.environ.get("ISSUE_AUTHOR_URL")


def parse_body() -> str:
    REGEX = r"### Name\s+(?P<name>.*)\s+### Affiliation\s+(?P<affil>.*)\s+### Website\/Twitter\/etc.\s+(?P<url>.*)\s+###"
    issue_body = os.environ.get("ISSUE_BODY")
    match = re.match(REGEX, issue_body, re.MULTILINE)

    result = {"name": "", "url": DEFAULT_URL, "affil": DEFAULT_AFFIL, "expert": False}

    # Make sure at least name is present and the issue is formatted as expected
    if (
        not match.group("name")
        or not match.group("affil")
        or not match.group("url")
        or match.group("name") == NO_RESPONSE_TEXT
    ):
        raise Exception("Issue body is not formatted as expected")

    result["name"] = match.group("name")
    if match.group("affil") != NO_RESPONSE_TEXT:
        result["affil"] = match.group("affil")
    if match.group("url") != NO_RESPONSE_TEXT:
        result["url"] = match.group("url")

    return json.dumps(result, indent="\t")

def compose_message(signature: str) -> str:
    # %0A is an escaped newline character
    msg = 'To auto-merge the following signature, replace the label of issue with `signature-approved`.%0A%0A```json%0A'
    msg += signature
    msg += '%0A```'
    return msg

def main():
    try:
        new_signature = parse_body()
        if len(sys.argv) > 1:
            if sys.argv[1] == '--compose-message':
                print(compose_message(new_signature.replace('\n', '%0A')))
            elif sys.argv[1] == '--commit-sign':
                pass
        else:
            raise Exception("No arguments provided")
    except Exception as e:
        print(e)
        return

main()