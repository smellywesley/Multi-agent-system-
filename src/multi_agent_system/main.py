"""CLI entry point."""

import argparse

import structlog

from multi_agent_system.config import get_settings
from multi_agent_system.logging_config import configure_logging
from multi_agent_system.workflows.review_workflow import ReviewWorkflow


def build_parser() -> argparse.ArgumentParser:
    """Create command-line parser."""
    parser = argparse.ArgumentParser(
        prog="multi-agent-system",
        description="Multi-agent system CLI",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Run review workflow")
    run_parser.add_argument("--task", required=True, help="Task for the orchestrator")

    return parser


def cli() -> int:
    """CLI function used by console script."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return 0

    settings = get_settings()
    configure_logging(settings.log_level)
    logger = structlog.get_logger(__name__)

    if args.command == "run":
        workflow = ReviewWorkflow()
        result = workflow.run(task=args.task)
        logger.info("workflow.completed", sender=result.sender, recipient=result.recipient)
        print(result.content)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(cli())
