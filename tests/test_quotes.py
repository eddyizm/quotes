# from fastapi.testclient import TestClient
# from src.main import app
# from src.core.routers import quote


# client = TestClient(app)

# # TODO mock out the db
# async def test_daily_q():
#     res = await client.daily_quote()
#     assert isinstance(res[0], int)


# async def test_approve_new_quote():
#     res = await client.approve_new_quote(1)
#     print(res)


# async def test_get_submitted_quote_by_id():
#     res = await client.get_submitted_quote_by_id(1)
#     print(res)


# async def test_get_submitted_quote_by_id_not_found():
#     res = await client.get_submitted_quote_by_id('test')
#     assert res is None
