def test_create_app_registers_health_and_characters():
    from app.sbapi_api.main import create_app

    rules = {rule.rule for rule in create_app().url_map.iter_rules()}

    assert "/health" in rules
    assert "/characters" in rules


def test_empty_subpackages_import():
    import app.sbapi_api.dtos
    import app.sbapi_api.services
