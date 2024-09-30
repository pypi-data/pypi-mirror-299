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
import datetime
import json
import os
import platform
import re
import subprocess
import traceback
import tempfile
import multiprocessing
import threading
import sys
import logging
from math import ceil
import urllib
from urllib.parse import urlparse
import copy
import git
import requests
from packaging import version
from bstack_utils.config import Config
from bstack_utils.constants import (bstack111ll1l1ll_opy_, bstack1l11111ll1_opy_, bstack1lll11l1l_opy_, bstack1l11l1l1l_opy_,
                                    bstack111ll1l11l_opy_, bstack111ll11l11_opy_, bstack111ll11lll_opy_, bstack111l1llll1_opy_)
from bstack_utils.messages import bstack1l1ll111l_opy_, bstack1llll11ll1_opy_
from bstack_utils.proxy import bstack111111ll1_opy_, bstack1l1ll1ll11_opy_
bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
logger = logging.getLogger(__name__)
def bstack11l111111l_opy_(config):
    return config[bstack1lll1l1_opy_ (u"ࠧࡶࡵࡨࡶࡓࡧ࡭ࡦࠩኦ")]
def bstack111llllll1_opy_(config):
    return config[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡌࡧࡼࠫኧ")]
def bstack1l1l1l11_opy_():
    try:
        import playwright
        return True
    except ImportError:
        return False
def bstack11111lllll_opy_(obj):
    values = []
    bstack111l11l1ll_opy_ = re.compile(bstack1lll1l1_opy_ (u"ࡴࠥࡢࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࡞ࡧ࠯ࠩࠨከ"), re.I)
    for key in obj.keys():
        if bstack111l11l1ll_opy_.match(key):
            values.append(obj[key])
    return values
def bstack1111llllll_opy_(config):
    tags = []
    tags.extend(bstack11111lllll_opy_(os.environ))
    tags.extend(bstack11111lllll_opy_(config))
    return tags
def bstack111111lll1_opy_(markers):
    tags = []
    for marker in markers:
        tags.append(marker.name)
    return tags
def bstack1111l1ll1l_opy_(bstack111l11ll1l_opy_):
    if not bstack111l11ll1l_opy_:
        return bstack1lll1l1_opy_ (u"ࠪࠫኩ")
    return bstack1lll1l1_opy_ (u"ࠦࢀࢃࠠࠩࡽࢀ࠭ࠧኪ").format(bstack111l11ll1l_opy_.name, bstack111l11ll1l_opy_.email)
def bstack11l111l111_opy_():
    try:
        repo = git.Repo(search_parent_directories=True)
        bstack111l11llll_opy_ = repo.common_dir
        info = {
            bstack1lll1l1_opy_ (u"ࠧࡹࡨࡢࠤካ"): repo.head.commit.hexsha,
            bstack1lll1l1_opy_ (u"ࠨࡳࡩࡱࡵࡸࡤࡹࡨࡢࠤኬ"): repo.git.rev_parse(repo.head.commit, short=True),
            bstack1lll1l1_opy_ (u"ࠢࡣࡴࡤࡲࡨ࡮ࠢክ"): repo.active_branch.name,
            bstack1lll1l1_opy_ (u"ࠣࡶࡤ࡫ࠧኮ"): repo.git.describe(all=True, tags=True, exact_match=True),
            bstack1lll1l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡶࡨࡶࠧኯ"): bstack1111l1ll1l_opy_(repo.head.commit.committer),
            bstack1lll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡷࡩࡷࡥࡤࡢࡶࡨࠦኰ"): repo.head.commit.committed_datetime.isoformat(),
            bstack1lll1l1_opy_ (u"ࠦࡦࡻࡴࡩࡱࡵࠦ኱"): bstack1111l1ll1l_opy_(repo.head.commit.author),
            bstack1lll1l1_opy_ (u"ࠧࡧࡵࡵࡪࡲࡶࡤࡪࡡࡵࡧࠥኲ"): repo.head.commit.authored_datetime.isoformat(),
            bstack1lll1l1_opy_ (u"ࠨࡣࡰ࡯ࡰ࡭ࡹࡥ࡭ࡦࡵࡶࡥ࡬࡫ࠢኳ"): repo.head.commit.message,
            bstack1lll1l1_opy_ (u"ࠢࡳࡱࡲࡸࠧኴ"): repo.git.rev_parse(bstack1lll1l1_opy_ (u"ࠣ࠯࠰ࡷ࡭ࡵࡷ࠮ࡶࡲࡴࡱ࡫ࡶࡦ࡮ࠥኵ")),
            bstack1lll1l1_opy_ (u"ࠤࡦࡳࡲࡳ࡯࡯ࡡࡪ࡭ࡹࡥࡤࡪࡴࠥ኶"): bstack111l11llll_opy_,
            bstack1lll1l1_opy_ (u"ࠥࡻࡴࡸ࡫ࡵࡴࡨࡩࡤ࡭ࡩࡵࡡࡧ࡭ࡷࠨ኷"): subprocess.check_output([bstack1lll1l1_opy_ (u"ࠦ࡬࡯ࡴࠣኸ"), bstack1lll1l1_opy_ (u"ࠧࡸࡥࡷ࠯ࡳࡥࡷࡹࡥࠣኹ"), bstack1lll1l1_opy_ (u"ࠨ࠭࠮ࡩ࡬ࡸ࠲ࡩ࡯࡮࡯ࡲࡲ࠲ࡪࡩࡳࠤኺ")]).strip().decode(
                bstack1lll1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ኻ")),
            bstack1lll1l1_opy_ (u"ࠣ࡮ࡤࡷࡹࡥࡴࡢࡩࠥኼ"): repo.git.describe(tags=True, abbrev=0, always=True),
            bstack1lll1l1_opy_ (u"ࠤࡦࡳࡲࡳࡩࡵࡵࡢࡷ࡮ࡴࡣࡦࡡ࡯ࡥࡸࡺ࡟ࡵࡣࡪࠦኽ"): repo.git.rev_list(
                bstack1lll1l1_opy_ (u"ࠥࡿࢂ࠴࠮ࡼࡿࠥኾ").format(repo.head.commit, repo.git.describe(tags=True, abbrev=0, always=True)), count=True)
        }
        remotes = repo.remotes
        bstack111l1l111l_opy_ = []
        for remote in remotes:
            bstack111l1l1lll_opy_ = {
                bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ኿"): remote.name,
                bstack1lll1l1_opy_ (u"ࠧࡻࡲ࡭ࠤዀ"): remote.url,
            }
            bstack111l1l111l_opy_.append(bstack111l1l1lll_opy_)
        bstack1111lll111_opy_ = {
            bstack1lll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ዁"): bstack1lll1l1_opy_ (u"ࠢࡨ࡫ࡷࠦዂ"),
            **info,
            bstack1lll1l1_opy_ (u"ࠣࡴࡨࡱࡴࡺࡥࡴࠤዃ"): bstack111l1l111l_opy_
        }
        bstack1111lll111_opy_ = bstack11111l111l_opy_(bstack1111lll111_opy_)
        return bstack1111lll111_opy_
    except git.InvalidGitRepositoryError:
        return {}
    except Exception as err:
        print(bstack1lll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡲࡲࡴࡺࡲࡡࡵ࡫ࡱ࡫ࠥࡍࡩࡵࠢࡰࡩࡹࡧࡤࡢࡶࡤࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲ࠻ࠢࡾࢁࠧዄ").format(err))
        return {}
def bstack11111l111l_opy_(bstack1111lll111_opy_):
    bstack1111l111ll_opy_ = bstack11111l1l11_opy_(bstack1111lll111_opy_)
    if bstack1111l111ll_opy_ and bstack1111l111ll_opy_ > bstack111ll1l11l_opy_:
        bstack111l111111_opy_ = bstack1111l111ll_opy_ - bstack111ll1l11l_opy_
        bstack111l1l1ll1_opy_ = bstack111111ll1l_opy_(bstack1111lll111_opy_[bstack1lll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡪࡶࡢࡱࡪࡹࡳࡢࡩࡨࠦዅ")], bstack111l111111_opy_)
        bstack1111lll111_opy_[bstack1lll1l1_opy_ (u"ࠦࡨࡵ࡭࡮࡫ࡷࡣࡲ࡫ࡳࡴࡣࡪࡩࠧ዆")] = bstack111l1l1ll1_opy_
        logger.info(bstack1lll1l1_opy_ (u"࡚ࠧࡨࡦࠢࡦࡳࡲࡳࡩࡵࠢ࡫ࡥࡸࠦࡢࡦࡧࡱࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪ࠮ࠡࡕ࡬ࡾࡪࠦ࡯ࡧࠢࡦࡳࡲࡳࡩࡵࠢࡤࡪࡹ࡫ࡲࠡࡶࡵࡹࡳࡩࡡࡵ࡫ࡲࡲࠥ࡯ࡳࠡࡽࢀࠤࡐࡈࠢ዇")
                    .format(bstack11111l1l11_opy_(bstack1111lll111_opy_) / 1024))
    return bstack1111lll111_opy_
def bstack11111l1l11_opy_(bstack1lll1ll111_opy_):
    try:
        if bstack1lll1ll111_opy_:
            bstack1111l1llll_opy_ = json.dumps(bstack1lll1ll111_opy_)
            bstack111111llll_opy_ = sys.getsizeof(bstack1111l1llll_opy_)
            return bstack111111llll_opy_
    except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"ࠨࡓࡰ࡯ࡨࡸ࡭࡯࡮ࡨࠢࡺࡩࡳࡺࠠࡸࡴࡲࡲ࡬ࠦࡷࡩ࡫࡯ࡩࠥࡩࡡ࡭ࡥࡸࡰࡦࡺࡩ࡯ࡩࠣࡷ࡮ࢀࡥࠡࡱࡩࠤࡏ࡙ࡏࡏࠢࡲࡦ࡯࡫ࡣࡵ࠼ࠣࡿࢂࠨወ").format(e))
    return -1
def bstack111111ll1l_opy_(field, bstack1111l1111l_opy_):
    try:
        bstack1111l11ll1_opy_ = len(bytes(bstack111ll11l11_opy_, bstack1lll1l1_opy_ (u"ࠧࡶࡶࡩ࠱࠽࠭ዉ")))
        bstack11111ll1ll_opy_ = bytes(field, bstack1lll1l1_opy_ (u"ࠨࡷࡷࡪ࠲࠾ࠧዊ"))
        bstack1111l1l1ll_opy_ = len(bstack11111ll1ll_opy_)
        bstack1111l1ll11_opy_ = ceil(bstack1111l1l1ll_opy_ - bstack1111l1111l_opy_ - bstack1111l11ll1_opy_)
        if bstack1111l1ll11_opy_ > 0:
            bstack1111ll111l_opy_ = bstack11111ll1ll_opy_[:bstack1111l1ll11_opy_].decode(bstack1lll1l1_opy_ (u"ࠩࡸࡸ࡫࠳࠸ࠨዋ"), errors=bstack1lll1l1_opy_ (u"ࠪ࡭࡬ࡴ࡯ࡳࡧࠪዌ")) + bstack111ll11l11_opy_
            return bstack1111ll111l_opy_
    except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡷࡶࡺࡴࡣࡢࡶ࡬ࡲ࡬ࠦࡦࡪࡧ࡯ࡨ࠱ࠦ࡮ࡰࡶ࡫࡭ࡳ࡭ࠠࡸࡣࡶࠤࡹࡸࡵ࡯ࡥࡤࡸࡪࡪࠠࡩࡧࡵࡩ࠿ࠦࡻࡾࠤው").format(e))
    return field
def bstack1llll1111_opy_():
    env = os.environ
    if (bstack1lll1l1_opy_ (u"ࠧࡐࡅࡏࡍࡌࡒࡘࡥࡕࡓࡎࠥዎ") in env and len(env[bstack1lll1l1_opy_ (u"ࠨࡊࡆࡐࡎࡍࡓ࡙࡟ࡖࡔࡏࠦዏ")]) > 0) or (
            bstack1lll1l1_opy_ (u"ࠢࡋࡇࡑࡏࡎࡔࡓࡠࡊࡒࡑࡊࠨዐ") in env and len(env[bstack1lll1l1_opy_ (u"ࠣࡌࡈࡒࡐࡏࡎࡔࡡࡋࡓࡒࡋࠢዑ")]) > 0):
        return {
            bstack1lll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢዒ"): bstack1lll1l1_opy_ (u"ࠥࡎࡪࡴ࡫ࡪࡰࡶࠦዓ"),
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢዔ"): env.get(bstack1lll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣ࡚ࡘࡌࠣዕ")),
            bstack1lll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣዖ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡋࡑࡅࡣࡓࡇࡍࡆࠤ዗")),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢዘ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣዙ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠥࡇࡎࠨዚ")) == bstack1lll1l1_opy_ (u"ࠦࡹࡸࡵࡦࠤዛ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠧࡉࡉࡓࡅࡏࡉࡈࡏࠢዜ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦዝ"): bstack1lll1l1_opy_ (u"ࠢࡄ࡫ࡵࡧࡱ࡫ࡃࡊࠤዞ"),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦዟ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡆࡍࡗࡉࡌࡆࡡࡅ࡙ࡎࡒࡄࡠࡗࡕࡐࠧዠ")),
            bstack1lll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧዡ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡏࡒࡄࡎࡈࡣࡏࡕࡂࠣዢ")),
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦዣ"): env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡊࡔࡆࡐࡊࡥࡂࡖࡋࡏࡈࡤࡔࡕࡎࠤዤ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠢࡄࡋࠥዥ")) == bstack1lll1l1_opy_ (u"ࠣࡶࡵࡹࡪࠨዦ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠤࡗࡖࡆ࡜ࡉࡔࠤዧ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣየ"): bstack1lll1l1_opy_ (u"࡙ࠦࡸࡡࡷ࡫ࡶࠤࡈࡏࠢዩ"),
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣዪ"): env.get(bstack1lll1l1_opy_ (u"ࠨࡔࡓࡃ࡙ࡍࡘࡥࡂࡖࡋࡏࡈࡤ࡝ࡅࡃࡡࡘࡖࡑࠨያ")),
            bstack1lll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤዬ"): env.get(bstack1lll1l1_opy_ (u"ࠣࡖࡕࡅ࡛ࡏࡓࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥይ")),
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣዮ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡘࡗࡇࡖࡊࡕࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤዯ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡏࠢደ")) == bstack1lll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥዱ") and env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡊࡡࡑࡅࡒࡋࠢዲ")) == bstack1lll1l1_opy_ (u"ࠢࡤࡱࡧࡩࡸ࡮ࡩࡱࠤዳ"):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨዴ"): bstack1lll1l1_opy_ (u"ࠤࡆࡳࡩ࡫ࡳࡩ࡫ࡳࠦድ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዶ"): None,
            bstack1lll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨዷ"): None,
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦዸ"): None
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠨࡂࡊࡖࡅ࡙ࡈࡑࡅࡕࡡࡅࡖࡆࡔࡃࡉࠤዹ")) and env.get(bstack1lll1l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡇࡔࡓࡍࡊࡖࠥዺ")):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨዻ"): bstack1lll1l1_opy_ (u"ࠤࡅ࡭ࡹࡨࡵࡤ࡭ࡨࡸࠧዼ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨዽ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡇࡏࡔࡃࡗࡆࡏࡊ࡚࡟ࡈࡋࡗࡣࡍ࡚ࡔࡑࡡࡒࡖࡎࡍࡉࡏࠤዾ")),
            bstack1lll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢዿ"): None,
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጀ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡃࡋࡗࡆ࡚ࡉࡋࡆࡖࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤጁ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡌࠦጂ")) == bstack1lll1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢጃ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠥࡈࡗࡕࡎࡆࠤጄ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጅ"): bstack1lll1l1_opy_ (u"ࠧࡊࡲࡰࡰࡨࠦጆ"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጇ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡅࡔࡒࡒࡊࡥࡂࡖࡋࡏࡈࡤࡒࡉࡏࡍࠥገ")),
            bstack1lll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥጉ"): None,
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣጊ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡈࡗࡕࡎࡆࡡࡅ࡙ࡎࡒࡄࡠࡐࡘࡑࡇࡋࡒࠣጋ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡏࠢጌ")) == bstack1lll1l1_opy_ (u"ࠧࡺࡲࡶࡧࠥግ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠨࡓࡆࡏࡄࡔࡍࡕࡒࡆࠤጎ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠢ࡯ࡣࡰࡩࠧጏ"): bstack1lll1l1_opy_ (u"ࠣࡕࡨࡱࡦࡶࡨࡰࡴࡨࠦጐ"),
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡷࡵࡰࠧ጑"): env.get(bstack1lll1l1_opy_ (u"ࠥࡗࡊࡓࡁࡑࡊࡒࡖࡊࡥࡏࡓࡉࡄࡒࡎࡠࡁࡕࡋࡒࡒࡤ࡛ࡒࡍࠤጒ")),
            bstack1lll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨጓ"): env.get(bstack1lll1l1_opy_ (u"࡙ࠧࡅࡎࡃࡓࡌࡔࡘࡅࡠࡌࡒࡆࡤࡔࡁࡎࡇࠥጔ")),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧጕ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡔࡇࡐࡅࡕࡎࡏࡓࡇࡢࡎࡔࡈ࡟ࡊࡆࠥ጖"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡌࠦ጗")) == bstack1lll1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢጘ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠥࡋࡎ࡚ࡌࡂࡄࡢࡇࡎࠨጙ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጚ"): bstack1lll1l1_opy_ (u"ࠧࡍࡩࡵࡎࡤࡦࠧጛ"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጜ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡄࡋࡢࡎࡔࡈ࡟ࡖࡔࡏࠦጝ")),
            bstack1lll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥጞ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡆࡍࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢጟ")),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤጠ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡏ࡟ࡋࡑࡅࡣࡎࡊࠢጡ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠧࡉࡉࠣጢ")) == bstack1lll1l1_opy_ (u"ࠨࡴࡳࡷࡨࠦጣ") and bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࠥጤ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨጥ"): bstack1lll1l1_opy_ (u"ࠤࡅࡹ࡮ࡲࡤ࡬࡫ࡷࡩࠧጦ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጧ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡎࡍ࡙ࡋ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥጨ")),
            bstack1lll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢጩ"): env.get(bstack1lll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡐࡏࡔࡆࡡࡏࡅࡇࡋࡌࠣጪ")) or env.get(bstack1lll1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡑࡉࡕࡇࡢࡔࡎࡖࡅࡍࡋࡑࡉࡤࡔࡁࡎࡇࠥጫ")),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢጬ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡌࡋࡗࡉࡤࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦጭ"))
        }
    if bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠥࡘࡋࡥࡂࡖࡋࡏࡈࠧጮ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤጯ"): bstack1lll1l1_opy_ (u"ࠧ࡜ࡩࡴࡷࡤࡰ࡙ࠥࡴࡶࡦ࡬ࡳ࡚ࠥࡥࡢ࡯ࠣࡗࡪࡸࡶࡪࡥࡨࡷࠧጰ"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤጱ"): bstack1lll1l1_opy_ (u"ࠢࡼࡿࡾࢁࠧጲ").format(env.get(bstack1lll1l1_opy_ (u"ࠨࡕ࡜ࡗ࡙ࡋࡍࡠࡖࡈࡅࡒࡌࡏࡖࡐࡇࡅ࡙ࡏࡏࡏࡕࡈࡖ࡛ࡋࡒࡖࡔࡌࠫጳ")), env.get(bstack1lll1l1_opy_ (u"ࠩࡖ࡝ࡘ࡚ࡅࡎࡡࡗࡉࡆࡓࡐࡓࡑࡍࡉࡈ࡚ࡉࡅࠩጴ"))),
            bstack1lll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧጵ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡘ࡟ࡓࡕࡇࡐࡣࡉࡋࡆࡊࡐࡌࡘࡎࡕࡎࡊࡆࠥጶ")),
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡳࡻ࡭ࡣࡧࡵࠦጷ"): env.get(bstack1lll1l1_opy_ (u"ࠨࡂࡖࡋࡏࡈࡤࡈࡕࡊࡎࡇࡍࡉࠨጸ"))
        }
    if bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠢࡂࡒࡓ࡚ࡊ࡟ࡏࡓࠤጹ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨጺ"): bstack1lll1l1_opy_ (u"ࠤࡄࡴࡵࡼࡥࡺࡱࡵࠦጻ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨጼ"): bstack1lll1l1_opy_ (u"ࠦࢀࢃ࠯ࡱࡴࡲ࡮ࡪࡩࡴ࠰ࡽࢀ࠳ࢀࢃ࠯ࡣࡷ࡬ࡰࡩࡹ࠯ࡼࡿࠥጽ").format(env.get(bstack1lll1l1_opy_ (u"ࠬࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡖࡔࡏࠫጾ")), env.get(bstack1lll1l1_opy_ (u"࠭ࡁࡑࡒ࡙ࡉ࡞ࡕࡒࡠࡃࡆࡇࡔ࡛ࡎࡕࡡࡑࡅࡒࡋࠧጿ")), env.get(bstack1lll1l1_opy_ (u"ࠧࡂࡒࡓ࡚ࡊ࡟ࡏࡓࡡࡓࡖࡔࡐࡅࡄࡖࡢࡗࡑ࡛ࡇࠨፀ")), env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡓࡔ࡛ࡋ࡙ࡐࡔࡢࡆ࡚ࡏࡌࡅࡡࡌࡈࠬፁ"))),
            bstack1lll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦፂ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡅࡕࡖࡖࡆ࡛ࡒࡖࡤࡐࡏࡃࡡࡑࡅࡒࡋࠢፃ")),
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥፄ"): env.get(bstack1lll1l1_opy_ (u"ࠧࡇࡐࡑࡘࡈ࡝ࡔࡘ࡟ࡃࡗࡌࡐࡉࡥࡎࡖࡏࡅࡉࡗࠨፅ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠨࡁ࡛ࡗࡕࡉࡤࡎࡔࡕࡒࡢ࡙ࡘࡋࡒࡠࡃࡊࡉࡓ࡚ࠢፆ")) and env.get(bstack1lll1l1_opy_ (u"ࠢࡕࡈࡢࡆ࡚ࡏࡌࡅࠤፇ")):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨፈ"): bstack1lll1l1_opy_ (u"ࠤࡄࡾࡺࡸࡥࠡࡅࡌࠦፉ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨፊ"): bstack1lll1l1_opy_ (u"ࠦࢀࢃࡻࡾ࠱ࡢࡦࡺ࡯࡬ࡥ࠱ࡵࡩࡸࡻ࡬ࡵࡵࡂࡦࡺ࡯࡬ࡥࡋࡧࡁࢀࢃࠢፋ").format(env.get(bstack1lll1l1_opy_ (u"࡙࡙ࠬࡔࡖࡈࡑࡤ࡚ࡅࡂࡏࡉࡓ࡚ࡔࡄࡂࡖࡌࡓࡓ࡙ࡅࡓࡘࡈࡖ࡚ࡘࡉࠨፌ")), env.get(bstack1lll1l1_opy_ (u"࠭ࡓ࡚ࡕࡗࡉࡒࡥࡔࡆࡃࡐࡔࡗࡕࡊࡆࡅࡗࠫፍ")), env.get(bstack1lll1l1_opy_ (u"ࠧࡃࡗࡌࡐࡉࡥࡂࡖࡋࡏࡈࡎࡊࠧፎ"))),
            bstack1lll1l1_opy_ (u"ࠣ࡬ࡲࡦࡤࡴࡡ࡮ࡧࠥፏ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊࡉࡅࠤፐ")),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡱࡹࡲࡨࡥࡳࠤፑ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡇ࡛ࡉࡍࡆࡢࡆ࡚ࡏࡌࡅࡋࡇࠦፒ"))
        }
    if any([env.get(bstack1lll1l1_opy_ (u"ࠧࡉࡏࡅࡇࡅ࡙ࡎࡒࡄࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥፓ")), env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡕࡉࡘࡕࡌࡗࡇࡇࡣࡘࡕࡕࡓࡅࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࠧፔ")), env.get(bstack1lll1l1_opy_ (u"ࠢࡄࡑࡇࡉࡇ࡛ࡉࡍࡆࡢࡗࡔ࡛ࡒࡄࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࠦፕ"))]):
        return {
            bstack1lll1l1_opy_ (u"ࠣࡰࡤࡱࡪࠨፖ"): bstack1lll1l1_opy_ (u"ࠤࡄ࡛ࡘࠦࡃࡰࡦࡨࡆࡺ࡯࡬ࡥࠤፗ"),
            bstack1lll1l1_opy_ (u"ࠥࡦࡺ࡯࡬ࡥࡡࡸࡶࡱࠨፘ"): env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡕࡄࡆࡄࡘࡍࡑࡊ࡟ࡑࡗࡅࡐࡎࡉ࡟ࡃࡗࡌࡐࡉࡥࡕࡓࡎࠥፙ")),
            bstack1lll1l1_opy_ (u"ࠧࡰ࡯ࡣࡡࡱࡥࡲ࡫ࠢፚ"): env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡐࡆࡈࡆ࡚ࡏࡌࡅࡡࡅ࡙ࡎࡒࡄࡠࡋࡇࠦ፛")),
            bstack1lll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥ࡮ࡶ࡯ࡥࡩࡷࠨ፜"): env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡒࡈࡊࡈࡕࡊࡎࡇࡣࡇ࡛ࡉࡍࡆࡢࡍࡉࠨ፝"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠤࡥࡥࡲࡨ࡯ࡰࡡࡥࡹ࡮ࡲࡤࡏࡷࡰࡦࡪࡸࠢ፞")):
        return {
            bstack1lll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣ፟"): bstack1lll1l1_opy_ (u"ࠦࡇࡧ࡭ࡣࡱࡲࠦ፠"),
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣ፡"): env.get(bstack1lll1l1_opy_ (u"ࠨࡢࡢ࡯ࡥࡳࡴࡥࡢࡶ࡫࡯ࡨࡗ࡫ࡳࡶ࡮ࡷࡷ࡚ࡸ࡬ࠣ።")),
            bstack1lll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፣"): env.get(bstack1lll1l1_opy_ (u"ࠣࡤࡤࡱࡧࡵ࡯ࡠࡵ࡫ࡳࡷࡺࡊࡰࡤࡑࡥࡲ࡫ࠢ፤")),
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ፥"): env.get(bstack1lll1l1_opy_ (u"ࠥࡦࡦࡳࡢࡰࡱࡢࡦࡺ࡯࡬ࡥࡐࡸࡱࡧ࡫ࡲࠣ፦"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠦ࡜ࡋࡒࡄࡍࡈࡖࠧ፧")) or env.get(bstack1lll1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ፨")):
        return {
            bstack1lll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦ፩"): bstack1lll1l1_opy_ (u"ࠢࡘࡧࡵࡧࡰ࡫ࡲࠣ፪"),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦ፫"): env.get(bstack1lll1l1_opy_ (u"ࠤ࡚ࡉࡗࡉࡋࡆࡔࡢࡆ࡚ࡏࡌࡅࡡࡘࡖࡑࠨ፬")),
            bstack1lll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧ፭"): bstack1lll1l1_opy_ (u"ࠦࡒࡧࡩ࡯ࠢࡓ࡭ࡵ࡫࡬ࡪࡰࡨࠦ፮") if env.get(bstack1lll1l1_opy_ (u"ࠧ࡝ࡅࡓࡅࡎࡉࡗࡥࡍࡂࡋࡑࡣࡕࡏࡐࡆࡎࡌࡒࡊࡥࡓࡕࡃࡕࡘࡊࡊࠢ፯")) else None,
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ፰"): env.get(bstack1lll1l1_opy_ (u"ࠢࡘࡇࡕࡇࡐࡋࡒࡠࡉࡌࡘࡤࡉࡏࡎࡏࡌࡘࠧ፱"))
        }
    if any([env.get(bstack1lll1l1_opy_ (u"ࠣࡉࡆࡔࡤࡖࡒࡐࡌࡈࡇ࡙ࠨ፲")), env.get(bstack1lll1l1_opy_ (u"ࠤࡊࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥ፳")), env.get(bstack1lll1l1_opy_ (u"ࠥࡋࡔࡕࡇࡍࡇࡢࡇࡑࡕࡕࡅࡡࡓࡖࡔࡐࡅࡄࡖࠥ፴"))]):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ፵"): bstack1lll1l1_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡉ࡬ࡰࡷࡧࠦ፶"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ፷"): None,
            bstack1lll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤ፸"): env.get(bstack1lll1l1_opy_ (u"ࠣࡒࡕࡓࡏࡋࡃࡕࡡࡌࡈࠧ፹")),
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣ፺"): env.get(bstack1lll1l1_opy_ (u"ࠥࡆ࡚ࡏࡌࡅࡡࡌࡈࠧ፻"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠦࡘࡎࡉࡑࡒࡄࡆࡑࡋࠢ፼")):
        return {
            bstack1lll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥ፽"): bstack1lll1l1_opy_ (u"ࠨࡓࡩ࡫ࡳࡴࡦࡨ࡬ࡦࠤ፾"),
            bstack1lll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥ፿"): env.get(bstack1lll1l1_opy_ (u"ࠣࡕࡋࡍࡕࡖࡁࡃࡎࡈࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᎀ")),
            bstack1lll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎁ"): bstack1lll1l1_opy_ (u"ࠥࡎࡴࡨࠠࠤࡽࢀࠦᎂ").format(env.get(bstack1lll1l1_opy_ (u"ࠫࡘࡎࡉࡑࡒࡄࡆࡑࡋ࡟ࡋࡑࡅࡣࡎࡊࠧᎃ"))) if env.get(bstack1lll1l1_opy_ (u"࡙ࠧࡈࡊࡒࡓࡅࡇࡒࡅࡠࡌࡒࡆࡤࡏࡄࠣᎄ")) else None,
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᎅ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡔࡊࡌࡔࡕࡇࡂࡍࡇࡢࡆ࡚ࡏࡌࡅࡡࡑ࡙ࡒࡈࡅࡓࠤᎆ"))
        }
    if bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠣࡐࡈࡘࡑࡏࡆ࡚ࠤᎇ"))):
        return {
            bstack1lll1l1_opy_ (u"ࠤࡱࡥࡲ࡫ࠢᎈ"): bstack1lll1l1_opy_ (u"ࠥࡒࡪࡺ࡬ࡪࡨࡼࠦᎉ"),
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡹࡷࡲࠢᎊ"): env.get(bstack1lll1l1_opy_ (u"ࠧࡊࡅࡑࡎࡒ࡝ࡤ࡛ࡒࡍࠤᎋ")),
            bstack1lll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎌ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡔࡋࡗࡉࡤࡔࡁࡎࡇࠥᎍ")),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎎ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᎏ"))
        }
    if bstack11ll1l1l1_opy_(env.get(bstack1lll1l1_opy_ (u"ࠥࡋࡎ࡚ࡈࡖࡄࡢࡅࡈ࡚ࡉࡐࡐࡖࠦ᎐"))):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤ᎑"): bstack1lll1l1_opy_ (u"ࠧࡍࡩࡵࡊࡸࡦࠥࡇࡣࡵ࡫ࡲࡲࡸࠨ᎒"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤ᎓"): bstack1lll1l1_opy_ (u"ࠢࡼࡿ࠲ࡿࢂ࠵ࡡࡤࡶ࡬ࡳࡳࡹ࠯ࡳࡷࡱࡷ࠴ࢁࡽࠣ᎔").format(env.get(bstack1lll1l1_opy_ (u"ࠨࡉࡌࡘࡍ࡛ࡂࡠࡕࡈࡖ࡛ࡋࡒࡠࡗࡕࡐࠬ᎕")), env.get(bstack1lll1l1_opy_ (u"ࠩࡊࡍ࡙ࡎࡕࡃࡡࡕࡉࡕࡕࡓࡊࡖࡒࡖ࡞࠭᎖")), env.get(bstack1lll1l1_opy_ (u"ࠪࡋࡎ࡚ࡈࡖࡄࡢࡖ࡚ࡔ࡟ࡊࡆࠪ᎗"))),
            bstack1lll1l1_opy_ (u"ࠦ࡯ࡵࡢࡠࡰࡤࡱࡪࠨ᎘"): env.get(bstack1lll1l1_opy_ (u"ࠧࡍࡉࡕࡊࡘࡆࡤ࡝ࡏࡓࡍࡉࡐࡔ࡝ࠢ᎙")),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧ᎚"): env.get(bstack1lll1l1_opy_ (u"ࠢࡈࡋࡗࡌ࡚ࡈ࡟ࡓࡗࡑࡣࡎࡊࠢ᎛"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡌࠦ᎜")) == bstack1lll1l1_opy_ (u"ࠤࡷࡶࡺ࡫ࠢ᎝") and env.get(bstack1lll1l1_opy_ (u"࡚ࠥࡊࡘࡃࡆࡎࠥ᎞")) == bstack1lll1l1_opy_ (u"ࠦ࠶ࠨ᎟"):
        return {
            bstack1lll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᎠ"): bstack1lll1l1_opy_ (u"ࠨࡖࡦࡴࡦࡩࡱࠨᎡ"),
            bstack1lll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᎢ"): bstack1lll1l1_opy_ (u"ࠣࡪࡷࡸࡵࡀ࠯࠰ࡽࢀࠦᎣ").format(env.get(bstack1lll1l1_opy_ (u"࡙ࠩࡉࡗࡉࡅࡍࡡࡘࡖࡑ࠭Ꭴ"))),
            bstack1lll1l1_opy_ (u"ࠥ࡮ࡴࡨ࡟࡯ࡣࡰࡩࠧᎥ"): None,
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎦ"): None,
        }
    if env.get(bstack1lll1l1_opy_ (u"࡚ࠧࡅࡂࡏࡆࡍ࡙࡟࡟ࡗࡇࡕࡗࡎࡕࡎࠣᎧ")):
        return {
            bstack1lll1l1_opy_ (u"ࠨ࡮ࡢ࡯ࡨࠦᎨ"): bstack1lll1l1_opy_ (u"ࠢࡕࡧࡤࡱࡨ࡯ࡴࡺࠤᎩ"),
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟ࡶࡴ࡯ࠦᎪ"): None,
            bstack1lll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᎫ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡘࡊࡇࡍࡄࡋࡗ࡝ࡤࡖࡒࡐࡌࡈࡇ࡙ࡥࡎࡂࡏࡈࠦᎬ")),
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᎭ"): env.get(bstack1lll1l1_opy_ (u"ࠧࡈࡕࡊࡎࡇࡣࡓ࡛ࡍࡃࡇࡕࠦᎮ"))
        }
    if any([env.get(bstack1lll1l1_opy_ (u"ࠨࡃࡐࡐࡆࡓ࡚ࡘࡓࡆࠤᎯ")), env.get(bstack1lll1l1_opy_ (u"ࠢࡄࡑࡑࡇࡔ࡛ࡒࡔࡇࡢ࡙ࡗࡒࠢᎰ")), env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡒࡒࡈࡕࡕࡓࡕࡈࡣ࡚࡙ࡅࡓࡐࡄࡑࡊࠨᎱ")), env.get(bstack1lll1l1_opy_ (u"ࠤࡆࡓࡓࡉࡏࡖࡔࡖࡉࡤ࡚ࡅࡂࡏࠥᎲ"))]):
        return {
            bstack1lll1l1_opy_ (u"ࠥࡲࡦࡳࡥࠣᎳ"): bstack1lll1l1_opy_ (u"ࠦࡈࡵ࡮ࡤࡱࡸࡶࡸ࡫ࠢᎴ"),
            bstack1lll1l1_opy_ (u"ࠧࡨࡵࡪ࡮ࡧࡣࡺࡸ࡬ࠣᎵ"): None,
            bstack1lll1l1_opy_ (u"ࠨࡪࡰࡤࡢࡲࡦࡳࡥࠣᎶ"): env.get(bstack1lll1l1_opy_ (u"ࠢࡃࡗࡌࡐࡉࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᎷ")) or None,
            bstack1lll1l1_opy_ (u"ࠣࡤࡸ࡭ࡱࡪ࡟࡯ࡷࡰࡦࡪࡸࠢᎸ"): env.get(bstack1lll1l1_opy_ (u"ࠤࡅ࡙ࡎࡒࡄࡠࡋࡇࠦᎹ"), 0)
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠥࡋࡔࡥࡊࡐࡄࡢࡒࡆࡓࡅࠣᎺ")):
        return {
            bstack1lll1l1_opy_ (u"ࠦࡳࡧ࡭ࡦࠤᎻ"): bstack1lll1l1_opy_ (u"ࠧࡍ࡯ࡄࡆࠥᎼ"),
            bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡻࡲ࡭ࠤᎽ"): None,
            bstack1lll1l1_opy_ (u"ࠢ࡫ࡱࡥࡣࡳࡧ࡭ࡦࠤᎾ"): env.get(bstack1lll1l1_opy_ (u"ࠣࡉࡒࡣࡏࡕࡂࡠࡐࡄࡑࡊࠨᎿ")),
            bstack1lll1l1_opy_ (u"ࠤࡥࡹ࡮ࡲࡤࡠࡰࡸࡱࡧ࡫ࡲࠣᏀ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡋࡔࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡅࡒ࡙ࡓ࡚ࡅࡓࠤᏁ"))
        }
    if env.get(bstack1lll1l1_opy_ (u"ࠦࡈࡌ࡟ࡃࡗࡌࡐࡉࡥࡉࡅࠤᏂ")):
        return {
            bstack1lll1l1_opy_ (u"ࠧࡴࡡ࡮ࡧࠥᏃ"): bstack1lll1l1_opy_ (u"ࠨࡃࡰࡦࡨࡊࡷ࡫ࡳࡩࠤᏄ"),
            bstack1lll1l1_opy_ (u"ࠢࡣࡷ࡬ࡰࡩࡥࡵࡳ࡮ࠥᏅ"): env.get(bstack1lll1l1_opy_ (u"ࠣࡅࡉࡣࡇ࡛ࡉࡍࡆࡢ࡙ࡗࡒࠢᏆ")),
            bstack1lll1l1_opy_ (u"ࠤ࡭ࡳࡧࡥ࡮ࡢ࡯ࡨࠦᏇ"): env.get(bstack1lll1l1_opy_ (u"ࠥࡇࡋࡥࡐࡊࡒࡈࡐࡎࡔࡅࡠࡐࡄࡑࡊࠨᏈ")),
            bstack1lll1l1_opy_ (u"ࠦࡧࡻࡩ࡭ࡦࡢࡲࡺࡳࡢࡦࡴࠥᏉ"): env.get(bstack1lll1l1_opy_ (u"ࠧࡉࡆࡠࡄࡘࡍࡑࡊ࡟ࡊࡆࠥᏊ"))
        }
    return {bstack1lll1l1_opy_ (u"ࠨࡢࡶ࡫࡯ࡨࡤࡴࡵ࡮ࡤࡨࡶࠧᏋ"): None}
def get_host_info():
    return {
        bstack1lll1l1_opy_ (u"ࠢࡩࡱࡶࡸࡳࡧ࡭ࡦࠤᏌ"): platform.node(),
        bstack1lll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠥᏍ"): platform.system(),
        bstack1lll1l1_opy_ (u"ࠤࡷࡽࡵ࡫ࠢᏎ"): platform.machine(),
        bstack1lll1l1_opy_ (u"ࠥࡺࡪࡸࡳࡪࡱࡱࠦᏏ"): platform.version(),
        bstack1lll1l1_opy_ (u"ࠦࡦࡸࡣࡩࠤᏐ"): platform.architecture()[0]
    }
def bstack1l11l11111_opy_():
    try:
        import selenium
        return True
    except ImportError:
        return False
def bstack1111ll1l1l_opy_():
    if bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡤࡹࡥࡴࡵ࡬ࡳࡳ࠭Ꮡ")):
        return bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࠬᏒ")
    return bstack1lll1l1_opy_ (u"ࠧࡶࡰ࡮ࡲࡴࡽ࡮ࡠࡩࡵ࡭ࡩ࠭Ꮣ")
def bstack1111l111l1_opy_(driver):
    info = {
        bstack1lll1l1_opy_ (u"ࠨࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᏔ"): driver.capabilities,
        bstack1lll1l1_opy_ (u"ࠩࡶࡩࡸࡹࡩࡰࡰࡢ࡭ࡩ࠭Ꮥ"): driver.session_id,
        bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫᏖ"): driver.capabilities.get(bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᏗ"), None),
        bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᏘ"): driver.capabilities.get(bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᏙ"), None),
        bstack1lll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᏚ"): driver.capabilities.get(bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᏛ"), None),
    }
    if bstack1111ll1l1l_opy_() == bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨᏜ"):
        info[bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࠫᏝ")] = bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰ࠮ࡣࡸࡸࡴࡳࡡࡵࡧࠪᏞ") if bstack1ll1l11l1_opy_() else bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧᏟ")
    return info
