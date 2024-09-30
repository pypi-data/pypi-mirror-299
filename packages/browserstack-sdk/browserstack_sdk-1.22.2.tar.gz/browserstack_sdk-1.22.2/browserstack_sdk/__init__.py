# coding: UTF-8
import sys
bstack1l1ll1l_opy_ = sys.version_info [0] == 2
bstack11llll1_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1lll1l1_opy_ (bstack11ll1l1_opy_):
    global bstack1l111ll_opy_
    bstack111ll1l_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack1l1_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack11ll1l_opy_ = bstack111ll1l_opy_ % len (bstack1l1_opy_)
    bstack1llll1l_opy_ = bstack1l1_opy_ [:bstack11ll1l_opy_] + bstack1l1_opy_ [bstack11ll1l_opy_:]
    if bstack1l1ll1l_opy_:
        bstack111l1_opy_ = unicode () .join ([unichr (ord (char) - bstack11llll1_opy_ - (bstack1ll11_opy_ + bstack111ll1l_opy_) % bstack11l111l_opy_) for bstack1ll11_opy_, char in enumerate (bstack1llll1l_opy_)])
    else:
        bstack111l1_opy_ = str () .join ([chr (ord (char) - bstack11llll1_opy_ - (bstack1ll11_opy_ + bstack111ll1l_opy_) % bstack11l111l_opy_) for bstack1ll11_opy_, char in enumerate (bstack1llll1l_opy_)])
    return eval (bstack111l1_opy_)
import atexit
import os
import signal
import sys
import yaml
import requests
import logging
import threading
import socket
import datetime
import string
import random
import json
import collections.abc
import re
import multiprocessing
import traceback
import copy
import tempfile
from packaging import version
from uuid import uuid4
from browserstack.local import Local
from urllib.parse import urlparse
from dotenv import load_dotenv
from bstack_utils.constants import *
from bstack_utils.percy import *
from browserstack_sdk.bstack1l1111l1ll_opy_ import *
from bstack_utils.percy_sdk import PercySDK
from bstack_utils.bstack11ll1l11_opy_ import bstack1l11l11l1l_opy_
import time
import requests
def bstack1l111lll_opy_():
  global CONFIG
  headers = {
        bstack1lll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩࡶ"): bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧࡷ"),
      }
  proxies = bstack111111ll1_opy_(CONFIG, bstack11ll1ll11_opy_)
  try:
    response = requests.get(bstack11ll1ll11_opy_, headers=headers, proxies=proxies, timeout=5)
    if response.json():
      bstack1lll11lll1_opy_ = response.json()[bstack1lll1l1_opy_ (u"ࠬ࡮ࡵࡣࡵࠪࡸ")]
      logger.debug(bstack1l1lll11l_opy_.format(response.json()))
      return bstack1lll11lll1_opy_
    else:
      logger.debug(bstack1111l1111_opy_.format(bstack1lll1l1_opy_ (u"ࠨࡒࡦࡵࡳࡳࡳࡹࡥࠡࡌࡖࡓࡓࠦࡰࡢࡴࡶࡩࠥ࡫ࡲࡳࡱࡵࠤࠧࡹ")))
  except Exception as e:
    logger.debug(bstack1111l1111_opy_.format(e))
def bstack1ll1l1ll1l_opy_(hub_url):
  global CONFIG
  url = bstack1lll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤࡺ")+  hub_url + bstack1lll1l1_opy_ (u"ࠣ࠱ࡦ࡬ࡪࡩ࡫ࠣࡻ")
  headers = {
        bstack1lll1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡸࡾࡶࡥࠨࡼ"): bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ࡽ"),
      }
  proxies = bstack111111ll1_opy_(CONFIG, url)
  try:
    start_time = time.perf_counter()
    requests.get(url, headers=headers, proxies=proxies, timeout=5)
    latency = time.perf_counter() - start_time
    logger.debug(bstack1ll1lllll_opy_.format(hub_url, latency))
    return dict(hub_url=hub_url, latency=latency)
  except Exception as e:
    logger.debug(bstack1l1l111ll1_opy_.format(hub_url, e))
def bstack1l1111llll_opy_():
  try:
    global bstack1ll1l1ll_opy_
    bstack1lll11lll1_opy_ = bstack1l111lll_opy_()
    bstack1l1lll1ll_opy_ = []
    results = []
    for bstack1l11l11lll_opy_ in bstack1lll11lll1_opy_:
      bstack1l1lll1ll_opy_.append(bstack1ll1ll1lll_opy_(target=bstack1ll1l1ll1l_opy_,args=(bstack1l11l11lll_opy_,)))
    for t in bstack1l1lll1ll_opy_:
      t.start()
    for t in bstack1l1lll1ll_opy_:
      results.append(t.join())
    bstack11l111l11_opy_ = {}
    for item in results:
      hub_url = item[bstack1lll1l1_opy_ (u"ࠫ࡭ࡻࡢࡠࡷࡵࡰࠬࡾ")]
      latency = item[bstack1lll1l1_opy_ (u"ࠬࡲࡡࡵࡧࡱࡧࡾ࠭ࡿ")]
      bstack11l111l11_opy_[hub_url] = latency
    bstack1l1l11ll1l_opy_ = min(bstack11l111l11_opy_, key= lambda x: bstack11l111l11_opy_[x])
    bstack1ll1l1ll_opy_ = bstack1l1l11ll1l_opy_
    logger.debug(bstack1l1l1111l1_opy_.format(bstack1l1l11ll1l_opy_))
  except Exception as e:
    logger.debug(bstack11ll11ll_opy_.format(e))
from bstack_utils.messages import *
from bstack_utils import bstack1l11ll1111_opy_
from bstack_utils.config import Config
from bstack_utils.helper import bstack1lll1l1lll_opy_, bstack1l1ll1l11_opy_, bstack1lll11111l_opy_, bstack1llll1l1ll_opy_, bstack1l1111ll11_opy_, \
  Notset, bstack111111lll_opy_, \
  bstack11l1ll11l_opy_, bstack1l11l1ll1_opy_, bstack1l1l1l1lll_opy_, bstack1llll1111_opy_, bstack1llllll1l1_opy_, bstack1l11l11111_opy_, \
  bstack1l1l1l11_opy_, \
  bstack1ll1l11lll_opy_, bstack11l11111_opy_, bstack1l11llll11_opy_, bstack1lllll1ll_opy_, \
  bstack1l1l11l1l1_opy_, bstack111ll111l_opy_, bstack11ll1l1l1_opy_, bstack1l1l11lll_opy_
from bstack_utils.bstack1l1l11ll1_opy_ import bstack1lll111l11_opy_
from bstack_utils.bstack1l1lll1ll1_opy_ import bstack1l11l1lll1_opy_
from bstack_utils.bstack1l1l111lll_opy_ import bstack1l11ll11l1_opy_, bstack11lll1ll1_opy_
from bstack_utils.bstack1l1ll11l1_opy_ import bstack1l1lll1lll_opy_
from bstack_utils.bstack1l1llll1ll_opy_ import bstack1llllll1ll_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack1l1lllllll_opy_
from bstack_utils.proxy import bstack1ll1ll1l1_opy_, bstack111111ll1_opy_, bstack1l1ll1ll11_opy_, bstack1lll1lll1l_opy_
import bstack_utils.bstack1l1l1ll1ll_opy_ as bstack1111ll1l_opy_
from browserstack_sdk.bstack1111ll1l1_opy_ import *
from browserstack_sdk.bstack1l1llllll_opy_ import *
from bstack_utils.bstack11l11ll1l_opy_ import bstack1l11l11l_opy_
from browserstack_sdk.bstack1llll1ll_opy_ import *
import bstack_utils.bstack1llll1l11l_opy_ as bstack1ll1l1111_opy_
import bstack_utils.bstack1l1lllll1l_opy_ as bstack1ll1ll11l_opy_
bstack11111111_opy_ = bstack1lll1l1_opy_ (u"࠭ࠠࠡ࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳࠦࠠࡪࡨࠫࡴࡦ࡭ࡥࠡ࠿ࡀࡁࠥࡼ࡯ࡪࡦࠣ࠴࠮ࠦࡻ࡝ࡰࠣࠤࠥࡺࡲࡺࡽ࡟ࡲࠥࡩ࡯࡯ࡵࡷࠤ࡫ࡹࠠ࠾ࠢࡵࡩࡶࡻࡩࡳࡧࠫࡠࠬ࡬ࡳ࡝ࠩࠬ࠿ࡡࡴࠠࠡࠢࠣࠤ࡫ࡹ࠮ࡢࡲࡳࡩࡳࡪࡆࡪ࡮ࡨࡗࡾࡴࡣࠩࡤࡶࡸࡦࡩ࡫ࡠࡲࡤࡸ࡭࠲ࠠࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡲࡢ࡭ࡳࡪࡥࡹࠫࠣ࠯ࠥࠨ࠺ࠣࠢ࠮ࠤࡏ࡙ࡏࡏ࠰ࡶࡸࡷ࡯࡮ࡨ࡫ࡩࡽ࠭ࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࠫࡥࡼࡧࡩࡵࠢࡱࡩࡼࡖࡡࡨࡧ࠵࠲ࡪࡼࡡ࡭ࡷࡤࡸࡪ࠮ࠢࠩࠫࠣࡁࡃࠦࡻࡾࠤ࠯ࠤࡡ࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡧࡦࡶࡖࡩࡸࡹࡩࡰࡰࡇࡩࡹࡧࡩ࡭ࡵࠥࢁࡡ࠭ࠩࠪࠫ࡞ࠦ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠢ࡞ࠫࠣ࠯ࠥࠨࠬ࡝࡞ࡱࠦ࠮ࡢ࡮ࠡࠢࠣࠤࢂࡩࡡࡵࡥ࡫ࠬࡪࡾࠩࡼ࡞ࡱࠤࠥࠦࠠࡾ࡞ࡱࠤࠥࢃ࡜࡯ࠢࠣ࠳࠯ࠦ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࠣ࠮࠴࠭ࢀ")
bstack111lll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠧ࡝ࡰ࠲࠮ࠥࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾ࠢ࠭࠳ࡡࡴࡣࡰࡰࡶࡸࠥࡨࡳࡵࡣࡦ࡯ࡤࡶࡡࡵࡪࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࡟ࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸ࠱ࡰࡪࡴࡧࡵࡪࠣ࠱ࠥ࠹࡝࡝ࡰࡦࡳࡳࡹࡴࠡࡤࡶࡸࡦࡩ࡫ࡠࡥࡤࡴࡸࠦ࠽ࠡࡲࡵࡳࡨ࡫ࡳࡴ࠰ࡤࡶ࡬ࡼ࡛ࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻ࠴࡬ࡦࡰࡪࡸ࡭ࠦ࠭ࠡ࠳ࡠࡠࡳࡩ࡯࡯ࡵࡷࠤࡵࡥࡩ࡯ࡦࡨࡼࠥࡃࠠࡱࡴࡲࡧࡪࡹࡳ࠯ࡣࡵ࡫ࡻࡡࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠳࡟࡟ࡲࡵࡸ࡯ࡤࡧࡶࡷ࠳ࡧࡲࡨࡸࠣࡁࠥࡶࡲࡰࡥࡨࡷࡸ࠴ࡡࡳࡩࡹ࠲ࡸࡲࡩࡤࡧࠫ࠴࠱ࠦࡰࡳࡱࡦࡩࡸࡹ࠮ࡢࡴࡪࡺ࠳ࡲࡥ࡯ࡩࡷ࡬ࠥ࠳ࠠ࠴ࠫ࡟ࡲࡨࡵ࡮ࡴࡶࠣ࡭ࡲࡶ࡯ࡳࡶࡢࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠴ࡠࡤࡶࡸࡦࡩ࡫ࠡ࠿ࠣࡶࡪࡷࡵࡪࡴࡨࠬࠧࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࠤࠬ࠿ࡡࡴࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴࡬ࡢࡷࡱࡧ࡭ࠦ࠽ࠡࡣࡶࡽࡳࡩࠠࠩ࡮ࡤࡹࡳࡩࡨࡐࡲࡷ࡭ࡴࡴࡳࠪࠢࡀࡂࠥࢁ࡜࡯࡮ࡨࡸࠥࡩࡡࡱࡵ࠾ࡠࡳࡺࡲࡺࠢࡾࡠࡳࡩࡡࡱࡵࠣࡁࠥࡐࡓࡐࡐ࠱ࡴࡦࡸࡳࡦࠪࡥࡷࡹࡧࡣ࡬ࡡࡦࡥࡵࡹࠩ࡝ࡰࠣࠤࢂࠦࡣࡢࡶࡦ࡬࠭࡫ࡸࠪࠢࡾࡠࡳࠦࠠࠡࠢࢀࡠࡳࠦࠠࡳࡧࡷࡹࡷࡴࠠࡢࡹࡤ࡭ࡹࠦࡩ࡮ࡲࡲࡶࡹࡥࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠷ࡣࡧࡹࡴࡢࡥ࡮࠲ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠴ࡣࡰࡰࡱࡩࡨࡺࠨࡼ࡞ࡱࠤࠥࠦࠠࡸࡵࡈࡲࡩࡶ࡯ࡪࡰࡷ࠾ࠥࡦࡷࡴࡵ࠽࠳࠴ࡩࡤࡱ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵࡁࡦࡥࡵࡹ࠽ࠥࡽࡨࡲࡨࡵࡤࡦࡗࡕࡍࡈࡵ࡭ࡱࡱࡱࡩࡳࡺࠨࡋࡕࡒࡒ࠳ࡹࡴࡳ࡫ࡱ࡫࡮࡬ࡹࠩࡥࡤࡴࡸ࠯ࠩࡾࡢ࠯ࡠࡳࠦࠠࠡࠢ࠱࠲࠳ࡲࡡࡶࡰࡦ࡬ࡔࡶࡴࡪࡱࡱࡷࡡࡴࠠࠡࡿࠬࡠࡳࢃ࡜࡯࠱࠭ࠤࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽࠾࠿ࡀࡁࡂࡃ࠽ࠡࠬ࠲ࡠࡳ࠭ࢁ")
from ._version import __version__
bstack1l1l1l11ll_opy_ = None
CONFIG = {}
bstack1ll1ll11_opy_ = {}
bstack1ll111l1l_opy_ = {}
bstack11l1l111l_opy_ = None
bstack111ll1lll_opy_ = None
bstack1l111l1ll_opy_ = None
bstack11l1llll_opy_ = -1
bstack11lll1lll_opy_ = 0
bstack1l1l111l1l_opy_ = bstack1llll111_opy_
bstack11l1l11ll_opy_ = 1
bstack11l1l1l11_opy_ = False
bstack1l1l11111l_opy_ = False
bstack1l111llll_opy_ = bstack1lll1l1_opy_ (u"ࠨࠩࢂ")
bstack1ll11l1111_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪࢃ")
bstack11lll1ll_opy_ = False
bstack1l1l1ll11l_opy_ = True
bstack111lllll_opy_ = bstack1lll1l1_opy_ (u"ࠪࠫࢄ")
bstack11l1l1ll1_opy_ = []
bstack1ll1l1ll_opy_ = bstack1lll1l1_opy_ (u"ࠫࠬࢅ")
bstack1l1ll11l_opy_ = False
bstack1l111l11l1_opy_ = None
bstack1l1ll1l1l_opy_ = None
bstack1ll1l11l_opy_ = None
bstack1l1l11l1l_opy_ = -1
bstack1l111lllll_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠬࢄࠧࢆ")), bstack1lll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ࢇ"), bstack1lll1l1_opy_ (u"ࠧ࠯ࡴࡲࡦࡴࡺ࠭ࡳࡧࡳࡳࡷࡺ࠭ࡩࡧ࡯ࡴࡪࡸ࠮࡫ࡵࡲࡲࠬ࢈"))
bstack111l1l1l_opy_ = 0
bstack1l1lll111l_opy_ = 0
bstack1ll111lll1_opy_ = []
bstack1l111ll1_opy_ = []
bstack11l1lll1l_opy_ = []
bstack1l1lllll1_opy_ = []
bstack11l111ll_opy_ = bstack1lll1l1_opy_ (u"ࠨࠩࢉ")
bstack1111111l_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪࢊ")
bstack1ll1ll11l1_opy_ = False
bstack1l1l111l11_opy_ = False
bstack1111lll11_opy_ = {}
bstack11l111lll_opy_ = None
bstack1l1l1111l_opy_ = None
bstack1l1llllll1_opy_ = None
bstack1l1ll1ll1_opy_ = None
bstack11l1l1111_opy_ = None
bstack1ll1l11ll1_opy_ = None
bstack1l1111111_opy_ = None
bstack111ll1ll_opy_ = None
bstack11l11l11l_opy_ = None
bstack1lll1l1ll1_opy_ = None
bstack1l1l1ll111_opy_ = None
bstack11lll1l1_opy_ = None
bstack1ll11ll11l_opy_ = None
bstack11l1ll11_opy_ = None
bstack1ll1lll1l1_opy_ = None
bstack111l111l_opy_ = None
bstack1llll1l1l1_opy_ = None
bstack1ll11l1lll_opy_ = None
bstack111l1lll_opy_ = None
bstack1l11l111l1_opy_ = None
bstack1l1l1ll1_opy_ = None
bstack1lllllll1_opy_ = None
bstack1l1l1ll1l_opy_ = False
bstack1111ll11l_opy_ = bstack1lll1l1_opy_ (u"ࠥࠦࢋ")
logger = bstack1l11ll1111_opy_.get_logger(__name__, bstack1l1l111l1l_opy_)
bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
percy = bstack1ll111l1l1_opy_()
bstack11llll111_opy_ = bstack1l11l11l1l_opy_()
bstack111llll1_opy_ = bstack1llll1ll_opy_()
def bstack1llll1ll1_opy_():
  global CONFIG
  global bstack1ll1ll11l1_opy_
  global bstack1lll11l1ll_opy_
  bstack1ll1ll111_opy_ = bstack1111l1l11_opy_(CONFIG)
  if bstack1l1111ll11_opy_(CONFIG):
    if (bstack1lll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡕࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ࢌ") in bstack1ll1ll111_opy_ and str(bstack1ll1ll111_opy_[bstack1lll1l1_opy_ (u"ࠬࡹ࡫ࡪࡲࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧࢍ")]).lower() == bstack1lll1l1_opy_ (u"࠭ࡴࡳࡷࡨࠫࢎ")):
      bstack1ll1ll11l1_opy_ = True
    bstack1lll11l1ll_opy_.bstack1l1lll1l11_opy_(bstack1ll1ll111_opy_.get(bstack1lll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡘ࡫ࡳࡴ࡫ࡲࡲࡘࡺࡡࡵࡷࡶࠫ࢏"), False))
  else:
    bstack1ll1ll11l1_opy_ = True
    bstack1lll11l1ll_opy_.bstack1l1lll1l11_opy_(True)
def bstack1lllll1lll_opy_():
  from appium.version import version as appium_version
  return version.parse(appium_version)
def bstack1l1l1l111_opy_():
  from selenium import webdriver
  return version.parse(webdriver.__version__)
def bstack111llllll_opy_():
  args = sys.argv
  for i in range(len(args)):
    if bstack1lll1l1_opy_ (u"ࠣ࠯࠰ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡥࡲࡲ࡫࡯ࡧࡧ࡫࡯ࡩࠧ࢐") == args[i].lower() or bstack1lll1l1_opy_ (u"ࠤ࠰࠱ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡧࡴࡴࡦࡪࡩࠥ࢑") == args[i].lower():
      path = args[i + 1]
      sys.argv.remove(args[i])
      sys.argv.remove(path)
      global bstack111lllll_opy_
      bstack111lllll_opy_ += bstack1lll1l1_opy_ (u"ࠪ࠱࠲ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠠࠨ࢒") + path
      return path
  return None
bstack11llllll1l_opy_ = re.compile(bstack1lll1l1_opy_ (u"ࡶࠧ࠴ࠪࡀ࡞ࠧࡿ࠭࠴ࠪࡀࠫࢀ࠲࠯ࡅࠢ࢓"))
def bstack111ll111_opy_(loader, node):
  value = loader.construct_scalar(node)
  for group in bstack11llllll1l_opy_.findall(value):
    if group is not None and os.environ.get(group) is not None:
      value = value.replace(bstack1lll1l1_opy_ (u"ࠧࠪࡻࠣ࢔") + group + bstack1lll1l1_opy_ (u"ࠨࡽࠣ࢕"), os.environ.get(group))
  return value
def bstack111lllll1_opy_():
  bstack111l111l1_opy_ = bstack111llllll_opy_()
  if bstack111l111l1_opy_ and os.path.exists(os.path.abspath(bstack111l111l1_opy_)):
    fileName = bstack111l111l1_opy_
  if bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡃࡐࡐࡉࡍࡌࡥࡆࡊࡎࡈࠫ࢖") in os.environ and os.path.exists(
          os.path.abspath(os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍ࡟ࡇࡋࡏࡉࠬࢗ")])) and not bstack1lll1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫ࡎࡢ࡯ࡨࠫ࢘") in locals():
    fileName = os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡆࡓࡓࡌࡉࡈࡡࡉࡍࡑࡋ࢙ࠧ")]
  if bstack1lll1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡐࡤࡱࡪ࢚࠭") in locals():
    bstack11ll11l_opy_ = os.path.abspath(fileName)
  else:
    bstack11ll11l_opy_ = bstack1lll1l1_opy_ (u"࢛ࠬ࠭")
  bstack1ll1ll1ll1_opy_ = os.getcwd()
  bstack11111ll11_opy_ = bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡿ࡭࡭ࠩ࢜")
  bstack1lllll1ll1_opy_ = bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡹࡢ࡯࡯ࠫ࢝")
  while (not os.path.exists(bstack11ll11l_opy_)) and bstack1ll1ll1ll1_opy_ != bstack1lll1l1_opy_ (u"ࠣࠤ࢞"):
    bstack11ll11l_opy_ = os.path.join(bstack1ll1ll1ll1_opy_, bstack11111ll11_opy_)
    if not os.path.exists(bstack11ll11l_opy_):
      bstack11ll11l_opy_ = os.path.join(bstack1ll1ll1ll1_opy_, bstack1lllll1ll1_opy_)
    if bstack1ll1ll1ll1_opy_ != os.path.dirname(bstack1ll1ll1ll1_opy_):
      bstack1ll1ll1ll1_opy_ = os.path.dirname(bstack1ll1ll1ll1_opy_)
    else:
      bstack1ll1ll1ll1_opy_ = bstack1lll1l1_opy_ (u"ࠤࠥ࢟")
  if not os.path.exists(bstack11ll11l_opy_):
    bstack1llll1l1l_opy_(
      bstack1ll1llll11_opy_.format(os.getcwd()))
  try:
    with open(bstack11ll11l_opy_, bstack1lll1l1_opy_ (u"ࠪࡶࠬࢠ")) as stream:
      yaml.add_implicit_resolver(bstack1lll1l1_opy_ (u"ࠦࠦࡶࡡࡵࡪࡨࡼࠧࢡ"), bstack11llllll1l_opy_)
      yaml.add_constructor(bstack1lll1l1_opy_ (u"ࠧࠧࡰࡢࡶ࡫ࡩࡽࠨࢢ"), bstack111ll111_opy_)
      config = yaml.load(stream, yaml.FullLoader)
      return config
  except:
    with open(bstack11ll11l_opy_, bstack1lll1l1_opy_ (u"࠭ࡲࠨࢣ")) as stream:
      try:
        config = yaml.safe_load(stream)
        return config
      except yaml.YAMLError as exc:
        bstack1llll1l1l_opy_(bstack111l11ll_opy_.format(str(exc)))
def bstack1l111l1l1_opy_(config):
  bstack1ll1lll1_opy_ = bstack1l1llll11_opy_(config)
  for option in list(bstack1ll1lll1_opy_):
    if option.lower() in bstack11lll11ll_opy_ and option != bstack11lll11ll_opy_[option.lower()]:
      bstack1ll1lll1_opy_[bstack11lll11ll_opy_[option.lower()]] = bstack1ll1lll1_opy_[option]
      del bstack1ll1lll1_opy_[option]
  return config
def bstack1ll11ll111_opy_():
  global bstack1ll111l1l_opy_
  for key, bstack11l1l11l1_opy_ in bstack11ll1lll1_opy_.items():
    if isinstance(bstack11l1l11l1_opy_, list):
      for var in bstack11l1l11l1_opy_:
        if var in os.environ and os.environ[var] and str(os.environ[var]).strip():
          bstack1ll111l1l_opy_[key] = os.environ[var]
          break
    elif bstack11l1l11l1_opy_ in os.environ and os.environ[bstack11l1l11l1_opy_] and str(os.environ[bstack11l1l11l1_opy_]).strip():
      bstack1ll111l1l_opy_[key] = os.environ[bstack11l1l11l1_opy_]
  if bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡌࡐࡅࡄࡐࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩࢤ") in os.environ:
    bstack1ll111l1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢥ")] = {}
    bstack1ll111l1l_opy_[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢦ")][bstack1lll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࢧ")] = os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡐࡔࡉࡁࡍࡡࡌࡈࡊࡔࡔࡊࡈࡌࡉࡗ࠭ࢨ")]
def bstack1l11111ll_opy_():
  global bstack1ll1ll11_opy_
  global bstack111lllll_opy_
  for idx, val in enumerate(sys.argv):
    if idx < len(sys.argv) and bstack1lll1l1_opy_ (u"ࠬ࠳࠭ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡬ࡰࡥࡤࡰࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࢩ").lower() == val.lower():
      bstack1ll1ll11_opy_[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪࢪ")] = {}
      bstack1ll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢫ")][bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࢬ")] = sys.argv[idx + 1]
      del sys.argv[idx:idx + 2]
      break
  for key, bstack1l11l1l11_opy_ in bstack11l11l111_opy_.items():
    if isinstance(bstack1l11l1l11_opy_, list):
      for idx, val in enumerate(sys.argv):
        for var in bstack1l11l1l11_opy_:
          if idx < len(sys.argv) and bstack1lll1l1_opy_ (u"ࠩ࠰࠱ࠬࢭ") + var.lower() == val.lower() and not key in bstack1ll1ll11_opy_:
            bstack1ll1ll11_opy_[key] = sys.argv[idx + 1]
            bstack111lllll_opy_ += bstack1lll1l1_opy_ (u"ࠪࠤ࠲࠳ࠧࢮ") + var + bstack1lll1l1_opy_ (u"ࠫࠥ࠭ࢯ") + sys.argv[idx + 1]
            del sys.argv[idx:idx + 2]
            break
    else:
      for idx, val in enumerate(sys.argv):
        if idx < len(sys.argv) and bstack1lll1l1_opy_ (u"ࠬ࠳࠭ࠨࢰ") + bstack1l11l1l11_opy_.lower() == val.lower() and not key in bstack1ll1ll11_opy_:
          bstack1ll1ll11_opy_[key] = sys.argv[idx + 1]
          bstack111lllll_opy_ += bstack1lll1l1_opy_ (u"࠭ࠠ࠮࠯ࠪࢱ") + bstack1l11l1l11_opy_ + bstack1lll1l1_opy_ (u"ࠧࠡࠩࢲ") + sys.argv[idx + 1]
          del sys.argv[idx:idx + 2]
def bstack1llll111ll_opy_(config):
  bstack1l1ll111ll_opy_ = config.keys()
  for bstack1ll1111ll1_opy_, bstack1l111ll111_opy_ in bstack1ll11ll1l_opy_.items():
    if bstack1l111ll111_opy_ in bstack1l1ll111ll_opy_:
      config[bstack1ll1111ll1_opy_] = config[bstack1l111ll111_opy_]
      del config[bstack1l111ll111_opy_]
  for bstack1ll1111ll1_opy_, bstack1l111ll111_opy_ in bstack111111l1_opy_.items():
    if isinstance(bstack1l111ll111_opy_, list):
      for bstack111l11ll1_opy_ in bstack1l111ll111_opy_:
        if bstack111l11ll1_opy_ in bstack1l1ll111ll_opy_:
          config[bstack1ll1111ll1_opy_] = config[bstack111l11ll1_opy_]
          del config[bstack111l11ll1_opy_]
          break
    elif bstack1l111ll111_opy_ in bstack1l1ll111ll_opy_:
      config[bstack1ll1111ll1_opy_] = config[bstack1l111ll111_opy_]
      del config[bstack1l111ll111_opy_]
  for bstack111l11ll1_opy_ in list(config):
    for bstack1111l1ll_opy_ in bstack1l111ll11_opy_:
      if bstack111l11ll1_opy_.lower() == bstack1111l1ll_opy_.lower() and bstack111l11ll1_opy_ != bstack1111l1ll_opy_:
        config[bstack1111l1ll_opy_] = config[bstack111l11ll1_opy_]
        del config[bstack111l11ll1_opy_]
  bstack1111ll11_opy_ = [{}]
  if not config.get(bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫࢳ")):
    config[bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࢴ")] = [{}]
  bstack1111ll11_opy_ = config[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࢵ")]
  for platform in bstack1111ll11_opy_:
    for bstack111l11ll1_opy_ in list(platform):
      for bstack1111l1ll_opy_ in bstack1l111ll11_opy_:
        if bstack111l11ll1_opy_.lower() == bstack1111l1ll_opy_.lower() and bstack111l11ll1_opy_ != bstack1111l1ll_opy_:
          platform[bstack1111l1ll_opy_] = platform[bstack111l11ll1_opy_]
          del platform[bstack111l11ll1_opy_]
  for bstack1ll1111ll1_opy_, bstack1l111ll111_opy_ in bstack111111l1_opy_.items():
    for platform in bstack1111ll11_opy_:
      if isinstance(bstack1l111ll111_opy_, list):
        for bstack111l11ll1_opy_ in bstack1l111ll111_opy_:
          if bstack111l11ll1_opy_ in platform:
            platform[bstack1ll1111ll1_opy_] = platform[bstack111l11ll1_opy_]
            del platform[bstack111l11ll1_opy_]
            break
      elif bstack1l111ll111_opy_ in platform:
        platform[bstack1ll1111ll1_opy_] = platform[bstack1l111ll111_opy_]
        del platform[bstack1l111ll111_opy_]
  for bstack1l11l11l11_opy_ in bstack11l11lll1_opy_:
    if bstack1l11l11l11_opy_ in config:
      if not bstack11l11lll1_opy_[bstack1l11l11l11_opy_] in config:
        config[bstack11l11lll1_opy_[bstack1l11l11l11_opy_]] = {}
      config[bstack11l11lll1_opy_[bstack1l11l11l11_opy_]].update(config[bstack1l11l11l11_opy_])
      del config[bstack1l11l11l11_opy_]
  for platform in bstack1111ll11_opy_:
    for bstack1l11l11l11_opy_ in bstack11l11lll1_opy_:
      if bstack1l11l11l11_opy_ in list(platform):
        if not bstack11l11lll1_opy_[bstack1l11l11l11_opy_] in platform:
          platform[bstack11l11lll1_opy_[bstack1l11l11l11_opy_]] = {}
        platform[bstack11l11lll1_opy_[bstack1l11l11l11_opy_]].update(platform[bstack1l11l11l11_opy_])
        del platform[bstack1l11l11l11_opy_]
  config = bstack1l111l1l1_opy_(config)
  return config
def bstack1lll11111_opy_(config):
  global bstack1ll11l1111_opy_
  if bstack1l1111ll11_opy_(config) and bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨࢶ") in config and str(config[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩࢷ")]).lower() != bstack1lll1l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬࢸ"):
    if not bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫࢹ") in config:
      config[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࡌࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬࢺ")] = {}
    if not config[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࢻ")].get(bstack1lll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡃ࡫ࡱࡥࡷࡿࡉ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡣࡷ࡭ࡴࡴࠧࢼ")) and not bstack1lll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࢽ") in config[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩࢾ")]:
      bstack1l11lll111_opy_ = datetime.datetime.now()
      bstack1lll1lllll_opy_ = bstack1l11lll111_opy_.strftime(bstack1lll1l1_opy_ (u"࠭ࠥࡥࡡࠨࡦࡤࠫࡈࠦࡏࠪࢿ"))
      hostname = socket.gethostname()
      bstack1l1111ll1l_opy_ = bstack1lll1l1_opy_ (u"ࠧࠨࣀ").join(random.choices(string.ascii_lowercase + string.digits, k=4))
      identifier = bstack1lll1l1_opy_ (u"ࠨࡽࢀࡣࢀࢃ࡟ࡼࡿࠪࣁ").format(bstack1lll1lllll_opy_, hostname, bstack1l1111ll1l_opy_)
      config[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ࣂ")][bstack1lll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣃ")] = identifier
    bstack1ll11l1111_opy_ = config[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨࣄ")].get(bstack1lll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧࣅ"))
  return config
