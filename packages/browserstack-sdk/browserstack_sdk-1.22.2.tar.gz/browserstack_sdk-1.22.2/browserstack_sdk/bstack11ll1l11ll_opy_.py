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
class RobotHandler():
    def __init__(self, args, logger, bstack11l1l1111l_opy_, bstack11l1l1l11l_opy_):
        self.args = args
        self.logger = logger
        self.bstack11l1l1111l_opy_ = bstack11l1l1111l_opy_
        self.bstack11l1l1l11l_opy_ = bstack11l1l1l11l_opy_
    @staticmethod
    def version():
        import robot
        return robot.__version__
    @staticmethod
    def bstack11ll111l11_opy_(bstack11l11ll1l1_opy_):
        bstack11l11ll1ll_opy_ = []
        if bstack11l11ll1l1_opy_:
            tokens = str(os.path.basename(bstack11l11ll1l1_opy_)).split(bstack1lll1l1_opy_ (u"ࠣࡡࠥ໶"))
            camelcase_name = bstack1lll1l1_opy_ (u"ࠤࠣࠦ໷").join(t.title() for t in tokens)
            suite_name, bstack11l11lll11_opy_ = os.path.splitext(camelcase_name)
            bstack11l11ll1ll_opy_.append(suite_name)
        return bstack11l11ll1ll_opy_
    @staticmethod
    def bstack11l11lll1l_opy_(typename):
        if bstack1lll1l1_opy_ (u"ࠥࡅࡸࡹࡥࡳࡶ࡬ࡳࡳࠨ໸") in typename:
            return bstack1lll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࡅࡳࡴࡲࡶࠧ໹")
        return bstack1lll1l1_opy_ (u"࡛ࠧ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡆࡴࡵࡳࡷࠨ໺")