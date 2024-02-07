from fastapi import Request


async def parse_body(request: Request):
    raw_body = await request.body()
    return raw_body.decode("ascii")