def bstack1ll1l11l1_opy_():
    if bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬᏠ")):
        return True
    if bstack11ll1l1l1_opy_(os.environ.get(bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡉࡔࡡࡄࡔࡕࡥࡁࡖࡖࡒࡑࡆ࡚ࡅࠨᏡ"), None)):
        return True
    return False
def bstack1l1ll1l11_opy_(bstack111l1l1l1l_opy_, url, data, config):
    headers = config.get(bstack1lll1l1_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᏢ"), None)
    proxies = bstack111111ll1_opy_(config, url)
    auth = config.get(bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᏣ"), None)
    response = requests.request(
            bstack111l1l1l1l_opy_,
            url=url,
            headers=headers,
            auth=auth,
            json=data,
            proxies=proxies
        )
    return response
def bstack1lll111l_opy_(bstack1l111111_opy_, size):
    bstack111111l11_opy_ = []
    while len(bstack1l111111_opy_) > size:
        bstack11l1111ll_opy_ = bstack1l111111_opy_[:size]
        bstack111111l11_opy_.append(bstack11l1111ll_opy_)
        bstack1l111111_opy_ = bstack1l111111_opy_[size:]
    bstack111111l11_opy_.append(bstack1l111111_opy_)
    return bstack111111l11_opy_
def bstack11111ll1l1_opy_(message, bstack1111ll1ll1_opy_=False):
    os.write(1, bytes(message, bstack1lll1l1_opy_ (u"ࠪࡹࡹ࡬࠭࠹ࠩᏤ")))
    os.write(1, bytes(bstack1lll1l1_opy_ (u"ࠫࡡࡴࠧᏥ"), bstack1lll1l1_opy_ (u"ࠬࡻࡴࡧ࠯࠻ࠫᏦ")))
    if bstack1111ll1ll1_opy_:
        with open(bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰ࠳࡯࠲࠳ࡼ࠱ࠬᏧ") + os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡇ࡛ࡉࡍࡆࡢࡌࡆ࡙ࡈࡆࡆࡢࡍࡉ࠭Ꮸ")] + bstack1lll1l1_opy_ (u"ࠨ࠰࡯ࡳ࡬࠭Ꮹ"), bstack1lll1l1_opy_ (u"ࠩࡤࠫᏪ")) as f:
            f.write(message + bstack1lll1l1_opy_ (u"ࠪࡠࡳ࠭Ꮻ"))
def bstack111111l1l1_opy_():
    return os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡅ࡚࡚ࡏࡎࡃࡗࡍࡔࡔࠧᏬ")].lower() == bstack1lll1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᏭ")
def bstack1lll11111l_opy_(bstack1111l11111_opy_):
    return bstack1lll1l1_opy_ (u"࠭ࡻࡾ࠱ࡾࢁࠬᏮ").format(bstack111ll1l1ll_opy_, bstack1111l11111_opy_)
def bstack1l11lll111_opy_():
    return bstack11ll11l11l_opy_().replace(tzinfo=None).isoformat() + bstack1lll1l1_opy_ (u"࡛ࠧࠩᏯ")
def bstack1111lll11l_opy_(start, finish):
    return (datetime.datetime.fromisoformat(finish.rstrip(bstack1lll1l1_opy_ (u"ࠨ࡜ࠪᏰ"))) - datetime.datetime.fromisoformat(start.rstrip(bstack1lll1l1_opy_ (u"ࠩ࡝ࠫᏱ")))).total_seconds() * 1000
def bstack11111ll11l_opy_(timestamp):
    return bstack111l11ll11_opy_(timestamp).isoformat() + bstack1lll1l1_opy_ (u"ࠪ࡞ࠬᏲ")
def bstack1111llll11_opy_(bstack1111ll1l11_opy_):
    date_format = bstack1lll1l1_opy_ (u"ࠫࠪ࡟ࠥ࡮ࠧࡧࠤࠪࡎ࠺ࠦࡏ࠽ࠩࡘ࠴ࠥࡧࠩᏳ")
    bstack1111l1lll1_opy_ = datetime.datetime.strptime(bstack1111ll1l11_opy_, date_format)
    return bstack1111l1lll1_opy_.isoformat() + bstack1lll1l1_opy_ (u"ࠬࡠࠧᏴ")
def bstack111l1111ll_opy_(outcome):
    _, exception, _ = outcome.excinfo or (None, None, None)
    if exception:
        return bstack1lll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭Ᏽ")
    else:
        return bstack1lll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧ᏶")
def bstack11ll1l1l1_opy_(val):
    if val is None:
        return False
    return val.__str__().lower() == bstack1lll1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᏷")
def bstack11111ll111_opy_(val):
    return val.__str__().lower() == bstack1lll1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᏸ")
def bstack11ll111ll1_opy_(bstack111l11l11l_opy_=Exception, class_method=False, default_value=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except bstack111l11l11l_opy_ as e:
                print(bstack1lll1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡹࡳࡩࡴࡪࡱࡱࠤࢀࢃࠠ࠮ࡀࠣࡿࢂࡀࠠࡼࡿࠥᏹ").format(func.__name__, bstack111l11l11l_opy_.__name__, str(e)))
                return default_value
        return wrapper
    def bstack11111lll11_opy_(bstack111l1ll1ll_opy_):
        def wrapped(cls, *args, **kwargs):
            try:
                return bstack111l1ll1ll_opy_(cls, *args, **kwargs)
            except bstack111l11l11l_opy_ as e:
                print(bstack1lll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡺࡴࡣࡵ࡫ࡲࡲࠥࢁࡽࠡ࠯ࡁࠤࢀࢃ࠺ࠡࡽࢀࠦᏺ").format(bstack111l1ll1ll_opy_.__name__, bstack111l11l11l_opy_.__name__, str(e)))
                return default_value
        return wrapped
    if class_method:
        return bstack11111lll11_opy_
    else:
        return decorator
def bstack1l1111ll11_opy_(bstack11l1l1111l_opy_):
    if bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᏻ") in bstack11l1l1111l_opy_ and bstack11111ll111_opy_(bstack11l1l1111l_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᏼ")]):
        return False
    if bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᏽ") in bstack11l1l1111l_opy_ and bstack11111ll111_opy_(bstack11l1l1111l_opy_[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᏾")]):
        return False
    return True
