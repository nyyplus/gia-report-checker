import asyncio
import json
import re
import aiohttp
import numpy

from loguru import logger
from config.database import table_tasks, table_gia_reports
from app.recaptcha_resolver import RecaptchaResolver

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class ReportChecker:

    def __init__(self):
        self.report_base_url = "https://data.gia.edu/RDWB/Captcha.jsp?reportno=%s&APIno=1&"

    async def get_tasks(self) -> list:
        cursor = table_tasks.find({"HasReport": False, "CertType": "GIA"}).limit(15)
        tasks = await cursor.to_list(length=15)
        return tasks

    async def save(self, session, task):
        try:
            resp = await session.get(
                "https://data.gia.edu/RDWB/Captcha.jsp?reportno=%s&APIno=2&" % task.get("CertNo"))
            html = await resp.text()
            result = re.search(r"postMessage\('(.*)',event.origin\);", html)
            if not result:
                logger.warning("CertNo:%s，Not report data!" % task.get("CertNo"))
                return
            report_data = json.loads(result.group(1))
            await self.download_pdf(session, report_data)
        except aiohttp.ClientConnectorError as e:
            logger.error("Connector error occurred: %s" % e)
        except Exception as e:
            logger.error("Error occurred:%s" % e)
        else:
            await table_gia_reports.insert_one(report_data)
            await table_tasks.find_one_and_update(
                {"_id": task.get("_id")},
                {"$set": {"HasReport": True}})
            logger.info("CertNo:%s，Report data Saved!" % task.get("CertNo"))

    async def download_pdf(self, session, report_data: dict):
        resp = await session.get(report_data.get("PDF_URL"))
        pdf_byte_data = await resp.content.read()
        with open(f'download/%s.pdf' % report_data.get("REPORT_NO"), mode='wb') as f:
            f.write(pdf_byte_data)
            logger.info("%s:Report pdf file download complete!" % report_data.get("REPORT_NO"))

    async def check(self, tasks):
        session = aiohttp.ClientSession()
        try:
            for task in tasks:
                resp = await session.get(self.report_base_url % task.get("CertNo"))
                html = await resp.text()
                need_verify = re.search(r'id="reportReCaptcha"', html)
                if need_verify:
                    await RecaptchaResolver().resolve(session)
                await self.save(session, task)
        except asyncio.CancelledError:
            logger.warning("Task has been stopped!")
        finally:
            await session.close()

    async def start(self):
        while True:
            tasks = await self.get_tasks()
            if not tasks:
                break
            task_groups = numpy.array_split(tasks, 3)
            task_list = [asyncio.create_task(self.check(tasks)) for tasks in task_groups]
            await asyncio.wait(task_list)