def bstack1ll1l1l1l1_opy_():
  bstack1l1l11l11_opy_ =  bstack1llll1111_opy_()[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠬࣆ")]
  return bstack1l1l11l11_opy_ if bstack1l1l11l11_opy_ else -1
def bstack11111l1ll_opy_(bstack1l1l11l11_opy_):
  global CONFIG
  if not bstack1lll1l1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣇ") in CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣈ")]:
    return
  CONFIG[bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫࣉ")] = CONFIG[bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ࣊")].replace(
    bstack1lll1l1_opy_ (u"ࠫࠩࢁࡂࡖࡋࡏࡈࡤࡔࡕࡎࡄࡈࡖࢂ࠭࣋"),
    str(bstack1l1l11l11_opy_)
  )
def bstack1l1l11111_opy_():
  global CONFIG
  if not bstack1lll1l1_opy_ (u"ࠬࠪࡻࡅࡃࡗࡉࡤ࡚ࡉࡎࡇࢀࠫ࣌") in CONFIG[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ࣍")]:
    return
  bstack1l11lll111_opy_ = datetime.datetime.now()
  bstack1lll1lllll_opy_ = bstack1l11lll111_opy_.strftime(bstack1lll1l1_opy_ (u"ࠧࠦࡦ࠰ࠩࡧ࠳ࠥࡉ࠼ࠨࡑࠬ࣎"))
  CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴ࣏ࠪ")] = CONFIG[bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵ࣐ࠫ")].replace(
    bstack1lll1l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾ࣑ࠩ"),
    bstack1lll1lllll_opy_
  )
def bstack11111l11l_opy_():
  global CONFIG
  if bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࣒࠭") in CONFIG and not bool(CONFIG[bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸ࣓ࠧ")]):
    del CONFIG[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣔ")]
    return
  if not bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩࣕ") in CONFIG:
    CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣖ")] = bstack1lll1l1_opy_ (u"ࠩࠦࠨࢀࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࢁࠬࣗ")
  if bstack1lll1l1_opy_ (u"ࠪࠨࢀࡊࡁࡕࡇࡢࡘࡎࡓࡅࡾࠩࣘ") in CONFIG[bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ࣙ")]:
    bstack1l1l11111_opy_()
    os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡤࡉࡏࡎࡄࡌࡒࡊࡊ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠩࣚ")] = CONFIG[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨࣛ")]
  if not bstack1lll1l1_opy_ (u"ࠧࠥࡽࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࡾࠩࣜ") in CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪࣝ")]:
    return
  bstack1l1l11l11_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪࣞ")
  bstack1ll11l11l_opy_ = bstack1ll1l1l1l1_opy_()
  if bstack1ll11l11l_opy_ != -1:
    bstack1l1l11l11_opy_ = bstack1lll1l1_opy_ (u"ࠪࡇࡎࠦࠧࣟ") + str(bstack1ll11l11l_opy_)
  if bstack1l1l11l11_opy_ == bstack1lll1l1_opy_ (u"ࠫࠬ࣠"):
    bstack1l1ll11ll1_opy_ = bstack111ll1111_opy_(CONFIG[bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࣡")])
    if bstack1l1ll11ll1_opy_ != -1:
      bstack1l1l11l11_opy_ = str(bstack1l1ll11ll1_opy_)
  if bstack1l1l11l11_opy_:
    bstack11111l1ll_opy_(bstack1l1l11l11_opy_)
    os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪ࣢")] = CONFIG[bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࣣࠩ")]
def bstack1ll1111lll_opy_(bstack1ll1ll1l11_opy_, bstack1111l11ll_opy_, path):
  bstack1lll1ll111_opy_ = {
    bstack1lll1l1_opy_ (u"ࠨ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬࣤ"): bstack1111l11ll_opy_
  }
  if os.path.exists(path):
    bstack1l11111l11_opy_ = json.load(open(path, bstack1lll1l1_opy_ (u"ࠩࡵࡦࠬࣥ")))
  else:
    bstack1l11111l11_opy_ = {}
  bstack1l11111l11_opy_[bstack1ll1ll1l11_opy_] = bstack1lll1ll111_opy_
  with open(path, bstack1lll1l1_opy_ (u"ࠥࡻ࠰ࠨࣦ")) as outfile:
    json.dump(bstack1l11111l11_opy_, outfile)
def bstack111ll1111_opy_(bstack1ll1ll1l11_opy_):
  bstack1ll1ll1l11_opy_ = str(bstack1ll1ll1l11_opy_)
  bstack111l11111_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠫࢃ࠭ࣧ")), bstack1lll1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬࣨ"))
  try:
    if not os.path.exists(bstack111l11111_opy_):
      os.makedirs(bstack111l11111_opy_)
    file_path = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"࠭ࡾࠨࣩ")), bstack1lll1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧ࣪"), bstack1lll1l1_opy_ (u"ࠨ࠰ࡥࡹ࡮ࡲࡤ࠮ࡰࡤࡱࡪ࠳ࡣࡢࡥ࡫ࡩ࠳ࡰࡳࡰࡰࠪ࣫"))
    if not os.path.isfile(file_path):
      with open(file_path, bstack1lll1l1_opy_ (u"ࠩࡺࠫ࣬")):
        pass
      with open(file_path, bstack1lll1l1_opy_ (u"ࠥࡻ࠰ࠨ࣭")) as outfile:
        json.dump({}, outfile)
    with open(file_path, bstack1lll1l1_opy_ (u"ࠫࡷ࣮࠭")) as bstack1lll11l111_opy_:
      bstack11111l11_opy_ = json.load(bstack1lll11l111_opy_)
    if bstack1ll1ll1l11_opy_ in bstack11111l11_opy_:
      bstack11l1l1l1_opy_ = bstack11111l11_opy_[bstack1ll1ll1l11_opy_][bstack1lll1l1_opy_ (u"ࠬ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳ࣯ࠩ")]
      bstack1l1l111111_opy_ = int(bstack11l1l1l1_opy_) + 1
      bstack1ll1111lll_opy_(bstack1ll1ll1l11_opy_, bstack1l1l111111_opy_, file_path)
      return bstack1l1l111111_opy_
    else:
      bstack1ll1111lll_opy_(bstack1ll1ll1l11_opy_, 1, file_path)
      return 1
  except Exception as e:
    logger.warn(bstack1l1ll111l_opy_.format(str(e)))
    return -1
def bstack1l111111ll_opy_(config):
  if not config[bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨࣰ")] or not config[bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࣱࠪ")]:
    return True
  else:
    return False
