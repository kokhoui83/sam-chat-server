import json
import pytest

from chat import app

@pytest.fixture()
def apigw_event():
    return {
        "queryStringParameters": {}
    }

def test_getChat(apigw_event):
    ret = app.getChat(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 400
    assert data["error"] == "missing query string parameter user"
