import asyncio
from loguru import logger
from config.app import GIA_WEBSITE_KEY, GIA_ENTRY_URL, GIA_VERIFY_URL
from config.app import YESCAPTCHA_CLIENT_KEY, YESCAPTCHA_RESPONSE_URL, YESCAPTCHA_TASK_URL

payload = {
    "clientKey": YESCAPTCHA_CLIENT_KEY,
    "task": {
        "websiteURL": GIA_ENTRY_URL,
        "websiteKey": GIA_WEBSITE_KEY,
        "type": "NoCaptchaTaskProxyless"
    }
}


class RecaptchaResolver:

    async def resolve(self, session):
        resp = await session.post(YESCAPTCHA_TASK_URL, json=payload)
        result = await resp.json()
        taskId = result.get('taskId')
        times = 0
        logger.info("start to get recaptcha response data")
        while times < 120:
            resp = await session.post(
                YESCAPTCHA_RESPONSE_URL,
                json={
                    "clientKey": YESCAPTCHA_CLIENT_KEY,
                    "taskId": taskId
                })
            result = await resp.json()
            solution = result.get('solution', {})
            if solution and solution.get("gRecaptchaResponse"):
                logger.info("submit response data to GIA")
                data = {
                    "grecaptcharesponse": solution.get("gRecaptchaResponse"),
                    "recaptcha_src": 0,
                    "reportno": "null"
                }
                resp = await session.post(GIA_VERIFY_URL, data=data)
                result = await resp.text()
                if "invalid" not in result:
                    logger.info("GIA verification succeeded")
                    return
                await self.resolve(session)
            times += 2
            await asyncio.sleep(2)
