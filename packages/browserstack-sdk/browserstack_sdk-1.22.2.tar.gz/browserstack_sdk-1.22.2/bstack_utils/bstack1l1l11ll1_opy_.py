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
from browserstack_sdk.bstack1111ll1l1_opy_ import bstack1lll1l111_opy_
from browserstack_sdk.bstack11ll1l11ll_opy_ import RobotHandler
def bstack1lll111l11_opy_(framework):
    if framework.lower() == bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶࠪኢ"):
        return bstack1lll1l111_opy_.version()
    elif framework.lower() == bstack1lll1l1_opy_ (u"ࠫࡷࡵࡢࡰࡶࠪኣ"):
        return RobotHandler.version()
    elif framework.lower() == bstack1lll1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬኤ"):
        import behave
        return behave.__version__
    else:
        return bstack1lll1l1_opy_ (u"࠭ࡵ࡯࡭ࡱࡳࡼࡴࠧእ")