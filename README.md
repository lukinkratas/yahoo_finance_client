# YFAS - Yahoo Finance ~~Async~~ Stonks

### TODO
- [ ] (Sync) client
- ~~[ ] AsyncClient - get crumb only once~~
    - crumb set as attribute in the constructor: TypeError: __init__() should return None, not 'coroutine'
    - crumb cached_property: RuntimeError: cannot reuse already awaited coroutine
    - fetch crumb via synchronous session - not possible session (cookies) and crumb have to 1:1 (otherwise HTTP401)
- ~~[ ] modules as enum~~ - Module.QUOTE_TYPE.value usage is meh