from core.routers import quote

# TODO mock out the db
async def test_daily_q():
    res = await quote.daily_quote()
    assert isinstance(res[0], int)