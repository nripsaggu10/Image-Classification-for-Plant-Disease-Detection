import asyncio

async def async_process_image(image_path):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, process_image, image_path)
