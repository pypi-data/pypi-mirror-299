from .running.runner import main
from .running.conf import App
from .utils.config import kconfig
from .utils.pytest_util import *
from .utils.allure_util import *
from .utils.log import logger
from .page import Page
from .core.api.request import HttpReq
from .core.api.case import TestCase as TC

__version__ = "0.1.42"
__description__ = "API/安卓/IOS/WEB平台自动化测试框架"
