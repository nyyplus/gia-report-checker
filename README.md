# GIA Report Checker


## Usage

Clone this repo:

```
git clone https://github.com/nyyplus/gia-report-checker.git
```

Then go to https://yescaptcha.com/i/5oYMnD and register your account, then get a `clientKey` from portal.

Then rename file `.env.example` to  `.env` , and edit the `.env` file:

```
MONGODB_HOST = "localhost"
MONGODB_PORT = 27017
MONGODB_DBNAME = "GiaReport"

YESCAPTCHA_CLIENT_KEY   = "<your client key>"
YESCAPTCHA_TASK_URL     = "https://api.yescaptcha.com/createTask"
YESCAPTCHA_RESPONSE_URL = "https://api.yescaptcha.com/getTaskResult"


GIA_WEBSITE_KEY = "6Ldlq7YUAAAAAB0evubQwbrUGQk8ABgyvWSeQTFO"
GIA_ENTRY_URL   = "https://data.gia.edu/RDWB/Captcha.jsp"
GIA_VERIFY_URL  = "https://data.gia.edu/RDWB/VerifyRecaptcha"

```

Next, you need to install packages:

```
pip3 install -r requirements.txt
```

At last, run demo:

```
python3 main.py
```

Result:
```bash

2022-10-19 00:40:14.333 | INFO     | app.recaptcha_resolver:resolve:23 - start to get recaptcha response data
2022-10-19 00:40:14.670 | INFO     | app.recaptcha_resolver:resolve:23 - start to get recaptcha response data
2022-10-19 00:40:14.860 | INFO     | app.recaptcha_resolver:resolve:23 - start to get recaptcha response data
2022-10-19 00:40:53.370 | INFO     | app.recaptcha_resolver:resolve:34 - submit response data to GIA
2022-10-19 00:40:54.413 | INFO     | app.recaptcha_resolver:resolve:43 - GIA verification succeeded
2022-10-19 00:40:56.972 | INFO     | app.recaptcha_resolver:resolve:34 - submit response data to GIA
2022-10-19 00:40:58.013 | INFO     | app.recaptcha_resolver:resolve:43 - GIA verification succeeded
2022-10-19 00:40:58.293 | INFO     | app.report_checker:download_pdf:51 - 7416803949:Report pdf file download complete!
2022-10-19 00:40:58.295 | INFO     | app.report_checker:save:44 - CertNo:7416803949，Report data Saved!
2022-10-19 00:41:02.648 | INFO     | app.report_checker:download_pdf:51 - 6432333562:Report pdf file download complete!
2022-10-19 00:41:02.650 | INFO     | app.report_checker:save:44 - CertNo:6432333562，Report data Saved!
2022-10-19 00:41:04.794 | INFO     | app.report_checker:download_pdf:51 - 2414612681:Report pdf file download complete!
2022-10-19 00:41:04.796 | INFO     | app.report_checker:save:44 - CertNo:2414612681，Report data Saved!
2022-10-19 00:41:06.862 | INFO     | app.report_checker:download_pdf:51 - 6371656334:Report pdf file download complete!
2022-10-19 00:41:06.864 | INFO     | app.report_checker:save:44 - CertNo:6371656334，Report data Saved!
2022-10-19 00:41:10.776 | INFO     | app.report_checker:download_pdf:51 - 2426594457:Report pdf file download complete!
2022-10-19 00:41:10.777 | INFO     | app.report_checker:save:44 - CertNo:2426594457，Report data Saved!
2022-10-19 00:41:12.058 | INFO     | app.report_checker:download_pdf:51 - 2416519405:Report pdf file download complete!
2022-10-19 00:41:12.060 | INFO     | app.report_checker:save:44 - CertNo:2416519405，Report data Saved!

```
