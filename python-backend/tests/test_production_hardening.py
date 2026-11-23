import pytest
from app.core.config import Settings, validate_production_security, safe_db_url_str
from app.api.admin import admin_update_settings, AdminSettingsPayload
from app.api.settings import load_settings

def test_safe_db_url_masks_password():
    raw_url = "postgresql://neondb_owner:npg_supersecretpass123@ep-cool-fog.ap-southeast-1.aws.neon.tech/neondb"
    masked = safe_db_url_str(raw_url)
    assert "supersecretpass" not in masked
    assert "neondb_owner" in masked

def test_production_enforces_postgresql_and_key():
    # 1. Reject SQLite in production
    s_sqlite = Settings(PRODUCTION=True, DATABASE_URL="sqlite:///lumea.db", SECRET_KEY="a"*32)
    with pytest.raises(ValueError, match="PostgreSQL DATABASE_URL is required"):
        validate_production_security(s_sqlite)

    # 2. Reject short key in production
    s_short_key = Settings(PRODUCTION=True, DATABASE_URL="postgresql://user:pass@localhost:5432/lumea", SECRET_KEY="short")
    with pytest.raises(ValueError, match="stable SECRET_KEY"):
        validate_production_security(s_short_key)

def test_partial_settings_save_preserves_unrelated_fields(monkeypatch, tmp_path):
    temp_file = str(tmp_path / "store_settings.json")
    monkeypatch.setattr("app.api.settings.SETTINGS_FILE", temp_file)

    # Get current settings
    initial = load_settings()
    tax_before = initial.get("tax_rate", 10.0)
    thresh_before = initial.get("free_shipping_threshold", 50.0)

    # Partial update: only update store_name
    payload = AdminSettingsPayload(store_name="Luméa Botanical Atelier")
    res = admin_update_settings(payload)
    assert res["status"] == "success"

    # Verify store_name changed
    assert res["data"]["store_name"] == "Luméa Botanical Atelier"
    # Verify tax_rate and free_shipping_threshold were NOT overwritten
    assert res["data"]["tax_rate"] == tax_before
    assert res["data"]["free_shipping_threshold"] == thresh_before
