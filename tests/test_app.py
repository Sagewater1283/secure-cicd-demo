from app.main import build_response


def test_health_check_returns_healthy_status() -> None:
    status_code, body = build_response("/health")

    assert status_code == 200
    assert body == {"status": "healthy"}


def test_security_summary_lists_pipeline_controls() -> None:
    status_code, body = build_response("/security-summary")

    assert status_code == 200
    assert "pipeline_controls" in body
    assert "Container image scanning" in body["pipeline_controls"]
    assert "dependency_strategy" in body
    assert "bind_strategy" in body


def test_unknown_route_returns_404() -> None:
    status_code, body = build_response("/missing")

    assert status_code == 404
    assert body == {"error": "not_found"}
