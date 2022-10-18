import asyncio
from loguru import logger

from app.report_checker import ReportChecker

if __name__ == '__main__':
    try:
        checker = ReportChecker()
        asyncio.run(checker.start())
    except KeyboardInterrupt:
        logger.warning("Application canceled")
