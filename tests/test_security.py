from who_pen_rag.security import contains_secret, redact_mapping


def test_redaction():
    result = redact_mapping({
        "llm_api_key": "example-secret-value",
        "model": "example-model",
    })
    assert "llm_api_key" not in result
    assert result["llm_api_key_configured"] is True
    assert result["model"] == "example-model"


def test_secret_detection():
    assert not contains_secret("gsk_")
    assert contains_secret("gsk_" + "A" * 30)
