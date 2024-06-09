import pytest
from prepare import *
from tests.test_user import register_login_user
# 一定写在前面


from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_badge(mock_user_data, mock_badge_data, new_database):
    # 注册登录
    register_login_user(client, mock_user_data, admin=True)
    # uid1 = client.get("check_login_state").json()['uid']
    res = client.post("/uploadBadge", json=mock_badge_data)
    assert res.status_code == 200
    badges = client.post("/getBadges").json()
    assert len(badges) == 1
    assert badges[0]['badgeName'] == mock_badge_data['badgeName']
    assert badges[0]['badgeDesc'] == mock_badge_data['badgeDesc']
    assert badges[0]['badgeUrl'] == mock_badge_data['badgeUrl']
    assert badges[0]['badgeColor'] == mock_badge_data['badgeColor']
    