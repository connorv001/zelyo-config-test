============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.0.2, pluggy-1.6.0
rootdir: /root/projects/zelyo-ops2
configfile: pyproject.toml
testpaths: tests
plugins: asyncio-1.3.0, cov-7.0.0, anyio-4.12.1
asyncio: mode=Mode.STRICT, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 19 items

tests/test_api.py ..                                                     [ 10%]
tests/test_config.py .                                                   [ 15%]
tests/test_dockerfile.py ..                                              [ 26%]
tests/test_integration.py .                                              [ 31%]
tests/test_main.py .                                                     [ 36%]
tests/test_mcp_client.py ..                                              [ 47%]
tests/test_mcp_handshake.py .                                            [ 52%]
tests/test_mcp_tools.py .                                                [ 57%]
tests/test_models.py ...                                                 [ 73%]
tests/test_parser.py ..                                                  [ 84%]
tests/test_scanner.py ...                                                [100%]

================================ tests coverage ================================
_______________ coverage: platform linux, python 3.12.3-final-0 ________________

Name                  Stmts   Miss  Cover   Missing
---------------------------------------------------
src/__init__.py           0      0   100%
src/api/__init__.py       0      0   100%
src/api/routes.py        18      0   100%
src/main.py               8      0   100%
src/mcp_client.py        25      0   100%
src/models.py            22      0   100%
src/parser.py            15      0   100%
src/scanner.py           12      0   100%
---------------------------------------------------
TOTAL                   100      0   100%
============================= 19 passed in 19.87s ==============================
