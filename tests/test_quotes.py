from core.routers import quote

# TODO mock out the db
async def test_daily_q():
    res = await quote.daily_quote()
    assert isinstance(res[0], int)


async def test_approve_new_quote():
    res = await quote.approve_new_quote(1)
    print(res)


async def test_get_submitted_quote_by_id():
    res = await quote.get_submitted_quote_by_id(1)
    print(res)


async def test_get_submitted_quote_by_id_not_found():
    res = await quote.get_submitted_quote_by_id('test')
    assert res is None