def bstack11l1ll1ll_opy_(config, index=0):
  global bstack11lll1ll_opy_
  bstack11llll1ll_opy_ = {}
  caps = bstack111lll111_opy_ + bstack1ll1111111_opy_
  if bstack11lll1ll_opy_:
    caps += bstack1l111llll1_opy_
  for key in config:
    if key in caps + [bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣲࠫ")]:
      continue
    bstack11llll1ll_opy_[key] = config[key]
  if bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬࣳ") in config:
    for bstack1ll1ll111l_opy_ in config[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣴ")][index]:
      if bstack1ll1ll111l_opy_ in caps:
        continue
      bstack11llll1ll_opy_[bstack1ll1ll111l_opy_] = config[bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧࣵ")][index][bstack1ll1ll111l_opy_]
  bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡑࡥࡲ࡫ࣶࠧ")] = socket.gethostname()
  if bstack1lll1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࠧࣷ") in bstack11llll1ll_opy_:
    del (bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨࣸ")])
  return bstack11llll1ll_opy_
def bstack1l1lll111_opy_(config):
  global bstack11lll1ll_opy_
  bstack1lll11lll_opy_ = {}
  caps = bstack1ll1111111_opy_
  if bstack11lll1ll_opy_:
    caps += bstack1l111llll1_opy_
  for key in caps:
    if key in config:
      bstack1lll11lll_opy_[key] = config[key]
  return bstack1lll11lll_opy_
def bstack11lllll1l_opy_(bstack11llll1ll_opy_, bstack1lll11lll_opy_):
  bstack1l1l11lll1_opy_ = {}
  for key in bstack11llll1ll_opy_.keys():
    if key in bstack1ll11ll1l_opy_:
      bstack1l1l11lll1_opy_[bstack1ll11ll1l_opy_[key]] = bstack11llll1ll_opy_[key]
    else:
      bstack1l1l11lll1_opy_[key] = bstack11llll1ll_opy_[key]
  for key in bstack1lll11lll_opy_:
    if key in bstack1ll11ll1l_opy_:
      bstack1l1l11lll1_opy_[bstack1ll11ll1l_opy_[key]] = bstack1lll11lll_opy_[key]
    else:
      bstack1l1l11lll1_opy_[key] = bstack1lll11lll_opy_[key]
  return bstack1l1l11lll1_opy_
def bstack1l111ll1ll_opy_(config, index=0):
  global bstack11lll1ll_opy_
  caps = {}
  config = copy.deepcopy(config)
  bstack1111l1l1l_opy_ = bstack1lll1l1lll_opy_(bstack11lllllll_opy_, config, logger)
  bstack1lll11lll_opy_ = bstack1l1lll111_opy_(config)
  bstack1l1l1l1l11_opy_ = bstack1ll1111111_opy_
  bstack1l1l1l1l11_opy_ += bstack1lll1l11l_opy_
  bstack1lll11lll_opy_ = update(bstack1lll11lll_opy_, bstack1111l1l1l_opy_)
  if bstack11lll1ll_opy_:
    bstack1l1l1l1l11_opy_ += bstack1l111llll1_opy_
  if bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࣹࠫ") in config:
    if bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࣺࠧ") in config[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ࣻ")][index]:
      caps[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩࣼ")] = config[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨࣽ")][index][bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫࣾ")]
    if bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨࣿ") in config[bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫऀ")][index]:
      caps[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪँ")] = str(config[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ं")][index][bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬः")])
    bstack11l11l1ll_opy_ = bstack1lll1l1lll_opy_(bstack11lllllll_opy_, config[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨऄ")][index], logger)
    bstack1l1l1l1l11_opy_ += list(bstack11l11l1ll_opy_.keys())
    for bstack1llllll11l_opy_ in bstack1l1l1l1l11_opy_:
      if bstack1llllll11l_opy_ in config[bstack1lll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩअ")][index]:
        if bstack1llllll11l_opy_ == bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩआ"):
          try:
            bstack11l11l1ll_opy_[bstack1llllll11l_opy_] = str(config[bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫइ")][index][bstack1llllll11l_opy_] * 1.0)
          except:
            bstack11l11l1ll_opy_[bstack1llllll11l_opy_] = str(config[bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬई")][index][bstack1llllll11l_opy_])
        else:
          bstack11l11l1ll_opy_[bstack1llllll11l_opy_] = config[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭उ")][index][bstack1llllll11l_opy_]
        del (config[bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧऊ")][index][bstack1llllll11l_opy_])
    bstack1lll11lll_opy_ = update(bstack1lll11lll_opy_, bstack11l11l1ll_opy_)
  bstack11llll1ll_opy_ = bstack11l1ll1ll_opy_(config, index)
  for bstack111l11ll1_opy_ in bstack1ll1111111_opy_ + list(bstack1111l1l1l_opy_.keys()):
    if bstack111l11ll1_opy_ in bstack11llll1ll_opy_:
      bstack1lll11lll_opy_[bstack111l11ll1_opy_] = bstack11llll1ll_opy_[bstack111l11ll1_opy_]
      del (bstack11llll1ll_opy_[bstack111l11ll1_opy_])
  if bstack111111lll_opy_(config):
    bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬऋ")] = True
    caps.update(bstack1lll11lll_opy_)
    caps[bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧऌ")] = bstack11llll1ll_opy_
  else:
    bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠧࡶࡵࡨ࡛࠸ࡉࠧऍ")] = False
    caps.update(bstack11lllll1l_opy_(bstack11llll1ll_opy_, bstack1lll11lll_opy_))
    if bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ऎ") in caps:
      caps[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪए")] = caps[bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨऐ")]
      del (caps[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩऑ")])
    if bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ऒ") in caps:
      caps[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨओ")] = caps[bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨऔ")]
      del (caps[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩक")])
  return caps
def bstack1llll1ll1l_opy_():
  global bstack1ll1l1ll_opy_
  if bstack1l1l1l111_opy_() <= version.parse(bstack1lll1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩख")):
    if bstack1ll1l1ll_opy_ != bstack1lll1l1_opy_ (u"ࠪࠫग"):
      return bstack1lll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧघ") + bstack1ll1l1ll_opy_ + bstack1lll1l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤङ")
    return bstack1lll11l1l_opy_
  if bstack1ll1l1ll_opy_ != bstack1lll1l1_opy_ (u"࠭ࠧच"):
    return bstack1lll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤछ") + bstack1ll1l1ll_opy_ + bstack1lll1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤज")
  return bstack1l11l1l1l_opy_
def bstack1lll111lll_opy_(options):
  return hasattr(options, bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪझ"))
def update(d, u):
  for k, v in u.items():
    if isinstance(v, collections.abc.Mapping):
      d[k] = update(d.get(k, {}), v)
    else:
      if isinstance(v, list):
        d[k] = d.get(k, []) + v
      else:
        d[k] = v
  return d
def bstack11l1lllll_opy_(options, bstack11l1l1lll_opy_):
  for bstack1l111lll1l_opy_ in bstack11l1l1lll_opy_:
    if bstack1l111lll1l_opy_ in [bstack1lll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨञ"), bstack1lll1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨट")]:
      continue
    if bstack1l111lll1l_opy_ in options._experimental_options:
      options._experimental_options[bstack1l111lll1l_opy_] = update(options._experimental_options[bstack1l111lll1l_opy_],
                                                         bstack11l1l1lll_opy_[bstack1l111lll1l_opy_])
    else:
      options.add_experimental_option(bstack1l111lll1l_opy_, bstack11l1l1lll_opy_[bstack1l111lll1l_opy_])
  if bstack1lll1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪठ") in bstack11l1l1lll_opy_:
    for arg in bstack11l1l1lll_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫड")]:
      options.add_argument(arg)
    del (bstack11l1l1lll_opy_[bstack1lll1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬढ")])
  if bstack1lll1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬण") in bstack11l1l1lll_opy_:
    for ext in bstack11l1l1lll_opy_[bstack1lll1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭त")]:
      options.add_extension(ext)
    del (bstack11l1l1lll_opy_[bstack1lll1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧथ")])
def bstack1lll111111_opy_(options, bstack1l11l11ll_opy_):
  if bstack1lll1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪद") in bstack1l11l11ll_opy_:
    for bstack1ll1ll1l1l_opy_ in bstack1l11l11ll_opy_[bstack1lll1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫध")]:
      if bstack1ll1ll1l1l_opy_ in options._preferences:
        options._preferences[bstack1ll1ll1l1l_opy_] = update(options._preferences[bstack1ll1ll1l1l_opy_], bstack1l11l11ll_opy_[bstack1lll1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬन")][bstack1ll1ll1l1l_opy_])
      else:
        options.set_preference(bstack1ll1ll1l1l_opy_, bstack1l11l11ll_opy_[bstack1lll1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ऩ")][bstack1ll1ll1l1l_opy_])
  if bstack1lll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭प") in bstack1l11l11ll_opy_:
    for arg in bstack1l11l11ll_opy_[bstack1lll1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧफ")]:
      options.add_argument(arg)
def bstack1llll1llll_opy_(options, bstack1ll1111ll_opy_):
  if bstack1lll1l1_opy_ (u"ࠪࡻࡪࡨࡶࡪࡧࡺࠫब") in bstack1ll1111ll_opy_:
    options.use_webview(bool(bstack1ll1111ll_opy_[bstack1lll1l1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࠬभ")]))
  bstack11l1lllll_opy_(options, bstack1ll1111ll_opy_)
def bstack1ll1l1l1ll_opy_(options, bstack1ll11ll11_opy_):
  for bstack1l1lll11_opy_ in bstack1ll11ll11_opy_:
    if bstack1l1lll11_opy_ in [bstack1lll1l1_opy_ (u"ࠬࡺࡥࡤࡪࡱࡳࡱࡵࡧࡺࡒࡵࡩࡻ࡯ࡥࡸࠩम"), bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫय")]:
      continue
    options.set_capability(bstack1l1lll11_opy_, bstack1ll11ll11_opy_[bstack1l1lll11_opy_])
  if bstack1lll1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬर") in bstack1ll11ll11_opy_:
    for arg in bstack1ll11ll11_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ऱ")]:
      options.add_argument(arg)
  if bstack1lll1l1_opy_ (u"ࠩࡷࡩࡨ࡮࡮ࡰ࡮ࡲ࡫ࡾࡖࡲࡦࡸ࡬ࡩࡼ࠭ल") in bstack1ll11ll11_opy_:
    options.bstack1lllll111l_opy_(bool(bstack1ll11ll11_opy_[bstack1lll1l1_opy_ (u"ࠪࡸࡪࡩࡨ࡯ࡱ࡯ࡳ࡬ࡿࡐࡳࡧࡹ࡭ࡪࡽࠧळ")]))
def bstack111l1l1l1_opy_(options, bstack1ll1ll1111_opy_):
  for bstack1l1ll11ll_opy_ in bstack1ll1ll1111_opy_:
    if bstack1l1ll11ll_opy_ in [bstack1lll1l1_opy_ (u"ࠫࡦࡪࡤࡪࡶ࡬ࡳࡳࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨऴ"), bstack1lll1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪव")]:
      continue
    options._options[bstack1l1ll11ll_opy_] = bstack1ll1ll1111_opy_[bstack1l1ll11ll_opy_]
  if bstack1lll1l1_opy_ (u"࠭ࡡࡥࡦ࡬ࡸ࡮ࡵ࡮ࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪश") in bstack1ll1ll1111_opy_:
    for bstack111ll11l_opy_ in bstack1ll1ll1111_opy_[bstack1lll1l1_opy_ (u"ࠧࡢࡦࡧ࡭ࡹ࡯࡯࡯ࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫष")]:
      options.bstack1ll1lll1ll_opy_(
        bstack111ll11l_opy_, bstack1ll1ll1111_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡧࡨ࡮ࡺࡩࡰࡰࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬस")][bstack111ll11l_opy_])
  if bstack1lll1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧह") in bstack1ll1ll1111_opy_:
    for arg in bstack1ll1ll1111_opy_[bstack1lll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨऺ")]:
      options.add_argument(arg)
def bstack1ll1ll1ll_opy_(options, caps):
  if not hasattr(options, bstack1lll1l1_opy_ (u"ࠫࡐࡋ࡙ࠨऻ")):
    return
  if options.KEY == bstack1lll1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ़ࠪ") and options.KEY in caps:
    bstack11l1lllll_opy_(options, caps[bstack1lll1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫऽ")])
  elif options.KEY == bstack1lll1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬा") and options.KEY in caps:
    bstack1lll111111_opy_(options, caps[bstack1lll1l1_opy_ (u"ࠨ࡯ࡲࡾ࠿࡬ࡩࡳࡧࡩࡳࡽࡕࡰࡵ࡫ࡲࡲࡸ࠭ि")])
  elif options.KEY == bstack1lll1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪी") and options.KEY in caps:
    bstack1ll1l1l1ll_opy_(options, caps[bstack1lll1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫु")])
  elif options.KEY == bstack1lll1l1_opy_ (u"ࠫࡲࡹ࠺ࡦࡦࡪࡩࡔࡶࡴࡪࡱࡱࡷࠬू") and options.KEY in caps:
    bstack1llll1llll_opy_(options, caps[bstack1lll1l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ृ")])
  elif options.KEY == bstack1lll1l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬॄ") and options.KEY in caps:
    bstack111l1l1l1_opy_(options, caps[bstack1lll1l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ॅ")])
def bstack1l11l1l1l1_opy_(caps):
  global bstack11lll1ll_opy_
  if isinstance(os.environ.get(bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩॆ")), str):
    bstack11lll1ll_opy_ = eval(os.getenv(bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪे")))
  if bstack11lll1ll_opy_:
    if bstack1lllll1lll_opy_() < version.parse(bstack1lll1l1_opy_ (u"ࠪ࠶࠳࠹࠮࠱ࠩै")):
      return None
    else:
      from appium.options.common.base import AppiumOptions
      options = AppiumOptions().load_capabilities(caps)
      return options
  else:
    browser = bstack1lll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫॉ")
    if bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪॊ") in caps:
      browser = caps[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫो")]
    elif bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࠨौ") in caps:
      browser = caps[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳ्ࠩ")]
    browser = str(browser).lower()
    if browser == bstack1lll1l1_opy_ (u"ࠩ࡬ࡴ࡭ࡵ࡮ࡦࠩॎ") or browser == bstack1lll1l1_opy_ (u"ࠪ࡭ࡵࡧࡤࠨॏ"):
      browser = bstack1lll1l1_opy_ (u"ࠫࡸࡧࡦࡢࡴ࡬ࠫॐ")
    if browser == bstack1lll1l1_opy_ (u"ࠬࡹࡡ࡮ࡵࡸࡲ࡬࠭॑"):
      browser = bstack1lll1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ॒࠭")
    if browser not in [bstack1lll1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ॓"), bstack1lll1l1_opy_ (u"ࠨࡧࡧ࡫ࡪ࠭॔"), bstack1lll1l1_opy_ (u"ࠩ࡬ࡩࠬॕ"), bstack1lll1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࠪॖ"), bstack1lll1l1_opy_ (u"ࠫ࡫࡯ࡲࡦࡨࡲࡼࠬॗ")]:
      return None
    try:
      package = bstack1lll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳ࠮ࡸࡧࡥࡨࡷ࡯ࡶࡦࡴ࠱ࡿࢂ࠴࡯ࡱࡶ࡬ࡳࡳࡹࠧक़").format(browser)
      name = bstack1lll1l1_opy_ (u"࠭ࡏࡱࡶ࡬ࡳࡳࡹࠧख़")
      browser_options = getattr(__import__(package, fromlist=[name]), name)
      options = browser_options()
      if not bstack1lll111lll_opy_(options):
        return None
      for bstack111l11ll1_opy_ in caps.keys():
        options.set_capability(bstack111l11ll1_opy_, caps[bstack111l11ll1_opy_])
      bstack1ll1ll1ll_opy_(options, caps)
      return options
    except Exception as e:
      logger.debug(str(e))
      return None
def bstack1l1l1l1ll1_opy_(options, bstack11lllll1ll_opy_):
  if not bstack1lll111lll_opy_(options):
    return
  for bstack111l11ll1_opy_ in bstack11lllll1ll_opy_.keys():
    if bstack111l11ll1_opy_ in bstack1lll1l11l_opy_:
      continue
    if bstack111l11ll1_opy_ in options._caps and type(options._caps[bstack111l11ll1_opy_]) in [dict, list]:
      options._caps[bstack111l11ll1_opy_] = update(options._caps[bstack111l11ll1_opy_], bstack11lllll1ll_opy_[bstack111l11ll1_opy_])
    else:
      options.set_capability(bstack111l11ll1_opy_, bstack11lllll1ll_opy_[bstack111l11ll1_opy_])
  bstack1ll1ll1ll_opy_(options, bstack11lllll1ll_opy_)
  if bstack1lll1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾ࡩ࡫ࡢࡶࡩࡪࡩࡷࡇࡤࡥࡴࡨࡷࡸ࠭ग़") in options._caps:
    if options._caps[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ज़")] and options._caps[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧड़")].lower() != bstack1lll1l1_opy_ (u"ࠪࡪ࡮ࡸࡥࡧࡱࡻࠫढ़"):
      del options._caps[bstack1lll1l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡦࡨࡦࡺ࡭ࡧࡦࡴࡄࡨࡩࡸࡥࡴࡵࠪफ़")]
def bstack1ll11111ll_opy_(proxy_config):
  if bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩय़") in proxy_config:
    proxy_config[bstack1lll1l1_opy_ (u"࠭ࡳࡴ࡮ࡓࡶࡴࡾࡹࠨॠ")] = proxy_config[bstack1lll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫॡ")]
    del (proxy_config[bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬॢ")])
  if bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡕࡻࡳࡩࠬॣ") in proxy_config and proxy_config[bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡖࡼࡴࡪ࠭।")].lower() != bstack1lll1l1_opy_ (u"ࠫࡩ࡯ࡲࡦࡥࡷࠫ॥"):
    proxy_config[bstack1lll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡘࡾࡶࡥࠨ०")] = bstack1lll1l1_opy_ (u"࠭࡭ࡢࡰࡸࡥࡱ࠭१")
  if bstack1lll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡇࡵࡵࡱࡦࡳࡳ࡬ࡩࡨࡗࡵࡰࠬ२") in proxy_config:
    proxy_config[bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡔࡺࡲࡨࠫ३")] = bstack1lll1l1_opy_ (u"ࠩࡳࡥࡨ࠭४")
  return proxy_config
def bstack11ll1111l_opy_(config, proxy):
  from selenium.webdriver.common.proxy import Proxy
  if not bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࠩ५") in config:
    return proxy
  config[bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࠪ६")] = bstack1ll11111ll_opy_(config[bstack1lll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࠫ७")])
  if proxy == None:
    proxy = Proxy(config[bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࠬ८")])
  return proxy
def bstack1llll111l_opy_(self):
  global CONFIG
  global bstack11lll1l1_opy_
  try:
    proxy = bstack1l1ll1ll11_opy_(CONFIG)
    if proxy:
      if proxy.endswith(bstack1lll1l1_opy_ (u"ࠧ࠯ࡲࡤࡧࠬ९")):
        proxies = bstack1ll1ll1l1_opy_(proxy, bstack1llll1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll111lll_opy_ = proxies.popitem()
          if bstack1lll1l1_opy_ (u"ࠣ࠼࠲࠳ࠧ॰") in bstack1ll111lll_opy_:
            return bstack1ll111lll_opy_
          else:
            return bstack1lll1l1_opy_ (u"ࠤ࡫ࡸࡹࡶ࠺࠰࠱ࠥॱ") + bstack1ll111lll_opy_
      else:
        return proxy
  except Exception as e:
    logger.error(bstack1lll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡰࡳࡱࡻࡽࠥࡻࡲ࡭ࠢ࠽ࠤࢀࢃࠢॲ").format(str(e)))
  return bstack11lll1l1_opy_(self)
def bstack1ll11lll_opy_():
  global CONFIG
  return bstack1lll1lll1l_opy_(CONFIG) and bstack1l11l11111_opy_() and bstack1l1l1l111_opy_() >= version.parse(bstack1l11lll1l1_opy_)
def bstack1l1l1l111l_opy_():
  global CONFIG
  return (bstack1lll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧॳ") in CONFIG or bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩॴ") in CONFIG) and bstack1l1l1l11_opy_()
def bstack1l1llll11_opy_(config):
  bstack1ll1lll1_opy_ = {}
  if bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪॵ") in config:
    bstack1ll1lll1_opy_ = config[bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࡓࡵࡺࡩࡰࡰࡶࠫॶ")]
  if bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧॷ") in config:
    bstack1ll1lll1_opy_ = config[bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨॸ")]
  proxy = bstack1l1ll1ll11_opy_(config)
  if proxy:
    if proxy.endswith(bstack1lll1l1_opy_ (u"ࠪ࠲ࡵࡧࡣࠨॹ")) and os.path.isfile(proxy):
      bstack1ll1lll1_opy_[bstack1lll1l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧॺ")] = proxy
    else:
      parsed_url = None
      if proxy.endswith(bstack1lll1l1_opy_ (u"ࠬ࠴ࡰࡢࡥࠪॻ")):
        proxies = bstack111111ll1_opy_(config, bstack1llll1ll1l_opy_())
        if len(proxies) > 0:
          protocol, bstack1ll111lll_opy_ = proxies.popitem()
          if bstack1lll1l1_opy_ (u"ࠨ࠺࠰࠱ࠥॼ") in bstack1ll111lll_opy_:
            parsed_url = urlparse(bstack1ll111lll_opy_)
          else:
            parsed_url = urlparse(protocol + bstack1lll1l1_opy_ (u"ࠢ࠻࠱࠲ࠦॽ") + bstack1ll111lll_opy_)
      else:
        parsed_url = urlparse(proxy)
      if parsed_url and parsed_url.hostname: bstack1ll1lll1_opy_[bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫॾ")] = str(parsed_url.hostname)
      if parsed_url and parsed_url.port: bstack1ll1lll1_opy_[bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬॿ")] = str(parsed_url.port)
      if parsed_url and parsed_url.username: bstack1ll1lll1_opy_[bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ঀ")] = str(parsed_url.username)
      if parsed_url and parsed_url.password: bstack1ll1lll1_opy_[bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧঁ")] = str(parsed_url.password)
  return bstack1ll1lll1_opy_
def bstack1111l1l11_opy_(config):
  if bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪং") in config:
    return config[bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫঃ")]
  return {}
def bstack1ll1llllll_opy_(caps):
  global bstack1ll11l1111_opy_
  if bstack1lll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ঄") in caps:
    caps[bstack1lll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩঅ")][bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨআ")] = True
    if bstack1ll11l1111_opy_:
      caps[bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫই")][bstack1lll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ঈ")] = bstack1ll11l1111_opy_
  else:
    caps[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡱࡵࡣࡢ࡮ࠪউ")] = True
    if bstack1ll11l1111_opy_:
      caps[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧঊ")] = bstack1ll11l1111_opy_
def bstack1lll1lll_opy_():
  global CONFIG
  if not bstack1l1111ll11_opy_(CONFIG):
    return
  if bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫঋ") in CONFIG and bstack11ll1l1l1_opy_(CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬঌ")]):
    if (
      bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭঍") in CONFIG
      and bstack11ll1l1l1_opy_(CONFIG[bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧ঎")].get(bstack1lll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡄ࡬ࡲࡦࡸࡹࡊࡰ࡬ࡸ࡮ࡧ࡬ࡪࡵࡤࡸ࡮ࡵ࡮ࠨএ")))
    ):
      logger.debug(bstack1lll1l1_opy_ (u"ࠧࡒ࡯ࡤࡣ࡯ࠤࡧ࡯࡮ࡢࡴࡼࠤࡳࡵࡴࠡࡵࡷࡥࡷࡺࡥࡥࠢࡤࡷࠥࡹ࡫ࡪࡲࡅ࡭ࡳࡧࡲࡺࡋࡱ࡭ࡹ࡯ࡡ࡭࡫ࡶࡥࡹ࡯࡯࡯ࠢ࡬ࡷࠥ࡫࡮ࡢࡤ࡯ࡩࡩࠨঐ"))
      return
    bstack1ll1lll1_opy_ = bstack1l1llll11_opy_(CONFIG)
    bstack111l11l11_opy_(CONFIG[bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ঑")], bstack1ll1lll1_opy_)
def bstack111l11l11_opy_(key, bstack1ll1lll1_opy_):
  global bstack1l1l1l11ll_opy_
  logger.info(bstack11lllllll1_opy_)
  try:
    bstack1l1l1l11ll_opy_ = Local()
    bstack1lllll11l1_opy_ = {bstack1lll1l1_opy_ (u"ࠧ࡬ࡧࡼࠫ঒"): key}
    bstack1lllll11l1_opy_.update(bstack1ll1lll1_opy_)
    logger.debug(bstack1l1l1llll_opy_.format(str(bstack1lllll11l1_opy_)))
    bstack1l1l1l11ll_opy_.start(**bstack1lllll11l1_opy_)
    if bstack1l1l1l11ll_opy_.isRunning():
      logger.info(bstack1ll11ll1l1_opy_)
  except Exception as e:
    bstack1llll1l1l_opy_(bstack1lll1l1ll_opy_.format(str(e)))
def bstack1l1lll11l1_opy_():
  global bstack1l1l1l11ll_opy_
  if bstack1l1l1l11ll_opy_.isRunning():
    logger.info(bstack1lll11ll1_opy_)
    bstack1l1l1l11ll_opy_.stop()
  bstack1l1l1l11ll_opy_ = None
def bstack1l11lll11l_opy_(bstack11111l111_opy_=[]):
  global CONFIG
  bstack111lll1l1_opy_ = []
  bstack1ll1ll1l_opy_ = [bstack1lll1l1_opy_ (u"ࠨࡱࡶࠫও"), bstack1lll1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬঔ"), bstack1lll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧক"), bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭খ"), bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪগ"), bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧঘ")]
  try:
    for err in bstack11111l111_opy_:
      bstack1l111111l1_opy_ = {}
      for k in bstack1ll1ll1l_opy_:
        val = CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪঙ")][int(err[bstack1lll1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧচ")])].get(k)
        if val:
          bstack1l111111l1_opy_[k] = val
      if(err[bstack1lll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨছ")] != bstack1lll1l1_opy_ (u"ࠪࠫজ")):
        bstack1l111111l1_opy_[bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡵࠪঝ")] = {
          err[bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪঞ")]: err[bstack1lll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬট")]
        }
        bstack111lll1l1_opy_.append(bstack1l111111l1_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡩࡳࡷࡳࡡࡵࡶ࡬ࡲ࡬ࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡧࡹࡩࡳࡺ࠺ࠡࠩঠ") + str(e))
  finally:
    return bstack111lll1l1_opy_
def bstack1l1ll1l1ll_opy_(file_name):
  bstack1lll111l1_opy_ = []
  try:
    bstack1111l11l1_opy_ = os.path.join(tempfile.gettempdir(), file_name)
    if os.path.exists(bstack1111l11l1_opy_):
      with open(bstack1111l11l1_opy_) as f:
        bstack1l11lllll1_opy_ = json.load(f)
        bstack1lll111l1_opy_ = bstack1l11lllll1_opy_
      os.remove(bstack1111l11l1_opy_)
    return bstack1lll111l1_opy_
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡪ࡮ࡴࡤࡪࡰࡪࠤࡪࡸࡲࡰࡴࠣࡰ࡮ࡹࡴ࠻ࠢࠪড") + str(e))
    return bstack1lll111l1_opy_
def bstack111l1ll1l_opy_():
  global bstack1111ll11l_opy_
  global bstack11l1l1ll1_opy_
  global bstack1ll111lll1_opy_
  global bstack1l111ll1_opy_
  global bstack11l1lll1l_opy_
  global bstack1111111l_opy_
  global CONFIG
  bstack1ll11ll1ll_opy_ = os.environ.get(bstack1lll1l1_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪঢ"))
  if bstack1ll11ll1ll_opy_ in [bstack1lll1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩণ"), bstack1lll1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪত")]:
    bstack1l11ll11ll_opy_()
  percy.shutdown()
  if bstack1111ll11l_opy_:
    logger.warning(bstack1l1lllll_opy_.format(str(bstack1111ll11l_opy_)))
  else:
    try:
      bstack1l11111l11_opy_ = bstack11l1ll11l_opy_(bstack1lll1l1_opy_ (u"ࠬ࠴ࡢࡴࡶࡤࡧࡰ࠳ࡣࡰࡰࡩ࡭࡬࠴ࡪࡴࡱࡱࠫথ"), logger)
      if bstack1l11111l11_opy_.get(bstack1lll1l1_opy_ (u"࠭࡮ࡶࡦࡪࡩࡤࡲ࡯ࡤࡣ࡯ࠫদ")) and bstack1l11111l11_opy_.get(bstack1lll1l1_opy_ (u"ࠧ࡯ࡷࡧ࡫ࡪࡥ࡬ࡰࡥࡤࡰࠬধ")).get(bstack1lll1l1_opy_ (u"ࠨࡪࡲࡷࡹࡴࡡ࡮ࡧࠪন")):
        logger.warning(bstack1l1lllll_opy_.format(str(bstack1l11111l11_opy_[bstack1lll1l1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧ঩")][bstack1lll1l1_opy_ (u"ࠪ࡬ࡴࡹࡴ࡯ࡣࡰࡩࠬপ")])))
    except Exception as e:
      logger.error(e)
  logger.info(bstack1ll11l11l1_opy_)
  global bstack1l1l1l11ll_opy_
  if bstack1l1l1l11ll_opy_:
    bstack1l1lll11l1_opy_()
  try:
    for driver in bstack11l1l1ll1_opy_:
      driver.quit()
  except Exception as e:
    pass
  logger.info(bstack11ll1l11l_opy_)
  if bstack1111111l_opy_ == bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪফ"):
    bstack11l1lll1l_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࡣࡪࡸࡲࡰࡴࡢࡰ࡮ࡹࡴ࠯࡬ࡶࡳࡳ࠭ব"))
  if bstack1111111l_opy_ == bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ভ") and len(bstack1l111ll1_opy_) == 0:
    bstack1l111ll1_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll1l1_opy_ (u"ࠧࡱࡹࡢࡴࡾࡺࡥࡴࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬম"))
    if len(bstack1l111ll1_opy_) == 0:
      bstack1l111ll1_opy_ = bstack1l1ll1l1ll_opy_(bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧয"))
  bstack1l11111lll_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪর")
  if len(bstack1ll111lll1_opy_) > 0:
    bstack1l11111lll_opy_ = bstack1l11lll11l_opy_(bstack1ll111lll1_opy_)
  elif len(bstack1l111ll1_opy_) > 0:
    bstack1l11111lll_opy_ = bstack1l11lll11l_opy_(bstack1l111ll1_opy_)
  elif len(bstack11l1lll1l_opy_) > 0:
    bstack1l11111lll_opy_ = bstack1l11lll11l_opy_(bstack11l1lll1l_opy_)
  elif len(bstack1l1lllll1_opy_) > 0:
    bstack1l11111lll_opy_ = bstack1l11lll11l_opy_(bstack1l1lllll1_opy_)
  if bool(bstack1l11111lll_opy_):
    bstack1l11ll1ll_opy_(bstack1l11111lll_opy_)
  else:
    bstack1l11ll1ll_opy_()
  bstack1l11l1ll1_opy_(bstack1llllllll1_opy_, logger)
  bstack1l11ll1111_opy_.bstack1l11llll1l_opy_(CONFIG)
  if len(bstack11l1lll1l_opy_) > 0:
    sys.exit(len(bstack11l1lll1l_opy_))
def bstack1l11l111l_opy_(bstack1l111l11l_opy_, frame):
  global bstack1lll11l1ll_opy_
  logger.error(bstack1ll111111l_opy_)
  bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭঱"), bstack1l111l11l_opy_)
  if hasattr(signal, bstack1lll1l1_opy_ (u"ࠫࡘ࡯ࡧ࡯ࡣ࡯ࡷࠬল")):
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠬࡹࡤ࡬ࡍ࡬ࡰࡱ࡙ࡩࡨࡰࡤࡰࠬ঳"), signal.Signals(bstack1l111l11l_opy_).name)
  else:
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"࠭ࡳࡥ࡭ࡎ࡭ࡱࡲࡓࡪࡩࡱࡥࡱ࠭঴"), bstack1lll1l1_opy_ (u"ࠧࡔࡋࡊ࡙ࡓࡑࡎࡐ࡙ࡑࠫ঵"))
  bstack1ll11ll1ll_opy_ = os.environ.get(bstack1lll1l1_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩশ"))
  if bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩষ"):
    bstack1l1lll1lll_opy_.stop(bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡗ࡮࡭࡮ࡢ࡮ࠪস")))
  bstack111l1ll1l_opy_()
  sys.exit(1)
def bstack1llll1l1l_opy_(err):
  logger.critical(bstack1llll11l1_opy_.format(str(err)))
  bstack1l11ll1ll_opy_(bstack1llll11l1_opy_.format(str(err)), True)
  atexit.unregister(bstack111l1ll1l_opy_)
  bstack1l11ll11ll_opy_()
  sys.exit(1)
def bstack11l111l1_opy_(error, message):
  logger.critical(str(error))
  logger.critical(message)
  bstack1l11ll1ll_opy_(message, True)
  atexit.unregister(bstack111l1ll1l_opy_)
  bstack1l11ll11ll_opy_()
  sys.exit(1)
def bstack1lll11l11l_opy_():
  global CONFIG
  global bstack1ll1ll11_opy_
  global bstack1ll111l1l_opy_
  global bstack1l1l1ll11l_opy_
  CONFIG = bstack111lllll1_opy_()
  load_dotenv(CONFIG.get(bstack1lll1l1_opy_ (u"ࠫࡪࡴࡶࡇ࡫࡯ࡩࠬহ")))
  bstack1ll11ll111_opy_()
  bstack1l11111ll_opy_()
  CONFIG = bstack1llll111ll_opy_(CONFIG)
  update(CONFIG, bstack1ll111l1l_opy_)
  update(CONFIG, bstack1ll1ll11_opy_)
  CONFIG = bstack1lll11111_opy_(CONFIG)
  bstack1l1l1ll11l_opy_ = bstack1l1111ll11_opy_(CONFIG)
  os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ঺")] = bstack1l1l1ll11l_opy_.__str__()
  bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ঻"), bstack1l1l1ll11l_opy_)
  if (bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧ়ࠪ") in CONFIG and bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫঽ") in bstack1ll1ll11_opy_) or (
          bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬা") in CONFIG and bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ি") not in bstack1ll111l1l_opy_):
    if os.getenv(bstack1lll1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡣࡈࡕࡍࡃࡋࡑࡉࡉࡥࡂࡖࡋࡏࡈࡤࡏࡄࠨী")):
      CONFIG[bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧু")] = os.getenv(bstack1lll1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡥࡃࡐࡏࡅࡍࡓࡋࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠪূ"))
    else:
      bstack11111l11l_opy_()
  elif (bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪৃ") not in CONFIG and bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪৄ") in CONFIG) or (
          bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ৅") in bstack1ll111l1l_opy_ and bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭৆") not in bstack1ll1ll11_opy_):
    del (CONFIG[bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭ে")])
  if bstack1l111111ll_opy_(CONFIG):
    bstack1llll1l1l_opy_(bstack1l1ll1llll_opy_)
  bstack11111lll_opy_()
  bstack1l111lll11_opy_()
  if bstack11lll1ll_opy_:
    CONFIG[bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱࠩৈ")] = bstack111l111ll_opy_(CONFIG)
    logger.info(bstack1lll1ll1ll_opy_.format(CONFIG[bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࠪ৉")]))
  if not bstack1l1l1ll11l_opy_:
    CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ৊")] = [{}]
def bstack11l11ll1_opy_(config, bstack1ll1l11l1_opy_):
  global CONFIG
  global bstack11lll1ll_opy_
  CONFIG = config
  bstack11lll1ll_opy_ = bstack1ll1l11l1_opy_
def bstack1l111lll11_opy_():
  global CONFIG
  global bstack11lll1ll_opy_
  if bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴࠬো") in CONFIG:
    try:
      from appium import version
    except Exception as e:
      bstack11l111l1_opy_(e, bstack11l1lll1_opy_)
    bstack11lll1ll_opy_ = True
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨৌ"), True)
def bstack111l111ll_opy_(config):
  bstack1l1l11l1_opy_ = bstack1lll1l1_opy_ (u"্ࠪࠫ")
  app = config[bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰࠨৎ")]
  if isinstance(app, str):
    if os.path.splitext(app)[1] in bstack1ll1l1l111_opy_:
      if os.path.exists(app):
        bstack1l1l11l1_opy_ = bstack1l1l11ll_opy_(config, app)
      elif bstack1lll11llll_opy_(app):
        bstack1l1l11l1_opy_ = app
      else:
        bstack1llll1l1l_opy_(bstack1lll1l1111_opy_.format(app))
    else:
      if bstack1lll11llll_opy_(app):
        bstack1l1l11l1_opy_ = app
      elif os.path.exists(app):
        bstack1l1l11l1_opy_ = bstack1l1l11ll_opy_(app)
      else:
        bstack1llll1l1l_opy_(bstack1lll1ll1_opy_)
  else:
    if len(app) > 2:
      bstack1llll1l1l_opy_(bstack111ll11ll_opy_)
    elif len(app) == 2:
      if bstack1lll1l1_opy_ (u"ࠬࡶࡡࡵࡪࠪ৏") in app and bstack1lll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲࡥࡩࡥࠩ৐") in app:
        if os.path.exists(app[bstack1lll1l1_opy_ (u"ࠧࡱࡣࡷ࡬ࠬ৑")]):
          bstack1l1l11l1_opy_ = bstack1l1l11ll_opy_(config, app[bstack1lll1l1_opy_ (u"ࠨࡲࡤࡸ࡭࠭৒")], app[bstack1lll1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡡ࡬ࡨࠬ৓")])
        else:
          bstack1llll1l1l_opy_(bstack1lll1l1111_opy_.format(app))
      else:
        bstack1llll1l1l_opy_(bstack111ll11ll_opy_)
    else:
      for key in app:
        if key in bstack11ll11l11_opy_:
          if key == bstack1lll1l1_opy_ (u"ࠪࡴࡦࡺࡨࠨ৔"):
            if os.path.exists(app[key]):
              bstack1l1l11l1_opy_ = bstack1l1l11ll_opy_(config, app[key])
            else:
              bstack1llll1l1l_opy_(bstack1lll1l1111_opy_.format(app))
          else:
            bstack1l1l11l1_opy_ = app[key]
        else:
          bstack1llll1l1l_opy_(bstack1l11l111_opy_)
  return bstack1l1l11l1_opy_
def bstack1lll11llll_opy_(bstack1l1l11l1_opy_):
  import re
  bstack11l1lll11_opy_ = re.compile(bstack1lll1l1_opy_ (u"ࡶࠧࡤ࡛ࡢ࠯ࡽࡅ࠲ࡠ࠰࠮࠻࡟ࡣ࠳ࡢ࠭࡞ࠬࠧࠦ৕"))
  bstack11l1111l_opy_ = re.compile(bstack1lll1l1_opy_ (u"ࡷࠨ࡞࡜ࡣ࠰ࡾࡆ࠳࡚࠱࠯࠼ࡠࡤ࠴࡜࠮࡟࠭࠳ࡠࡧ࠭ࡻࡃ࠰࡞࠵࠳࠹࡝ࡡ࠱ࡠ࠲ࡣࠪࠥࠤ৖"))
  if bstack1lll1l1_opy_ (u"࠭ࡢࡴ࠼࠲࠳ࠬৗ") in bstack1l1l11l1_opy_ or re.fullmatch(bstack11l1lll11_opy_, bstack1l1l11l1_opy_) or re.fullmatch(bstack11l1111l_opy_, bstack1l1l11l1_opy_):
    return True
  else:
    return False
def bstack1l1l11ll_opy_(config, path, bstack1ll11l1ll_opy_=None):
  import requests
  from requests_toolbelt.multipart.encoder import MultipartEncoder
  import hashlib
  md5_hash = hashlib.md5(open(os.path.abspath(path), bstack1lll1l1_opy_ (u"ࠧࡳࡤࠪ৘")).read()).hexdigest()
  bstack111l1llll_opy_ = bstack1llll1l11_opy_(md5_hash)
  bstack1l1l11l1_opy_ = None
  if bstack111l1llll_opy_:
    logger.info(bstack1l1l1ll1l1_opy_.format(bstack111l1llll_opy_, md5_hash))
    return bstack111l1llll_opy_
  bstack1l1l11l111_opy_ = MultipartEncoder(
    fields={
      bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪ࠭৙"): (os.path.basename(path), open(os.path.abspath(path), bstack1lll1l1_opy_ (u"ࠩࡵࡦࠬ৚")), bstack1lll1l1_opy_ (u"ࠪࡸࡪࡾࡴ࠰ࡲ࡯ࡥ࡮ࡴࠧ৛")),
      bstack1lll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡣ࡮ࡪࠧড়"): bstack1ll11l1ll_opy_
    }
  )
  response = requests.post(bstack1l11ll1ll1_opy_, data=bstack1l1l11l111_opy_,
                           headers={bstack1lll1l1_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫঢ়"): bstack1l1l11l111_opy_.content_type},
                           auth=(config[bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ৞")], config[bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪয়")]))
  try:
    res = json.loads(response.text)
    bstack1l1l11l1_opy_ = res[bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴࡤࡻࡲ࡭ࠩৠ")]
    logger.info(bstack1llll11ll_opy_.format(bstack1l1l11l1_opy_))
    bstack11l11l1l1_opy_(md5_hash, bstack1l1l11l1_opy_)
  except ValueError as err:
    bstack1llll1l1l_opy_(bstack1l11lll1l_opy_.format(str(err)))
  return bstack1l1l11l1_opy_
def bstack11111lll_opy_(framework_name=None, args=None):
  global CONFIG
  global bstack11l1l11ll_opy_
  bstack1l11l111ll_opy_ = 1
  bstack1l1l1llll1_opy_ = 1
  if bstack1lll1l1_opy_ (u"ࠩࡳࡥࡷࡧ࡬࡭ࡧ࡯ࡷࡕ࡫ࡲࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩৡ") in CONFIG:
    bstack1l1l1llll1_opy_ = CONFIG[bstack1lll1l1_opy_ (u"ࠪࡴࡦࡸࡡ࡭࡮ࡨࡰࡸࡖࡥࡳࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪৢ")]
  else:
    bstack1l1l1llll1_opy_ = bstack1l111l111l_opy_(framework_name, args) or 1
  if bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧৣ") in CONFIG:
    bstack1l11l111ll_opy_ = len(CONFIG[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ৤")])
  bstack11l1l11ll_opy_ = int(bstack1l1l1llll1_opy_) * int(bstack1l11l111ll_opy_)
def bstack1l111l111l_opy_(framework_name, args):
  if framework_name == bstack1ll1lll1l_opy_ and args and bstack1lll1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ৥") in args:
      bstack1ll111l111_opy_ = args.index(bstack1lll1l1_opy_ (u"ࠧ࠮࠯ࡳࡶࡴࡩࡥࡴࡵࡨࡷࠬ০"))
      return int(args[bstack1ll111l111_opy_ + 1]) or 1
  return 1
def bstack1llll1l11_opy_(md5_hash):
  bstack1ll1l11l1l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠨࢀࠪ১")), bstack1lll1l1_opy_ (u"ࠩ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩ২"), bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶࡕࡱ࡮ࡲࡥࡩࡓࡄ࠶ࡊࡤࡷ࡭࠴ࡪࡴࡱࡱࠫ৩"))
  if os.path.exists(bstack1ll1l11l1l_opy_):
    bstack1l11111l_opy_ = json.load(open(bstack1ll1l11l1l_opy_, bstack1lll1l1_opy_ (u"ࠫࡷࡨࠧ৪")))
    if md5_hash in bstack1l11111l_opy_:
      bstack1l1ll1l1l1_opy_ = bstack1l11111l_opy_[md5_hash]
      bstack1l1l111l1_opy_ = datetime.datetime.now()
      bstack1lll1ll11l_opy_ = datetime.datetime.strptime(bstack1l1ll1l1l1_opy_[bstack1lll1l1_opy_ (u"ࠬࡺࡩ࡮ࡧࡶࡸࡦࡳࡰࠨ৫")], bstack1lll1l1_opy_ (u"࠭ࠥࡥ࠱ࠨࡱ࠴࡙ࠫࠡࠧࡋ࠾ࠪࡓ࠺ࠦࡕࠪ৬"))
      if (bstack1l1l111l1_opy_ - bstack1lll1ll11l_opy_).days > 30:
        return None
      elif version.parse(str(__version__)) > version.parse(bstack1l1ll1l1l1_opy_[bstack1lll1l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ৭")]):
        return None
      return bstack1l1ll1l1l1_opy_[bstack1lll1l1_opy_ (u"ࠨ࡫ࡧࠫ৮")]
  else:
    return None
def bstack11l11l1l1_opy_(md5_hash, bstack1l1l11l1_opy_):
  bstack111l11111_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠩࢁࠫ৯")), bstack1lll1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪৰ"))
  if not os.path.exists(bstack111l11111_opy_):
    os.makedirs(bstack111l11111_opy_)
  bstack1ll1l11l1l_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠫࢃ࠭ৱ")), bstack1lll1l1_opy_ (u"ࠬ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬ৲"), bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࡘࡴࡱࡵࡡࡥࡏࡇ࠹ࡍࡧࡳࡩ࠰࡭ࡷࡴࡴࠧ৳"))
  bstack1l1l1111_opy_ = {
    bstack1lll1l1_opy_ (u"ࠧࡪࡦࠪ৴"): bstack1l1l11l1_opy_,
    bstack1lll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡹࡴࡢ࡯ࡳࠫ৵"): datetime.datetime.strftime(datetime.datetime.now(), bstack1lll1l1_opy_ (u"ࠩࠨࡨ࠴ࠫ࡭࠰ࠧ࡜ࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠭৶")),
    bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ৷"): str(__version__)
  }
  if os.path.exists(bstack1ll1l11l1l_opy_):
    bstack1l11111l_opy_ = json.load(open(bstack1ll1l11l1l_opy_, bstack1lll1l1_opy_ (u"ࠫࡷࡨࠧ৸")))
  else:
    bstack1l11111l_opy_ = {}
  bstack1l11111l_opy_[md5_hash] = bstack1l1l1111_opy_
  with open(bstack1ll1l11l1l_opy_, bstack1lll1l1_opy_ (u"ࠧࡽࠫࠣ৹")) as outfile:
    json.dump(bstack1l11111l_opy_, outfile)
def bstack1l11ll1lll_opy_(self):
  return
def bstack1llll1111l_opy_(self):
  return
def bstack1l11ll111_opy_(self):
  global bstack1ll11ll11l_opy_
  bstack1ll11ll11l_opy_(self)
def bstack1l11111l1_opy_():
  global bstack1ll1l11l_opy_
  bstack1ll1l11l_opy_ = True
def bstack1111lll1l_opy_(self):
  global bstack1l111llll_opy_
  global bstack11l1l111l_opy_
  global bstack1l1l1111l_opy_
  try:
    if bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭৺") in bstack1l111llll_opy_ and self.session_id != None and bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡘࡺࡡࡵࡷࡶࠫ৻"), bstack1lll1l1_opy_ (u"ࠨࠩৼ")) != bstack1lll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪ৽"):
      bstack1l11l1111l_opy_ = bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪ৾") if len(threading.current_thread().bstackTestErrorMessages) == 0 else bstack1lll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ৿")
      if bstack1l11l1111l_opy_ == bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬ਀"):
        bstack1l1l11l1l1_opy_(logger)
      if self != None:
        bstack1l11ll11l1_opy_(self, bstack1l11l1111l_opy_, bstack1lll1l1_opy_ (u"࠭ࠬࠡࠩਁ").join(threading.current_thread().bstackTestErrorMessages))
    threading.current_thread().testStatus = bstack1lll1l1_opy_ (u"ࠧࠨਂ")
    if bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨਃ") in bstack1l111llll_opy_ and getattr(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ਄"), None):
      bstack1lll1l111_opy_.bstack1lll1111_opy_(self, bstack1111lll11_opy_, logger, wait=True)
    if bstack1lll1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪਅ") in bstack1l111llll_opy_:
      if not threading.currentThread().behave_test_status:
        bstack1l11ll11l1_opy_(self, bstack1lll1l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦਆ"))
      bstack1ll1ll11l_opy_.bstack11111ll1l_opy_(self)
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡸࡺࡡࡵࡷࡶ࠾ࠥࠨਇ") + str(e))
  bstack1l1l1111l_opy_(self)
  self.session_id = None
def bstack1llll1l1_opy_(self, *args, **kwargs):
  try:
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    from bstack_utils.helper import bstack1l1l1l1l1l_opy_
    global bstack1l111llll_opy_
    command_executor = kwargs.get(bstack1lll1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳࠩਈ"), bstack1lll1l1_opy_ (u"ࠧࠨਉ"))
    bstack1l11l1l1ll_opy_ = False
    if type(command_executor) == str and bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਊ") in command_executor:
      bstack1l11l1l1ll_opy_ = True
    elif isinstance(command_executor, RemoteConnection) and bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬ਋") in str(getattr(command_executor, bstack1lll1l1_opy_ (u"ࠪࡣࡺࡸ࡬ࠨ਌"), bstack1lll1l1_opy_ (u"ࠫࠬ਍"))):
      bstack1l11l1l1ll_opy_ = True
    else:
      return bstack11l111lll_opy_(self, *args, **kwargs)
    if bstack1l11l1l1ll_opy_:
      if kwargs.get(bstack1lll1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭਎")):
        kwargs[bstack1lll1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧਏ")] = bstack1l1l1l1l1l_opy_(kwargs[bstack1lll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨਐ")], bstack1l111llll_opy_)
      elif kwargs.get(bstack1lll1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ਑")):
        kwargs[bstack1lll1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ਒")] = bstack1l1l1l1l1l_opy_(kwargs[bstack1lll1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪਓ")], bstack1l111llll_opy_)
  except Exception as e:
    logger.error(bstack1lll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦਔ").format(str(e)))
  return bstack11l111lll_opy_(self, *args, **kwargs)
def bstack1lll111ll_opy_(self, command_executor=bstack1lll1l1_opy_ (u"ࠧ࡮ࡴࡵࡲ࠽࠳࠴࠷࠲࠸࠰࠳࠲࠵࠴࠱࠻࠶࠷࠸࠹ࠨਕ"), *args, **kwargs):
  bstack1l11l1111_opy_ = bstack1llll1l1_opy_(self, command_executor=command_executor, *args, **kwargs)
  if not bstack1llllll1ll_opy_.on():
    return bstack1l11l1111_opy_
  try:
    logger.debug(bstack1lll1l1_opy_ (u"࠭ࡃࡰ࡯ࡰࡥࡳࡪࠠࡆࡺࡨࡧࡺࡺ࡯ࡳࠢࡺ࡬ࡪࡴࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣ࡭ࡸࠦࡦࡢ࡮ࡶࡩࠥ࠳ࠠࡼࡿࠪਖ").format(str(command_executor)))
    logger.debug(bstack1lll1l1_opy_ (u"ࠧࡉࡷࡥࠤ࡚ࡘࡌࠡ࡫ࡶࠤ࠲ࠦࡻࡾࠩਗ").format(str(command_executor._url)))
    from selenium.webdriver.remote.remote_connection import RemoteConnection
    if isinstance(command_executor, RemoteConnection) and bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰࠫਘ") in command_executor._url:
      bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡶࡩࡸࡹࡩࡰࡰࠪਙ"), True)
  except:
    pass
  if (isinstance(command_executor, str) and bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠭ਚ") in command_executor):
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡣࡸ࡫ࡳࡴ࡫ࡲࡲࠬਛ"), True)
  threading.current_thread().bstackSessionDriver = self
  bstack1l1lll1lll_opy_.bstack1lllll11_opy_(self)
  return bstack1l11l1111_opy_
def bstack1l1llll1_opy_(args):
  return bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷ࠭ਜ") in str(args)
def bstack1l11ll1l1l_opy_(self, driver_command, *args, **kwargs):
  global bstack1l11l111l1_opy_
  global bstack1l1l1ll1l_opy_
  bstack1l1l1ll11_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪਝ"), None) and bstack1llll1l1ll_opy_(
          threading.current_thread(), bstack1lll1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ਞ"), None)
  bstack1ll111l11l_opy_ = getattr(self, bstack1lll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨਟ"), None) != None and getattr(self, bstack1lll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩਠ"), None) == True
  if not bstack1l1l1ll1l_opy_ and bstack1l1l1ll11l_opy_ and bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪਡ") in CONFIG and CONFIG[bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫਢ")] == True and bstack1l1lllllll_opy_.bstack1lll11ll11_opy_(driver_command) and (bstack1ll111l11l_opy_ or bstack1l1l1ll11_opy_) and not bstack1l1llll1_opy_(args):
    try:
      bstack1l1l1ll1l_opy_ = True
      logger.debug(bstack1lll1l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࢀࢃࠧਣ").format(driver_command))
      logger.debug(perform_scan(self, driver_command=driver_command))
    except Exception as err:
      logger.debug(bstack1lll1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡳࡩࡷ࡬࡯ࡳ࡯ࠣࡷࡨࡧ࡮ࠡࡽࢀࠫਤ").format(str(err)))
    bstack1l1l1ll1l_opy_ = False
  response = bstack1l11l111l1_opy_(self, driver_command, *args, **kwargs)
  if (bstack1lll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ਥ") in str(bstack1l111llll_opy_).lower() or bstack1lll1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨਦ") in str(bstack1l111llll_opy_).lower()) and bstack1llllll1ll_opy_.on():
    try:
      if driver_command == bstack1lll1l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ਧ"):
        bstack1l1lll1lll_opy_.bstack1l1111l1_opy_({
            bstack1lll1l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩਨ"): response[bstack1lll1l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪ਩")],
            bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬਪ"): bstack1l1lll1lll_opy_.current_test_uuid() if bstack1l1lll1lll_opy_.current_test_uuid() else bstack1llllll1ll_opy_.current_hook_uuid()
        })
    except:
      pass
  return response
def bstack11l1l111_opy_(self, command_executor,
             desired_capabilities=None, browser_profile=None, proxy=None,
             keep_alive=True, file_detector=None, options=None):
  global CONFIG
  global bstack11l1l111l_opy_
  global bstack11l1llll_opy_
  global bstack1l111l1ll_opy_
  global bstack11l1l1l11_opy_
  global bstack1l1l11111l_opy_
  global bstack1l111llll_opy_
  global bstack11l111lll_opy_
  global bstack11l1l1ll1_opy_
  global bstack1l1l11l1l_opy_
  global bstack1111lll11_opy_
  CONFIG[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡘࡊࡋࠨਫ")] = str(bstack1l111llll_opy_) + str(__version__)
  command_executor = bstack1llll1ll1l_opy_()
  logger.debug(bstack1ll1l11ll_opy_.format(command_executor))
  proxy = bstack11ll1111l_opy_(CONFIG, proxy)
  bstack111l1l11l_opy_ = 0 if bstack11l1llll_opy_ < 0 else bstack11l1llll_opy_
  try:
    if bstack11l1l1l11_opy_ is True:
      bstack111l1l11l_opy_ = int(multiprocessing.current_process().name)
    elif bstack1l1l11111l_opy_ is True:
      bstack111l1l11l_opy_ = int(threading.current_thread().name)
  except:
    bstack111l1l11l_opy_ = 0
  bstack11lllll1ll_opy_ = bstack1l111ll1ll_opy_(CONFIG, bstack111l1l11l_opy_)
  logger.debug(bstack1l11111111_opy_.format(str(bstack11lllll1ll_opy_)))
  if bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫਬ") in CONFIG and bstack11ll1l1l1_opy_(CONFIG[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬਭ")]):
    bstack1ll1llllll_opy_(bstack11lllll1ll_opy_)
  if bstack1111ll1l_opy_.bstack1l11llllll_opy_(CONFIG, bstack111l1l11l_opy_) and bstack1111ll1l_opy_.bstack1ll1l1ll1_opy_(bstack11lllll1ll_opy_, options, desired_capabilities):
    threading.current_thread().a11yPlatform = True
    bstack1111ll1l_opy_.set_capabilities(bstack11lllll1ll_opy_, CONFIG)
  if desired_capabilities:
    bstack1llll11l_opy_ = bstack1llll111ll_opy_(desired_capabilities)
    bstack1llll11l_opy_[bstack1lll1l1_opy_ (u"ࠩࡸࡷࡪ࡝࠳ࡄࠩਮ")] = bstack111111lll_opy_(CONFIG)
    bstack1lll11ll1l_opy_ = bstack1l111ll1ll_opy_(bstack1llll11l_opy_)
    if bstack1lll11ll1l_opy_:
      bstack11lllll1ll_opy_ = update(bstack1lll11ll1l_opy_, bstack11lllll1ll_opy_)
    desired_capabilities = None
  if options:
    bstack1l1l1l1ll1_opy_(options, bstack11lllll1ll_opy_)
  if not options:
    options = bstack1l11l1l1l1_opy_(bstack11lllll1ll_opy_)
  bstack1111lll11_opy_ = CONFIG.get(bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ਯ"))[bstack111l1l11l_opy_]
  if proxy and bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠫ࠹࠴࠱࠱࠰࠳ࠫਰ")):
    options.proxy(proxy)
  if options and bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠬ࠹࠮࠹࠰࠳ࠫ਱")):
    desired_capabilities = None
  if (
          not options and not desired_capabilities
  ) or (
          bstack1l1l1l111_opy_() < version.parse(bstack1lll1l1_opy_ (u"࠭࠳࠯࠺࠱࠴ࠬਲ")) and not desired_capabilities
  ):
    desired_capabilities = {}
    desired_capabilities.update(bstack11lllll1ll_opy_)
  logger.info(bstack1l1l1111ll_opy_)
  if bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠧ࠵࠰࠴࠴࠳࠶ࠧਲ਼")):
    bstack11l111lll_opy_(self, command_executor=command_executor,
              options=options, keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠨ࠵࠱࠼࠳࠶ࠧ਴")):
    bstack11l111lll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities, options=options,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  elif bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠩ࠵࠲࠺࠹࠮࠱ࠩਵ")):
    bstack11l111lll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive, file_detector=file_detector)
  else:
    bstack11l111lll_opy_(self, command_executor=command_executor,
              desired_capabilities=desired_capabilities,
              browser_profile=browser_profile, proxy=proxy,
              keep_alive=keep_alive)
  try:
    bstack1lll1l1l1l_opy_ = bstack1lll1l1_opy_ (u"ࠪࠫਸ਼")
    if bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠫ࠹࠴࠰࠯࠲ࡥ࠵ࠬ਷")):
      bstack1lll1l1l1l_opy_ = self.caps.get(bstack1lll1l1_opy_ (u"ࠧࡵࡰࡵ࡫ࡰࡥࡱࡎࡵࡣࡗࡵࡰࠧਸ"))
    else:
      bstack1lll1l1l1l_opy_ = self.capabilities.get(bstack1lll1l1_opy_ (u"ࠨ࡯ࡱࡶ࡬ࡱࡦࡲࡈࡶࡤࡘࡶࡱࠨਹ"))
    if bstack1lll1l1l1l_opy_:
      bstack1l11llll11_opy_(bstack1lll1l1l1l_opy_)
      if bstack1l1l1l111_opy_() <= version.parse(bstack1lll1l1_opy_ (u"ࠧ࠴࠰࠴࠷࠳࠶ࠧ਺")):
        self.command_executor._url = bstack1lll1l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࠤ਻") + bstack1ll1l1ll_opy_ + bstack1lll1l1_opy_ (u"ࠤ࠽࠼࠵࠵ࡷࡥ࠱࡫ࡹࡧࠨ਼")
      else:
        self.command_executor._url = bstack1lll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳ࠧ਽") + bstack1lll1l1l1l_opy_ + bstack1lll1l1_opy_ (u"ࠦ࠴ࡽࡤ࠰ࡪࡸࡦࠧਾ")
      logger.debug(bstack11l11111l_opy_.format(bstack1lll1l1l1l_opy_))
    else:
      logger.debug(bstack1l11lll1ll_opy_.format(bstack1lll1l1_opy_ (u"ࠧࡕࡰࡵ࡫ࡰࡥࡱࠦࡈࡶࡤࠣࡲࡴࡺࠠࡧࡱࡸࡲࡩࠨਿ")))
  except Exception as e:
    logger.debug(bstack1l11lll1ll_opy_.format(e))
  if bstack1lll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬੀ") in bstack1l111llll_opy_:
    bstack11l111111_opy_(bstack11l1llll_opy_, bstack1l1l11l1l_opy_)
  bstack11l1l111l_opy_ = self.session_id
  if bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧੁ") in bstack1l111llll_opy_ or bstack1lll1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨੂ") in bstack1l111llll_opy_ or bstack1lll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ੃") in bstack1l111llll_opy_:
    threading.current_thread().bstackSessionId = self.session_id
    threading.current_thread().bstackSessionDriver = self
    threading.current_thread().bstackTestErrorMessages = []
    bstack1l1lll1lll_opy_.bstack1lllll11_opy_(self)
  bstack11l1l1ll1_opy_.append(self)
  if bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੄") in CONFIG and bstack1lll1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੅") in CONFIG[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ੆")][bstack111l1l11l_opy_]:
    bstack1l111l1ll_opy_ = CONFIG[bstack1lll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩੇ")][bstack111l1l11l_opy_][bstack1lll1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬੈ")]
  logger.debug(bstack11ll11ll1_opy_.format(bstack11l1l111l_opy_))
try:
  try:
    import Browser
    from subprocess import Popen
    def bstack1ll11l1l11_opy_(self, args, bufsize=-1, executable=None,
              stdin=None, stdout=None, stderr=None,
              preexec_fn=None, close_fds=True,
              shell=False, cwd=None, env=None, universal_newlines=None,
              startupinfo=None, creationflags=0,
              restore_signals=True, start_new_session=False,
              pass_fds=(), *, user=None, group=None, extra_groups=None,
              encoding=None, errors=None, text=None, umask=-1, pipesize=-1):
      global CONFIG
      global bstack1l1ll11l_opy_
      if(bstack1lll1l1_opy_ (u"ࠣ࡫ࡱࡨࡪࡾ࠮࡫ࡵࠥ੉") in args[1]):
        with open(os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠩࢁࠫ੊")), bstack1lll1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪੋ"), bstack1lll1l1_opy_ (u"ࠫ࠳ࡹࡥࡴࡵ࡬ࡳࡳ࡯ࡤࡴ࠰ࡷࡼࡹ࠭ੌ")), bstack1lll1l1_opy_ (u"ࠬࡽ੍ࠧ")) as fp:
          fp.write(bstack1lll1l1_opy_ (u"ࠨࠢ੎"))
        if(not os.path.exists(os.path.join(os.path.dirname(args[1]), bstack1lll1l1_opy_ (u"ࠢࡪࡰࡧࡩࡽࡥࡢࡴࡶࡤࡧࡰ࠴ࡪࡴࠤ੏")))):
          with open(args[1], bstack1lll1l1_opy_ (u"ࠨࡴࠪ੐")) as f:
            lines = f.readlines()
            index = next((i for i, line in enumerate(lines) if bstack1lll1l1_opy_ (u"ࠩࡤࡷࡾࡴࡣࠡࡨࡸࡲࡨࡺࡩࡰࡰࠣࡣࡳ࡫ࡷࡑࡣࡪࡩ࠭ࡩ࡯࡯ࡶࡨࡼࡹ࠲ࠠࡱࡣࡪࡩࠥࡃࠠࡷࡱ࡬ࡨࠥ࠶ࠩࠨੑ") in line), None)
            if index is not None:
                lines.insert(index+2, bstack11111111_opy_)
            lines.insert(1, bstack111lll1ll_opy_)
            f.seek(0)
            with open(os.path.join(os.path.dirname(args[1]), bstack1lll1l1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੒")), bstack1lll1l1_opy_ (u"ࠫࡼ࠭੓")) as bstack1111l1ll1_opy_:
              bstack1111l1ll1_opy_.writelines(lines)
        CONFIG[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡗࡉࡑࠧ੔")] = str(bstack1l111llll_opy_) + str(__version__)
        bstack111l1l11l_opy_ = 0 if bstack11l1llll_opy_ < 0 else bstack11l1llll_opy_
        try:
          if bstack11l1l1l11_opy_ is True:
            bstack111l1l11l_opy_ = int(multiprocessing.current_process().name)
          elif bstack1l1l11111l_opy_ is True:
            bstack111l1l11l_opy_ = int(threading.current_thread().name)
        except:
          bstack111l1l11l_opy_ = 0
        CONFIG[bstack1lll1l1_opy_ (u"ࠨࡵࡴࡧ࡚࠷ࡈࠨ੕")] = False
        CONFIG[bstack1lll1l1_opy_ (u"ࠢࡪࡵࡓࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹࠨ੖")] = True
        bstack11lllll1ll_opy_ = bstack1l111ll1ll_opy_(CONFIG, bstack111l1l11l_opy_)
        logger.debug(bstack1l11111111_opy_.format(str(bstack11lllll1ll_opy_)))
        if CONFIG.get(bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬ੗")):
          bstack1ll1llllll_opy_(bstack11lllll1ll_opy_)
        if bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੘") in CONFIG and bstack1lll1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨਖ਼") in CONFIG[bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧਗ਼")][bstack111l1l11l_opy_]:
          bstack1l111l1ll_opy_ = CONFIG[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨਜ਼")][bstack111l1l11l_opy_][bstack1lll1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫੜ")]
        args.append(os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠧࡿࠩ੝")), bstack1lll1l1_opy_ (u"ࠨ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨਫ਼"), bstack1lll1l1_opy_ (u"ࠩ࠱ࡷࡪࡹࡳࡪࡱࡱ࡭ࡩࡹ࠮ࡵࡺࡷࠫ੟")))
        args.append(str(threading.get_ident()))
        args.append(json.dumps(bstack11lllll1ll_opy_))
        args[1] = os.path.join(os.path.dirname(args[1]), bstack1lll1l1_opy_ (u"ࠥ࡭ࡳࡪࡥࡹࡡࡥࡷࡹࡧࡣ࡬࠰࡭ࡷࠧ੠"))
      bstack1l1ll11l_opy_ = True
      return bstack1ll1lll1l1_opy_(self, args, bufsize=bufsize, executable=executable,
                    stdin=stdin, stdout=stdout, stderr=stderr,
                    preexec_fn=preexec_fn, close_fds=close_fds,
                    shell=shell, cwd=cwd, env=env, universal_newlines=universal_newlines,
                    startupinfo=startupinfo, creationflags=creationflags,
                    restore_signals=restore_signals, start_new_session=start_new_session,
                    pass_fds=pass_fds, user=user, group=group, extra_groups=extra_groups,
                    encoding=encoding, errors=errors, text=text, umask=umask, pipesize=pipesize)
  except Exception as e:
    pass
  import playwright._impl._api_structures
  import playwright._impl._helper
  def bstack1l11l1l1_opy_(self,
        executablePath = None,
        channel = None,
        args = None,
        ignoreDefaultArgs = None,
        handleSIGINT = None,
        handleSIGTERM = None,
        handleSIGHUP = None,
        timeout = None,
        env = None,
        headless = None,
        devtools = None,
        proxy = None,
        downloadsPath = None,
        slowMo = None,
        tracesDir = None,
        chromiumSandbox = None,
        firefoxUserPrefs = None
        ):
    global CONFIG
    global bstack11l1llll_opy_
    global bstack1l111l1ll_opy_
    global bstack11l1l1l11_opy_
    global bstack1l1l11111l_opy_
    global bstack1l111llll_opy_
    CONFIG[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭੡")] = str(bstack1l111llll_opy_) + str(__version__)
    bstack111l1l11l_opy_ = 0 if bstack11l1llll_opy_ < 0 else bstack11l1llll_opy_
    try:
      if bstack11l1l1l11_opy_ is True:
        bstack111l1l11l_opy_ = int(multiprocessing.current_process().name)
      elif bstack1l1l11111l_opy_ is True:
        bstack111l1l11l_opy_ = int(threading.current_thread().name)
    except:
      bstack111l1l11l_opy_ = 0
    CONFIG[bstack1lll1l1_opy_ (u"ࠧ࡯ࡳࡑ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠦ੢")] = True
    bstack11lllll1ll_opy_ = bstack1l111ll1ll_opy_(CONFIG, bstack111l1l11l_opy_)
    logger.debug(bstack1l11111111_opy_.format(str(bstack11lllll1ll_opy_)))
    if CONFIG.get(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࠪ੣")):
      bstack1ll1llllll_opy_(bstack11lllll1ll_opy_)
    if bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ੤") in CONFIG and bstack1lll1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭੥") in CONFIG[bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ੦")][bstack111l1l11l_opy_]:
      bstack1l111l1ll_opy_ = CONFIG[bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭੧")][bstack111l1l11l_opy_][bstack1lll1l1_opy_ (u"ࠫࡸ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩ੨")]
    import urllib
    import json
    bstack111l1ll1_opy_ = bstack1lll1l1_opy_ (u"ࠬࡽࡳࡴ࠼࠲࠳ࡨࡪࡰ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡤࡱࡰ࠳ࡵࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࡀࡥࡤࡴࡸࡃࠧ੩") + urllib.parse.quote(json.dumps(bstack11lllll1ll_opy_))
    browser = self.connect(bstack111l1ll1_opy_)
    return browser
except Exception as e:
    pass
def bstack1lllll1l11_opy_():
    global bstack1l1ll11l_opy_
    global bstack1l111llll_opy_
    try:
        from playwright._impl._browser_type import BrowserType
        from bstack_utils.helper import bstack11llll11l_opy_
        if not bstack1l1l1ll11l_opy_:
          global bstack1lllllll1_opy_
          if not bstack1lllllll1_opy_:
            from bstack_utils.helper import bstack1ll111111_opy_, bstack1ll111ll1l_opy_
            bstack1lllllll1_opy_ = bstack1ll111111_opy_()
            bstack1ll111ll1l_opy_(bstack1l111llll_opy_)
          BrowserType.connect = bstack11llll11l_opy_
          return
        BrowserType.launch = bstack1l11l1l1_opy_
        bstack1l1ll11l_opy_ = True
    except Exception as e:
        pass
    try:
      import Browser
      from subprocess import Popen
      Popen.__init__ = bstack1ll11l1l11_opy_
      bstack1l1ll11l_opy_ = True
    except Exception as e:
      pass
def bstack1llll1l111_opy_(context, bstack1ll1ll11ll_opy_):
  try:
    context.page.evaluate(bstack1lll1l1_opy_ (u"ࠨ࡟ࠡ࠿ࡁࠤࢀࢃࠢ੪"), bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠫ੫")+ json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l1_opy_ (u"ࠣࡿࢀࠦ੬"))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠤࡨࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲ࡯ࡥࡾࡽࡲࡪࡩ࡫ࡸࠥࡹࡥࡴࡵ࡬ࡳࡳࠦ࡮ࡢ࡯ࡨࠤࢀࢃࠢ੭"), e)
def bstack1111111ll_opy_(context, message, level):
  try:
    context.page.evaluate(bstack1lll1l1_opy_ (u"ࠥࡣࠥࡃ࠾ࠡࡽࢀࠦ੮"), bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩ੯") + json.dumps(message) + bstack1lll1l1_opy_ (u"ࠬ࠲ࠢ࡭ࡧࡹࡩࡱࠨ࠺ࠨੰ") + json.dumps(level) + bstack1lll1l1_opy_ (u"࠭ࡽࡾࠩੱ"))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠢࡦࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶࠣࡥࡳࡴ࡯ࡵࡣࡷ࡭ࡴࡴࠠࡼࡿࠥੲ"), e)
def bstack1l11l11l1_opy_(self, url):
  global bstack11l1ll11_opy_
  try:
    bstack1llll11lll_opy_(url)
  except Exception as err:
    logger.debug(bstack1ll1l1l11l_opy_.format(str(err)))
  try:
    bstack11l1ll11_opy_(self, url)
  except Exception as e:
    try:
      bstack1lll1111l1_opy_ = str(e)
      if any(err_msg in bstack1lll1111l1_opy_ for err_msg in bstack1lll1111ll_opy_):
        bstack1llll11lll_opy_(url, True)
    except Exception as err:
      logger.debug(bstack1ll1l1l11l_opy_.format(str(err)))
    raise e
def bstack111ll11l1_opy_(self):
  global bstack1l1ll1l1l_opy_
  bstack1l1ll1l1l_opy_ = self
  return
def bstack1111l1lll_opy_(self):
  global bstack1l111l11l1_opy_
  bstack1l111l11l1_opy_ = self
  return
def bstack1l111ll1l1_opy_(test_name, bstack1l1l11l1ll_opy_):
  global CONFIG
  if percy.bstack11llll1l1_opy_() == bstack1lll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨੳ"):
    bstack1l1ll111l1_opy_ = os.path.relpath(bstack1l1l11l1ll_opy_, start=os.getcwd())
    suite_name, _ = os.path.splitext(bstack1l1ll111l1_opy_)
    bstack1llllll11_opy_ = suite_name + bstack1lll1l1_opy_ (u"ࠤ࠰ࠦੴ") + test_name
    threading.current_thread().percySessionName = bstack1llllll11_opy_
def bstack11ll1llll_opy_(self, test, *args, **kwargs):
  global bstack1l1llllll1_opy_
  test_name = None
  bstack1l1l11l1ll_opy_ = None
  if test:
    test_name = str(test.name)
    bstack1l1l11l1ll_opy_ = str(test.source)
  bstack1l111ll1l1_opy_(test_name, bstack1l1l11l1ll_opy_)
  bstack1l1llllll1_opy_(self, test, *args, **kwargs)
def bstack1l1lll1111_opy_(driver, bstack1llllll11_opy_):
  if not bstack1ll1ll11l1_opy_ and bstack1llllll11_opy_:
      bstack1l111ll11l_opy_ = {
          bstack1lll1l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪੵ"): bstack1lll1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ੶"),
          bstack1lll1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ੷"): {
              bstack1lll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ੸"): bstack1llllll11_opy_
          }
      }
      bstack1lllllll11_opy_ = bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࢁࠬ੹").format(json.dumps(bstack1l111ll11l_opy_))
      driver.execute_script(bstack1lllllll11_opy_)
  if bstack111ll1lll_opy_:
      bstack1l111l1lll_opy_ = {
          bstack1lll1l1_opy_ (u"ࠨࡣࡦࡸ࡮ࡵ࡮ࠨ੺"): bstack1lll1l1_opy_ (u"ࠩࡤࡲࡳࡵࡴࡢࡶࡨࠫ੻"),
          bstack1lll1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭੼"): {
              bstack1lll1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩ੽"): bstack1llllll11_opy_ + bstack1lll1l1_opy_ (u"ࠬࠦࡰࡢࡵࡶࡩࡩࠧࠧ੾"),
              bstack1lll1l1_opy_ (u"࠭࡬ࡦࡸࡨࡰࠬ੿"): bstack1lll1l1_opy_ (u"ࠧࡪࡰࡩࡳࠬ઀")
          }
      }
      if bstack111ll1lll_opy_.status == bstack1lll1l1_opy_ (u"ࠨࡒࡄࡗࡘ࠭ઁ"):
          bstack1lllll1111_opy_ = bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࢀࢃࠧં").format(json.dumps(bstack1l111l1lll_opy_))
          driver.execute_script(bstack1lllll1111_opy_)
          bstack1l11ll11l1_opy_(driver, bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪઃ"))
      elif bstack111ll1lll_opy_.status == bstack1lll1l1_opy_ (u"ࠫࡋࡇࡉࡍࠩ઄"):
          reason = bstack1lll1l1_opy_ (u"ࠧࠨઅ")
          bstack1l1l1l11l1_opy_ = bstack1llllll11_opy_ + bstack1lll1l1_opy_ (u"࠭ࠠࡧࡣ࡬ࡰࡪࡪࠧઆ")
          if bstack111ll1lll_opy_.message:
              reason = str(bstack111ll1lll_opy_.message)
              bstack1l1l1l11l1_opy_ = bstack1l1l1l11l1_opy_ + bstack1lll1l1_opy_ (u"ࠧࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶ࠿ࠦࠧઇ") + reason
          bstack1l111l1lll_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫઈ")] = {
              bstack1lll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨઉ"): bstack1lll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩઊ"),
              bstack1lll1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩઋ"): bstack1l1l1l11l1_opy_
          }
          bstack1lllll1111_opy_ = bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࡿࠪઌ").format(json.dumps(bstack1l111l1lll_opy_))
          driver.execute_script(bstack1lllll1111_opy_)
          bstack1l11ll11l1_opy_(driver, bstack1lll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ઍ"), reason)
          bstack111ll111l_opy_(reason, str(bstack111ll1lll_opy_), str(bstack11l1llll_opy_), logger)
def bstack1l1ll11lll_opy_(driver, test):
  if percy.bstack11llll1l1_opy_() == bstack1lll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧ઎") and percy.bstack1ll111llll_opy_() == bstack1lll1l1_opy_ (u"ࠣࡶࡨࡷࡹࡩࡡࡴࡧࠥએ"):
      bstack11lll111l_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡔࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬઐ"), None)
      bstack1ll1111l1_opy_(driver, bstack11lll111l_opy_, test)
  if bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠪ࡭ࡸࡇ࠱࠲ࡻࡗࡩࡸࡺࠧઑ"), None) and bstack1llll1l1ll_opy_(
          threading.current_thread(), bstack1lll1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ઒"), None):
      logger.info(bstack1lll1l1_opy_ (u"ࠧࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠣࡔࡷࡵࡣࡦࡵࡶ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡯ࡳࠡࡷࡱࡨࡪࡸࡷࡢࡻ࠱ࠤࠧઓ"))
      bstack1111ll1l_opy_.bstack11ll1l111_opy_(driver, name=test.name, path=test.source)
def bstack1lll1l11ll_opy_(test, bstack1llllll11_opy_):
    try:
      data = {}
      if test:
        data[bstack1lll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫઔ")] = bstack1llllll11_opy_
      if bstack111ll1lll_opy_:
        if bstack111ll1lll_opy_.status == bstack1lll1l1_opy_ (u"ࠧࡑࡃࡖࡗࠬક"):
          data[bstack1lll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨખ")] = bstack1lll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩગ")
        elif bstack111ll1lll_opy_.status == bstack1lll1l1_opy_ (u"ࠪࡊࡆࡏࡌࠨઘ"):
          data[bstack1lll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫઙ")] = bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬચ")
          if bstack111ll1lll_opy_.message:
            data[bstack1lll1l1_opy_ (u"࠭ࡲࡦࡣࡶࡳࡳ࠭છ")] = str(bstack111ll1lll_opy_.message)
      user = CONFIG[bstack1lll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩજ")]
      key = CONFIG[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫઝ")]
      url = bstack1lll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡤࡴ࡮࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡤࡹࡹࡵ࡭ࡢࡶࡨ࠳ࡸ࡫ࡳࡴ࡫ࡲࡲࡸ࠵ࡻࡾ࠰࡭ࡷࡴࡴࠧઞ").format(user, key, bstack11l1l111l_opy_)
      headers = {
        bstack1lll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩટ"): bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧઠ"),
      }
      if bool(data):
        requests.put(url, json=data, headers=headers)
    except Exception as e:
      logger.error(bstack1l1l1l1l_opy_.format(str(e)))
def bstack1ll11lll1l_opy_(test, bstack1llllll11_opy_):
  global CONFIG
  global bstack1l111l11l1_opy_
  global bstack1l1ll1l1l_opy_
  global bstack11l1l111l_opy_
  global bstack111ll1lll_opy_
  global bstack1l111l1ll_opy_
  global bstack1l1ll1ll1_opy_
  global bstack11l1l1111_opy_
  global bstack1ll1l11ll1_opy_
  global bstack1l1l1ll1_opy_
  global bstack11l1l1ll1_opy_
  global bstack1111lll11_opy_
  try:
    if not bstack11l1l111l_opy_:
      with open(os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠬࢄࠧડ")), bstack1lll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ઢ"), bstack1lll1l1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩણ"))) as f:
        bstack1ll1l1l1_opy_ = json.loads(bstack1lll1l1_opy_ (u"ࠣࡽࠥત") + f.read().strip() + bstack1lll1l1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫથ") + bstack1lll1l1_opy_ (u"ࠥࢁࠧદ"))
        bstack11l1l111l_opy_ = bstack1ll1l1l1_opy_[str(threading.get_ident())]
  except:
    pass
  if bstack11l1l1ll1_opy_:
    for driver in bstack11l1l1ll1_opy_:
      if bstack11l1l111l_opy_ == driver.session_id:
        if test:
          bstack1l1ll11lll_opy_(driver, test)
        bstack1l1lll1111_opy_(driver, bstack1llllll11_opy_)
  elif bstack11l1l111l_opy_:
    bstack1lll1l11ll_opy_(test, bstack1llllll11_opy_)
  if bstack1l111l11l1_opy_:
    bstack11l1l1111_opy_(bstack1l111l11l1_opy_)
  if bstack1l1ll1l1l_opy_:
    bstack1ll1l11ll1_opy_(bstack1l1ll1l1l_opy_)
  if bstack1ll1l11l_opy_:
    bstack1l1l1ll1_opy_()
def bstack11lll1l11_opy_(self, test, *args, **kwargs):
  bstack1llllll11_opy_ = None
  if test:
    bstack1llllll11_opy_ = str(test.name)
  bstack1ll11lll1l_opy_(test, bstack1llllll11_opy_)
  bstack1l1ll1ll1_opy_(self, test, *args, **kwargs)
def bstack1llll11l11_opy_(self, parent, test, skip_on_failure=None, rpa=False):
  global bstack1l1111111_opy_
  global CONFIG
  global bstack11l1l1ll1_opy_
  global bstack11l1l111l_opy_
  bstack1l1111l11_opy_ = None
  try:
    if bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪધ"), None):
      try:
        if not bstack11l1l111l_opy_:
          with open(os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠬࢄࠧન")), bstack1lll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭઩"), bstack1lll1l1_opy_ (u"ࠧ࠯ࡵࡨࡷࡸ࡯࡯࡯࡫ࡧࡷ࠳ࡺࡸࡵࠩપ"))) as f:
            bstack1ll1l1l1_opy_ = json.loads(bstack1lll1l1_opy_ (u"ࠣࡽࠥફ") + f.read().strip() + bstack1lll1l1_opy_ (u"ࠩࠥࡼࠧࡀࠠࠣࡻࠥࠫબ") + bstack1lll1l1_opy_ (u"ࠥࢁࠧભ"))
            bstack11l1l111l_opy_ = bstack1ll1l1l1_opy_[str(threading.get_ident())]
      except:
        pass
      if bstack11l1l1ll1_opy_:
        for driver in bstack11l1l1ll1_opy_:
          if bstack11l1l111l_opy_ == driver.session_id:
            bstack1l1111l11_opy_ = driver
    bstack1l1lll1l1_opy_ = bstack1111ll1l_opy_.bstack1lllll11ll_opy_(test.tags)
    if bstack1l1111l11_opy_:
      threading.current_thread().isA11yTest = bstack1111ll1l_opy_.bstack1l111l1l1l_opy_(bstack1l1111l11_opy_, bstack1l1lll1l1_opy_)
    else:
      threading.current_thread().isA11yTest = bstack1l1lll1l1_opy_
  except:
    pass
  bstack1l1111111_opy_(self, parent, test, skip_on_failure=skip_on_failure, rpa=rpa)
  global bstack111ll1lll_opy_
  bstack111ll1lll_opy_ = self._test
def bstack111111l1l_opy_():
  global bstack1l111lllll_opy_
  try:
    if os.path.exists(bstack1l111lllll_opy_):
      os.remove(bstack1l111lllll_opy_)
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠫࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡤࡦ࡮ࡨࡸ࡮ࡴࡧࠡࡴࡲࡦࡴࡺࠠࡳࡧࡳࡳࡷࡺࠠࡧ࡫࡯ࡩ࠿ࠦࠧમ") + str(e))
def bstack1ll1l11111_opy_():
  global bstack1l111lllll_opy_
  bstack1l11111l11_opy_ = {}
  try:
    if not os.path.isfile(bstack1l111lllll_opy_):
      with open(bstack1l111lllll_opy_, bstack1lll1l1_opy_ (u"ࠬࡽࠧય")):
        pass
      with open(bstack1l111lllll_opy_, bstack1lll1l1_opy_ (u"ࠨࡷࠬࠤર")) as outfile:
        json.dump({}, outfile)
    if os.path.exists(bstack1l111lllll_opy_):
      bstack1l11111l11_opy_ = json.load(open(bstack1l111lllll_opy_, bstack1lll1l1_opy_ (u"ࠧࡳࡤࠪ઱")))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠨࡇࡵࡶࡴࡸࠠࡪࡰࠣࡶࡪࡧࡤࡪࡰࡪࠤࡷࡵࡢࡰࡶࠣࡶࡪࡶ࡯ࡳࡶࠣࡪ࡮ࡲࡥ࠻ࠢࠪલ") + str(e))
  finally:
    return bstack1l11111l11_opy_
def bstack11l111111_opy_(platform_index, item_index):
  global bstack1l111lllll_opy_
  try:
    bstack1l11111l11_opy_ = bstack1ll1l11111_opy_()
    bstack1l11111l11_opy_[item_index] = platform_index
    with open(bstack1l111lllll_opy_, bstack1lll1l1_opy_ (u"ࠤࡺ࠯ࠧળ")) as outfile:
      json.dump(bstack1l11111l11_opy_, outfile)
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡽࡲࡪࡶ࡬ࡲ࡬ࠦࡴࡰࠢࡵࡳࡧࡵࡴࠡࡴࡨࡴࡴࡸࡴࠡࡨ࡬ࡰࡪࡀࠠࠨ઴") + str(e))
def bstack111lll11_opy_(bstack11ll1l1l_opy_):
  global CONFIG
  bstack1ll1111l1l_opy_ = bstack1lll1l1_opy_ (u"ࠫࠬવ")
  if not bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨશ") in CONFIG:
    logger.info(bstack1lll1l1_opy_ (u"࠭ࡎࡰࠢࡳࡰࡦࡺࡦࡰࡴࡰࡷࠥࡶࡡࡴࡵࡨࡨࠥࡻ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡩࡨࡲࡪࡸࡡࡵࡧࠣࡶࡪࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡓࡱࡥࡳࡹࠦࡲࡶࡰࠪષ"))
  try:
    platform = CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪસ")][bstack11ll1l1l_opy_]
    if bstack1lll1l1_opy_ (u"ࠨࡱࡶࠫહ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠩࡲࡷࠬ઺")]) + bstack1lll1l1_opy_ (u"ࠪ࠰ࠥ࠭઻")
    if bstack1lll1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴ઼ࠧ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨઽ")]) + bstack1lll1l1_opy_ (u"࠭ࠬࠡࠩા")
    if bstack1lll1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫિ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬી")]) + bstack1lll1l1_opy_ (u"ࠩ࠯ࠤࠬુ")
    if bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬૂ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ૃ")]) + bstack1lll1l1_opy_ (u"ࠬ࠲ࠠࠨૄ")
    if bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫૅ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ૆")]) + bstack1lll1l1_opy_ (u"ࠨ࠮ࠣࠫે")
    if bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪૈ") in platform:
      bstack1ll1111l1l_opy_ += str(platform[bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫૉ")]) + bstack1lll1l1_opy_ (u"ࠫ࠱ࠦࠧ૊")
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"࡙ࠬ࡯࡮ࡧࠣࡩࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥ࡯ࡧࡵࡥࡹ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡺࡲࡪࡰࡪࠤ࡫ࡵࡲࠡࡴࡨࡴࡴࡸࡴࠡࡩࡨࡲࡪࡸࡡࡵ࡫ࡲࡲࠬો") + str(e))
  finally:
    if bstack1ll1111l1l_opy_[len(bstack1ll1111l1l_opy_) - 2:] == bstack1lll1l1_opy_ (u"࠭ࠬࠡࠩૌ"):
      bstack1ll1111l1l_opy_ = bstack1ll1111l1l_opy_[:-2]
    return bstack1ll1111l1l_opy_
def bstack11l1l1l1l_opy_(path, bstack1ll1111l1l_opy_):
  try:
    import xml.etree.ElementTree as ET
    bstack11l111l1l_opy_ = ET.parse(path)
    bstack1lll1111l_opy_ = bstack11l111l1l_opy_.getroot()
    bstack1ll11l1l_opy_ = None
    for suite in bstack1lll1111l_opy_.iter(bstack1lll1l1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ્࠭")):
      if bstack1lll1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨ૎") in suite.attrib:
        suite.attrib[bstack1lll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ૏")] += bstack1lll1l1_opy_ (u"ࠪࠤࠬૐ") + bstack1ll1111l1l_opy_
        bstack1ll11l1l_opy_ = suite
    bstack1l11l1ll11_opy_ = None
    for robot in bstack1lll1111l_opy_.iter(bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪ૑")):
      bstack1l11l1ll11_opy_ = robot
    bstack1ll111l11_opy_ = len(bstack1l11l1ll11_opy_.findall(bstack1lll1l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૒")))
    if bstack1ll111l11_opy_ == 1:
      bstack1l11l1ll11_opy_.remove(bstack1l11l1ll11_opy_.findall(bstack1lll1l1_opy_ (u"࠭ࡳࡶ࡫ࡷࡩࠬ૓"))[0])
      bstack1ll11111_opy_ = ET.Element(bstack1lll1l1_opy_ (u"ࠧࡴࡷ࡬ࡸࡪ࠭૔"), attrib={bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭૕"): bstack1lll1l1_opy_ (u"ࠩࡖࡹ࡮ࡺࡥࡴࠩ૖"), bstack1lll1l1_opy_ (u"ࠪ࡭ࡩ࠭૗"): bstack1lll1l1_opy_ (u"ࠫࡸ࠶ࠧ૘")})
      bstack1l11l1ll11_opy_.insert(1, bstack1ll11111_opy_)
      bstack1ll1l1lll_opy_ = None
      for suite in bstack1l11l1ll11_opy_.iter(bstack1lll1l1_opy_ (u"ࠬࡹࡵࡪࡶࡨࠫ૙")):
        bstack1ll1l1lll_opy_ = suite
      bstack1ll1l1lll_opy_.append(bstack1ll11l1l_opy_)
      bstack1l1lll1l_opy_ = None
      for status in bstack1ll11l1l_opy_.iter(bstack1lll1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭૚")):
        bstack1l1lll1l_opy_ = status
      bstack1ll1l1lll_opy_.append(bstack1l1lll1l_opy_)
    bstack11l111l1l_opy_.write(path)
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠧࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡳࡥࡷࡹࡩ࡯ࡩࠣࡻ࡭࡯࡬ࡦࠢࡪࡩࡳ࡫ࡲࡢࡶ࡬ࡲ࡬ࠦࡲࡰࡤࡲࡸࠥࡸࡥࡱࡱࡵࡸࠬ૛") + str(e))
def bstack1l11ll1l11_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name):
  global bstack1ll11l1lll_opy_
  global CONFIG
  if bstack1lll1l1_opy_ (u"ࠣࡲࡼࡸ࡭ࡵ࡮ࡱࡣࡷ࡬ࠧ૜") in options:
    del options[bstack1lll1l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡲࡤࡸ࡭ࠨ૝")]
  bstack1lll1ll111_opy_ = bstack1ll1l11111_opy_()
  for bstack1l1l1l1l1_opy_ in bstack1lll1ll111_opy_.keys():
    path = os.path.join(os.getcwd(), bstack1lll1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࡡࡵࡩࡸࡻ࡬ࡵࡵࠪ૞"), str(bstack1l1l1l1l1_opy_), bstack1lll1l1_opy_ (u"ࠫࡴࡻࡴࡱࡷࡷ࠲ࡽࡳ࡬ࠨ૟"))
    bstack11l1l1l1l_opy_(path, bstack111lll11_opy_(bstack1lll1ll111_opy_[bstack1l1l1l1l1_opy_]))
  bstack111111l1l_opy_()
  return bstack1ll11l1lll_opy_(outs_dir, pabot_args, options, start_time_string, tests_root_name)
def bstack11l1llll1_opy_(self, ff_profile_dir):
  global bstack111ll1ll_opy_
  if not ff_profile_dir:
    return None
  return bstack111ll1ll_opy_(self, ff_profile_dir)
def bstack1ll111ll_opy_(datasources, opts_for_run, outs_dir, pabot_args, suite_group):
  from pabot.pabot import QueueItem
  global CONFIG
  global bstack1ll11l1111_opy_
  bstack111ll1ll1_opy_ = []
  if bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨૠ") in CONFIG:
    bstack111ll1ll1_opy_ = CONFIG[bstack1lll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩૡ")]
  return [
    QueueItem(
      datasources,
      outs_dir,
      opts_for_run,
      suite,
      pabot_args[bstack1lll1l1_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣૢ")],
      pabot_args[bstack1lll1l1_opy_ (u"ࠣࡸࡨࡶࡧࡵࡳࡦࠤૣ")],
      argfile,
      pabot_args.get(bstack1lll1l1_opy_ (u"ࠤ࡫࡭ࡻ࡫ࠢ૤")),
      pabot_args[bstack1lll1l1_opy_ (u"ࠥࡴࡷࡵࡣࡦࡵࡶࡩࡸࠨ૥")],
      platform[0],
      bstack1ll11l1111_opy_
    )
    for suite in suite_group
    for argfile in pabot_args[bstack1lll1l1_opy_ (u"ࠦࡦࡸࡧࡶ࡯ࡨࡲࡹ࡬ࡩ࡭ࡧࡶࠦ૦")] or [(bstack1lll1l1_opy_ (u"ࠧࠨ૧"), None)]
    for platform in enumerate(bstack111ll1ll1_opy_)
  ]
def bstack1ll11l11_opy_(self, datasources, outs_dir, options,
                        execution_item, command, verbose, argfile,
                        hive=None, processes=0, platform_index=0, bstack1ll11lll1_opy_=bstack1lll1l1_opy_ (u"࠭ࠧ૨")):
  global bstack1lll1l1ll1_opy_
  self.platform_index = platform_index
  self.bstack1lll111l1l_opy_ = bstack1ll11lll1_opy_
  bstack1lll1l1ll1_opy_(self, datasources, outs_dir, options,
                      execution_item, command, verbose, argfile, hive, processes)
def bstack1l1ll1111l_opy_(caller_id, datasources, is_last, item, outs_dir):
  global bstack1l1l1ll111_opy_
  global bstack111lllll_opy_
  bstack1lllll1l1l_opy_ = copy.deepcopy(item)
  if not bstack1lll1l1_opy_ (u"ࠧࡷࡣࡵ࡭ࡦࡨ࡬ࡦࠩ૩") in item.options:
    bstack1lllll1l1l_opy_.options[bstack1lll1l1_opy_ (u"ࠨࡸࡤࡶ࡮ࡧࡢ࡭ࡧࠪ૪")] = []
  bstack1ll1l1l11_opy_ = bstack1lllll1l1l_opy_.options[bstack1lll1l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૫")].copy()
  for v in bstack1lllll1l1l_opy_.options[bstack1lll1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૬")]:
    if bstack1lll1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪ૭") in v:
      bstack1ll1l1l11_opy_.remove(v)
    if bstack1lll1l1_opy_ (u"ࠬࡈࡓࡕࡃࡆࡏࡈࡒࡉࡂࡔࡊࡗࠬ૮") in v:
      bstack1ll1l1l11_opy_.remove(v)
    if bstack1lll1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ૯") in v:
      bstack1ll1l1l11_opy_.remove(v)
  bstack1ll1l1l11_opy_.insert(0, bstack1lll1l1_opy_ (u"ࠧࡃࡕࡗࡅࡈࡑࡐࡍࡃࡗࡊࡔࡘࡍࡊࡐࡇࡉ࡝ࡀࡻࡾࠩ૰").format(bstack1lllll1l1l_opy_.platform_index))
  bstack1ll1l1l11_opy_.insert(0, bstack1lll1l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡅࡇࡉࡐࡔࡉࡁࡍࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖ࠿ࢁࡽࠨ૱").format(bstack1lllll1l1l_opy_.bstack1lll111l1l_opy_))
  bstack1lllll1l1l_opy_.options[bstack1lll1l1_opy_ (u"ࠩࡹࡥࡷ࡯ࡡࡣ࡮ࡨࠫ૲")] = bstack1ll1l1l11_opy_
  if bstack111lllll_opy_:
    bstack1lllll1l1l_opy_.options[bstack1lll1l1_opy_ (u"ࠪࡺࡦࡸࡩࡢࡤ࡯ࡩࠬ૳")].insert(0, bstack1lll1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡇࡑࡏࡁࡓࡉࡖ࠾ࢀࢃࠧ૴").format(bstack111lllll_opy_))
  return bstack1l1l1ll111_opy_(caller_id, datasources, is_last, bstack1lllll1l1l_opy_, outs_dir)
def bstack1ll1lll11l_opy_(command, item_index):
  if bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭૵")):
    os.environ[bstack1lll1l1_opy_ (u"࠭ࡃࡖࡔࡕࡉࡓ࡚࡟ࡑࡎࡄࡘࡋࡕࡒࡎࡡࡇࡅ࡙ࡇࠧ૶")] = json.dumps(CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ૷")][item_index % bstack11lll1lll_opy_])
  global bstack111lllll_opy_
  if bstack111lllll_opy_:
    command[0] = command[0].replace(bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ૸"), bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠮ࡵࡧ࡯ࠥࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱࠦ࠭࠮ࡤࡶࡸࡦࡩ࡫ࡠ࡫ࡷࡩࡲࡥࡩ࡯ࡦࡨࡼࠥ࠭ૹ") + str(
      item_index) + bstack1lll1l1_opy_ (u"ࠪࠤࠬૺ") + bstack111lllll_opy_, 1)
  else:
    command[0] = command[0].replace(bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪૻ"),
                                    bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠱ࡸࡪ࡫ࠡࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠢ࠰࠱ࡧࡹࡴࡢࡥ࡮ࡣ࡮ࡺࡥ࡮ࡡ࡬ࡲࡩ࡫ࡸࠡࠩૼ") + str(item_index), 1)
def bstack11ll111l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index):
  global bstack11l11l11l_opy_
  bstack1ll1lll11l_opy_(command, item_index)
  return bstack11l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index)
def bstack11ll1111_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir):
  global bstack11l11l11l_opy_
  bstack1ll1lll11l_opy_(command, item_index)
  return bstack11l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir)
def bstack1l11ll11_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout):
  global bstack11l11l11l_opy_
  bstack1ll1lll11l_opy_(command, item_index)
  return bstack11l11l11l_opy_(command, stderr, stdout, item_name, verbose, pool_id, item_index, outs_dir, process_timeout)
def is_driver_active(driver):
  return True if driver and driver.session_id else False
def bstack1111lll1_opy_(self, runner, quiet=False, capture=True):
  global bstack11111ll1_opy_
  bstack1111l1l1_opy_ = bstack11111ll1_opy_(self, runner, quiet=quiet, capture=capture)
  if self.exception:
    if not hasattr(runner, bstack1lll1l1_opy_ (u"࠭ࡥࡹࡥࡨࡴࡹ࡯࡯࡯ࡡࡤࡶࡷ࠭૽")):
      runner.exception_arr = []
    if not hasattr(runner, bstack1lll1l1_opy_ (u"ࠧࡦࡺࡦࡣࡹࡸࡡࡤࡧࡥࡥࡨࡱ࡟ࡢࡴࡵࠫ૾")):
      runner.exc_traceback_arr = []
    runner.exception = self.exception
    runner.exc_traceback = self.exc_traceback
    runner.exception_arr.append(self.exception)
    runner.exc_traceback_arr.append(self.exc_traceback)
  return bstack1111l1l1_opy_
def bstack11llllllll_opy_(runner, hook_name, context, element, bstack1l1111111l_opy_, *args):
  try:
    if runner.hooks.get(hook_name):
      bstack111llll1_opy_.bstack1l11l1lll_opy_(hook_name, element)
    bstack1l1111111l_opy_(runner, hook_name, context, *args)
    if runner.hooks.get(hook_name):
      bstack111llll1_opy_.bstack1ll111l1ll_opy_(element)
      if hook_name not in [bstack1lll1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠬ૿"), bstack1lll1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬ଀")] and args and hasattr(args[0], bstack1lll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡡࡰࡩࡸࡹࡡࡨࡧࠪଁ")):
        args[0].error_message = bstack1lll1l1_opy_ (u"ࠫࠬଂ")
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠬࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡࡪࡤࡲࡩࡲࡥࠡࡪࡲࡳࡰࡹࠠࡪࡰࠣࡦࡪ࡮ࡡࡷࡧ࠽ࠤࢀࢃࠧଃ").format(str(e)))
def bstack1lll1l111l_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    if runner.hooks.get(bstack1lll1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ଄")).__name__ != bstack1lll1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࡣࡩ࡫ࡦࡢࡷ࡯ࡸࡤ࡮࡯ࡰ࡭ࠥଅ"):
      bstack11llllllll_opy_(runner, name, context, runner, bstack1l1111111l_opy_, *args)
    try:
      threading.current_thread().bstackSessionDriver if bstack1l1llll11l_opy_(bstack1lll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡔࡧࡶࡷ࡮ࡵ࡮ࡅࡴ࡬ࡺࡪࡸࠧଆ")) else context.browser
      runner.driver_initialised = bstack1lll1l1_opy_ (u"ࠤࡥࡩ࡫ࡵࡲࡦࡡࡤࡰࡱࠨଇ")
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࠣࡨࡷ࡯ࡶࡦࡴࠣ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡸ࡫ࠠࡢࡶࡷࡶ࡮ࡨࡵࡵࡧ࠽ࠤࢀࢃࠧଈ").format(str(e)))
def bstack1lllllllll_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    bstack11llllllll_opy_(runner, name, context, context.feature, bstack1l1111111l_opy_, *args)
    try:
      if not bstack1ll1ll11l1_opy_:
        bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llll11l_opy_(bstack1lll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଉ")) else context.browser
        if is_driver_active(bstack1l1111l11_opy_):
          if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨଊ")
          bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack1llll1l111_opy_(context, bstack1ll1ll11ll_opy_)
          bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଋ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l1_opy_ (u"ࠧࡾࡿࠪଌ"))
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠨࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡸ࡫ࡴࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡱࡥࡲ࡫ࠠࡪࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡪࡪࡧࡴࡶࡴࡨ࠾ࠥࢁࡽࠨ଍").format(str(e)))
def bstack1lll1llll_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    bstack111llll1_opy_.start_test(context)
    bstack11llllllll_opy_(runner, name, context, context.scenario, bstack1l1111111l_opy_, *args)
def bstack1l1ll1l11l_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    if len(context.scenario.tags) == 0: bstack111llll1_opy_.start_test(context)
    bstack11llllllll_opy_(runner, name, context, context.scenario, bstack1l1111111l_opy_, *args)
    threading.current_thread().a11y_stop = False
    bstack1ll1ll11l_opy_.bstack1111l111l_opy_(context, *args)
    try:
      bstack1l1111l11_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡕࡨࡷࡸ࡯࡯࡯ࡆࡵ࡭ࡻ࡫ࡲࠨ଎"), context.browser)
      if is_driver_active(bstack1l1111l11_opy_):
        bstack1l1lll1lll_opy_.bstack1lllll11_opy_(bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଏ"), {}))
        if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡩࡥ࡯ࡣࡵ࡭ࡴࠨଐ")
        if (not bstack1ll1ll11l1_opy_):
          scenario_name = args[0].name
          feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l1_opy_ (u"ࠬࠦ࠭ࠡࠩ଑") + scenario_name
          if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡳࡤࡧࡱࡥࡷ࡯࡯ࠣ଒"):
            bstack1llll1l111_opy_(context, bstack1ll1ll11ll_opy_)
            bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଓ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l1_opy_ (u"ࠨࡿࢀࠫଔ"))
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡥ࡯ࡣࡵ࡭ࡴࡀࠠࡼࡿࠪକ").format(str(e)))
def bstack1l1ll111_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    bstack11llllllll_opy_(runner, name, context, args[0], bstack1l1111111l_opy_, *args)
    try:
      bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llll11l_opy_(bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଖ")) else context.browser
      if is_driver_active(bstack1l1111l11_opy_):
        if runner.driver_initialised is None: runner.driver_initialised = bstack1lll1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤଗ")
        bstack111llll1_opy_.bstack11ll1l1ll_opy_(args[0])
        if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥଘ"):
          feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
          bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l1_opy_ (u"࠭ࠠ࠮ࠢࠪଙ") + context.scenario.name
          bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࡾࠦࡦࡩࡴࡪࡱࡱࠦ࠿ࠦࠢࡴࡧࡷࡗࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠣ࠮ࠣࠦࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠢ࠻ࠢࡾࠦࡳࡧ࡭ࡦࠤ࠽ࠤࠬଚ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l1_opy_ (u"ࠨࡿࢀࠫଛ"))
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠩࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡹࡥࡵࠢࡶࡩࡸࡹࡩࡰࡰࠣࡲࡦࡳࡥࠡ࡫ࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡺࡥࡱ࠼ࠣࡿࢂ࠭ଜ").format(str(e)))
def bstack1lll1llll1_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
  bstack111llll1_opy_.bstack11llll11_opy_(args[0])
  try:
    bstack1ll111ll1_opy_ = args[0].status.name
    bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡖࡩࡸࡹࡩࡰࡰࡇࡶ࡮ࡼࡥࡳࠩଝ") in threading.current_thread().__dict__.keys() else context.browser
    if is_driver_active(bstack1l1111l11_opy_):
      if runner.driver_initialised is None:
        runner.driver_initialised  = bstack1lll1l1_opy_ (u"ࠫ࡮ࡴࡳࡵࡧࡳࠫଞ")
        feature_name = bstack1ll1ll11ll_opy_ = str(runner.feature.name)
        bstack1ll1ll11ll_opy_ = feature_name + bstack1lll1l1_opy_ (u"ࠬࠦ࠭ࠡࠩଟ") + context.scenario.name
        bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࠥࡥࡨࡺࡩࡰࡰࠥ࠾ࠥࠨࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡲࡦࡳࡥࠣ࠼ࠣࠫଠ") + json.dumps(bstack1ll1ll11ll_opy_) + bstack1lll1l1_opy_ (u"ࠧࡾࡿࠪଡ"))
    if str(bstack1ll111ll1_opy_).lower() == bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨଢ"):
      bstack11l11ll11_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪଣ")
      bstack1111ll111_opy_ = bstack1lll1l1_opy_ (u"ࠪࠫତ")
      bstack1l1l11ll11_opy_ = bstack1lll1l1_opy_ (u"ࠫࠬଥ")
      try:
        import traceback
        bstack11l11ll11_opy_ = runner.exception.__class__.__name__
        bstack1l1l11llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111ll111_opy_ = bstack1lll1l1_opy_ (u"ࠬࠦࠧଦ").join(bstack1l1l11llll_opy_)
        bstack1l1l11ll11_opy_ = bstack1l1l11llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11ll11l_opy_.format(str(e)))
      bstack11l11ll11_opy_ += bstack1l1l11ll11_opy_
      bstack1111111ll_opy_(context, json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧଧ") + str(bstack1111ll111_opy_)),
                          bstack1lll1l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨନ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨ଩"):
        bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧପ"), None), bstack1lll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥଫ"), bstack11l11ll11_opy_)
        bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩବ") + json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠧࠦ࠭ࠡࡈࡤ࡭ࡱ࡫ࡤࠢ࡞ࡱࠦଭ") + str(bstack1111ll111_opy_)) + bstack1lll1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦࡪࡸࡲࡰࡴࠥࢁࢂ࠭ମ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡶࡨࡴࠧଯ"):
        bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨର"), bstack1lll1l1_opy_ (u"ࠤࡖࡧࡪࡴࡡࡳ࡫ࡲࠤ࡫ࡧࡩ࡭ࡧࡧࠤࡼ࡯ࡴࡩ࠼ࠣࡠࡳࠨ଱") + str(bstack11l11ll11_opy_))
    else:
      bstack1111111ll_opy_(context, bstack1lll1l1_opy_ (u"ࠥࡔࡦࡹࡳࡦࡦࠤࠦଲ"), bstack1lll1l1_opy_ (u"ࠦ࡮ࡴࡦࡰࠤଳ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡴࡦࡲࠥ଴"):
        bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"࠭ࡰࡢࡩࡨࠫଵ"), None), bstack1lll1l1_opy_ (u"ࠢࡱࡣࡶࡷࡪࡪࠢଶ"))
      bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭ଷ") + json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠤࠣ࠱ࠥࡖࡡࡴࡵࡨࡨࠦࠨସ")) + bstack1lll1l1_opy_ (u"ࠪ࠰ࠥࠨ࡬ࡦࡸࡨࡰࠧࡀࠠࠣ࡫ࡱࡪࡴࠨࡽࡾࠩହ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠤ଺"):
        bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠧࡶࡡࡴࡵࡨࡨࠧ଻"))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡰࡥࡷࡱࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡵࡷࡥࡹࡻࡳࠡ࡫ࡱࠤࡦ࡬ࡴࡦࡴࠣࡷࡹ࡫ࡰ࠻ࠢࡾࢁ଼ࠬ").format(str(e)))
  bstack11llllllll_opy_(runner, name, context, args[0], bstack1l1111111l_opy_, *args)
def bstack1lll1lll11_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
  bstack111llll1_opy_.end_test(args[0])
  try:
    bstack1111111l1_opy_ = args[0].status.name
    bstack1l1111l11_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡓࡦࡵࡶ࡭ࡴࡴࡄࡳ࡫ࡹࡩࡷ࠭ଽ"), context.browser)
    bstack1ll1ll11l_opy_.bstack11111ll1l_opy_(bstack1l1111l11_opy_)
    if str(bstack1111111l1_opy_).lower() == bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨା"):
      bstack11l11ll11_opy_ = bstack1lll1l1_opy_ (u"ࠩࠪି")
      bstack1111ll111_opy_ = bstack1lll1l1_opy_ (u"ࠪࠫୀ")
      bstack1l1l11ll11_opy_ = bstack1lll1l1_opy_ (u"ࠫࠬୁ")
      try:
        import traceback
        bstack11l11ll11_opy_ = runner.exception.__class__.__name__
        bstack1l1l11llll_opy_ = traceback.format_tb(runner.exc_traceback)
        bstack1111ll111_opy_ = bstack1lll1l1_opy_ (u"ࠬࠦࠧୂ").join(bstack1l1l11llll_opy_)
        bstack1l1l11ll11_opy_ = bstack1l1l11llll_opy_[-1]
      except Exception as e:
        logger.debug(bstack1l11ll11l_opy_.format(str(e)))
      bstack11l11ll11_opy_ += bstack1l1l11ll11_opy_
      bstack1111111ll_opy_(context, json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧୃ") + str(bstack1111ll111_opy_)),
                          bstack1lll1l1_opy_ (u"ࠢࡦࡴࡵࡳࡷࠨୄ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥ୅") or runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱࠩ୆"):
        bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨେ"), None), bstack1lll1l1_opy_ (u"ࠦ࡫ࡧࡩ࡭ࡧࡧࠦୈ"), bstack11l11ll11_opy_)
        bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୉") + json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠨࠠ࠮ࠢࡉࡥ࡮ࡲࡥࡥࠣ࡟ࡲࠧ୊") + str(bstack1111ll111_opy_)) + bstack1lll1l1_opy_ (u"ࠧ࠭ࠢࠥࡰࡪࡼࡥ࡭ࠤ࠽ࠤࠧ࡫ࡲࡳࡱࡵࠦࢂࢃࠧୋ"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡦࡩࡳࡧࡲࡪࡱࠥୌ") or runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠩ࡬ࡲࡸࡺࡥࡱ୍ࠩ"):
        bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪ୎"), bstack1lll1l1_opy_ (u"ࠦࡘࡩࡥ࡯ࡣࡵ࡭ࡴࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ୏") + str(bstack11l11ll11_opy_))
    else:
      bstack1111111ll_opy_(context, bstack1lll1l1_opy_ (u"ࠧࡖࡡࡴࡵࡨࡨࠦࠨ୐"), bstack1lll1l1_opy_ (u"ࠨࡩ࡯ࡨࡲࠦ୑"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୒") or runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୓"):
        bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"ࠩࡳࡥ࡬࡫ࠧ୔"), None), bstack1lll1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥ୕"))
      bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࡻࠣࡣࡦࡸ࡮ࡵ࡮ࠣ࠼ࠣࠦࡦࡴ࡮ࡰࡶࡤࡸࡪࠨࠬࠡࠤࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠧࡀࠠࡼࠤࡧࡥࡹࡧࠢ࠻ࠩୖ") + json.dumps(str(args[0].name) + bstack1lll1l1_opy_ (u"ࠧࠦ࠭ࠡࡒࡤࡷࡸ࡫ࡤࠢࠤୗ")) + bstack1lll1l1_opy_ (u"࠭ࠬࠡࠤ࡯ࡩࡻ࡫࡬ࠣ࠼ࠣࠦ࡮ࡴࡦࡰࠤࢀࢁࠬ୘"))
      if runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠢࡣࡧࡩࡳࡷ࡫࡟ࡴࡥࡨࡲࡦࡸࡩࡰࠤ୙") or runner.driver_initialised == bstack1lll1l1_opy_ (u"ࠨ࡫ࡱࡷࡹ࡫ࡰࠨ୚"):
        bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠤࡳࡥࡸࡹࡥࡥࠤ୛"))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬଡ଼").format(str(e)))
  bstack11llllllll_opy_(runner, name, context, context.scenario, bstack1l1111111l_opy_, *args)
  if len(context.scenario.tags) == 0: threading.current_thread().current_test_uuid = None
def bstack1l1llll1l1_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    bstack11llllllll_opy_(runner, name, context, context.scenario, bstack1l1111111l_opy_, *args)
    threading.current_thread().current_test_uuid = None
def bstack1llll111l1_opy_(runner, name, context, bstack1l1111111l_opy_, *args):
    try:
      bstack1l1111l11_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪଢ଼"), context.browser)
      if context.failed is True:
        bstack11111111l_opy_ = []
        bstack11ll11111_opy_ = []
        bstack1l1ll11111_opy_ = []
        bstack1lllll11l_opy_ = bstack1lll1l1_opy_ (u"ࠬ࠭୞")
        try:
          import traceback
          for exc in runner.exception_arr:
            bstack11111111l_opy_.append(exc.__class__.__name__)
          for exc_tb in runner.exc_traceback_arr:
            bstack1l1l11llll_opy_ = traceback.format_tb(exc_tb)
            bstack1l1ll1lll_opy_ = bstack1lll1l1_opy_ (u"࠭ࠠࠨୟ").join(bstack1l1l11llll_opy_)
            bstack11ll11111_opy_.append(bstack1l1ll1lll_opy_)
            bstack1l1ll11111_opy_.append(bstack1l1l11llll_opy_[-1])
        except Exception as e:
          logger.debug(bstack1l11ll11l_opy_.format(str(e)))
        bstack11l11ll11_opy_ = bstack1lll1l1_opy_ (u"ࠧࠨୠ")
        for i in range(len(bstack11111111l_opy_)):
          bstack11l11ll11_opy_ += bstack11111111l_opy_[i] + bstack1l1ll11111_opy_[i] + bstack1lll1l1_opy_ (u"ࠨ࡞ࡱࠫୡ")
        bstack1lllll11l_opy_ = bstack1lll1l1_opy_ (u"ࠩࠣࠫୢ").join(bstack11ll11111_opy_)
        if runner.driver_initialised in [bstack1lll1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦୣ"), bstack1lll1l1_opy_ (u"ࠦࡧ࡫ࡦࡰࡴࡨࡣࡦࡲ࡬ࠣ୤")]:
          bstack1111111ll_opy_(context, bstack1lllll11l_opy_, bstack1lll1l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦ୥"))
          bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"࠭ࡰࡢࡩࡨࠫ୦"), None), bstack1lll1l1_opy_ (u"ࠢࡧࡣ࡬ࡰࡪࡪࠢ୧"), bstack11l11ll11_opy_)
          bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࠧࡧࡣࡵ࡫ࡲࡲࠧࡀࠠࠣࡣࡱࡲࡴࡺࡡࡵࡧࠥ࠰ࠥࠨࡡࡳࡩࡸࡱࡪࡴࡴࡴࠤ࠽ࠤࢀࠨࡤࡢࡶࡤࠦ࠿࠭୨") + json.dumps(bstack1lllll11l_opy_) + bstack1lll1l1_opy_ (u"ࠩ࠯ࠤࠧࡲࡥࡷࡧ࡯ࠦ࠿ࠦࠢࡦࡴࡵࡳࡷࠨࡽࡾࠩ୩"))
          bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠥࡪࡦ࡯࡬ࡦࡦࠥ୪"), bstack1lll1l1_opy_ (u"ࠦࡘࡵ࡭ࡦࠢࡶࡧࡪࡴࡡࡳ࡫ࡲࡷࠥ࡬ࡡࡪ࡮ࡨࡨ࠿ࠦ࡜࡯ࠤ୫") + str(bstack11l11ll11_opy_))
          bstack1111l111_opy_ = bstack1lllll1ll_opy_(bstack1lllll11l_opy_, runner.feature.name, logger)
          if (bstack1111l111_opy_ != None):
            bstack1l1lllll1_opy_.append(bstack1111l111_opy_)
      else:
        if runner.driver_initialised in [bstack1lll1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤ࡬ࡥࡢࡶࡸࡶࡪࠨ୬"), bstack1lll1l1_opy_ (u"ࠨࡢࡦࡨࡲࡶࡪࡥࡡ࡭࡮ࠥ୭")]:
          bstack1111111ll_opy_(context, bstack1lll1l1_opy_ (u"ࠢࡇࡧࡤࡸࡺࡸࡥ࠻ࠢࠥ୮") + str(runner.feature.name) + bstack1lll1l1_opy_ (u"ࠣࠢࡳࡥࡸࡹࡥࡥࠣࠥ୯"), bstack1lll1l1_opy_ (u"ࠤ࡬ࡲ࡫ࡵࠢ୰"))
          bstack11lll1ll1_opy_(getattr(context, bstack1lll1l1_opy_ (u"ࠪࡴࡦ࡭ࡥࠨୱ"), None), bstack1lll1l1_opy_ (u"ࠦࡵࡧࡳࡴࡧࡧࠦ୲"))
          bstack1l1111l11_opy_.execute_script(bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࡼࠤࡤࡧࡹ࡯࡯࡯ࠤ࠽ࠤࠧࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠢ࠭ࠢࠥࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸࠨ࠺ࠡࡽࠥࡨࡦࡺࡡࠣ࠼ࠪ୳") + json.dumps(bstack1lll1l1_opy_ (u"ࠨࡆࡦࡣࡷࡹࡷ࡫࠺ࠡࠤ୴") + str(runner.feature.name) + bstack1lll1l1_opy_ (u"ࠢࠡࡲࡤࡷࡸ࡫ࡤࠢࠤ୵")) + bstack1lll1l1_opy_ (u"ࠨ࠮ࠣࠦࡱ࡫ࡶࡦ࡮ࠥ࠾ࠥࠨࡩ࡯ࡨࡲࠦࢂࢃࠧ୶"))
          bstack1l11ll11l1_opy_(bstack1l1111l11_opy_, bstack1lll1l1_opy_ (u"ࠩࡳࡥࡸࡹࡥࡥࠩ୷"))
          bstack1111l111_opy_ = bstack1lllll1ll_opy_(bstack1lllll11l_opy_, runner.feature.name, logger)
          if (bstack1111l111_opy_ != None):
            bstack1l1lllll1_opy_.append(bstack1111l111_opy_)
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠪࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡭ࡢࡴ࡮ࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡹࡴࡢࡶࡸࡷࠥ࡯࡮ࠡࡣࡩࡸࡪࡸࠠࡧࡧࡤࡸࡺࡸࡥ࠻ࠢࡾࢁࠬ୸").format(str(e)))
    bstack11llllllll_opy_(runner, name, context, context.feature, bstack1l1111111l_opy_, *args)
def bstack111l11l1_opy_(self, name, context, *args):
  if bstack1l1l1ll11l_opy_:
    platform_index = int(threading.current_thread()._name) % bstack11lll1lll_opy_
    bstack1l1111ll_opy_ = CONFIG[bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ୹")][platform_index]
    os.environ[bstack1lll1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭୺")] = json.dumps(bstack1l1111ll_opy_)
  global bstack1l1111111l_opy_
  if not hasattr(self, bstack1lll1l1_opy_ (u"࠭ࡤࡳ࡫ࡹࡩࡷࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡴࡧࡧࠫ୻")):
    self.driver_initialised = None
  bstack1ll11111l_opy_ = {
      bstack1lll1l1_opy_ (u"ࠧࡣࡧࡩࡳࡷ࡫࡟ࡢ࡮࡯ࠫ୼"): bstack1lll1l111l_opy_,
      bstack1lll1l1_opy_ (u"ࠨࡤࡨࡪࡴࡸࡥࡠࡨࡨࡥࡹࡻࡲࡦࠩ୽"): bstack1lllllllll_opy_,
      bstack1lll1l1_opy_ (u"ࠩࡥࡩ࡫ࡵࡲࡦࡡࡷࡥ࡬࠭୾"): bstack1lll1llll_opy_,
      bstack1lll1l1_opy_ (u"ࠪࡦࡪ࡬࡯ࡳࡧࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬ୿"): bstack1l1ll1l11l_opy_,
      bstack1lll1l1_opy_ (u"ࠫࡧ࡫ࡦࡰࡴࡨࡣࡸࡺࡥࡱࠩ஀"): bstack1l1ll111_opy_,
      bstack1lll1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡸࡺࡥࡱࠩ஁"): bstack1lll1llll1_opy_,
      bstack1lll1l1_opy_ (u"࠭ࡡࡧࡶࡨࡶࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠧஂ"): bstack1lll1lll11_opy_,
      bstack1lll1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡴࡢࡩࠪஃ"): bstack1l1llll1l1_opy_,
      bstack1lll1l1_opy_ (u"ࠨࡣࡩࡸࡪࡸ࡟ࡧࡧࡤࡸࡺࡸࡥࠨ஄"): bstack1llll111l1_opy_,
      bstack1lll1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡣ࡯ࡰࠬஅ"): lambda *args: bstack11llllllll_opy_(*args, self)
  }
  handler = bstack1ll11111l_opy_.get(name, bstack1l1111111l_opy_)
  handler(self, name, context, bstack1l1111111l_opy_, *args)
  if name in [bstack1lll1l1_opy_ (u"ࠪࡥ࡫ࡺࡥࡳࡡࡩࡩࡦࡺࡵࡳࡧࠪஆ"), bstack1lll1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஇ"), bstack1lll1l1_opy_ (u"ࠬࡧࡦࡵࡧࡵࡣࡦࡲ࡬ࠨஈ")]:
    try:
      bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llll11l_opy_(bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࡙ࡥࡴࡵ࡬ࡳࡳࡊࡲࡪࡸࡨࡶࠬஉ")) else context.browser
      bstack1l111l1111_opy_ = (
        (name == bstack1lll1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡡ࡭࡮ࠪஊ") and self.driver_initialised == bstack1lll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡣ࡯ࡰࠧ஋")) or
        (name == bstack1lll1l1_opy_ (u"ࠩࡤࡪࡹ࡫ࡲࡠࡨࡨࡥࡹࡻࡲࡦࠩ஌") and self.driver_initialised == bstack1lll1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࡢࡪࡪࡧࡴࡶࡴࡨࠦ஍")) or
        (name == bstack1lll1l1_opy_ (u"ࠫࡦ࡬ࡴࡦࡴࡢࡷࡨ࡫࡮ࡢࡴ࡬ࡳࠬஎ") and self.driver_initialised in [bstack1lll1l1_opy_ (u"ࠧࡨࡥࡧࡱࡵࡩࡤࡹࡣࡦࡰࡤࡶ࡮ࡵࠢஏ"), bstack1lll1l1_opy_ (u"ࠨࡩ࡯ࡵࡷࡩࡵࠨஐ")]) or
        (name == bstack1lll1l1_opy_ (u"ࠧࡢࡨࡷࡩࡷࡥࡳࡵࡧࡳࠫ஑") and self.driver_initialised == bstack1lll1l1_opy_ (u"ࠣࡤࡨࡪࡴࡸࡥࡠࡵࡷࡩࡵࠨஒ"))
      )
      if bstack1l111l1111_opy_:
        self.driver_initialised = None
        bstack1l1111l11_opy_.quit()
    except Exception:
      pass
def bstack111l11lll_opy_(config, startdir):
  return bstack1lll1l1_opy_ (u"ࠤࡧࡶ࡮ࡼࡥࡳ࠼ࠣࡿ࠵ࢃࠢஓ").format(bstack1lll1l1_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠤஔ"))
notset = Notset()
def bstack11lll1l1l_opy_(self, name: str, default=notset, skip: bool = False):
  global bstack111l111l_opy_
  if str(name).lower() == bstack1lll1l1_opy_ (u"ࠫࡩࡸࡩࡷࡧࡵࠫக"):
    return bstack1lll1l1_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠦ஖")
  else:
    return bstack111l111l_opy_(self, name, default, skip)
def bstack1l1ll1l111_opy_(item, when):
  global bstack1llll1l1l1_opy_
  try:
    bstack1llll1l1l1_opy_(item, when)
  except Exception as e:
    pass
def bstack1ll1l1111l_opy_():
  return
def bstack1l1111l1l1_opy_(type, name, status, reason, bstack111ll1l11_opy_, bstack1l1l1l1111_opy_):
  bstack1l111ll11l_opy_ = {
    bstack1lll1l1_opy_ (u"࠭ࡡࡤࡶ࡬ࡳࡳ࠭஗"): type,
    bstack1lll1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ஘"): {}
  }
  if type == bstack1lll1l1_opy_ (u"ࠨࡣࡱࡲࡴࡺࡡࡵࡧࠪங"):
    bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬச")][bstack1lll1l1_opy_ (u"ࠪࡰࡪࡼࡥ࡭ࠩ஛")] = bstack111ll1l11_opy_
    bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧஜ")][bstack1lll1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪ஝")] = json.dumps(str(bstack1l1l1l1111_opy_))
  if type == bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠧஞ"):
    bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪட")][bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭஠")] = name
  if type == bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹ࡙ࡥࡴࡵ࡬ࡳࡳ࡙ࡴࡢࡶࡸࡷࠬ஡"):
    bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭஢")][bstack1lll1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫண")] = status
    if status == bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬத"):
      bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ஥")][bstack1lll1l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧ஦")] = json.dumps(str(reason))
  bstack1lllllll11_opy_ = bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࡿࢂ࠭஧").format(json.dumps(bstack1l111ll11l_opy_))
  return bstack1lllllll11_opy_
def bstack1l11lll11_opy_(driver_command, response):
    if driver_command == bstack1lll1l1_opy_ (u"ࠩࡶࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹ࠭ந"):
        bstack1l1lll1lll_opy_.bstack1l1111l1_opy_({
            bstack1lll1l1_opy_ (u"ࠪ࡭ࡲࡧࡧࡦࠩன"): response[bstack1lll1l1_opy_ (u"ࠫࡻࡧ࡬ࡶࡧࠪப")],
            bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬ஫"): bstack1l1lll1lll_opy_.current_test_uuid()
        })
def bstack1ll1111l11_opy_(item, call, rep):
  global bstack111l1lll_opy_
  global bstack11l1l1ll1_opy_
  global bstack1ll1ll11l1_opy_
  name = bstack1lll1l1_opy_ (u"࠭ࠧ஬")
  try:
    if rep.when == bstack1lll1l1_opy_ (u"ࠧࡤࡣ࡯ࡰࠬ஭"):
      bstack11l1l111l_opy_ = threading.current_thread().bstackSessionId
      try:
        if not bstack1ll1ll11l1_opy_:
          name = str(rep.nodeid)
          bstack1l111111l_opy_ = bstack1l1111l1l1_opy_(bstack1lll1l1_opy_ (u"ࠨࡵࡨࡸࡘ࡫ࡳࡴ࡫ࡲࡲࡓࡧ࡭ࡦࠩம"), name, bstack1lll1l1_opy_ (u"ࠩࠪய"), bstack1lll1l1_opy_ (u"ࠪࠫர"), bstack1lll1l1_opy_ (u"ࠫࠬற"), bstack1lll1l1_opy_ (u"ࠬ࠭ல"))
          threading.current_thread().bstack11l11l1l_opy_ = name
          for driver in bstack11l1l1ll1_opy_:
            if bstack11l1l111l_opy_ == driver.session_id:
              driver.execute_script(bstack1l111111l_opy_)
      except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"࠭ࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࡑࡥࡲ࡫ࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭ள").format(str(e)))
      try:
        bstack1l11l11l_opy_(rep.outcome.lower())
        if rep.outcome.lower() != bstack1lll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡵ࡫ࡤࠨழ"):
          status = bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨவ") if rep.outcome.lower() == bstack1lll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩஶ") else bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪஷ")
          reason = bstack1lll1l1_opy_ (u"ࠫࠬஸ")
          if status == bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬஹ"):
            reason = rep.longrepr.reprcrash.message
            if (not threading.current_thread().bstackTestErrorMessages):
              threading.current_thread().bstackTestErrorMessages = []
            threading.current_thread().bstackTestErrorMessages.append(reason)
          level = bstack1lll1l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫ஺") if status == bstack1lll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ஻") else bstack1lll1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ஼")
          data = name + bstack1lll1l1_opy_ (u"ࠩࠣࡴࡦࡹࡳࡦࡦࠤࠫ஽") if status == bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪா") else name + bstack1lll1l1_opy_ (u"ࠫࠥ࡬ࡡࡪ࡮ࡨࡨࠦࠦࠧி") + reason
          bstack1ll11111l1_opy_ = bstack1l1111l1l1_opy_(bstack1lll1l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧீ"), bstack1lll1l1_opy_ (u"࠭ࠧு"), bstack1lll1l1_opy_ (u"ࠧࠨூ"), bstack1lll1l1_opy_ (u"ࠨࠩ௃"), level, data)
          for driver in bstack11l1l1ll1_opy_:
            if bstack11l1l111l_opy_ == driver.session_id:
              driver.execute_script(bstack1ll11111l1_opy_)
      except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"ࠩࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡣࡰࡰࡷࡩࡽࡺࠠࡧࡱࡵࠤࡵࡿࡴࡦࡵࡷ࠱ࡧࡪࡤࠡࡵࡨࡷࡸ࡯࡯࡯࠼ࠣࡿࢂ࠭௄").format(str(e)))
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠪࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡳࡵࡣࡷࡩࠥ࡯࡮ࠡࡲࡼࡸࡪࡹࡴ࠮ࡤࡧࡨࠥࡺࡥࡴࡶࠣࡷࡹࡧࡴࡶࡵ࠽ࠤࢀࢃࠧ௅").format(str(e)))
  bstack111l1lll_opy_(item, call, rep)
def bstack1ll1111l1_opy_(driver, bstack1l111l1ll1_opy_, test=None):
  global bstack11l1llll_opy_
  if test != None:
    bstack111l1l1ll_opy_ = getattr(test, bstack1lll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩெ"), None)
    bstack1l11ll1l_opy_ = getattr(test, bstack1lll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪே"), None)
    PercySDK.screenshot(driver, bstack1l111l1ll1_opy_, bstack111l1l1ll_opy_=bstack111l1l1ll_opy_, bstack1l11ll1l_opy_=bstack1l11ll1l_opy_, bstack1ll1l111l_opy_=bstack11l1llll_opy_)
  else:
    PercySDK.screenshot(driver, bstack1l111l1ll1_opy_)
def bstack1ll1l1llll_opy_(driver):
  if bstack11llll111_opy_.bstack1ll111l1_opy_() is True or bstack11llll111_opy_.capturing() is True:
    return
  bstack11llll111_opy_.bstack11lll11l1_opy_()
  while not bstack11llll111_opy_.bstack1ll111l1_opy_():
    bstack1ll1l1lll1_opy_ = bstack11llll111_opy_.bstack1l11l1l11l_opy_()
    bstack1ll1111l1_opy_(driver, bstack1ll1l1lll1_opy_)
  bstack11llll111_opy_.bstack11ll1lll_opy_()
def bstack1l1111l111_opy_(sequence, driver_command, response = None, bstack1l11lllll_opy_ = None, args = None):
    try:
      if sequence != bstack1lll1l1_opy_ (u"࠭ࡢࡦࡨࡲࡶࡪ࠭ை"):
        return
      if percy.bstack11llll1l1_opy_() == bstack1lll1l1_opy_ (u"ࠢࡧࡣ࡯ࡷࡪࠨ௉"):
        return
      bstack1ll1l1lll1_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫொ"), None)
      for command in bstack1l1111ll1_opy_:
        if command == driver_command:
          for driver in bstack11l1l1ll1_opy_:
            bstack1ll1l1llll_opy_(driver)
      bstack1l1ll1lll1_opy_ = percy.bstack1ll111llll_opy_()
      if driver_command in bstack1l1l1lll1l_opy_[bstack1l1ll1lll1_opy_]:
        bstack11llll111_opy_.bstack11ll111l1_opy_(bstack1ll1l1lll1_opy_, driver_command)
    except Exception as e:
      pass
def bstack11111llll_opy_(framework_name):
  if bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡰࡳࡩࡥࡣࡢ࡮࡯ࡩࡩ࠭ோ")):
      return
  bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡢࡱࡴࡪ࡟ࡤࡣ࡯ࡰࡪࡪࠧௌ"), True)
  global bstack1l111llll_opy_
  global bstack1l1ll11l_opy_
  global bstack1l1l111l11_opy_
  bstack1l111llll_opy_ = framework_name
  logger.info(bstack1lllll1l1_opy_.format(bstack1l111llll_opy_.split(bstack1lll1l1_opy_ (u"ࠫ࠲்࠭"))[0]))
  bstack1llll1ll1_opy_()
  try:
    from selenium import webdriver
    from selenium.webdriver.common.service import Service
    from selenium.webdriver.remote.webdriver import WebDriver
    if bstack1l1l1ll11l_opy_:
      Service.start = bstack1l11ll1lll_opy_
      Service.stop = bstack1llll1111l_opy_
      webdriver.Remote.get = bstack1l11l11l1_opy_
      WebDriver.close = bstack1l11ll111_opy_
      WebDriver.quit = bstack1111lll1l_opy_
      webdriver.Remote.__init__ = bstack11l1l111_opy_
      WebDriver.getAccessibilityResults = getAccessibilityResults
      WebDriver.get_accessibility_results = getAccessibilityResults
      WebDriver.getAccessibilityResultsSummary = getAccessibilityResultsSummary
      WebDriver.get_accessibility_results_summary = getAccessibilityResultsSummary
      WebDriver.performScan = perform_scan
      WebDriver.perform_scan = perform_scan
    if not bstack1l1l1ll11l_opy_:
        webdriver.Remote.__init__ = bstack1lll111ll_opy_
    WebDriver.execute = bstack1l11ll1l1l_opy_
    bstack1l1ll11l_opy_ = True
  except Exception as e:
    pass
  try:
    if bstack1l1l1ll11l_opy_:
      from QWeb.keywords import browser
      browser.close_browser = bstack1l11111l1_opy_
  except Exception as e:
    pass
  bstack1lllll1l11_opy_()
  if not bstack1l1ll11l_opy_:
    bstack11l111l1_opy_(bstack1lll1l1_opy_ (u"ࠧࡖࡡࡤ࡭ࡤ࡫ࡪࡹࠠ࡯ࡱࡷࠤ࡮ࡴࡳࡵࡣ࡯ࡰࡪࡪࠢ௎"), bstack1l1lllll11_opy_)
  if bstack1ll11lll_opy_():
    try:
      from selenium.webdriver.remote.remote_connection import RemoteConnection
      RemoteConnection._get_proxy_url = bstack1llll111l_opy_
    except Exception as e:
      logger.error(bstack1llll11ll1_opy_.format(str(e)))
  if bstack1l1l1l111l_opy_():
    bstack1ll1l11lll_opy_(CONFIG, logger)
  if (bstack1lll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬ௏") in str(framework_name).lower()):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        if percy.bstack11llll1l1_opy_() == bstack1lll1l1_opy_ (u"ࠢࡵࡴࡸࡩࠧௐ"):
          bstack1l11l1lll1_opy_(bstack1l1111l111_opy_)
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        WebDriverCreator._get_ff_profile = bstack11l1llll1_opy_
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCache.close = bstack1111l1lll_opy_
      except Exception as e:
        logger.warn(bstack1l111l1l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        ApplicationCache.close = bstack111ll11l1_opy_
      except Exception as e:
        logger.debug(bstack1ll1l111ll_opy_ + str(e))
    except Exception as e:
      bstack11l111l1_opy_(e, bstack1l111l1l11_opy_)
    Output.start_test = bstack11ll1llll_opy_
    Output.end_test = bstack11lll1l11_opy_
    TestStatus.__init__ = bstack1llll11l11_opy_
    QueueItem.__init__ = bstack1ll11l11_opy_
    pabot._create_items = bstack1ll111ll_opy_
    try:
      from pabot import __version__ as bstack11l11llll_opy_
      if version.parse(bstack11l11llll_opy_) >= version.parse(bstack1lll1l1_opy_ (u"ࠨ࠴࠱࠵࠺࠴࠰ࠨ௑")):
        pabot._run = bstack1l11ll11_opy_
      elif version.parse(bstack11l11llll_opy_) >= version.parse(bstack1lll1l1_opy_ (u"ࠩ࠵࠲࠶࠹࠮࠱ࠩ௒")):
        pabot._run = bstack11ll1111_opy_
      else:
        pabot._run = bstack11ll111l_opy_
    except Exception as e:
      pabot._run = bstack11ll111l_opy_
    pabot._create_command_for_execution = bstack1l1ll1111l_opy_
    pabot._report_results = bstack1l11ll1l11_opy_
  if bstack1lll1l1_opy_ (u"ࠪࡦࡪ࡮ࡡࡷࡧࠪ௓") in str(framework_name).lower():
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l111l1_opy_(e, bstack111l1111_opy_)
    Runner.run_hook = bstack111l11l1_opy_
    Step.run = bstack1111lll1_opy_
  if bstack1lll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫ௔") in str(framework_name).lower():
    if not bstack1l1l1ll11l_opy_:
      return
    try:
      if percy.bstack11llll1l1_opy_() == bstack1lll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥ௕"):
          bstack1l11l1lll1_opy_(bstack1l1111l111_opy_)
      from pytest_selenium import pytest_selenium
      from _pytest.config import Config
      pytest_selenium.pytest_report_header = bstack111l11lll_opy_
      from pytest_selenium.drivers import browserstack
      browserstack.pytest_selenium_runtest_makereport = bstack1ll1l1111l_opy_
      Config.getoption = bstack11lll1l1l_opy_
    except Exception as e:
      pass
    try:
      from pytest_bdd import reporting
      reporting.runtest_makereport = bstack1ll1111l11_opy_
    except Exception as e:
      pass
def bstack1l1ll1ll1l_opy_():
  global CONFIG
  if bstack1lll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭௖") in CONFIG and int(CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧௗ")]) > 1:
    logger.warn(bstack1l11lll1_opy_)
def bstack1l11ll1l1_opy_(arg, bstack111lll11l_opy_, bstack1lll111l1_opy_=None):
  global CONFIG
  global bstack1ll1l1ll_opy_
  global bstack11lll1ll_opy_
  global bstack1l1l1ll11l_opy_
  global bstack1lll11l1ll_opy_
  bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨ௘")
  if bstack111lll11l_opy_ and isinstance(bstack111lll11l_opy_, str):
    bstack111lll11l_opy_ = eval(bstack111lll11l_opy_)
  CONFIG = bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠩࡆࡓࡓࡌࡉࡈࠩ௙")]
  bstack1ll1l1ll_opy_ = bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠪࡌ࡚ࡈ࡟ࡖࡔࡏࠫ௚")]
  bstack11lll1ll_opy_ = bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠫࡎ࡙࡟ࡂࡒࡓࡣࡆ࡛ࡔࡐࡏࡄࡘࡊ࠭௛")]
  bstack1l1l1ll11l_opy_ = bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ௜")]
  bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡳࡦࡵࡶ࡭ࡴࡴࠧ௝"), bstack1l1l1ll11l_opy_)
  os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩ௞")] = bstack1ll11ll1ll_opy_
  os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡄࡑࡑࡊࡎࡍࠧ௟")] = json.dumps(CONFIG)
  os.environ[bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡊࡘࡆࡤ࡛ࡒࡍࠩ௠")] = bstack1ll1l1ll_opy_
  os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡌࡗࡤࡇࡐࡑࡡࡄ࡙࡙ࡕࡍࡂࡖࡈࠫ௡")] = str(bstack11lll1ll_opy_)
  os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔ࡞࡚ࡅࡔࡖࡢࡔࡑ࡛ࡇࡊࡐࠪ௢")] = str(True)
  if bstack1l1l1l1lll_opy_(arg, [bstack1lll1l1_opy_ (u"ࠬ࠳࡮ࠨ௣"), bstack1lll1l1_opy_ (u"࠭࠭࠮ࡰࡸࡱࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧ௤")]) != -1:
    os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡐ࡚ࡖࡈࡗ࡙ࡥࡐࡂࡔࡄࡐࡑࡋࡌࠨ௥")] = str(True)
  if len(sys.argv) <= 1:
    logger.critical(bstack1111lllll_opy_)
    return
  bstack1l111l11_opy_()
  global bstack11l1l11ll_opy_
  global bstack11l1llll_opy_
  global bstack1ll11l1111_opy_
  global bstack111lllll_opy_
  global bstack1l111ll1_opy_
  global bstack1l1l111l11_opy_
  global bstack11l1l1l11_opy_
  arg.append(bstack1lll1l1_opy_ (u"ࠣ࠯࡚ࠦ௦"))
  arg.append(bstack1lll1l1_opy_ (u"ࠤ࡬࡫ࡳࡵࡲࡦ࠼ࡐࡳࡩࡻ࡬ࡦࠢࡤࡰࡷ࡫ࡡࡥࡻࠣ࡭ࡲࡶ࡯ࡳࡶࡨࡨ࠿ࡶࡹࡵࡧࡶࡸ࠳ࡖࡹࡵࡧࡶࡸ࡜ࡧࡲ࡯࡫ࡱ࡫ࠧ௧"))
  arg.append(bstack1lll1l1_opy_ (u"ࠥ࠱࡜ࠨ௨"))
  arg.append(bstack1lll1l1_opy_ (u"ࠦ࡮࡭࡮ࡰࡴࡨ࠾࡙࡮ࡥࠡࡪࡲࡳࡰ࡯࡭ࡱ࡮ࠥ௩"))
  global bstack11l111lll_opy_
  global bstack1l1l1111l_opy_
  global bstack1l11l111l1_opy_
  global bstack1l1111111_opy_
  global bstack111ll1ll_opy_
  global bstack1lll1l1ll1_opy_
  global bstack1l1l1ll111_opy_
  global bstack1ll11ll11l_opy_
  global bstack11l1ll11_opy_
  global bstack11lll1l1_opy_
  global bstack111l111l_opy_
  global bstack1llll1l1l1_opy_
  global bstack111l1lll_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l111lll_opy_ = webdriver.Remote.__init__
    bstack1l1l1111l_opy_ = WebDriver.quit
    bstack1ll11ll11l_opy_ = WebDriver.close
    bstack11l1ll11_opy_ = WebDriver.get
    bstack1l11l111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  if bstack1lll1lll1l_opy_(CONFIG) and bstack1l11l11111_opy_():
    if bstack1l1l1l111_opy_() < version.parse(bstack1l11lll1l1_opy_):
      logger.error(bstack11l11lll_opy_.format(bstack1l1l1l111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11lll1l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1llll11ll1_opy_.format(str(e)))
  try:
    from _pytest.config import Config
    bstack111l111l_opy_ = Config.getoption
    from _pytest import runner
    bstack1llll1l1l1_opy_ = runner._update_current_test_var
  except Exception as e:
    logger.warn(e, bstack1111llll_opy_)
  try:
    from pytest_bdd import reporting
    bstack111l1lll_opy_ = reporting.runtest_makereport
  except Exception as e:
    logger.debug(bstack1lll1l1_opy_ (u"ࠬࡖ࡬ࡦࡣࡶࡩࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹ࠳ࡢࡥࡦࠣࡸࡴࠦࡲࡶࡰࠣࡴࡾࡺࡥࡴࡶ࠰ࡦࡩࡪࠠࡵࡧࡶࡸࡸ࠭௪"))
  bstack1ll11l1111_opy_ = CONFIG.get(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪ௫"), {}).get(bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ௬"))
  bstack11l1l1l11_opy_ = True
  bstack11111llll_opy_(bstack1lll1lll1_opy_)
  os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩ௭")] = CONFIG[bstack1lll1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ௮")]
  os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡄࡇࡈࡋࡓࡔࡡࡎࡉ࡞࠭௯")] = CONFIG[bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ௰")]
  os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨ௱")] = bstack1l1l1ll11l_opy_.__str__()
  from _pytest.config import main as bstack111l11l1l_opy_
  bstack1lll1ll1l_opy_ = []
  try:
    bstack11ll11lll_opy_ = bstack111l11l1l_opy_(arg)
    if bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪ௲") in multiprocessing.current_process().__dict__.keys():
      for bstack1111ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll1ll1l_opy_.append(bstack1111ll1ll_opy_)
    try:
      bstack1l111l1l_opy_ = (bstack1lll1ll1l_opy_, int(bstack11ll11lll_opy_))
      bstack1lll111l1_opy_.append(bstack1l111l1l_opy_)
    except:
      bstack1lll111l1_opy_.append((bstack1lll1ll1l_opy_, bstack11ll11lll_opy_))
  except Exception as e:
    logger.error(traceback.format_exc())
    bstack1lll1ll1l_opy_.append({bstack1lll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ௳"): bstack1lll1l1_opy_ (u"ࠨࡒࡵࡳࡨ࡫ࡳࡴࠢࠪ௴") + os.environ.get(bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒࡏࡅ࡙ࡌࡏࡓࡏࡢࡍࡓࡊࡅ࡙ࠩ௵")), bstack1lll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩ௶"): traceback.format_exc(), bstack1lll1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪ௷"): int(os.environ.get(bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡕࡒࡁࡕࡈࡒࡖࡒࡥࡉࡏࡆࡈ࡜ࠬ௸")))})
    bstack1lll111l1_opy_.append((bstack1lll1ll1l_opy_, 1))
def bstack11l1l1ll_opy_(arg):
  global bstack1l1lll111l_opy_
  bstack11111llll_opy_(bstack1ll1llll_opy_)
  os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ௹")] = str(bstack11lll1ll_opy_)
  from behave.__main__ import main as bstack1ll11l1ll1_opy_
  status_code = bstack1ll11l1ll1_opy_(arg)
  if status_code != 0:
    bstack1l1lll111l_opy_ = status_code
def bstack11lll111_opy_():
  logger.info(bstack11lll1111_opy_)
  import argparse
  parser = argparse.ArgumentParser()
  parser.add_argument(bstack1lll1l1_opy_ (u"ࠧࡴࡧࡷࡹࡵ࠭௺"), help=bstack1lll1l1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠢࡦࡳࡳ࡬ࡩࡨࠩ௻"))
  parser.add_argument(bstack1lll1l1_opy_ (u"ࠩ࠰ࡹࠬ௼"), bstack1lll1l1_opy_ (u"ࠪ࠱࠲ࡻࡳࡦࡴࡱࡥࡲ࡫ࠧ௽"), help=bstack1lll1l1_opy_ (u"ࠫ࡞ࡵࡵࡳࠢࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠡࡷࡶࡩࡷࡴࡡ࡮ࡧࠪ௾"))
  parser.add_argument(bstack1lll1l1_opy_ (u"ࠬ࠳࡫ࠨ௿"), bstack1lll1l1_opy_ (u"࠭࠭࠮࡭ࡨࡽࠬఀ"), help=bstack1lll1l1_opy_ (u"࡚ࠧࡱࡸࡶࠥࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠤࡦࡩࡣࡦࡵࡶࠤࡰ࡫ࡹࠨఁ"))
  parser.add_argument(bstack1lll1l1_opy_ (u"ࠨ࠯ࡩࠫం"), bstack1lll1l1_opy_ (u"ࠩ࠰࠱࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧః"), help=bstack1lll1l1_opy_ (u"ࠪ࡝ࡴࡻࡲࠡࡶࡨࡷࡹࠦࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࠩఄ"))
  bstack1ll11lllll_opy_ = parser.parse_args()
  try:
    bstack11l1111l1_opy_ = bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡫ࡪࡴࡥࡳ࡫ࡦ࠲ࡾࡳ࡬࠯ࡵࡤࡱࡵࡲࡥࠨఅ")
    if bstack1ll11lllll_opy_.framework and bstack1ll11lllll_opy_.framework not in (bstack1lll1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬఆ"), bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧఇ")):
      bstack11l1111l1_opy_ = bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡦࡳࡣࡰࡩࡼࡵࡲ࡬࠰ࡼࡱࡱ࠴ࡳࡢ࡯ࡳࡰࡪ࠭ఈ")
    bstack1llllll111_opy_ = os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack11l1111l1_opy_)
    bstack111ll1l1_opy_ = open(bstack1llllll111_opy_, bstack1lll1l1_opy_ (u"ࠨࡴࠪఉ"))
    bstack1ll1l111_opy_ = bstack111ll1l1_opy_.read()
    bstack111ll1l1_opy_.close()
    if bstack1ll11lllll_opy_.username:
      bstack1ll1l111_opy_ = bstack1ll1l111_opy_.replace(bstack1lll1l1_opy_ (u"ࠩ࡜ࡓ࡚ࡘ࡟ࡖࡕࡈࡖࡓࡇࡍࡆࠩఊ"), bstack1ll11lllll_opy_.username)
    if bstack1ll11lllll_opy_.key:
      bstack1ll1l111_opy_ = bstack1ll1l111_opy_.replace(bstack1lll1l1_opy_ (u"ࠪ࡝ࡔ࡛ࡒࡠࡃࡆࡇࡊ࡙ࡓࡠࡍࡈ࡝ࠬఋ"), bstack1ll11lllll_opy_.key)
    if bstack1ll11lllll_opy_.framework:
      bstack1ll1l111_opy_ = bstack1ll1l111_opy_.replace(bstack1lll1l1_opy_ (u"ࠫ࡞ࡕࡕࡓࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬఌ"), bstack1ll11lllll_opy_.framework)
    file_name = bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡾࡳ࡬ࠨ఍")
    file_path = os.path.abspath(file_name)
    bstack1l1ll11l11_opy_ = open(file_path, bstack1lll1l1_opy_ (u"࠭ࡷࠨఎ"))
    bstack1l1ll11l11_opy_.write(bstack1ll1l111_opy_)
    bstack1l1ll11l11_opy_.close()
    logger.info(bstack11l1ll111_opy_)
    try:
      os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡆࡓࡃࡐࡉ࡜ࡕࡒࡌࠩఏ")] = bstack1ll11lllll_opy_.framework if bstack1ll11lllll_opy_.framework != None else bstack1lll1l1_opy_ (u"ࠣࠤఐ")
      config = yaml.safe_load(bstack1ll1l111_opy_)
      config[bstack1lll1l1_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ఑")] = bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰ࡷࡪࡺࡵࡱࠩఒ")
      bstack1l1llll1l_opy_(bstack1l11ll111l_opy_, config)
    except Exception as e:
      logger.debug(bstack1llll1ll11_opy_.format(str(e)))
  except Exception as e:
    logger.error(bstack1lllllll1l_opy_.format(str(e)))
def bstack1l1llll1l_opy_(bstack1lll11ll_opy_, config, bstack1l1lll1l1l_opy_={}):
  global bstack1l1l1ll11l_opy_
  global bstack1111111l_opy_
  global bstack1lll11l1ll_opy_
  if not config:
    return
  bstack11ll11l1_opy_ = bstack1llllllll_opy_ if not bstack1l1l1ll11l_opy_ else (
    bstack11ll1ll1l_opy_ if bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰࠨఓ") in config else bstack11ll111ll_opy_)
  bstack1l11l1l111_opy_ = False
  bstack1l111l11ll_opy_ = False
  if bstack1l1l1ll11l_opy_ is True:
      if bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱࠩఔ") in config:
          bstack1l11l1l111_opy_ = True
      else:
          bstack1l111l11ll_opy_ = True
  bstack1l1l1l1ll_opy_ = bstack1ll1l1111_opy_.bstack11l11l11_opy_(config, bstack1111111l_opy_)
  data = {
    bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨక"): config[bstack1lll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩఖ")],
    bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫగ"): config[bstack1lll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴࡍࡨࡽࠬఘ")],
    bstack1lll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧఙ"): bstack1lll11ll_opy_,
    bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡴࡦࡥࡷࡩࡩࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨచ"): os.environ.get(bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡋࡘࡁࡎࡇ࡚ࡓࡗࡑࠧఛ"), bstack1111111l_opy_),
    bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨజ"): bstack11l111ll_opy_,
    bstack1lll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡲࡧ࡬ࡠࡪࡸࡦࡤࡻࡲ࡭ࠩఝ"): bstack11l11111_opy_(),
    bstack1lll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫఞ"): {
      bstack1lll1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࡣ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧట"): str(config[bstack1lll1l1_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪఠ")]) if bstack1lll1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫడ") in config else bstack1lll1l1_opy_ (u"ࠧࡻ࡮࡬ࡰࡲࡻࡳࠨఢ"),
      bstack1lll1l1_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࡗࡧࡵࡷ࡮ࡵ࡮ࠨణ"): sys.version,
      bstack1lll1l1_opy_ (u"ࠧࡳࡧࡩࡩࡷࡸࡥࡳࠩత"): bstack11lllll1_opy_(os.getenv(bstack1lll1l1_opy_ (u"ࠣࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠥథ"), bstack1lll1l1_opy_ (u"ࠤࠥద"))),
      bstack1lll1l1_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬధ"): bstack1lll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫన"),
      bstack1lll1l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹ࠭఩"): bstack11ll11l1_opy_,
      bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫప"): bstack1l1l1l1ll_opy_,
      bstack1lll1l1_opy_ (u"ࠧࡵࡧࡶࡸ࡭ࡻࡢࡠࡷࡸ࡭ࡩ࠭ఫ"): os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭బ")],
      bstack1lll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬభ"): bstack1lll111l11_opy_(os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡉࡖࡆࡓࡅࡘࡑࡕࡏࠬమ"), bstack1111111l_opy_)),
      bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧయ"): config[bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨర")] if config[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩఱ")] else bstack1lll1l1_opy_ (u"ࠢࡶࡰ࡮ࡲࡴࡽ࡮ࠣల"),
      bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪళ"): str(config[bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫఴ")]) if bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬవ") in config else bstack1lll1l1_opy_ (u"ࠦࡺࡴ࡫࡯ࡱࡺࡲࠧశ"),
      bstack1lll1l1_opy_ (u"ࠬࡵࡳࠨష"): sys.platform,
      bstack1lll1l1_opy_ (u"࠭ࡨࡰࡵࡷࡲࡦࡳࡥࠨస"): socket.gethostname(),
      bstack1lll1l1_opy_ (u"ࠧࡴࡦ࡮ࡖࡺࡴࡉࡥࠩహ"): bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠨࡵࡧ࡯ࡗࡻ࡮ࡊࡦࠪ఺"))
    }
  }
  if not bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠩࡶࡨࡰࡑࡩ࡭࡮ࡖ࡭࡬ࡴࡡ࡭ࠩ఻")) is None:
    data[bstack1lll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ఼࠭")][bstack1lll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡓࡥࡵࡣࡧࡥࡹࡧࠧఽ")] = {
      bstack1lll1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬా"): bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡣࡰ࡯࡬࡭ࡧࡧࠫి"),
      bstack1lll1l1_opy_ (u"ࠧࡴ࡫ࡪࡲࡦࡲࠧీ"): bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠨࡵࡧ࡯ࡐ࡯࡬࡭ࡕ࡬࡫ࡳࡧ࡬ࠨు")),
      bstack1lll1l1_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࡐࡸࡱࡧ࡫ࡲࠨూ"): bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱࡋࡪ࡮࡯ࡒࡴ࠭ృ"))
    }
  if bstack1lll11ll_opy_ == bstack1ll11l11ll_opy_:
    data[bstack1lll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡴࡷࡵࡰࡦࡴࡷ࡭ࡪࡹࠧౄ")][bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡇࡴࡴࡦࡪࡩࠪ౅")] = bstack1l1l11lll_opy_(config)
    data[bstack1lll1l1_opy_ (u"࠭ࡥࡷࡧࡱࡸࡤࡶࡲࡰࡲࡨࡶࡹ࡯ࡥࡴࠩె")][bstack1lll1l1_opy_ (u"ࠧࡪࡵࡓࡩࡷࡩࡹࡂࡷࡷࡳࡊࡴࡡࡣ࡮ࡨࡨࠬే")] = percy.bstack111l1ll11_opy_
    data[bstack1lll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡱࡴࡲࡴࡪࡸࡴࡪࡧࡶࠫై")][bstack1lll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡃࡷ࡬ࡰࡩࡏࡤࠨ౉")] = percy.bstack1l1l111l_opy_
  update(data[bstack1lll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡳࡶࡴࡶࡥࡳࡶ࡬ࡩࡸ࠭ొ")], bstack1l1lll1l1l_opy_)
  try:
    response = bstack1l1ll1l11_opy_(bstack1lll1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩో"), bstack1lll11111l_opy_(bstack11ll1ll1_opy_), data, {
      bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡪࠪౌ"): (config[bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ్")], config[bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ౎")])
    })
    if response:
      logger.debug(bstack1l1l1lll11_opy_.format(bstack1lll11ll_opy_, str(response.json())))
  except Exception as e:
    logger.debug(bstack1ll11lll11_opy_.format(str(e)))
def bstack11lllll1_opy_(framework):
  return bstack1lll1l1_opy_ (u"ࠣࡽࢀ࠱ࡵࡿࡴࡩࡱࡱࡥ࡬࡫࡮ࡵ࠱ࡾࢁࠧ౏").format(str(framework), __version__) if framework else bstack1lll1l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࡼࡿࠥ౐").format(
    __version__)
def bstack1l111l11_opy_():
  global CONFIG
  global bstack1l1l111l1l_opy_
  if bool(CONFIG):
    return
  try:
    bstack1lll11l11l_opy_()
    logger.debug(bstack1l1l11l11l_opy_.format(str(CONFIG)))
    bstack1l1l111l1l_opy_ = bstack1l11ll1111_opy_.bstack1llll1lll1_opy_(CONFIG, bstack1l1l111l1l_opy_)
    bstack1llll1ll1_opy_()
  except Exception as e:
    logger.error(bstack1lll1l1_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦࡳࡦࡶࡸࡴ࠱ࠦࡥࡳࡴࡲࡶ࠿ࠦࠢ౑") + str(e))
    sys.exit(1)
  sys.excepthook = bstack1lll1ll1l1_opy_
  atexit.register(bstack111l1ll1l_opy_)
  signal.signal(signal.SIGINT, bstack1l11l111l_opy_)
  signal.signal(signal.SIGTERM, bstack1l11l111l_opy_)
def bstack1lll1ll1l1_opy_(exctype, value, traceback):
  global bstack11l1l1ll1_opy_
  try:
    for driver in bstack11l1l1ll1_opy_:
      bstack1l11ll11l1_opy_(driver, bstack1lll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࠫ౒"), bstack1lll1l1_opy_ (u"࡙ࠧࡥࡴࡵ࡬ࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡷࡪࡶ࡫࠾ࠥࡢ࡮ࠣ౓") + str(value))
  except Exception:
    pass
  bstack1l11ll1ll_opy_(value, True)
  sys.__excepthook__(exctype, value, traceback)
  sys.exit(1)
def bstack1l11ll1ll_opy_(message=bstack1lll1l1_opy_ (u"࠭ࠧ౔"), bstack1lll1l1l1_opy_ = False):
  global CONFIG
  bstack11l1ll1l_opy_ = bstack1lll1l1_opy_ (u"ࠧࡨ࡮ࡲࡦࡦࡲࡅࡹࡥࡨࡴࡹ࡯࡯࡯ౕࠩ") if bstack1lll1l1l1_opy_ else bstack1lll1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸౖࠧ")
  try:
    if message:
      bstack1l1lll1l1l_opy_ = {
        bstack11l1ll1l_opy_ : str(message)
      }
      bstack1l1llll1l_opy_(bstack1ll11l11ll_opy_, CONFIG, bstack1l1lll1l1l_opy_)
    else:
      bstack1l1llll1l_opy_(bstack1ll11l11ll_opy_, CONFIG)
  except Exception as e:
    logger.debug(bstack1lll11l11_opy_.format(str(e)))
def bstack1lll111l_opy_(bstack1l111111_opy_, size):
  bstack111111l11_opy_ = []
  while len(bstack1l111111_opy_) > size:
    bstack11l1111ll_opy_ = bstack1l111111_opy_[:size]
    bstack111111l11_opy_.append(bstack11l1111ll_opy_)
    bstack1l111111_opy_ = bstack1l111111_opy_[size:]
  bstack111111l11_opy_.append(bstack1l111111_opy_)
  return bstack111111l11_opy_
def bstack1l1ll11l1l_opy_(args):
  if bstack1lll1l1_opy_ (u"ࠩ࠰ࡱࠬ౗") in args and bstack1lll1l1_opy_ (u"ࠪࡴࡩࡨࠧౘ") in args:
    return True
  return False
def run_on_browserstack(bstack1lll1ll11_opy_=None, bstack1lll111l1_opy_=None, bstack1l1ll1ll_opy_=False):
  global CONFIG
  global bstack1ll1l1ll_opy_
  global bstack11lll1ll_opy_
  global bstack1111111l_opy_
  global bstack1lll11l1ll_opy_
  bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠫࠬౙ")
  bstack1l11l1ll1_opy_(bstack1llllllll1_opy_, logger)
  if bstack1lll1ll11_opy_ and isinstance(bstack1lll1ll11_opy_, str):
    bstack1lll1ll11_opy_ = eval(bstack1lll1ll11_opy_)
  if bstack1lll1ll11_opy_:
    CONFIG = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠬࡉࡏࡏࡈࡌࡋࠬౚ")]
    bstack1ll1l1ll_opy_ = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"࠭ࡈࡖࡄࡢ࡙ࡗࡒࠧ౛")]
    bstack11lll1ll_opy_ = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠧࡊࡕࡢࡅࡕࡖ࡟ࡂࡗࡗࡓࡒࡇࡔࡆࠩ౜")]
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪౝ"), bstack11lll1ll_opy_)
    bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ౞")
  bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱࡒࡶࡰࡌࡨࠬ౟"), uuid4().__str__())
  logger.debug(bstack1lll1l1_opy_ (u"ࠫࡸࡪ࡫ࡓࡷࡱࡍࡩࡃࠧౠ") + bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠬࡹࡤ࡬ࡔࡸࡲࡎࡪࠧౡ")))
  if not bstack1l1ll1ll_opy_:
    if len(sys.argv) <= 1:
      logger.critical(bstack1111lllll_opy_)
      return
    if sys.argv[1] == bstack1lll1l1_opy_ (u"࠭࠭࠮ࡸࡨࡶࡸ࡯࡯࡯ࠩౢ") or sys.argv[1] == bstack1lll1l1_opy_ (u"ࠧ࠮ࡸࠪౣ"):
      logger.info(bstack1lll1l1_opy_ (u"ࠨࡄࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠠࡑࡻࡷ࡬ࡴࡴࠠࡔࡆࡎࠤࡻࢁࡽࠨ౤").format(__version__))
      return
    if sys.argv[1] == bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࠨ౥"):
      bstack11lll111_opy_()
      return
  args = sys.argv
  bstack1l111l11_opy_()
  global bstack11l1l11ll_opy_
  global bstack11lll1lll_opy_
  global bstack11l1l1l11_opy_
  global bstack1l1l11111l_opy_
  global bstack11l1llll_opy_
  global bstack1ll11l1111_opy_
  global bstack111lllll_opy_
  global bstack1ll111lll1_opy_
  global bstack1l111ll1_opy_
  global bstack1l1l111l11_opy_
  global bstack111l1l1l_opy_
  bstack11lll1lll_opy_ = len(CONFIG.get(bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭౦"), []))
  if not bstack1ll11ll1ll_opy_:
    if args[1] == bstack1lll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ౧") or args[1] == bstack1lll1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠸࠭౨"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭౩")
      args = args[2:]
    elif args[1] == bstack1lll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭౪"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧ౫")
      args = args[2:]
    elif args[1] == bstack1lll1l1_opy_ (u"ࠩࡳࡥࡧࡵࡴࠨ౬"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠪࡴࡦࡨ࡯ࡵࠩ౭")
      args = args[2:]
    elif args[1] == bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶ࠰࡭ࡳࡺࡥࡳࡰࡤࡰࠬ౮"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷ࠱࡮ࡴࡴࡦࡴࡱࡥࡱ࠭౯")
      args = args[2:]
    elif args[1] == bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭౰"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧ౱")
      args = args[2:]
    elif args[1] == bstack1lll1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨ౲"):
      bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩ౳")
      args = args[2:]
    else:
      if not bstack1lll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭౴") in CONFIG or str(CONFIG[bstack1lll1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౵")]).lower() in [bstack1lll1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ౶"), bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠹ࠧ౷")]:
        bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ౸")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ౹")]).lower() == bstack1lll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨ౺"):
        bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩ౻")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ౼")]).lower() == bstack1lll1l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫ౽"):
        bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬ౾")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ౿")]).lower() == bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨಀ"):
        bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩಁ")
        args = args[1:]
      elif str(CONFIG[bstack1lll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ಂ")]).lower() == bstack1lll1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫಃ"):
        bstack1ll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬ಄")
        args = args[1:]
      else:
        os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࠨಅ")] = bstack1ll11ll1ll_opy_
        bstack1llll1l1l_opy_(bstack1ll1lllll1_opy_)
  os.environ[bstack1lll1l1_opy_ (u"ࠧࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࡢ࡙ࡘࡋࡄࠨಆ")] = bstack1ll11ll1ll_opy_
  bstack1111111l_opy_ = bstack1ll11ll1ll_opy_
  global bstack1ll1lll1l1_opy_
  global bstack1lllllll1_opy_
  if bstack1lll1ll11_opy_:
    try:
      os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡇࡔࡄࡑࡊ࡝ࡏࡓࡍࠪಇ")] = bstack1ll11ll1ll_opy_
      bstack1l1llll1l_opy_(bstack1l1111l1l_opy_, CONFIG)
    except Exception as e:
      logger.debug(bstack1ll1llll1_opy_.format(str(e)))
  global bstack11l111lll_opy_
  global bstack1l1l1111l_opy_
  global bstack1l1llllll1_opy_
  global bstack1l1ll1ll1_opy_
  global bstack1ll1l11ll1_opy_
  global bstack11l1l1111_opy_
  global bstack1l1111111_opy_
  global bstack111ll1ll_opy_
  global bstack11l11l11l_opy_
  global bstack1lll1l1ll1_opy_
  global bstack1l1l1ll111_opy_
  global bstack1ll11ll11l_opy_
  global bstack1l1111111l_opy_
  global bstack11111ll1_opy_
  global bstack11l1ll11_opy_
  global bstack11lll1l1_opy_
  global bstack111l111l_opy_
  global bstack1llll1l1l1_opy_
  global bstack1ll11l1lll_opy_
  global bstack111l1lll_opy_
  global bstack1l11l111l1_opy_
  try:
    from selenium import webdriver
    from selenium.webdriver.remote.webdriver import WebDriver
    bstack11l111lll_opy_ = webdriver.Remote.__init__
    bstack1l1l1111l_opy_ = WebDriver.quit
    bstack1ll11ll11l_opy_ = WebDriver.close
    bstack11l1ll11_opy_ = WebDriver.get
    bstack1l11l111l1_opy_ = WebDriver.execute
  except Exception as e:
    pass
  try:
    import Browser
    from subprocess import Popen
    bstack1ll1lll1l1_opy_ = Popen.__init__
  except Exception as e:
    pass
  try:
    from bstack_utils.helper import bstack1ll111111_opy_
    bstack1lllllll1_opy_ = bstack1ll111111_opy_()
  except Exception as e:
    pass
  try:
    global bstack1l1l1ll1_opy_
    from QWeb.keywords import browser
    bstack1l1l1ll1_opy_ = browser.close_browser
  except Exception as e:
    pass
  if bstack1lll1lll1l_opy_(CONFIG) and bstack1l11l11111_opy_():
    if bstack1l1l1l111_opy_() < version.parse(bstack1l11lll1l1_opy_):
      logger.error(bstack11l11lll_opy_.format(bstack1l1l1l111_opy_()))
    else:
      try:
        from selenium.webdriver.remote.remote_connection import RemoteConnection
        bstack11lll1l1_opy_ = RemoteConnection._get_proxy_url
      except Exception as e:
        logger.error(bstack1llll11ll1_opy_.format(str(e)))
  if not CONFIG.get(bstack1lll1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡄࡹࡹࡵࡃࡢࡲࡷࡹࡷ࡫ࡌࡰࡩࡶࠫಈ"), False) and not bstack1lll1ll11_opy_:
    logger.info(bstack1ll11l1l1_opy_)
  if bstack1ll11ll1ll_opy_ != bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಉ") or (bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫಊ") and not bstack1lll1ll11_opy_):
    bstack1l1111llll_opy_()
  if (bstack1ll11ll1ll_opy_ in [bstack1lll1l1_opy_ (u"ࠬࡶࡡࡣࡱࡷࠫಋ"), bstack1lll1l1_opy_ (u"࠭ࡲࡰࡤࡲࡸࠬಌ"), bstack1lll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠳ࡩ࡯ࡶࡨࡶࡳࡧ࡬ࠨ಍")]):
    try:
      from robot import run_cli
      from robot.output import Output
      from robot.running.status import TestStatus
      from pabot.pabot import QueueItem
      from pabot import pabot
      try:
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCreator
        from SeleniumLibrary.keywords.webdrivertools.webdrivertools import WebDriverCache
        WebDriverCreator._get_ff_profile = bstack11l1llll1_opy_
        bstack11l1l1111_opy_ = WebDriverCache.close
      except Exception as e:
        logger.warn(bstack1l111l1l11_opy_ + str(e))
      try:
        from AppiumLibrary.utils.applicationcache import ApplicationCache
        bstack1ll1l11ll1_opy_ = ApplicationCache.close
      except Exception as e:
        logger.debug(bstack1ll1l111ll_opy_ + str(e))
    except Exception as e:
      bstack11l111l1_opy_(e, bstack1l111l1l11_opy_)
    if bstack1ll11ll1ll_opy_ != bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಎ"):
      bstack111111l1l_opy_()
    bstack1l1llllll1_opy_ = Output.start_test
    bstack1l1ll1ll1_opy_ = Output.end_test
    bstack1l1111111_opy_ = TestStatus.__init__
    bstack11l11l11l_opy_ = pabot._run
    bstack1lll1l1ll1_opy_ = QueueItem.__init__
    bstack1l1l1ll111_opy_ = pabot._create_command_for_execution
    bstack1ll11l1lll_opy_ = pabot._report_results
  if bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩಏ"):
    try:
      from behave.runner import Runner
      from behave.model import Step
    except Exception as e:
      bstack11l111l1_opy_(e, bstack111l1111_opy_)
    bstack1l1111111l_opy_ = Runner.run_hook
    bstack11111ll1_opy_ = Step.run
  if bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪಐ"):
    try:
      from _pytest.config import Config
      bstack111l111l_opy_ = Config.getoption
      from _pytest import runner
      bstack1llll1l1l1_opy_ = runner._update_current_test_var
    except Exception as e:
      logger.warn(e, bstack1111llll_opy_)
    try:
      from pytest_bdd import reporting
      bstack111l1lll_opy_ = reporting.runtest_makereport
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸ࠲ࡨࡤࡥࠢࡷࡳࠥࡸࡵ࡯ࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡥࡨࡩࠦࡴࡦࡵࡷࡷࠬ಑"))
  try:
    framework_name = bstack1lll1l1_opy_ (u"ࠬࡸ࡯ࡣࡱࡷࠫಒ") if bstack1ll11ll1ll_opy_ in [bstack1lll1l1_opy_ (u"࠭ࡰࡢࡤࡲࡸࠬಓ"), bstack1lll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ಔ"), bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಕ")] else bstack1llll1lll_opy_(bstack1ll11ll1ll_opy_)
    bstack1l11llll1_opy_ = {
      bstack1lll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪಖ"): bstack1lll1l1_opy_ (u"ࠪࡿ࠵ࢃ࠭ࡤࡷࡦࡹࡲࡨࡥࡳࠩಗ").format(framework_name) if bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠫࡵࡿࡴࡦࡵࡷࠫಘ") and bstack1llllll1l1_opy_() else framework_name,
      bstack1lll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩಙ"): bstack1lll111l11_opy_(framework_name),
      bstack1lll1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫಚ"): __version__,
      bstack1lll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨಛ"): bstack1ll11ll1ll_opy_
    }
    if bstack1ll11ll1ll_opy_ in bstack1lll111ll1_opy_:
      if bstack1l1l1ll11l_opy_ and bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨಜ") in CONFIG and CONFIG[bstack1lll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩಝ")] == True:
        if bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪಞ") in CONFIG:
          os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬಟ")] = os.getenv(bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ಠ"), json.dumps(CONFIG[bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ಡ")]))
          CONFIG[bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧಢ")].pop(bstack1lll1l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ಣ"), None)
          CONFIG[bstack1lll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩತ")].pop(bstack1lll1l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨಥ"), None)
        bstack1l11llll1_opy_[bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫದ")] = {
          bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪಧ"): bstack1lll1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨನ"),
          bstack1lll1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࠨ಩"): str(bstack1l1l1l111_opy_())
        }
    if bstack1ll11ll1ll_opy_ not in [bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡪࡰࡷࡩࡷࡴࡡ࡭ࠩಪ")]:
      bstack11ll11l1l_opy_ = bstack1l1lll1lll_opy_.launch(CONFIG, bstack1l11llll1_opy_)
  except Exception as e:
    logger.debug(bstack11l1l11l_opy_.format(bstack1lll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡈࡶࡤࠪಫ"), str(e)))
  if bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪಬ"):
    bstack11l1l1l11_opy_ = True
    if bstack1lll1ll11_opy_ and bstack1l1ll1ll_opy_:
      bstack1ll11l1111_opy_ = CONFIG.get(bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࡐࡲࡷ࡭ࡴࡴࡳࠨಭ"), {}).get(bstack1lll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧಮ"))
      bstack11111llll_opy_(bstack1ll1l1ll11_opy_)
    elif bstack1lll1ll11_opy_:
      bstack1ll11l1111_opy_ = CONFIG.get(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࡑࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪಯ"), {}).get(bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩರ"))
      global bstack11l1l1ll1_opy_
      try:
        if bstack1l1ll11l1l_opy_(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಱ")]) and multiprocessing.current_process().name == bstack1lll1l1_opy_ (u"ࠩ࠳ࠫಲ"):
          bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ಳ")].remove(bstack1lll1l1_opy_ (u"ࠫ࠲ࡳࠧ಴"))
          bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨವ")].remove(bstack1lll1l1_opy_ (u"࠭ࡰࡥࡤࠪಶ"))
          bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪಷ")] = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫಸ")][0]
          with open(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬಹ")], bstack1lll1l1_opy_ (u"ࠪࡶࠬ಺")) as f:
            bstack1111l11l_opy_ = f.read()
          bstack111llll1l_opy_ = bstack1lll1l1_opy_ (u"ࠦࠧࠨࡦࡳࡱࡰࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡷࡩࡱࠠࡪ࡯ࡳࡳࡷࡺࠠࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡩ࡯࡫ࡷ࡭ࡦࡲࡩࡻࡧ࠾ࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢ࡭ࡳ࡯ࡴࡪࡣ࡯࡭ࡿ࡫ࠨࡼࡿࠬ࠿ࠥ࡬ࡲࡰ࡯ࠣࡴࡩࡨࠠࡪ࡯ࡳࡳࡷࡺࠠࡑࡦࡥ࠿ࠥࡵࡧࡠࡦࡥࠤࡂࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࡀࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡧࡩ࡫ࠦ࡭ࡰࡦࡢࡦࡷ࡫ࡡ࡬ࠪࡶࡩࡱ࡬ࠬࠡࡣࡵ࡫࠱ࠦࡴࡦ࡯ࡳࡳࡷࡧࡲࡺࠢࡀࠤ࠵࠯࠺ࠋࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡴࡳࡻ࠽ࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡦࡸࡧࠡ࠿ࠣࡷࡹࡸࠨࡪࡰࡷࠬࡦࡸࡧࠪ࠭࠴࠴࠮ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࡪࡾࡣࡦࡲࡷࠤࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡢࡵࠣࡩ࠿ࠐࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡰࡢࡵࡶࠎࠥࠦࠠࠡࠢࠣࠤࠥࠦࠠࠡࠢࡲ࡫ࡤࡪࡢࠩࡵࡨࡰ࡫࠲ࡡࡳࡩ࠯ࡸࡪࡳࡰࡰࡴࡤࡶࡾ࠯ࠊࠡࠢࠣࠤࠥࠦࠠࠡࠢࠣࡔࡩࡨ࠮ࡥࡱࡢࡦࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤ࠱ࡨࡴࡥࡢࡳࡧࡤ࡯ࠥࡃࠠ࡮ࡱࡧࡣࡧࡸࡥࡢ࡭ࠍࠤࠥࠦࠠࠡࠢࠣࠤࠥࠦࡐࡥࡤࠫ࠭࠳ࡹࡥࡵࡡࡷࡶࡦࡩࡥࠩࠫ࡟ࡲࠧࠨࠢ಻").format(str(bstack1lll1ll11_opy_))
          bstack1lll1l1l11_opy_ = bstack111llll1l_opy_ + bstack1111l11l_opy_
          bstack1ll11llll1_opy_ = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠬ࡬ࡩ࡭ࡧࡢࡲࡦࡳࡥࠨ಼")] + bstack1lll1l1_opy_ (u"࠭࡟ࡣࡵࡷࡥࡨࡱ࡟ࡵࡧࡰࡴ࠳ࡶࡹࠨಽ")
          with open(bstack1ll11llll1_opy_, bstack1lll1l1_opy_ (u"ࠧࡸࠩಾ")):
            pass
          with open(bstack1ll11llll1_opy_, bstack1lll1l1_opy_ (u"ࠣࡹ࠮ࠦಿ")) as f:
            f.write(bstack1lll1l1l11_opy_)
          import subprocess
          bstack1l1111lll1_opy_ = subprocess.run([bstack1lll1l1_opy_ (u"ࠤࡳࡽࡹ࡮࡯࡯ࠤೀ"), bstack1ll11llll1_opy_])
          if os.path.exists(bstack1ll11llll1_opy_):
            os.unlink(bstack1ll11llll1_opy_)
          os._exit(bstack1l1111lll1_opy_.returncode)
        else:
          if bstack1l1ll11l1l_opy_(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ು")]):
            bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧೂ")].remove(bstack1lll1l1_opy_ (u"ࠬ࠳࡭ࠨೃ"))
            bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"࠭ࡦࡪ࡮ࡨࡣࡳࡧ࡭ࡦࠩೄ")].remove(bstack1lll1l1_opy_ (u"ࠧࡱࡦࡥࠫ೅"))
            bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫೆ")] = bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೇ")][0]
          bstack11111llll_opy_(bstack1ll1l1ll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೈ")])))
          sys.argv = sys.argv[2:]
          mod_globals = globals()
          mod_globals[bstack1lll1l1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭೉")] = bstack1lll1l1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧೊ")
          mod_globals[bstack1lll1l1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨೋ")] = os.path.abspath(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠧࡧ࡫࡯ࡩࡤࡴࡡ࡮ࡧࠪೌ")])
          exec(open(bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨ್ࠫ")]).read(), mod_globals)
      except BaseException as e:
        try:
          traceback.print_exc()
          logger.error(bstack1lll1l1_opy_ (u"ࠩࡆࡥࡺ࡭ࡨࡵࠢࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲ࠿ࠦࡻࡾࠩ೎").format(str(e)))
          for driver in bstack11l1l1ll1_opy_:
            bstack1lll111l1_opy_.append({
              bstack1lll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ೏"): bstack1lll1ll11_opy_[bstack1lll1l1_opy_ (u"ࠫ࡫࡯࡬ࡦࡡࡱࡥࡲ࡫ࠧ೐")],
              bstack1lll1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ೑"): str(e),
              bstack1lll1l1_opy_ (u"࠭ࡩ࡯ࡦࡨࡼࠬ೒"): multiprocessing.current_process().name
            })
            bstack1l11ll11l1_opy_(driver, bstack1lll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧ೓"), bstack1lll1l1_opy_ (u"ࠣࡕࡨࡷࡸ࡯࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡺ࡭ࡹ࡮࠺ࠡ࡞ࡱࠦ೔") + str(e))
        except Exception:
          pass
      finally:
        try:
          for driver in bstack11l1l1ll1_opy_:
            driver.quit()
        except Exception as e:
          pass
    else:
      percy.init(bstack11lll1ll_opy_, CONFIG, logger)
      bstack1lll1lll_opy_()
      bstack1l1ll1ll1l_opy_()
      bstack111lll11l_opy_ = {
        bstack1lll1l1_opy_ (u"ࠩࡩ࡭ࡱ࡫࡟࡯ࡣࡰࡩࠬೕ"): args[0],
        bstack1lll1l1_opy_ (u"ࠪࡇࡔࡔࡆࡊࡉࠪೖ"): CONFIG,
        bstack1lll1l1_opy_ (u"ࠫࡍ࡛ࡂࡠࡗࡕࡐࠬ೗"): bstack1ll1l1ll_opy_,
        bstack1lll1l1_opy_ (u"ࠬࡏࡓࡠࡃࡓࡔࡤࡇࡕࡕࡑࡐࡅ࡙ࡋࠧ೘"): bstack11lll1ll_opy_
      }
      percy.bstack1l11l1ll_opy_()
      if bstack1lll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ೙") in CONFIG:
        bstack1l111lll1_opy_ = []
        manager = multiprocessing.Manager()
        bstack1llll11l1l_opy_ = manager.list()
        if bstack1l1ll11l1l_opy_(args):
          for index, platform in enumerate(CONFIG[bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ೚")]):
            if index == 0:
              bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫ೛")] = args
            bstack1l111lll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack111lll11l_opy_, bstack1llll11l1l_opy_)))
        else:
          for index, platform in enumerate(CONFIG[bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬ೜")]):
            bstack1l111lll1_opy_.append(multiprocessing.Process(name=str(index),
                                                       target=run_on_browserstack,
                                                       args=(bstack111lll11l_opy_, bstack1llll11l1l_opy_)))
        for t in bstack1l111lll1_opy_:
          t.start()
        for t in bstack1l111lll1_opy_:
          t.join()
        bstack1ll111lll1_opy_ = list(bstack1llll11l1l_opy_)
      else:
        if bstack1l1ll11l1l_opy_(args):
          bstack111lll11l_opy_[bstack1lll1l1_opy_ (u"ࠪࡪ࡮ࡲࡥࡠࡰࡤࡱࡪ࠭ೝ")] = args
          test = multiprocessing.Process(name=str(0),
                                         target=run_on_browserstack, args=(bstack111lll11l_opy_,))
          test.start()
          test.join()
        else:
          bstack11111llll_opy_(bstack1ll1l1ll11_opy_)
          sys.path.append(os.path.dirname(os.path.abspath(args[0])))
          mod_globals = globals()
          mod_globals[bstack1lll1l1_opy_ (u"ࠫࡤࡥ࡮ࡢ࡯ࡨࡣࡤ࠭ೞ")] = bstack1lll1l1_opy_ (u"ࠬࡥ࡟࡮ࡣ࡬ࡲࡤࡥࠧ೟")
          mod_globals[bstack1lll1l1_opy_ (u"࠭࡟ࡠࡨ࡬ࡰࡪࡥ࡟ࠨೠ")] = os.path.abspath(args[0])
          sys.argv = sys.argv[2:]
          exec(open(args[0]).read(), mod_globals)
  elif bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠧࡱࡣࡥࡳࡹ࠭ೡ") or bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺࠧೢ"):
    percy.init(bstack11lll1ll_opy_, CONFIG, logger)
    percy.bstack1l11l1ll_opy_()
    try:
      from pabot import pabot
    except Exception as e:
      bstack11l111l1_opy_(e, bstack1l111l1l11_opy_)
    bstack1lll1lll_opy_()
    bstack11111llll_opy_(bstack1ll1lll1l_opy_)
    if bstack1l1l1ll11l_opy_:
      bstack11111lll_opy_(bstack1ll1lll1l_opy_, args)
      if bstack1lll1l1_opy_ (u"ࠩ࠰࠱ࡵࡸ࡯ࡤࡧࡶࡷࡪࡹࠧೣ") in args:
        i = args.index(bstack1lll1l1_opy_ (u"ࠪ࠱࠲ࡶࡲࡰࡥࡨࡷࡸ࡫ࡳࠨ೤"))
        args.pop(i)
        args.pop(i)
      if bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ೥") not in CONFIG:
        CONFIG[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ೦")] = [{}]
        bstack11lll1lll_opy_ = 1
      if bstack11l1l11ll_opy_ == 0:
        bstack11l1l11ll_opy_ = 1
      args.insert(0, str(bstack11l1l11ll_opy_))
      args.insert(0, str(bstack1lll1l1_opy_ (u"࠭࠭࠮ࡲࡵࡳࡨ࡫ࡳࡴࡧࡶࠫ೧")))
    if bstack1l1lll1lll_opy_.on():
      try:
        from robot.run import USAGE
        from robot.utils import ArgumentParser
        from pabot.arguments import _parse_pabot_args
        bstack1lllll111_opy_, pabot_args = _parse_pabot_args(args)
        opts, bstack1ll1lll111_opy_ = ArgumentParser(
            USAGE,
            auto_pythonpath=False,
            auto_argumentfile=True,
            env_options=bstack1lll1l1_opy_ (u"ࠢࡓࡑࡅࡓ࡙ࡥࡏࡑࡖࡌࡓࡓ࡙ࠢ೨"),
        ).parse_args(bstack1lllll111_opy_)
        bstack1ll11l111l_opy_ = args.index(bstack1lllll111_opy_[0]) if len(bstack1lllll111_opy_) > 0 else len(args)
        args.insert(bstack1ll11l111l_opy_, str(bstack1lll1l1_opy_ (u"ࠨ࠯࠰ࡰ࡮ࡹࡴࡦࡰࡨࡶࠬ೩")))
        args.insert(bstack1ll11l111l_opy_ + 1, str(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡡࡵࡳࡧࡵࡴࡠ࡮࡬ࡷࡹ࡫࡮ࡦࡴ࠱ࡴࡾ࠭೪"))))
        if bstack11ll1l1l1_opy_(os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ೫"))) and str(os.environ.get(bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࡡࡗࡉࡘ࡚ࡓࠨ೬"), bstack1lll1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ೭"))) != bstack1lll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫ೮"):
          for bstack1l1111l11l_opy_ in bstack1ll1lll111_opy_:
            args.remove(bstack1l1111l11l_opy_)
          bstack111ll1l1l_opy_ = os.environ.get(bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࡤ࡚ࡅࡔࡖࡖࠫ೯")).split(bstack1lll1l1_opy_ (u"ࠨ࠮ࠪ೰"))
          for bstack1l11l11ll1_opy_ in bstack111ll1l1l_opy_:
            args.append(bstack1l11l11ll1_opy_)
      except Exception as e:
        logger.error(bstack1lll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡶࡷࡥࡨ࡮ࡩ࡯ࡩࠣࡰ࡮ࡹࡴࡦࡰࡨࡶࠥ࡬࡯ࡳࠢࡒࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠰ࠤࠧೱ").format(e))
    pabot.main(args)
  elif bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵ࠯࡬ࡲࡹ࡫ࡲ࡯ࡣ࡯ࠫೲ"):
    try:
      from robot import run_cli
    except Exception as e:
      bstack11l111l1_opy_(e, bstack1l111l1l11_opy_)
    for a in args:
      if bstack1lll1l1_opy_ (u"ࠫࡇ࡙ࡔࡂࡅࡎࡔࡑࡇࡔࡇࡑࡕࡑࡎࡔࡄࡆ࡚ࠪೳ") in a:
        bstack11l1llll_opy_ = int(a.split(bstack1lll1l1_opy_ (u"ࠬࡀࠧ೴"))[1])
      if bstack1lll1l1_opy_ (u"࠭ࡂࡔࡖࡄࡇࡐࡊࡅࡇࡎࡒࡇࡆࡒࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ೵") in a:
        bstack1ll11l1111_opy_ = str(a.split(bstack1lll1l1_opy_ (u"ࠧ࠻ࠩ೶"))[1])
      if bstack1lll1l1_opy_ (u"ࠨࡄࡖࡘࡆࡉࡋࡄࡎࡌࡅࡗࡍࡓࠨ೷") in a:
        bstack111lllll_opy_ = str(a.split(bstack1lll1l1_opy_ (u"ࠩ࠽ࠫ೸"))[1])
    bstack1l11llll_opy_ = None
    if bstack1lll1l1_opy_ (u"ࠪ࠱࠲ࡨࡳࡵࡣࡦ࡯ࡤ࡯ࡴࡦ࡯ࡢ࡭ࡳࡪࡥࡹࠩ೹") in args:
      i = args.index(bstack1lll1l1_opy_ (u"ࠫ࠲࠳ࡢࡴࡶࡤࡧࡰࡥࡩࡵࡧࡰࡣ࡮ࡴࡤࡦࡺࠪ೺"))
      args.pop(i)
      bstack1l11llll_opy_ = args.pop(i)
    if bstack1l11llll_opy_ is not None:
      global bstack1l1l11l1l_opy_
      bstack1l1l11l1l_opy_ = bstack1l11llll_opy_
    bstack11111llll_opy_(bstack1ll1lll1l_opy_)
    run_cli(args)
    if bstack1lll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵࠩ೻") in multiprocessing.current_process().__dict__.keys():
      for bstack1111ll1ll_opy_ in multiprocessing.current_process().bstack_error_list:
        bstack1lll111l1_opy_.append(bstack1111ll1ll_opy_)
  elif bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭೼"):
    percy.init(bstack11lll1ll_opy_, CONFIG, logger)
    percy.bstack1l11l1ll_opy_()
    bstack1l1l1lll1_opy_ = bstack1lll1l111_opy_(args, logger, CONFIG, bstack1l1l1ll11l_opy_)
    bstack1l1l1lll1_opy_.bstack1l111ll1l_opy_()
    bstack1lll1lll_opy_()
    bstack1l1l11111l_opy_ = True
    bstack1l1l111l11_opy_ = bstack1l1l1lll1_opy_.bstack1ll1111l_opy_()
    bstack1l1l1lll1_opy_.bstack111lll11l_opy_(bstack1ll1ll11l1_opy_)
    bstack11llllll_opy_ = bstack1l1l1lll1_opy_.bstack1l1l1lllll_opy_(bstack1l11ll1l1_opy_, {
      bstack1lll1l1_opy_ (u"ࠧࡉࡗࡅࡣ࡚ࡘࡌࠨ೽"): bstack1ll1l1ll_opy_,
      bstack1lll1l1_opy_ (u"ࠨࡋࡖࡣࡆࡖࡐࡠࡃࡘࡘࡔࡓࡁࡕࡇࠪ೾"): bstack11lll1ll_opy_,
      bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡃࡘࡘࡔࡓࡁࡕࡋࡒࡒࠬ೿"): bstack1l1l1ll11l_opy_
    })
    try:
      bstack1lll1ll1l_opy_, bstack1ll1l1l1l_opy_ = map(list, zip(*bstack11llllll_opy_))
      bstack1l111ll1_opy_ = bstack1lll1ll1l_opy_[0]
      for status_code in bstack1ll1l1l1l_opy_:
        if status_code != 0:
          bstack111l1l1l_opy_ = status_code
          break
    except Exception as e:
      logger.debug(bstack1lll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡢࡸࡨࠤࡪࡸࡲࡰࡴࡶࠤࡦࡴࡤࠡࡵࡷࡥࡹࡻࡳࠡࡥࡲࡨࡪ࠴ࠠࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࠾ࠥࢁࡽࠣഀ").format(str(e)))
  elif bstack1ll11ll1ll_opy_ == bstack1lll1l1_opy_ (u"ࠫࡧ࡫ࡨࡢࡸࡨࠫഁ"):
    try:
      from behave.__main__ import main as bstack1ll11l1ll1_opy_
      from behave.configuration import Configuration
    except Exception as e:
      bstack11l111l1_opy_(e, bstack111l1111_opy_)
    bstack1lll1lll_opy_()
    bstack1l1l11111l_opy_ = True
    bstack1ll1lll11_opy_ = 1
    if bstack1lll1l1_opy_ (u"ࠬࡶࡡࡳࡣ࡯ࡰࡪࡲࡳࡑࡧࡵࡔࡱࡧࡴࡧࡱࡵࡱࠬം") in CONFIG:
      bstack1ll1lll11_opy_ = CONFIG[bstack1lll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ഃ")]
    if bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪഄ") in CONFIG:
      bstack111l1lll1_opy_ = int(bstack1ll1lll11_opy_) * int(len(CONFIG[bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫഅ")]))
    else:
      bstack111l1lll1_opy_ = int(bstack1ll1lll11_opy_)
    config = Configuration(args)
    bstack1lll1l11l1_opy_ = config.paths
    if len(bstack1lll1l11l1_opy_) == 0:
      import glob
      pattern = bstack1lll1l1_opy_ (u"ࠩ࠭࠮࠴࠰࠮ࡧࡧࡤࡸࡺࡸࡥࠨആ")
      bstack11lllll11_opy_ = glob.glob(pattern, recursive=True)
      args.extend(bstack11lllll11_opy_)
      config = Configuration(args)
      bstack1lll1l11l1_opy_ = config.paths
    bstack1llllll1l_opy_ = [os.path.normpath(item) for item in bstack1lll1l11l1_opy_]
    bstack11l1ll1l1_opy_ = [os.path.normpath(item) for item in args]
    bstack1llll11111_opy_ = [item for item in bstack11l1ll1l1_opy_ if item not in bstack1llllll1l_opy_]
    import platform as pf
    if pf.system().lower() == bstack1lll1l1_opy_ (u"ࠪࡻ࡮ࡴࡤࡰࡹࡶࠫഇ"):
      from pathlib import PureWindowsPath, PurePosixPath
      bstack1llllll1l_opy_ = [str(PurePosixPath(PureWindowsPath(bstack1l1l111ll_opy_)))
                    for bstack1l1l111ll_opy_ in bstack1llllll1l_opy_]
    bstack111111111_opy_ = []
    for spec in bstack1llllll1l_opy_:
      bstack1l11l1ll1l_opy_ = []
      bstack1l11l1ll1l_opy_ += bstack1llll11111_opy_
      bstack1l11l1ll1l_opy_.append(spec)
      bstack111111111_opy_.append(bstack1l11l1ll1l_opy_)
    execution_items = []
    for bstack1l11l1ll1l_opy_ in bstack111111111_opy_:
      if bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧഈ") in CONFIG:
        for index, _ in enumerate(CONFIG[bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨഉ")]):
          item = {}
          item[bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࠪഊ")] = bstack1lll1l1_opy_ (u"ࠧࠡࠩഋ").join(bstack1l11l1ll1l_opy_)
          item[bstack1lll1l1_opy_ (u"ࠨ࡫ࡱࡨࡪࡾࠧഌ")] = index
          execution_items.append(item)
      else:
        item = {}
        item[bstack1lll1l1_opy_ (u"ࠩࡤࡶ࡬࠭഍")] = bstack1lll1l1_opy_ (u"ࠪࠤࠬഎ").join(bstack1l11l1ll1l_opy_)
        item[bstack1lll1l1_opy_ (u"ࠫ࡮ࡴࡤࡦࡺࠪഏ")] = 0
        execution_items.append(item)
    bstack111llll11_opy_ = bstack1lll111l_opy_(execution_items, bstack111l1lll1_opy_)
    for execution_item in bstack111llll11_opy_:
      bstack1l111lll1_opy_ = []
      for item in execution_item:
        bstack1l111lll1_opy_.append(bstack1ll1ll1lll_opy_(name=str(item[bstack1lll1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫഐ")]),
                                             target=bstack11l1l1ll_opy_,
                                             args=(item[bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࠪ഑")],)))
      for t in bstack1l111lll1_opy_:
        t.start()
      for t in bstack1l111lll1_opy_:
        t.join()
  else:
    bstack1llll1l1l_opy_(bstack1ll1lllll1_opy_)
  if not bstack1lll1ll11_opy_:
    bstack1l11ll11ll_opy_()
  bstack1l11ll1111_opy_.bstack1l1ll1l1_opy_()
def browserstack_initialize(bstack111l1l11_opy_=None):
  run_on_browserstack(bstack111l1l11_opy_, None, True)
def bstack1l11ll11ll_opy_():
  global CONFIG
  global bstack1111111l_opy_
  global bstack111l1l1l_opy_
  global bstack1l1lll111l_opy_
  global bstack1lll11l1ll_opy_
  bstack1l1lll1lll_opy_.stop()
  bstack1llllll1ll_opy_.bstack1l1l1l11l_opy_()
  [bstack1lll1l1l_opy_, bstack1ll11ll1_opy_] = get_build_link()
  if bstack1lll1l1l_opy_ is not None and bstack1ll1l1l1l1_opy_() != -1:
    sessions = bstack1ll1l11l11_opy_(bstack1lll1l1l_opy_)
    bstack1l1l1lll_opy_(sessions, bstack1ll11ll1_opy_)
  if bstack1111111l_opy_ == bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࠧഒ") and bstack111l1l1l_opy_ != 0:
    sys.exit(bstack111l1l1l_opy_)
  if bstack1111111l_opy_ == bstack1lll1l1_opy_ (u"ࠨࡤࡨ࡬ࡦࡼࡥࠨഓ") and bstack1l1lll111l_opy_ != 0:
    sys.exit(bstack1l1lll111l_opy_)
def bstack1llll1lll_opy_(bstack1l11111l1l_opy_):
  if bstack1l11111l1l_opy_:
    return bstack1l11111l1l_opy_.capitalize()
  else:
    return bstack1lll1l1_opy_ (u"ࠩࠪഔ")
def bstack111l1l111_opy_(bstack1ll11l1l1l_opy_):
  if bstack1lll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨക") in bstack1ll11l1l1l_opy_ and bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩഖ")] != bstack1lll1l1_opy_ (u"ࠬ࠭ഗ"):
    return bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫഘ")]
  else:
    bstack1llllll11_opy_ = bstack1lll1l1_opy_ (u"ࠢࠣങ")
    if bstack1lll1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨച") in bstack1ll11l1l1l_opy_ and bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩഛ")] != None:
      bstack1llllll11_opy_ += bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪജ")] + bstack1lll1l1_opy_ (u"ࠦ࠱ࠦࠢഝ")
      if bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠬࡵࡳࠨഞ")] == bstack1lll1l1_opy_ (u"ࠨࡩࡰࡵࠥട"):
        bstack1llllll11_opy_ += bstack1lll1l1_opy_ (u"ࠢࡪࡑࡖࠤࠧഠ")
      bstack1llllll11_opy_ += (bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬഡ")] or bstack1lll1l1_opy_ (u"ࠩࠪഢ"))
      return bstack1llllll11_opy_
    else:
      bstack1llllll11_opy_ += bstack1llll1lll_opy_(bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫണ")]) + bstack1lll1l1_opy_ (u"ࠦࠥࠨത") + (
              bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧഥ")] or bstack1lll1l1_opy_ (u"࠭ࠧദ")) + bstack1lll1l1_opy_ (u"ࠢ࠭ࠢࠥധ")
      if bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡱࡶࠫന")] == bstack1lll1l1_opy_ (u"ࠤ࡚࡭ࡳࡪ࡯ࡸࡵࠥഩ"):
        bstack1llllll11_opy_ += bstack1lll1l1_opy_ (u"࡛ࠥ࡮ࡴࠠࠣപ")
      bstack1llllll11_opy_ += bstack1ll11l1l1l_opy_[bstack1lll1l1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨഫ")] or bstack1lll1l1_opy_ (u"ࠬ࠭ബ")
      return bstack1llllll11_opy_
def bstack1ll1l111l1_opy_(bstack1ll11l111_opy_):
  if bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠨࡤࡰࡰࡨࠦഭ"):
    return bstack1lll1l1_opy_ (u"ࠧ࠽ࡶࡧࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࠣࡷࡹࡿ࡬ࡦ࠿ࠥࡧࡴࡲ࡯ࡳ࠼ࡪࡶࡪ࡫࡮࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡪࡶࡪ࡫࡮ࠣࡀࡆࡳࡲࡶ࡬ࡦࡶࡨࡨࡁ࠵ࡦࡰࡰࡷࡂࡁ࠵ࡴࡥࡀࠪമ")
  elif bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠣࡨࡤ࡭ࡱ࡫ࡤࠣയ"):
    return bstack1lll1l1_opy_ (u"ࠩ࠿ࡸࡩࠦࡣ࡭ࡣࡶࡷࡂࠨࡢࡴࡶࡤࡧࡰ࠳ࡤࡢࡶࡤࠦࠥࡹࡴࡺ࡮ࡨࡁࠧࡩ࡯࡭ࡱࡵ࠾ࡷ࡫ࡤ࠼ࠤࡁࡀ࡫ࡵ࡮ࡵࠢࡦࡳࡱࡵࡲ࠾ࠤࡵࡩࡩࠨ࠾ࡇࡣ࡬ࡰࡪࡪ࠼࠰ࡨࡲࡲࡹࡄ࠼࠰ࡶࡧࡂࠬര")
  elif bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠥࡴࡦࡹࡳࡦࡦࠥറ"):
    return bstack1lll1l1_opy_ (u"ࠫࡁࡺࡤࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨࠠࡴࡶࡼࡰࡪࡃࠢࡤࡱ࡯ࡳࡷࡀࡧࡳࡧࡨࡲࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡧࡳࡧࡨࡲࠧࡄࡐࡢࡵࡶࡩࡩࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫല")
  elif bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠧ࡫ࡲࡳࡱࡵࠦള"):
    return bstack1lll1l1_opy_ (u"࠭࠼ࡵࡦࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࠢࡶࡸࡾࡲࡥ࠾ࠤࡦࡳࡱࡵࡲ࠻ࡴࡨࡨࡀࠨ࠾࠽ࡨࡲࡲࡹࠦࡣࡰ࡮ࡲࡶࡂࠨࡲࡦࡦࠥࡂࡊࡸࡲࡰࡴ࠿࠳࡫ࡵ࡮ࡵࡀ࠿࠳ࡹࡪ࠾ࠨഴ")
  elif bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠢࡵ࡫ࡰࡩࡴࡻࡴࠣവ"):
    return bstack1lll1l1_opy_ (u"ࠨ࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠥࠤࡸࡺࡹ࡭ࡧࡀࠦࡨࡵ࡬ࡰࡴ࠽ࠧࡪ࡫ࡡ࠴࠴࠹࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࠩࡥࡦࡣ࠶࠶࠻ࠨ࠾ࡕ࡫ࡰࡩࡴࡻࡴ࠽࠱ࡩࡳࡳࡺ࠾࠽࠱ࡷࡨࡃ࠭ശ")
  elif bstack1ll11l111_opy_ == bstack1lll1l1_opy_ (u"ࠤࡵࡹࡳࡴࡩ࡯ࡩࠥഷ"):
    return bstack1lll1l1_opy_ (u"ࠪࡀࡹࡪࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࠦࡳࡵࡻ࡯ࡩࡂࠨࡣࡰ࡮ࡲࡶ࠿ࡨ࡬ࡢࡥ࡮࠿ࠧࡄ࠼ࡧࡱࡱࡸࠥࡩ࡯࡭ࡱࡵࡁࠧࡨ࡬ࡢࡥ࡮ࠦࡃࡘࡵ࡯ࡰ࡬ࡲ࡬ࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫസ")
  else:
    return bstack1lll1l1_opy_ (u"ࠫࡁࡺࡤࠡࡣ࡯࡭࡬ࡴ࠽ࠣࡥࡨࡲࡹ࡫ࡲࠣࠢࡦࡰࡦࡹࡳ࠾ࠤࡥࡷࡹࡧࡣ࡬࠯ࡧࡥࡹࡧࠢࠡࡵࡷࡽࡱ࡫࠽ࠣࡥࡲࡰࡴࡸ࠺ࡣ࡮ࡤࡧࡰࡁࠢ࠿࠾ࡩࡳࡳࡺࠠࡤࡱ࡯ࡳࡷࡃࠢࡣ࡮ࡤࡧࡰࠨ࠾ࠨഹ") + bstack1llll1lll_opy_(
      bstack1ll11l111_opy_) + bstack1lll1l1_opy_ (u"ࠬࡂ࠯ࡧࡱࡱࡸࡃࡂ࠯ࡵࡦࡁࠫഺ")
def bstack111lll1l_opy_(session):
  return bstack1lll1l1_opy_ (u"࠭࠼ࡵࡴࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡶࡴࡽࠢ࠿࠾ࡷࡨࠥࡩ࡬ࡢࡵࡶࡁࠧࡨࡳࡵࡣࡦ࡯࠲ࡪࡡࡵࡣࠣࡷࡪࡹࡳࡪࡱࡱ࠱ࡳࡧ࡭ࡦࠤࡁࡀࡦࠦࡨࡳࡧࡩࡁࠧࢁࡽࠣࠢࡷࡥࡷ࡭ࡥࡵ࠿ࠥࡣࡧࡲࡡ࡯࡭ࠥࡂࢀࢃ࠼࠰ࡣࡁࡀ࠴ࡺࡤ࠿ࡽࢀࡿࢂࡂࡴࡥࠢࡤࡰ࡮࡭࡮࠾ࠤࡦࡩࡳࡺࡥࡳࠤࠣࡧࡱࡧࡳࡴ࠿ࠥࡦࡸࡺࡡࡤ࡭࠰ࡨࡦࡺࡡࠣࡀࡾࢁࡁ࠵ࡴࡥࡀ࠿ࡸࡩࠦࡡ࡭࡫ࡪࡲࡂࠨࡣࡦࡰࡷࡩࡷࠨࠠࡤ࡮ࡤࡷࡸࡃࠢࡣࡵࡷࡥࡨࡱ࠭ࡥࡣࡷࡥࠧࡄࡻࡾ࠾࠲ࡸࡩࡄ࠼ࡵࡦࠣࡥࡱ࡯ࡧ࡯࠿ࠥࡧࡪࡴࡴࡦࡴࠥࠤࡨࡲࡡࡴࡵࡀࠦࡧࡹࡴࡢࡥ࡮࠱ࡩࡧࡴࡢࠤࡁࡿࢂࡂ࠯ࡵࡦࡁࡀࡹࡪࠠࡢ࡮࡬࡫ࡳࡃࠢࡤࡧࡱࡸࡪࡸࠢࠡࡥ࡯ࡥࡸࡹ࠽ࠣࡤࡶࡸࡦࡩ࡫࠮ࡦࡤࡸࡦࠨ࠾ࡼࡿ࠿࠳ࡹࡪ࠾࠽࠱ࡷࡶࡃ഻࠭").format(
    session[bstack1lll1l1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࡟ࡶࡴ࡯഼ࠫ")], bstack111l1l111_opy_(session), bstack1ll1l111l1_opy_(session[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡴࡶࡤࡸࡺࡹࠧഽ")]),
    bstack1ll1l111l1_opy_(session[bstack1lll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩാ")]),
    bstack1llll1lll_opy_(session[bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫി")] or session[bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫീ")] or bstack1lll1l1_opy_ (u"ࠬ࠭ു")) + bstack1lll1l1_opy_ (u"ࠨࠠࠣൂ") + (session[bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩൃ")] or bstack1lll1l1_opy_ (u"ࠨࠩൄ")),
    session[bstack1lll1l1_opy_ (u"ࠩࡲࡷࠬ൅")] + bstack1lll1l1_opy_ (u"ࠥࠤࠧെ") + session[bstack1lll1l1_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨേ")], session[bstack1lll1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧൈ")] or bstack1lll1l1_opy_ (u"࠭ࠧ൉"),
    session[bstack1lll1l1_opy_ (u"ࠧࡤࡴࡨࡥࡹ࡫ࡤࡠࡣࡷࠫൊ")] if session[bstack1lll1l1_opy_ (u"ࠨࡥࡵࡩࡦࡺࡥࡥࡡࡤࡸࠬോ")] else bstack1lll1l1_opy_ (u"ࠩࠪൌ"))
def bstack1l1l1lll_opy_(sessions, bstack1ll11ll1_opy_):
  try:
    bstack1lll1l11_opy_ = bstack1lll1l1_opy_ (u"്ࠥࠦ")
    if not os.path.exists(bstack111111ll_opy_):
      os.mkdir(bstack111111ll_opy_)
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), bstack1lll1l1_opy_ (u"ࠫࡦࡹࡳࡦࡶࡶ࠳ࡷ࡫ࡰࡰࡴࡷ࠲࡭ࡺ࡭࡭ࠩൎ")), bstack1lll1l1_opy_ (u"ࠬࡸࠧ൏")) as f:
      bstack1lll1l11_opy_ = f.read()
    bstack1lll1l11_opy_ = bstack1lll1l11_opy_.replace(bstack1lll1l1_opy_ (u"࠭ࡻࠦࡔࡈࡗ࡚ࡒࡔࡔࡡࡆࡓ࡚ࡔࡔࠦࡿࠪ൐"), str(len(sessions)))
    bstack1lll1l11_opy_ = bstack1lll1l11_opy_.replace(bstack1lll1l1_opy_ (u"ࠧࡼࠧࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠪࢃࠧ൑"), bstack1ll11ll1_opy_)
    bstack1lll1l11_opy_ = bstack1lll1l11_opy_.replace(bstack1lll1l1_opy_ (u"ࠨࡽࠨࡆ࡚ࡏࡌࡅࡡࡑࡅࡒࡋࠥࡾࠩ൒"),
                                              sessions[0].get(bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡰࡤࡱࡪ࠭൓")) if sessions[0] else bstack1lll1l1_opy_ (u"ࠪࠫൔ"))
    with open(os.path.join(bstack111111ll_opy_, bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠰ࡶࡪࡶ࡯ࡳࡶ࠱࡬ࡹࡳ࡬ࠨൕ")), bstack1lll1l1_opy_ (u"ࠬࡽࠧൖ")) as stream:
      stream.write(bstack1lll1l11_opy_.split(bstack1lll1l1_opy_ (u"࠭ࡻࠦࡕࡈࡗࡘࡏࡏࡏࡕࡢࡈࡆ࡚ࡁࠦࡿࠪൗ"))[0])
      for session in sessions:
        stream.write(bstack111lll1l_opy_(session))
      stream.write(bstack1lll1l11_opy_.split(bstack1lll1l1_opy_ (u"ࠧࡼࠧࡖࡉࡘ࡙ࡉࡐࡐࡖࡣࡉࡇࡔࡂࠧࢀࠫ൘"))[1])
    logger.info(bstack1lll1l1_opy_ (u"ࠨࡉࡨࡲࡪࡸࡡࡵࡧࡧࠤࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠣࡦࡺ࡯࡬ࡥࠢࡤࡶࡹ࡯ࡦࡢࡥࡷࡷࠥࡧࡴࠡࡽࢀࠫ൙").format(bstack111111ll_opy_));
  except Exception as e:
    logger.debug(bstack1lll11l1l1_opy_.format(str(e)))
def bstack1ll1l11l11_opy_(bstack1lll1l1l_opy_):
  global CONFIG
  try:
    host = bstack1lll1l1_opy_ (u"ࠩࡤࡴ࡮࠳ࡣ࡭ࡱࡸࡨࠬ൚") if bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶࠧ൛") in CONFIG else bstack1lll1l1_opy_ (u"ࠫࡦࡶࡩࠨ൜")
    user = CONFIG[bstack1lll1l1_opy_ (u"ࠬࡻࡳࡦࡴࡑࡥࡲ࡫ࠧ൝")]
    key = CONFIG[bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩ൞")]
    bstack1ll111ll11_opy_ = bstack1lll1l1_opy_ (u"ࠧࡢࡲࡳ࠱ࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ൟ") if bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴࠬൠ") in CONFIG else bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫൡ")
    url = bstack1lll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴ࠼࠲࠳ࢀࢃ࠺ࡼࡿࡃࡿࢂ࠴ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡩ࡯࡮࠱ࡾࢁ࠴ࡨࡵࡪ࡮ࡧࡷ࠴ࢁࡽ࠰ࡵࡨࡷࡸ࡯࡯࡯ࡵ࠱࡮ࡸࡵ࡮ࠨൢ").format(user, key, host, bstack1ll111ll11_opy_,
                                                                                bstack1lll1l1l_opy_)
    headers = {
      bstack1lll1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲ࡺࡹࡱࡧࠪൣ"): bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨ൤"),
    }
    proxies = bstack111111ll1_opy_(CONFIG, url)
    response = requests.get(url, headers=headers, proxies=proxies)
    if response.json():
      return list(map(lambda session: session[bstack1lll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࡢࡷࡪࡹࡳࡪࡱࡱࠫ൥")], response.json()))
  except Exception as e:
    logger.debug(bstack11111l1l_opy_.format(str(e)))
def get_build_link():
  global CONFIG
  global bstack11l111ll_opy_
  try:
    if bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൦") in CONFIG:
      host = bstack1lll1l1_opy_ (u"ࠨࡣࡳ࡭࠲ࡩ࡬ࡰࡷࡧࠫ൧") if bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵ࠭൨") in CONFIG else bstack1lll1l1_opy_ (u"ࠪࡥࡵ࡯ࠧ൩")
      user = CONFIG[bstack1lll1l1_opy_ (u"ࠫࡺࡹࡥࡳࡐࡤࡱࡪ࠭൪")]
      key = CONFIG[bstack1lll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ൫")]
      bstack1ll111ll11_opy_ = bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ൬") if bstack1lll1l1_opy_ (u"ࠧࡢࡲࡳࠫ൭") in CONFIG else bstack1lll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ൮")
      url = bstack1lll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡿࢂࡀࡻࡾࡂࡾࢁ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡽࢀ࠳ࡧࡻࡩ࡭ࡦࡶ࠲࡯ࡹ࡯࡯ࠩ൯").format(user, key, host, bstack1ll111ll11_opy_)
      headers = {
        bstack1lll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱ࡹࡿࡰࡦࠩ൰"): bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ൱"),
      }
      if bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ൲") in CONFIG:
        params = {bstack1lll1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ൳"): CONFIG[bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ൴")], bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൵"): CONFIG[bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ൶")]}
      else:
        params = {bstack1lll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ൷"): CONFIG[bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ൸")]}
      proxies = bstack111111ll1_opy_(CONFIG, url)
      response = requests.get(url, params=params, headers=headers, proxies=proxies)
      if response.json():
        bstack1111llll1_opy_ = response.json()[0][bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࡡࡥࡹ࡮ࡲࡤࠨ൹")]
        if bstack1111llll1_opy_:
          bstack1ll11ll1_opy_ = bstack1111llll1_opy_[bstack1lll1l1_opy_ (u"࠭ࡰࡶࡤ࡯࡭ࡨࡥࡵࡳ࡮ࠪൺ")].split(bstack1lll1l1_opy_ (u"ࠧࡱࡷࡥࡰ࡮ࡩ࠭ࡣࡷ࡬ࡰࡩ࠭ൻ"))[0] + bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡳ࠰ࠩർ") + bstack1111llll1_opy_[
            bstack1lll1l1_opy_ (u"ࠩ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬൽ")]
          logger.info(bstack11llll1l_opy_.format(bstack1ll11ll1_opy_))
          bstack11l111ll_opy_ = bstack1111llll1_opy_[bstack1lll1l1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ൾ")]
          bstack1l1llll111_opy_ = CONFIG[bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧൿ")]
          if bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ඀") in CONFIG:
            bstack1l1llll111_opy_ += bstack1lll1l1_opy_ (u"࠭ࠠࠨඁ") + CONFIG[bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩං")]
          if bstack1l1llll111_opy_ != bstack1111llll1_opy_[bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ඃ")]:
            logger.debug(bstack1l11l1llll_opy_.format(bstack1111llll1_opy_[bstack1lll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧ඄")], bstack1l1llll111_opy_))
          return [bstack1111llll1_opy_[bstack1lll1l1_opy_ (u"ࠪ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭අ")], bstack1ll11ll1_opy_]
    else:
      logger.warn(bstack1lll11l1_opy_)
  except Exception as e:
    logger.debug(bstack1ll11llll_opy_.format(str(e)))
  return [None, None]
def bstack1llll11lll_opy_(url, bstack11111l1l1_opy_=False):
  global CONFIG
  global bstack1111ll11l_opy_
  if not bstack1111ll11l_opy_:
    hostname = bstack11llllll11_opy_(url)
    is_private = bstack11l111ll1_opy_(hostname)
    if (bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨආ") in CONFIG and not bstack11ll1l1l1_opy_(CONFIG[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩඇ")])) and (is_private or bstack11111l1l1_opy_):
      bstack1111ll11l_opy_ = hostname
def bstack11llllll11_opy_(url):
  return urlparse(url).hostname
def bstack11l111ll1_opy_(hostname):
  for bstack1l111l111_opy_ in bstack1l11111ll1_opy_:
    regex = re.compile(bstack1l111l111_opy_)
    if regex.match(hostname):
      return True
  return False
def bstack1l1llll11l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def getAccessibilityResults(driver):
  global CONFIG
  global bstack11l1llll_opy_
  bstack1l1111lll_opy_ = not (bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"࠭ࡩࡴࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪඈ"), None) and bstack1llll1l1ll_opy_(
          threading.current_thread(), bstack1lll1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ඉ"), None))
  bstack111l1111l_opy_ = getattr(driver, bstack1lll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨඊ"), None) != True
  if not bstack1111ll1l_opy_.bstack1l11llllll_opy_(CONFIG, bstack11l1llll_opy_) or (bstack111l1111l_opy_ and bstack1l1111lll_opy_):
    logger.warning(bstack1lll1l1_opy_ (u"ࠤࡑࡳࡹࠦࡡ࡯ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡦࡵࡶ࡭ࡴࡴࠬࠡࡥࡤࡲࡳࡵࡴࠡࡴࡨࡸࡷ࡯ࡥࡷࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶ࠲ࠧඋ"))
    return {}
  try:
    logger.debug(bstack1lll1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥ࡭ࡥࡵࡶ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧඌ"))
    logger.debug(perform_scan(driver))
    results = driver.execute_async_script(bstack1l1lllllll_opy_.bstack11lll11l_opy_)
    return results
  except Exception:
    logger.error(bstack1lll1l1_opy_ (u"ࠦࡓࡵࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡹࡨࡶࡪࠦࡦࡰࡷࡱࡨ࠳ࠨඍ"))
    return {}
def getAccessibilityResultsSummary(driver):
  global CONFIG
  global bstack11l1llll_opy_
  bstack1l1111lll_opy_ = not (bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠬ࡯ࡳࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩඎ"), None) and bstack1llll1l1ll_opy_(
          threading.current_thread(), bstack1lll1l1_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬඏ"), None))
  bstack111l1111l_opy_ = getattr(driver, bstack1lll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧඐ"), None) != True
  if not bstack1111ll1l_opy_.bstack1l11llllll_opy_(CONFIG, bstack11l1llll_opy_) or (bstack111l1111l_opy_ and bstack1l1111lll_opy_):
    logger.warning(bstack1lll1l1_opy_ (u"ࠣࡐࡲࡸࠥࡧ࡮ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡥࡴࡵ࡬ࡳࡳ࠲ࠠࡤࡣࡱࡲࡴࡺࠠࡳࡧࡷࡶ࡮࡫ࡶࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡷࡺࡳ࡭ࡢࡴࡼ࠲ࠧඑ"))
    return {}
  try:
    logger.debug(bstack1lll1l1_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤ࡬࡫ࡴࡵ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡳࡶ࡯ࡰࡥࡷࡿࠧඒ"))
    logger.debug(perform_scan(driver))
    bstack1ll1llll1l_opy_ = driver.execute_async_script(bstack1l1lllllll_opy_.bstack11llllll1_opy_)
    return bstack1ll1llll1l_opy_
  except Exception:
    logger.error(bstack1lll1l1_opy_ (u"ࠥࡒࡴࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡶ࡯ࡰࡥࡷࡿࠠࡸࡣࡶࠤ࡫ࡵࡵ࡯ࡦ࠱ࠦඓ"))
    return {}
def perform_scan(driver, *args, **kwargs):
  global CONFIG
  global bstack11l1llll_opy_
  bstack1l1111lll_opy_ = not (bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠫ࡮ࡹࡁ࠲࠳ࡼࡘࡪࡹࡴࠨඔ"), None) and bstack1llll1l1ll_opy_(
          threading.current_thread(), bstack1lll1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫඕ"), None))
  bstack111l1111l_opy_ = getattr(driver, bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭ඖ"), None) != True
  if not bstack1111ll1l_opy_.bstack1l11llllll_opy_(CONFIG, bstack11l1llll_opy_) or (bstack111l1111l_opy_ and bstack1l1111lll_opy_):
    logger.warning(bstack1lll1l1_opy_ (u"ࠢࡏࡱࡷࠤࡦࡴࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸ࡫ࡳࡴ࡫ࡲࡲ࠱ࠦࡣࡢࡰࡱࡳࡹࠦࡲࡶࡰࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡨࡧ࡮࠯ࠤ඗"))
    return {}
  try:
    bstack1l1lll11ll_opy_ = driver.execute_async_script(bstack1l1lllllll_opy_.perform_scan, {bstack1lll1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ඘"): kwargs.get(bstack1lll1l1_opy_ (u"ࠩࡧࡶ࡮ࡼࡥࡳࡡࡦࡳࡲࡳࡡ࡯ࡦࠪ඙"), None) or bstack1lll1l1_opy_ (u"ࠪࠫක")})
    return bstack1l1lll11ll_opy_
  except Exception:
    logger.error(bstack1lll1l1_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡳࡷࡱࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡩࡡ࡯࠰ࠥඛ"))
    return {}