# Demonstrates the api_request_context fixture (pure API testing, no browser) — see the README's
# "API testing" section. There's no locator involved in an HTTP call, so nothing here gets healed;
# what's worth demonstrating is that every request still shows up in --tamash-report with its URL,
# duration, and status code, the same as a browser action would. Uses jsonplaceholder.typicode.com,
# a stable, free, no-auth-required public test API — chosen specifically so this test doesn't
# depend on the same live demo site (or its login flow) as everything else in this repo.

BASE_URL = "https://jsonplaceholder.typicode.com"


def test_get_a_single_user(api_request_context):
    response = api_request_context.get(f"{BASE_URL}/users/1")
    assert response.status == 200

    body = response.json()
    assert body["id"] == 1
    assert "email" in body
    assert "@" in body["email"]


def test_get_posts_filtered_by_user(api_request_context):
    response = api_request_context.get(f"{BASE_URL}/posts", params={"userId": "1"})
    assert response.status == 200

    posts = response.json()
    assert len(posts) > 0
    assert all(post["userId"] == 1 for post in posts)


def test_post_creates_a_resource(api_request_context):
    response = api_request_context.post(
        f"{BASE_URL}/posts",
        data={"title": "Self-healing works", "body": "Recorded in the report too.", "userId": 1},
    )
    # jsonplaceholder is a fake API — it accepts the write and echoes back a fabricated id (201),
    # rather than persisting anything real. Still exercises and reports a real POST + JSON body.
    assert response.status == 201

    created = response.json()
    assert created["title"] == "Self-healing works"
    assert created["id"] is not None
