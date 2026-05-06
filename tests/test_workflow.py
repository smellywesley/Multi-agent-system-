from multi_agent_system.workflows.review_workflow import ReviewWorkflow


def test_review_workflow_run() -> None:
    workflow = ReviewWorkflow()
    result = workflow.run("Analyze this text")

    assert result.sender == "reviewer"
    assert result.recipient == "extractor"
