import asyncio

# Patch asyncio.coroutine if it's missing (for legacy support)
if not hasattr(asyncio, "coroutine"):
    asyncio.coroutine = lambda x: x
