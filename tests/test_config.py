from multi_agent_system.config import Settings


def test_settings_defaults() -> None:
    settings = Settings()
    assert settings.env == "development"
    assert settings.log_level == "INFO"
