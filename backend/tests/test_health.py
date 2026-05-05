"""
Tests for the health-check endpoints.
Owner: Praise-God Tobby (QA/Test Engineer, 2309116418)
Implemented by: Mohanad Aref Ali Sultan (Backend Developer, 2309115898)
"""
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://test:test@localhost:5432/testdb"
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


class TestBasicHealth:
    """Tests for GET /health — basic liveness probe.

    Expected response shape:
        {"status": "ok", "database": "connected", "uptime": "running", "timestamp": "...Z"}
    """

    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_is_ok(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "ok"

    def test_health_database_field_present(self):
        response = client.get("/health")
        data = response.json()
        assert "database" in data

    def test_health_database_is_connected(self):
        """Database must be reachable when running against PostgreSQL."""
        response = client.get("/health")
        data = response.json()
        assert data["database"] == "connected"

    def test_health_uptime_field_present(self):
        response = client.get("/health")
        data = response.json()
        assert "uptime" in data
        assert data["uptime"] in ("running", "starting")

    def test_health_timestamp_is_utc(self):
        response = client.get("/health")
        data = response.json()
        assert "timestamp" in data
        assert data["timestamp"].endswith("Z")

    def test_health_no_auth_required(self):
        """Health endpoint must be accessible without authentication."""
        response = client.get("/health")
        assert response.status_code == 200


class TestDetailedHealth:
    """Tests for GET /health/detailed — technical monitoring endpoint."""

    def test_detailed_health_returns_200(self):
        response = client.get("/health/detailed")
        assert response.status_code == 200

    def test_detailed_health_status_is_valid(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert data["status"] in ("healthy", "degraded", "unhealthy")

    def test_detailed_health_has_components(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert "components" in data

    def test_detailed_health_database_component_present(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert "database" in data["components"]

    def test_detailed_health_database_is_healthy(self):
        """Database must be reachable when tests are running against PostgreSQL."""
        response = client.get("/health/detailed")
        data = response.json()
        assert data["components"]["database"]["status"] == "healthy"

    def test_detailed_health_database_has_response_time(self):
        response = client.get("/health/detailed")
        data = response.json()
        db = data["components"]["database"]
        assert "response_time_ms" in db
        assert isinstance(db["response_time_ms"], (int, float))
        assert db["response_time_ms"] >= 0

    def test_detailed_health_has_uptime(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], int)
        assert data["uptime_seconds"] >= 0

    def test_detailed_health_has_system_section(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert "system" in data

    def test_detailed_health_system_has_python_version(self):
        response = client.get("/health/detailed")
        data = response.json()
        assert "python_version" in data["system"]
        assert len(data["system"]["python_version"]) > 0

    def test_detailed_health_overall_status_matches_database(self):
        """Overall status must be unhealthy if the database is unhealthy."""
        response = client.get("/health/detailed")
        data = response.json()
        db_status = data["components"]["database"]["status"]
        if db_status == "unhealthy":
            assert data["status"] == "unhealthy"

    def test_detailed_health_no_auth_required(self):
        """Health endpoint must be accessible without authentication."""
        # No cookies, no Authorization header — should still return 200
        import requests
        response = client.get("/health/detailed")
        assert response.status_code == 200
