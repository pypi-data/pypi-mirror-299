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
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l111l111_opy_, bstack1llll1111_opy_, get_host_info, bstack1111llllll_opy_, \
 bstack1l1111ll11_opy_, bstack1llll1l1ll_opy_, bstack11ll111ll1_opy_, bstack11111ll1l1_opy_, bstack1l11lll111_opy_
import bstack_utils.bstack1l1l1ll1ll_opy_ as bstack1111ll1l_opy_
from bstack_utils.bstack1l1llll1ll_opy_ import bstack1llllll1ll_opy_
from bstack_utils.percy import bstack1ll111l1l1_opy_
from bstack_utils.config import Config
bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
logger = logging.getLogger(__name__)
percy = bstack1ll111l1l1_opy_()
@bstack11ll111ll1_opy_(class_method=False)
def bstack1ll1l1lll11_opy_(bs_config, bstack1l11llll1_opy_):
  try:
    data = {
        bstack1lll1l1_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧᜰ"): bstack1lll1l1_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭ᜱ"),
        bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨᜲ"): bs_config.get(bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᜳ"), bstack1lll1l1_opy_ (u"᜴ࠫࠬ")),
        bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ᜵"): bs_config.get(bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ᜶"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᜷"): bs_config.get(bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ᜸")),
        bstack1lll1l1_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ᜹"): bs_config.get(bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᜺"), bstack1lll1l1_opy_ (u"ࠫࠬ᜻")),
        bstack1lll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ᜼"): bstack1l11lll111_opy_(),
        bstack1lll1l1_opy_ (u"࠭ࡴࡢࡩࡶࠫ᜽"): bstack1111llllll_opy_(bs_config),
        bstack1lll1l1_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ᜾"): get_host_info(),
        bstack1lll1l1_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ᜿"): bstack1llll1111_opy_(),
        bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᝀ"): os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩᝁ")),
        bstack1lll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩᝂ"): os.environ.get(bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪᝃ"), False),
        bstack1lll1l1_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨᝄ"): bstack11l111l111_opy_(),
        bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᝅ"): bstack1ll1l111ll1_opy_(),
        bstack1lll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬᝆ"): bstack1ll1l1111ll_opy_(bstack1l11llll1_opy_),
        bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧᝇ"): bstack11l11l11_opy_(bs_config, bstack1l11llll1_opy_.get(bstack1lll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫᝈ"), bstack1lll1l1_opy_ (u"ࠫࠬᝉ"))),
        bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧᝊ"): bstack1l1111ll11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1lll1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢᝋ").format(str(error)))
    return None
def bstack1ll1l1111ll_opy_(framework):
  return {
    bstack1lll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᝌ"): framework.get(bstack1lll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩᝍ"), bstack1lll1l1_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩᝎ")),
    bstack1lll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝏ"): framework.get(bstack1lll1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᝐ")),
    bstack1lll1l1_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᝑ"): framework.get(bstack1lll1l1_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫᝒ")),
    bstack1lll1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᝓ"): bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᝔"),
    bstack1lll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᝕"): framework.get(bstack1lll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ᝖"))
  }
def bstack11l11l11_opy_(bs_config, framework):
  bstack1l11l1l111_opy_ = False
  bstack1l111l11ll_opy_ = False
  if bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰࠨ᝗") in bs_config:
    bstack1l11l1l111_opy_ = True
  else:
    bstack1l111l11ll_opy_ = True
  bstack1l1l1l1ll_opy_ = {
    bstack1lll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ᝘"): bstack1llllll1ll_opy_.bstack1ll1l11111l_opy_(bs_config, framework),
    bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᝙"): bstack1111ll1l_opy_.bstack11l11ll11l_opy_(bs_config),
    bstack1lll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭᝚"): bs_config.get(bstack1lll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ᝛"), False),
    bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ᝜"): bstack1l111l11ll_opy_,
    bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ᝝"): bstack1l11l1l111_opy_
  }
  return bstack1l1l1l1ll_opy_
@bstack11ll111ll1_opy_(class_method=False)
def bstack1ll1l111ll1_opy_():
  try:
    bstack1ll11lllll1_opy_ = json.loads(os.getenv(bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᝞"), bstack1lll1l1_opy_ (u"ࠬࢁࡽࠨ᝟")))
    return {
        bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᝠ"): bstack1ll11lllll1_opy_
    }
  except Exception as error:
    logger.error(bstack1lll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨᝡ").format(str(error)))
    return {}
def bstack1ll1l11l1l1_opy_(array, bstack1ll11llll1l_opy_, bstack1ll11llllll_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll11llll1l_opy_]
    result[key] = o[bstack1ll11llllll_opy_]
  return result
def bstack1ll1l11llll_opy_(bstack1lll11ll_opy_=bstack1lll1l1_opy_ (u"ࠨࠩᝢ")):
  bstack1ll1l1111l1_opy_ = bstack1111ll1l_opy_.on()
  bstack1ll1l111l11_opy_ = bstack1llllll1ll_opy_.on()
  bstack1ll1l111l1l_opy_ = percy.bstack11llll1l1_opy_()
  if bstack1ll1l111l1l_opy_ and not bstack1ll1l111l11_opy_ and not bstack1ll1l1111l1_opy_:
    return bstack1lll11ll_opy_ not in [bstack1lll1l1_opy_ (u"ࠩࡆࡆ࡙࡙ࡥࡴࡵ࡬ࡳࡳࡉࡲࡦࡣࡷࡩࡩ࠭ᝣ"), bstack1lll1l1_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧᝤ")]
  elif bstack1ll1l1111l1_opy_ and not bstack1ll1l111l11_opy_:
    return bstack1lll11ll_opy_ not in [bstack1lll1l1_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡘࡺࡡࡳࡶࡨࡨࠬᝥ"), bstack1lll1l1_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧᝦ"), bstack1lll1l1_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪᝧ")]
  return bstack1ll1l1111l1_opy_ or bstack1ll1l111l11_opy_ or bstack1ll1l111l1l_opy_
@bstack11ll111ll1_opy_(class_method=False)
def bstack1ll1l111lll_opy_(bstack1lll11ll_opy_, test=None):
  bstack1ll1l111111_opy_ = bstack1111ll1l_opy_.on()
  if not bstack1ll1l111111_opy_ or bstack1lll11ll_opy_ not in [bstack1lll1l1_opy_ (u"ࠧࡕࡧࡶࡸࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩᝨ")] or test == None:
    return None
  return {
    bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᝩ"): bstack1ll1l111111_opy_ and bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡤ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᝪ"), None) == True and bstack1111ll1l_opy_.bstack1lllll11ll_opy_(test[bstack1lll1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨᝫ")])
  }