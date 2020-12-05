"""Test Axis Object Analytics API.

pytest --cov-report term-missing --cov=axis.applications.object_analytics tests/applications/test_object_analytics.py
"""

import pytest
from unittest.mock import AsyncMock

from axis.applications.object_analytics import ObjectAnalytics


@pytest.fixture
def object_analytics() -> ObjectAnalytics:
    """Returns the fence_guard mock object."""
    mock_request = AsyncMock()
    mock_request.return_value = ""
    return ObjectAnalytics(mock_request)


async def test_get_no_configuration(object_analytics):
    """Test no response from get_configuration"""
    object_analytics._request.return_value = {}
    await object_analytics.update()
    object_analytics._request.assert_called_with(
        "post",
        "/local/objectanalytics/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.0",
            "context": "Axis library",
            "params": {},
        },
    )

    assert len(object_analytics.values()) == 0


async def test_get_empty_configuration(object_analytics):
    """Test empty get_configuration"""
    object_analytics._request.return_value = response_get_configuration_empty
    await object_analytics.update()
    object_analytics._request.assert_called_with(
        "post",
        "/local/objectanalytics/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.0",
            "context": "Axis library",
            "params": {},
        },
    )

    assert len(object_analytics.values()) == 0


async def test_get_configuration(object_analytics):
    """Test get_configuration"""
    object_analytics._request.return_value = response_get_configuration
    await object_analytics.update()
    object_analytics._request.assert_called_with(
        "post",
        "/local/objectanalytics/control.cgi",
        json={
            "method": "getConfiguration",
            "apiVersion": "1.0",
            "context": "Axis library",
            "params": {},
        },
    )

    assert len(object_analytics.values()) == 2

    scenario1 = object_analytics["Device1Scenario1"]
    assert scenario1.id == "Device1Scenario1"
    assert scenario1.name == "Scenario 1"
    assert scenario1.camera == [{"id": 1}]
    assert scenario1.uid == 1
    assert scenario1.filters == [
        {"distance": 5, "type": "distanceSwayingObject"},
        {"time": 1, "type": "timeShortLivedLimit"},
        {"height": 3, "type": "sizePercentage", "width": 3},
    ]
    assert scenario1.object_classifications == []
    assert scenario1.perspectives == []
    assert scenario1.presets == []
    assert scenario1.triggers == [
        {
            "type": "includeArea",
            "vertices": [
                [-0.97, -0.97],
                [-0.97, 0.97],
                [0.97, 0.97],
                [0.97, -0.97],
            ],
        }
    ]
    assert scenario1.trigger_type == "motion"

    scenario2 = object_analytics["Device1Scenario2"]
    assert scenario2.id == "Device1Scenario2"
    assert scenario2.name == "Scenario 2"
    assert scenario2.camera == [{"id": 1}]
    assert scenario2.uid == 2
    assert scenario2.filters == [
        {"time": 1, "type": "timeShortLivedLimit"},
        {"height": 3, "type": "sizePercentage", "width": 3},
    ]
    assert scenario2.object_classifications == [{"type": "human"}]
    assert scenario2.perspectives == []
    assert scenario2.presets == []
    assert scenario2.triggers == [
        {
            "alarmDirection": "leftToRight",
            "type": "fence",
            "vertices": [[0, -0.7], [0, 0.7]],
        }
    ]
    assert scenario2.trigger_type == "fence"


response_get_configuration_empty = {
    "apiVersion": "1.0",
    "context": "Axis library",
    "data": {
        "devices": [{"id": 1, "rotation": 180, "type": "camera"}],
        "metadataOverlay": [],
        "perspectives": [],
        "scenarios": [],
        "status": {},
    },
    "method": "getConfiguration",
}


response_get_configuration = {
    "apiVersion": "1.0",
    "context": "Axis library",
    "data": {
        "devices": [{"id": 1, "rotation": 180, "type": "camera"}],
        "metadataOverlay": [],
        "perspectives": [],
        "scenarios": [
            {
                "devices": [{"id": 1}],
                "filters": [
                    {"distance": 5, "type": "distanceSwayingObject"},
                    {"time": 1, "type": "timeShortLivedLimit"},
                    {"height": 3, "type": "sizePercentage", "width": 3},
                ],
                "id": 1,
                "name": "Scenario 1",
                "objectClassifications": [],
                "perspectives": [],
                "presets": [],
                "triggers": [
                    {
                        "type": "includeArea",
                        "vertices": [
                            [-0.97, -0.97],
                            [-0.97, 0.97],
                            [0.97, 0.97],
                            [0.97, -0.97],
                        ],
                    }
                ],
                "type": "motion",
            },
            {
                "devices": [{"id": 1}],
                "filters": [
                    {"time": 1, "type": "timeShortLivedLimit"},
                    {"height": 3, "type": "sizePercentage", "width": 3},
                ],
                "id": 2,
                "name": "Scenario 2",
                "objectClassifications": [{"type": "human"}],
                "perspectives": [],
                "presets": [],
                "triggers": [
                    {
                        "alarmDirection": "leftToRight",
                        "type": "fence",
                        "vertices": [[0, -0.7], [0, 0.7]],
                    }
                ],
                "type": "fence",
            },
        ],
        "status": {},
    },
    "method": "getConfiguration",
}