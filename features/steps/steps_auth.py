from behave import given, when, then

@given('I have login payload with "{email}" and "{password}"')
def step_impl(context, email, password):
    context.payload = {"email": email}
    if password.strip():   # only add password if it's not empty
        context.payload["password"] = password

@when("I POST to /login")
def step_impl(context):
    context.resp = context.client.request(
        "POST",
        "/login",
        json=context.payload,
        test_name="behave_reqres_login"
    )

@then("response status should be {status:d}")
def step_impl(context, status):
    actual = context.resp.status_code
    assert actual == status, f"Expected {status} but got {actual}"

@then('response should contain "{field}"')
def step_impl(context, field):
    j = context.resp.json()
    assert field in j, f"Expected field '{field}' in response but got: {j}"