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
import threading
import logging
import bstack_utils.bstack1l1l1ll1ll_opy_ as bstack1111ll1l_opy_
from bstack_utils.helper import bstack1llll1l1ll_opy_
logger = logging.getLogger(__name__)
def bstack1l1llll11l_opy_(key_name):
  return True if key_name in threading.current_thread().__dict__.keys() else False
def bstack1111l111l_opy_(context, *args):
    tags = getattr(args[0], bstack1lll1l1_opy_ (u"ࠪࡸࡦ࡭ࡳࠨྼ"), [])
    bstack1l1lll1l1_opy_ = bstack1111ll1l_opy_.bstack1lllll11ll_opy_(tags)
    threading.current_thread().isA11yTest = bstack1l1lll1l1_opy_
    try:
      bstack1l1111l11_opy_ = threading.current_thread().bstackSessionDriver if bstack1l1llll11l_opy_(bstack1lll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡗࡪࡹࡳࡪࡱࡱࡈࡷ࡯ࡶࡦࡴࠪ྽")) else context.browser
      if bstack1l1111l11_opy_ and bstack1l1111l11_opy_.session_id and bstack1l1lll1l1_opy_ and bstack1llll1l1ll_opy_(
              threading.current_thread(), bstack1lll1l1_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ྾"), None):
          threading.current_thread().isA11yTest = bstack1111ll1l_opy_.bstack1l111l1l1l_opy_(bstack1l1111l11_opy_, bstack1l1lll1l1_opy_)
    except Exception as e:
       logger.debug(bstack1lll1l1_opy_ (u"࠭ࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢࡶࡸࡦࡸࡴࠡࡣ࠴࠵ࡾࠦࡩ࡯ࠢࡥࡩ࡭ࡧࡶࡦ࠼ࠣࡿࢂ࠭྿").format(str(e)))
def bstack11111ll1l_opy_(bstack1l1111l11_opy_):
    if bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠧࡪࡵࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ࿀"), None) and bstack1llll1l1ll_opy_(
      threading.current_thread(), bstack1lll1l1_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ࿁"), None) and not bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡤ࠵࠶ࡿ࡟ࡴࡶࡲࡴࠬ࿂"), False):
      threading.current_thread().a11y_stop = True
      bstack1111ll1l_opy_.bstack11ll1l111_opy_(bstack1l1111l11_opy_, name=bstack1lll1l1_opy_ (u"ࠥࠦ࿃"), path=bstack1lll1l1_opy_ (u"ࠦࠧ࿄"))