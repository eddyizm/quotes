from core.routers import quote

# TODO mock out the db
async def test_daily_q():
    res = await quote.daily_quote()
    assert isinstance(res[0], int)


async def test_approve_new_quote():
    res = await quote.approve_new_quote(1)
    print(res)
