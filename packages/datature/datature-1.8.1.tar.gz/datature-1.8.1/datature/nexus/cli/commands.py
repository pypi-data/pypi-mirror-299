#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""
  ████
██    ██   Datature
  ██  ██   Powering Breakthrough AI
    ██

@File    :   commands.py
@Author  :   Raighne.Weng
@Contact :   developers@datature.io
@License :   Apache License 2.0
@Desc    :   CLI supported commands
"""

import sys
from argparse import ArgumentParser, _SubParsersAction
from datetime import datetime
from typing import Optional

from datature import nexus

# pylint: disable=W0212


class Commands:
    """All Datature CLI commands."""

    def __init__(self) -> None:
        self.parser = ArgumentParser(
            prog="datature",
            description="Command line tool to create/upload/download datasets on datature nexus.",
        )

        self.parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {nexus.__version__}"
        )

        self.subparsers = self.parser.add_subparsers(dest="command")
        self._add_project_parser()
        self._add_asset_parser()
        self._add_annotation_parser()
        self._add_artifact_parser()
        self._add_batch_parser()
        self._add_help_parser()

    def _add_project_parser(self):
        """Project level parser."""
        projects = self.subparsers.add_parser(
            "projects",
            help="Projects management.",
            description="datature projects - auth/list/select project from saved project.",
        )
        projects_action = projects.add_subparsers(dest="action")

        projects_action.add_parser("auth", help="Authenticate and save the project.")
        projects_action.add_parser(
            "select", help="Select the project from saved projects."
        )
        projects_action.add_parser("list", help="List the saved projects.")

        projects_action.add_parser(
            "help", help="Show this help message and exit.", add_help=False
        )

    def _add_asset_parser(self):
        """Asset level parser."""
        assets = self.subparsers.add_parser(
            "assets",
            help="Assets management.",
            description="datature assets - upload/group assets.",
        )
        assets_action = assets.add_subparsers(dest="action")

        assets_upload = assets_action.add_parser(
            "upload",
            help="Bulk update assets.",
        )
        assets_upload.add_argument("path", nargs="*", help="The asset path to upload.")
        assets_upload.add_argument(
            "groups", nargs="*", help="The asset groups to upload."
        )

        assets_group = assets_action.add_parser(
            "groups",
            help="List assets group details.",
        )
        assets_group.add_argument("group", nargs="*", help="The asset group name.")

        assets_action.add_parser(
            "help", help="Show this help message and exit.", add_help=False
        )

    def _add_annotation_parser(self):
        """Annotation level parser."""
        annotations = self.subparsers.add_parser(
            "annotations",
            help="Annotations management.",
            description="datature annotations - upload/download annotations.",
        )
        annotations_action = annotations.add_subparsers(dest="action")

        annotations_upload = annotations_action.add_parser(
            "upload",
            help="Bulk upload annotations from file.",
        )
        annotations_upload.add_argument(
            "path", nargs="*", help="The annotations file path."
        )

        annotations_download = annotations_action.add_parser(
            "download",
            help="Bulk download annotations to file.",
        )
        annotations_download.add_argument(
            "path", nargs="*", help="The annotations file path."
        )
        annotations_download.add_argument(
            "format", nargs="*", help="The annotations format to download."
        )

        annotations_action.add_parser(
            "help", help="Show this help message and exit.", add_help=False
        )

    def _add_artifact_parser(self):
        """Artifact level parser."""
        artifacts = self.subparsers.add_parser(
            "artifacts",
            help="Artifacts management.",
            description="datature artifacts - download artifact models.",
        )
        artifacts_action = artifacts.add_subparsers(dest="action")

        artifacts_download = artifacts_action.add_parser(
            "download",
            help="Download artifact model.",
        )
        artifacts_download.add_argument(
            "artifact_id", nargs="*", help="The id of the artifact."
        )
        artifacts_download.add_argument(
            "format", nargs="*", help="The artifact model format."
        )

        artifacts_action.add_parser(
            "help", help="Show this help message and exit.", add_help=False
        )

    def _add_batch_parser(self):
        """Batch level parser."""
        batch = self.subparsers.add_parser(
            "batch",
            help="Batch job management.",
            description="datature batch jobs - manage batch jobs.",
        )
        entity = batch.add_subparsers(dest="entity")
        entity.add_parser(
            "help", help="Show this help message and exit.", add_help=False
        )
        details_parser = ArgumentParser(add_help=False)
        details_parser.add_argument(
            "id",
            type=str,
            nargs="?",
            help="ID of the entry to get details for.",
        )

        def _add_jobs_parser():
            jobs = entity.add_parser("jobs", help="Manage batch jobs.")
            jobs_action = jobs.add_subparsers(dest="action")
            jobs_action.add_parser(
                "create",
                help="Create a new batch job.",
            )
            jobs_action.add_parser(
                "get",
                parents=[details_parser],
                help="Get details of a batch job.",
            )
            jobs_action.add_parser(
                "list",
                help="List batch jobs.",
            )
            jobs_action.add_parser(
                "wait-until-done",
                parents=[details_parser],
                help="Wait for a batch job to complete.",
            )
            jobs_action.add_parser(
                "cancel",
                parents=[details_parser],
                help="Cancel a batch job.",
            )
            jobs_action.add_parser(
                "delete",
                parents=[details_parser],
                help="Delete a batch job.",
            )
            jobs_action.add_parser(
                "help", help="Show this help message and exit.", add_help=False
            )

            job_logs = jobs_action.add_parser(
                "logs",
                parents=[details_parser],
                help="Get logs of a batch job.",
            )
            job_logs.add_argument(
                "--max_entries",
                type=int,
                default=0,
                help="Maximum number of log entries to return.",
            )
            job_logs.add_argument(
                "--since",
                type=int,
                default=0,
                help="Only return logs after this timestamp.",
            )
            job_logs.add_argument(
                "--until",
                type=int,
                default=int(datetime.now().timestamp()) * 1000,
                help="Only return logs before this timestamp.",
            )
            job_logs.add_argument(
                "--level",
                type=str,
                default="Info",
                help="Only return logs at this level or higher.",
            )
            job_logs.add_argument(
                "--output",
                type=str,
                default="",
                help="Output log to file.",
            )

        def _add_wehooksecrets_parser():
            webhooksecrets = entity.add_parser(
                "webhooksecrets", help="Manage webhook secrets."
            )
            webhooksecrets_action = webhooksecrets.add_subparsers(dest="action")
            webhooksecrets_action.add_parser(
                "create",
                help="Create a new webhook secret.",
            )
            webhooksecrets_action.add_parser(
                "help", help="Show this help message and exit.", add_help=False
            )

        def _add_webhooks_parser():
            webhooks = entity.add_parser("webhooks", help="Manage webhooks.")
            webhooks_action = webhooks.add_subparsers(dest="action")
            webhooks_action.add_parser(
                "create",
                help="Create a new webhook.",
            )
            webhooks_action.add_parser(
                "get",
                parents=[details_parser],
                help="Get details of a webhook.",
            )
            webhooks_action.add_parser(
                "list",
                help="List webhooks.",
            )
            webhooks_action.add_parser(
                "update",
                parents=[details_parser],
                help="Update a webhook.",
            )
            webhooks_action.add_parser(
                "update-secret",
                parents=[details_parser],
                help="Update the secret of a webhook.",
            )
            webhooks_action.add_parser(
                "delete",
                parents=[details_parser],
                help="Delete a webhook.",
            )
            webhooks_action.add_parser(
                "test",
                parents=[details_parser],
                help="Test a webhook by sending a test payload.",
            )
            webhooks_action.add_parser(
                "help", help="Show this help message and exit.", add_help=False
            )

        def _add_datasets_parser():
            datasets = entity.add_parser("datasets", help="Manage datasets.")
            datasets_action = datasets.add_subparsers(dest="action")
            datasets_action.add_parser(
                "create",
                help="Create a new dataset.",
            )
            datasets_action.add_parser(
                "get",
                parents=[details_parser],
                help="Get details of a dataset.",
            )
            datasets_action.add_parser(
                "list",
                help="List datasets.",
            )
            datasets_action.add_parser(
                "delete",
                parents=[details_parser],
                help="Delete a dataset.",
            )
            datasets_action.add_parser(
                "help", help="Show this help message and exit.", add_help=False
            )

        _add_jobs_parser()
        _add_wehooksecrets_parser()
        _add_webhooks_parser()
        _add_datasets_parser()

    def _add_help_parser(self):
        """Help level parser."""
        help_parser = self.subparsers.add_parser(
            "help",
            description="Show this help message and exit.",
        )
        help_action = help_parser.add_subparsers(dest="action")

        command_names = ["project", "asset", "annotation", "artifact", "batch"]
        for command_name in command_names:
            help_action.add_parser(command_name)

    def parse_args(self) -> ArgumentParser:
        """
        Parses and validates the CLI commands.

        :return: The parser to use.
        """
        args = self.parser.parse_args()

        if not args.command:
            self.print_help()
            sys.exit()

        return args

    def print_help(self, subparser: Optional[str] = None):
        """
        Prints the help information.

        :param subparser: The name of subparser.
        :return: None
        """
        parser = self.parser

        if subparser:
            parser = next(
                action.choices[subparser]
                for action in parser._actions
                if isinstance(action, _SubParsersAction) and subparser in action.choices
            )

        parser.print_help()
