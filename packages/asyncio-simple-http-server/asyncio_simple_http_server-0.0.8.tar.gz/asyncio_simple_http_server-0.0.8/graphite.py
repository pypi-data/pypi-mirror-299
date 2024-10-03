from asyncio_simple_http_server import HttpServer, HttpResponseException, HttpRequest, HttpResponse, HttpHeaders, uri_mapping, uri_variable_mapping, uri_pattern_mapping
import logging
import asyncio


class MyHandler:
    @uri_mapping('/render', method='POST')
    def test_post(self, headers, raw_body):
      print(headers)
      print(raw_body)

async def main():
    http_server = HttpServer()
    http_server.set_http_debug_enabled(True)
    http_server.add_handler(MyHandler())
    http_server.add_default_response_headers({
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*'
    })

    await http_server.start('0.0.0.0', 57025)
    print(f'Serving on {http_server.bind_address_description()}')

    await http_server.serve_forever()

if __name__ == '__main__':
    log_format = '%(asctime)-15s %(levelname)s %(name)-8s %(filename)s %(funcName)s():%(lineno)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    asyncio.run(main())
