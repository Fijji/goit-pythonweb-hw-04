import asyncio
import logging
from argparse import ArgumentParser
from aiopath import AsyncPath
from aioshutil import copyfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def read_folder(source: AsyncPath, output: AsyncPath):
    if not await source.exists():
        logger.error(f"Source folder does not exist: {source}")
        return

    async for item in source.iterdir():
        if await item.is_dir():
            await read_folder(item, output)
        elif await item.is_file():
            await copy_file(item, output)

async def copy_file(file: AsyncPath, output: AsyncPath):
    extension = file.suffix.lstrip('.') or 'no_extension'
    target_folder = output / extension
    try:
        await target_folder.mkdir(parents=True, exist_ok=True)
        target_file = target_folder / file.name
        await copyfile(file, target_file)
        logger.info(f"Copied: {file} -> {target_file}")
    except Exception as e:
        logger.error(f"Failed to copy {file} to {target_folder}: {e}")

async def main():
    parser = ArgumentParser(description="Async sort files by extension.")
    parser.add_argument("source", type=str, help="Path to the source folder.")
    parser.add_argument("output", type=str, help="Path to the output folder.")
    args = parser.parse_args()

    source = AsyncPath(args.source)
    output = AsyncPath(args.output)

    logger.info("Starting file sorting...")
    await read_folder(source, output)
    logger.info("File sorting completed.")

# python main.py test_source test_output
if __name__ == "__main__":
    asyncio.run(main())
