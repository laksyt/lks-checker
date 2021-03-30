from aiohttp import TraceConfig, web

from laksyt.entities.http.timer import create_request_timer


class TestTimer:

    def test_create_request_timer(self):
        # When
        timer = create_request_timer()

        # Then
        assert timer is not None
        assert isinstance(timer, TraceConfig)

    async def test_time_request(self, aiohttp_client, loop):
        # Given
        async def route(_):
            return web.Response(text='Response')

        app = web.Application()
        app.router.add_get('/', route)
        client = await aiohttp_client(
            app,
            trace_configs=[create_request_timer()]
        )

        # When
        response = await client.get('/')

        # Then
        assert response.time is not None
        assert isinstance(response.time, float)