def bstack1llllll1l1_opy_():
    try:
        from pytest_bdd import reporting
        return True
    except Exception as e:
        return False
def bstack1llll1ll1l_opy_(hub_url):
    if bstack1l1l1l111_opy_() <= version.parse(bstack1lll1l1_opy_ (u"ࠩ࠶࠲࠶࠹࠮࠱ࠩ᏿")):
        if hub_url != bstack1lll1l1_opy_ (u"ࠪࠫ᐀"):
            return bstack1lll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᐁ") + hub_url + bstack1lll1l1_opy_ (u"ࠧࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠤᐂ")
        return bstack1lll11l1l_opy_
    if hub_url != bstack1lll1l1_opy_ (u"࠭ࠧᐃ"):
        return bstack1lll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࡀ࠯࠰ࠤᐄ") + hub_url + bstack1lll1l1_opy_ (u"ࠣ࠱ࡺࡨ࠴࡮ࡵࡣࠤᐅ")
    return bstack1l11l1l1l_opy_
def bstack11111l11ll_opy_():
    return isinstance(os.getenv(bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡒ࡜ࡘࡊ࡙ࡔࡠࡒࡏ࡙ࡌࡏࡎࠨᐆ")), str)
def bstack11llllll11_opy_(url):
    return urlparse(url).hostname
def bstack11l111ll1_opy_(hostname):
    for bstack1l111l111_opy_ in bstack1l11111ll1_opy_:
        regex = re.compile(bstack1l111l111_opy_)
        if regex.match(hostname):
            return True
    return False
def bstack11111llll1_opy_(bstack111l11111l_opy_, file_name, logger):
    bstack111l11111_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠪࢂࠬᐇ")), bstack111l11111l_opy_)
    try:
        if not os.path.exists(bstack111l11111_opy_):
            os.makedirs(bstack111l11111_opy_)
        file_path = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠫࢃ࠭ᐈ")), bstack111l11111l_opy_, file_name)
        if not os.path.isfile(file_path):
            with open(file_path, bstack1lll1l1_opy_ (u"ࠬࡽࠧᐉ")):
                pass
            with open(file_path, bstack1lll1l1_opy_ (u"ࠨࡷࠬࠤᐊ")) as outfile:
                json.dump({}, outfile)
        return file_path
    except Exception as e:
        logger.debug(bstack1l1ll111l_opy_.format(str(e)))
def bstack11111lll1l_opy_(file_name, key, value, logger):
    file_path = bstack11111llll1_opy_(bstack1lll1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᐋ"), file_name, logger)
    if file_path != None:
        if os.path.exists(file_path):
            bstack1l11111l11_opy_ = json.load(open(file_path, bstack1lll1l1_opy_ (u"ࠨࡴࡥࠫᐌ")))
        else:
            bstack1l11111l11_opy_ = {}
        bstack1l11111l11_opy_[key] = value
        with open(file_path, bstack1lll1l1_opy_ (u"ࠤࡺ࠯ࠧᐍ")) as outfile:
            json.dump(bstack1l11111l11_opy_, outfile)
def bstack11l1ll11l_opy_(file_name, logger):
    file_path = bstack11111llll1_opy_(bstack1lll1l1_opy_ (u"ࠪ࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࠪᐎ"), file_name, logger)
    bstack1l11111l11_opy_ = {}
    if file_path != None and os.path.exists(file_path):
        with open(file_path, bstack1lll1l1_opy_ (u"ࠫࡷ࠭ᐏ")) as bstack1lll11l111_opy_:
            bstack1l11111l11_opy_ = json.load(bstack1lll11l111_opy_)
    return bstack1l11111l11_opy_
def bstack1l11l1ll1_opy_(file_path, logger):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
    except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"ࠬࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡥࡧ࡯ࡩࡹ࡯࡮ࡨࠢࡩ࡭ࡱ࡫࠺ࠡࠩᐐ") + file_path + bstack1lll1l1_opy_ (u"࠭ࠠࠨᐑ") + str(e))
def bstack1l1l1l111_opy_():
    from selenium import webdriver
    return version.parse(webdriver.__version__)
class Notset:
    def __repr__(self):
        return bstack1lll1l1_opy_ (u"ࠢ࠽ࡐࡒࡘࡘࡋࡔ࠿ࠤᐒ")
def bstack111111lll_opy_(config):
    if bstack1lll1l1_opy_ (u"ࠨ࡫ࡶࡔࡱࡧࡹࡸࡴ࡬࡫࡭ࡺࠧᐓ") in config:
        del (config[bstack1lll1l1_opy_ (u"ࠩ࡬ࡷࡕࡲࡡࡺࡹࡵ࡭࡬࡮ࡴࠨᐔ")])
        return False
    if bstack1l1l1l111_opy_() < version.parse(bstack1lll1l1_opy_ (u"ࠪ࠷࠳࠺࠮࠱ࠩᐕ")):
        return False
    if bstack1l1l1l111_opy_() >= version.parse(bstack1lll1l1_opy_ (u"ࠫ࠹࠴࠱࠯࠷ࠪᐖ")):
        return True
    if bstack1lll1l1_opy_ (u"ࠬࡻࡳࡦ࡙࠶ࡇࠬᐗ") in config and config[bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧ࡚࠷ࡈ࠭ᐘ")] is False:
        return False
    else:
        return True
def bstack1l1l1l1lll_opy_(args_list, bstack11111l1ll1_opy_):
    index = -1
    for value in bstack11111l1ll1_opy_:
        try:
            index = args_list.index(value)
            return index
        except Exception as e:
            return index
    return index
class Result:
    def __init__(self, result=None, duration=None, exception=None, bstack11llll1ll1_opy_=None):
        self.result = result
        self.duration = duration
        self.exception = exception
        self.exception_type = type(self.exception).__name__ if exception else None
        self.bstack11llll1ll1_opy_ = bstack11llll1ll1_opy_
    @classmethod
    def passed(cls):
        return Result(result=bstack1lll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᐙ"))
    @classmethod
    def failed(cls, exception=None):
        return Result(result=bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᐚ"), exception=exception)
    def bstack11l11lll1l_opy_(self):
        if self.result != bstack1lll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᐛ"):
            return None
        if isinstance(self.exception_type, str) and bstack1lll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨᐜ") in self.exception_type:
            return bstack1lll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧᐝ")
        return bstack1lll1l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨᐞ")
    def bstack111111ll11_opy_(self):
        if self.result != bstack1lll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ᐟ"):
            return None
        if self.bstack11llll1ll1_opy_:
            return self.bstack11llll1ll1_opy_
        return bstack11111l1111_opy_(self.exception)
def bstack11111l1111_opy_(exc):
    return [traceback.format_exception(exc)]
def bstack111l11l1l1_opy_(message):
    if isinstance(message, str):
        return not bool(message and message.strip())
    return True
def bstack1llll1l1ll_opy_(object, key, default_value):
    if not object or not object.__dict__:
        return default_value
    if key in object.__dict__.keys():
        return object.__dict__.get(key)
    return default_value
def bstack1ll1l11lll_opy_(config, logger):
    try:
        import playwright
        bstack1111ll11ll_opy_ = playwright.__file__
        bstack111111l1ll_opy_ = os.path.split(bstack1111ll11ll_opy_)
        bstack111l1ll111_opy_ = bstack111111l1ll_opy_[0] + bstack1lll1l1_opy_ (u"ࠧ࠰ࡦࡵ࡭ࡻ࡫ࡲ࠰ࡲࡤࡧࡰࡧࡧࡦ࠱࡯࡭ࡧ࠵ࡣ࡭࡫࠲ࡧࡱ࡯࠮࡫ࡵࠪᐠ")
        os.environ[bstack1lll1l1_opy_ (u"ࠨࡉࡏࡓࡇࡇࡌࡠࡃࡊࡉࡓ࡚࡟ࡉࡖࡗࡔࡤࡖࡒࡐ࡚࡜ࠫᐡ")] = bstack1l1ll1ll11_opy_(config)
        with open(bstack111l1ll111_opy_, bstack1lll1l1_opy_ (u"ࠩࡵࠫᐢ")) as f:
            bstack1111l11l_opy_ = f.read()
            bstack1111lll1l1_opy_ = bstack1lll1l1_opy_ (u"ࠪ࡫ࡱࡵࡢࡢ࡮࠰ࡥ࡬࡫࡮ࡵࠩᐣ")
            bstack111l1l11l1_opy_ = bstack1111l11l_opy_.find(bstack1111lll1l1_opy_)
            if bstack111l1l11l1_opy_ == -1:
              process = subprocess.Popen(bstack1lll1l1_opy_ (u"ࠦࡳࡶ࡭ࠡ࡫ࡱࡷࡹࡧ࡬࡭ࠢࡪࡰࡴࡨࡡ࡭࠯ࡤ࡫ࡪࡴࡴࠣᐤ"), shell=True, cwd=bstack111111l1ll_opy_[0])
              process.wait()
              bstack1111l11l1l_opy_ = bstack1lll1l1_opy_ (u"ࠬࠨࡵࡴࡧࠣࡷࡹࡸࡩࡤࡶࠥ࠿ࠬᐥ")
              bstack111l1l1l11_opy_ = bstack1lll1l1_opy_ (u"ࠨࠢࠣࠢ࡟ࠦࡺࡹࡥࠡࡵࡷࡶ࡮ࡩࡴ࡝ࠤ࠾ࠤࡨࡵ࡮ࡴࡶࠣࡿࠥࡨ࡯ࡰࡶࡶࡸࡷࡧࡰࠡࡿࠣࡁࠥࡸࡥࡲࡷ࡬ࡶࡪ࠮ࠧࡨ࡮ࡲࡦࡦࡲ࠭ࡢࡩࡨࡲࡹ࠭ࠩ࠼ࠢ࡬ࡪࠥ࠮ࡰࡳࡱࡦࡩࡸࡹ࠮ࡦࡰࡹ࠲ࡌࡒࡏࡃࡃࡏࡣࡆࡍࡅࡏࡖࡢࡌ࡙࡚ࡐࡠࡒࡕࡓ࡝࡟ࠩࠡࡤࡲࡳࡹࡹࡴࡳࡣࡳࠬ࠮ࡁࠠࠣࠤࠥᐦ")
              bstack111l111l1l_opy_ = bstack1111l11l_opy_.replace(bstack1111l11l1l_opy_, bstack111l1l1l11_opy_)
              with open(bstack111l1ll111_opy_, bstack1lll1l1_opy_ (u"ࠧࡸࠩᐧ")) as f:
                f.write(bstack111l111l1l_opy_)
    except Exception as e:
        logger.error(bstack1llll11ll1_opy_.format(str(e)))
def bstack11l11111_opy_():
  try:
    bstack111l1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡳࡡ࡭ࡡ࡫ࡹࡧࡥࡵࡳ࡮࠱࡮ࡸࡵ࡮ࠨᐨ"))
    bstack11111l1l1l_opy_ = []
    if os.path.exists(bstack111l1l1111_opy_):
      with open(bstack111l1l1111_opy_) as f:
        bstack11111l1l1l_opy_ = json.load(f)
      os.remove(bstack111l1l1111_opy_)
    return bstack11111l1l1l_opy_
  except:
    pass
  return []
def bstack1l11llll11_opy_(bstack1lll1l1l1l_opy_):
  try:
    bstack11111l1l1l_opy_ = []
    bstack111l1l1111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡭ࡢ࡮ࡢ࡬ࡺࡨ࡟ࡶࡴ࡯࠲࡯ࡹ࡯࡯ࠩᐩ"))
    if os.path.exists(bstack111l1l1111_opy_):
      with open(bstack111l1l1111_opy_) as f:
        bstack11111l1l1l_opy_ = json.load(f)
    bstack11111l1l1l_opy_.append(bstack1lll1l1l1l_opy_)
    with open(bstack111l1l1111_opy_, bstack1lll1l1_opy_ (u"ࠪࡻࠬᐪ")) as f:
        json.dump(bstack11111l1l1l_opy_, f)
  except:
    pass
def bstack1l1l11l1l1_opy_(logger, bstack1111lll1ll_opy_ = False):
  try:
    test_name = os.environ.get(bstack1lll1l1_opy_ (u"ࠫࡕ࡟ࡔࡆࡕࡗࡣ࡙ࡋࡓࡕࡡࡑࡅࡒࡋࠧᐫ"), bstack1lll1l1_opy_ (u"ࠬ࠭ᐬ"))
    if test_name == bstack1lll1l1_opy_ (u"࠭ࠧᐭ"):
        test_name = threading.current_thread().__dict__.get(bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷࡩࡸࡺࡂࡥࡦࡢࡸࡪࡹࡴࡠࡰࡤࡱࡪ࠭ᐮ"), bstack1lll1l1_opy_ (u"ࠨࠩᐯ"))
    bstack1111l1l1l1_opy_ = bstack1lll1l1_opy_ (u"ࠩ࠯ࠤࠬᐰ").join(threading.current_thread().bstackTestErrorMessages)
    if bstack1111lll1ll_opy_:
        bstack111l1l11l_opy_ = os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡓࡐࡆ࡚ࡆࡐࡔࡐࡣࡎࡔࡄࡆ࡚ࠪᐱ"), bstack1lll1l1_opy_ (u"ࠫ࠵࠭ᐲ"))
        bstack1111l111_opy_ = {bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᐳ"): test_name, bstack1lll1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᐴ"): bstack1111l1l1l1_opy_, bstack1lll1l1_opy_ (u"ࠧࡪࡰࡧࡩࡽ࠭ᐵ"): bstack111l1l11l_opy_}
        bstack1111ll1lll_opy_ = []
        bstack1111lllll1_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࡠࡲࡳࡴࡤ࡫ࡲࡳࡱࡵࡣࡱ࡯ࡳࡵ࠰࡭ࡷࡴࡴࠧᐶ"))
        if os.path.exists(bstack1111lllll1_opy_):
            with open(bstack1111lllll1_opy_) as f:
                bstack1111ll1lll_opy_ = json.load(f)
        bstack1111ll1lll_opy_.append(bstack1111l111_opy_)
        with open(bstack1111lllll1_opy_, bstack1lll1l1_opy_ (u"ࠩࡺࠫᐷ")) as f:
            json.dump(bstack1111ll1lll_opy_, f)
    else:
        bstack1111l111_opy_ = {bstack1lll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨᐸ"): test_name, bstack1lll1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᐹ"): bstack1111l1l1l1_opy_, bstack1lll1l1_opy_ (u"ࠬ࡯࡮ࡥࡧࡻࠫᐺ"): str(multiprocessing.current_process().name)}
        if bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡥࡥࡳࡴࡲࡶࡤࡲࡩࡴࡶࠪᐻ") not in multiprocessing.current_process().__dict__.keys():
            multiprocessing.current_process().bstack_error_list = []
        multiprocessing.current_process().bstack_error_list.append(bstack1111l111_opy_)
  except Exception as e:
      logger.warn(bstack1lll1l1_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡷࡹࡵࡲࡦࠢࡳࡽࡹ࡫ࡳࡵࠢࡩࡹࡳࡴࡥ࡭ࠢࡧࡥࡹࡧ࠺ࠡࡽࢀࠦᐼ").format(e))
def bstack111ll111l_opy_(error_message, test_name, index, logger):
  try:
    bstack111l1lll11_opy_ = []
    bstack1111l111_opy_ = {bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᐽ"): test_name, bstack1lll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᐾ"): error_message, bstack1lll1l1_opy_ (u"ࠪ࡭ࡳࡪࡥࡹࠩᐿ"): index}
    bstack111l11l111_opy_ = os.path.join(tempfile.gettempdir(), bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࡢࡩࡷࡸ࡯ࡳࡡ࡯࡭ࡸࡺ࠮࡫ࡵࡲࡲࠬᑀ"))
    if os.path.exists(bstack111l11l111_opy_):
        with open(bstack111l11l111_opy_) as f:
            bstack111l1lll11_opy_ = json.load(f)
    bstack111l1lll11_opy_.append(bstack1111l111_opy_)
    with open(bstack111l11l111_opy_, bstack1lll1l1_opy_ (u"ࠬࡽࠧᑁ")) as f:
        json.dump(bstack111l1lll11_opy_, f)
  except Exception as e:
    logger.warn(bstack1lll1l1_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡶࡸࡴࡸࡥࠡࡴࡲࡦࡴࡺࠠࡧࡷࡱࡲࡪࡲࠠࡥࡣࡷࡥ࠿ࠦࡻࡾࠤᑂ").format(e))
def bstack1lllll1ll_opy_(bstack1lllll11l_opy_, name, logger):
  try:
    bstack1111l111_opy_ = {bstack1lll1l1_opy_ (u"ࠧ࡯ࡣࡰࡩࠬᑃ"): name, bstack1lll1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᑄ"): bstack1lllll11l_opy_, bstack1lll1l1_opy_ (u"ࠩ࡬ࡲࡩ࡫ࡸࠨᑅ"): str(threading.current_thread()._name)}
    return bstack1111l111_opy_
  except Exception as e:
    logger.warn(bstack1lll1l1_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡳࡵࡱࡵࡩࠥࡨࡥࡩࡣࡹࡩࠥ࡬ࡵ࡯ࡰࡨࡰࠥࡪࡡࡵࡣ࠽ࠤࢀࢃࠢᑆ").format(e))
  return
def bstack111l111l11_opy_():
    return platform.system() == bstack1lll1l1_opy_ (u"ࠫ࡜࡯࡮ࡥࡱࡺࡷࠬᑇ")
def bstack1lll1l1lll_opy_(bstack1111ll1111_opy_, config, logger):
    bstack1111l1l11l_opy_ = {}
    try:
        return {key: config[key] for key in config if bstack1111ll1111_opy_.match(key)}
    except Exception as e:
        logger.debug(bstack1lll1l1_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡨ࡬ࡰࡹ࡫ࡲࠡࡥࡲࡲ࡫࡯ࡧࠡ࡭ࡨࡽࡸࠦࡢࡺࠢࡵࡩ࡬࡫ࡸࠡ࡯ࡤࡸࡨ࡮࠺ࠡࡽࢀࠦᑈ").format(e))
    return bstack1111l1l11l_opy_
def bstack111l1l11ll_opy_(bstack1111l11lll_opy_, bstack111111l11l_opy_):
    bstack111l111lll_opy_ = version.parse(bstack1111l11lll_opy_)
    bstack1111l11l11_opy_ = version.parse(bstack111111l11l_opy_)
    if bstack111l111lll_opy_ > bstack1111l11l11_opy_:
        return 1
    elif bstack111l111lll_opy_ < bstack1111l11l11_opy_:
        return -1
    else:
        return 0
def bstack11ll11l11l_opy_():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
def bstack111l11ll11_opy_(timestamp):
    return datetime.datetime.fromtimestamp(timestamp, datetime.timezone.utc).replace(tzinfo=None)
def bstack11111l11l1_opy_(framework):
    from browserstack_sdk._version import __version__
    return str(framework) + str(__version__)
def bstack1l1l1l1l1l_opy_(options, framework):
    if options is None:
        return
    if getattr(options, bstack1lll1l1_opy_ (u"࠭ࡧࡦࡶࠪᑉ"), None):
        caps = options
    else:
        caps = options.to_capabilities()
    bstack11llll1ll_opy_ = caps.get(bstack1lll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑊ"))
    bstack1111llll1l_opy_ = True
    if bstack11111ll111_opy_(caps.get(bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡶࡵࡨ࡛࠸ࡉࠧᑋ"))) or bstack11111ll111_opy_(caps.get(bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩᑌ"))):
        bstack1111llll1l_opy_ = False
    if bstack111111lll_opy_({bstack1lll1l1_opy_ (u"ࠥࡹࡸ࡫ࡗ࠴ࡅࠥᑍ"): bstack1111llll1l_opy_}):
        bstack11llll1ll_opy_ = bstack11llll1ll_opy_ or {}
        bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑎ")] = bstack11111l11l1_opy_(framework)
        bstack11llll1ll_opy_[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑏ")] = bstack111111l1l1_opy_()
        if getattr(options, bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹࡿࠧᑐ"), None):
            options.set_capability(bstack1lll1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᑑ"), bstack11llll1ll_opy_)
        else:
            options[bstack1lll1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᑒ")] = bstack11llll1ll_opy_
    else:
        if getattr(options, bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵࡻࠪᑓ"), None):
            options.set_capability(bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡔࡆࡎࠫᑔ"), bstack11111l11l1_opy_(framework))
            options.set_capability(bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᑕ"), bstack111111l1l1_opy_())
        else:
            options[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡖࡈࡐ࠭ᑖ")] = bstack11111l11l1_opy_(framework)
            options[bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᑗ")] = bstack111111l1l1_opy_()
    return options
def bstack111l1111l1_opy_(bstack11111l1lll_opy_, framework):
    if bstack11111l1lll_opy_ and len(bstack11111l1lll_opy_.split(bstack1lll1l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᑘ"))) > 1:
        ws_url = bstack11111l1lll_opy_.split(bstack1lll1l1_opy_ (u"ࠨࡥࡤࡴࡸࡃࠧᑙ"))[0]
        if bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱࠬᑚ") in ws_url:
            from browserstack_sdk._version import __version__
            bstack111l11lll1_opy_ = json.loads(urllib.parse.unquote(bstack11111l1lll_opy_.split(bstack1lll1l1_opy_ (u"ࠪࡧࡦࡶࡳ࠾ࠩᑛ"))[1]))
            bstack111l11lll1_opy_ = bstack111l11lll1_opy_ or {}
            bstack111l11lll1_opy_[bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬᑜ")] = str(framework) + str(__version__)
            bstack111l11lll1_opy_[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᑝ")] = bstack111111l1l1_opy_()
            bstack11111l1lll_opy_ = bstack11111l1lll_opy_.split(bstack1lll1l1_opy_ (u"࠭ࡣࡢࡲࡶࡁࠬᑞ"))[0] + bstack1lll1l1_opy_ (u"ࠧࡤࡣࡳࡷࡂ࠭ᑟ") + urllib.parse.quote(json.dumps(bstack111l11lll1_opy_))
    return bstack11111l1lll_opy_
def bstack1ll111111_opy_():
    global bstack1lllllll1_opy_
    from playwright._impl._browser_type import BrowserType
    bstack1lllllll1_opy_ = BrowserType.connect
    return bstack1lllllll1_opy_
def bstack1ll111ll1l_opy_(framework_name):
    global bstack1l111llll_opy_
    bstack1l111llll_opy_ = framework_name
    return framework_name
def bstack11llll11l_opy_(self, *args, **kwargs):
    global bstack1lllllll1_opy_
    try:
        global bstack1l111llll_opy_
        if bstack1lll1l1_opy_ (u"ࠨࡹࡶࡉࡳࡪࡰࡰ࡫ࡱࡸࠬᑠ") in kwargs:
            kwargs[bstack1lll1l1_opy_ (u"ࠩࡺࡷࡊࡴࡤࡱࡱ࡬ࡲࡹ࠭ᑡ")] = bstack111l1111l1_opy_(
                kwargs.get(bstack1lll1l1_opy_ (u"ࠪࡻࡸࡋ࡮ࡥࡲࡲ࡭ࡳࡺࠧᑢ"), None),
                bstack1l111llll_opy_
            )
    except Exception as e:
        logger.error(bstack1lll1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡫࡮ࠡࡲࡵࡳࡨ࡫ࡳࡴ࡫ࡱ࡫࡙ࠥࡄࡌࠢࡦࡥࡵࡹ࠺ࠡࡽࢀࠦᑣ").format(str(e)))
    return bstack1lllllll1_opy_(self, *args, **kwargs)
def bstack111l111ll1_opy_(bstack111l1lll1l_opy_, proxies):
    proxy_settings = {}
    try:
        if not proxies:
            proxies = bstack111111ll1_opy_(bstack111l1lll1l_opy_, bstack1lll1l1_opy_ (u"ࠧࠨᑤ"))
        if proxies and proxies.get(bstack1lll1l1_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᑥ")):
            parsed_url = urlparse(proxies.get(bstack1lll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᑦ")))
            if parsed_url and parsed_url.hostname: proxy_settings[bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡈࡰࡵࡷࠫᑧ")] = str(parsed_url.hostname)
            if parsed_url and parsed_url.port: proxy_settings[bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᑨ")] = str(parsed_url.port)
            if parsed_url and parsed_url.username: proxy_settings[bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡗࡶࡩࡷ࠭ᑩ")] = str(parsed_url.username)
            if parsed_url and parsed_url.password: proxy_settings[bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡓࡥࡸࡹࠧᑪ")] = str(parsed_url.password)
        return proxy_settings
    except:
        return proxy_settings
def bstack1l1l11lll_opy_(bstack111l1lll1l_opy_):
    bstack1111ll11l1_opy_ = {
        bstack111l1llll1_opy_[bstack111l1ll1l1_opy_]: bstack111l1lll1l_opy_[bstack111l1ll1l1_opy_]
        for bstack111l1ll1l1_opy_ in bstack111l1lll1l_opy_
        if bstack111l1ll1l1_opy_ in bstack111l1llll1_opy_
    }
    bstack1111ll11l1_opy_[bstack1lll1l1_opy_ (u"ࠧࡶࡲࡰࡺࡼࡗࡪࡺࡴࡪࡰࡪࡷࠧᑫ")] = bstack111l111ll1_opy_(bstack111l1lll1l_opy_, bstack1lll11l1ll_opy_.get_property(bstack1lll1l1_opy_ (u"ࠨࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸࠨᑬ")))
    bstack1111l1l111_opy_ = [element.lower() for element in bstack111ll11lll_opy_]
    bstack111l1ll11l_opy_(bstack1111ll11l1_opy_, bstack1111l1l111_opy_)
    return bstack1111ll11l1_opy_
def bstack111l1ll11l_opy_(d, keys):
    for key in list(d.keys()):
        if key.lower() in keys:
            d[key] = bstack1lll1l1_opy_ (u"ࠢࠫࠬ࠭࠮ࠧᑭ")
    for value in d.values():
        if isinstance(value, dict):
            bstack111l1ll11l_opy_(value, keys)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    bstack111l1ll11l_opy_(item, keys)