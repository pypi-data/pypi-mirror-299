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
import sys
class bstack11lll1l1ll_opy_:
    def __init__(self, handler):
        self._111lll11ll_opy_ = sys.stdout.write
        self._111lll1111_opy_ = sys.stderr.write
        self.handler = handler
        self._started = False
    def start(self):
        if self._started:
            return
        self._started = True
        sys.stdout.write = self.bstack111lll11l1_opy_
        sys.stdout.error = self.bstack111lll111l_opy_
    def bstack111lll11l1_opy_(self, _str):
        self._111lll11ll_opy_(_str)
        if self.handler:
            self.handler({bstack1lll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫ࿅"): bstack1lll1l1_opy_ (u"࠭ࡉࡏࡈࡒ࿆ࠫ"), bstack1lll1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ࿇"): _str})
    def bstack111lll111l_opy_(self, _str):
        self._111lll1111_opy_(_str)
        if self.handler:
            self.handler({bstack1lll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ࿈"): bstack1lll1l1_opy_ (u"ࠩࡈࡖࡗࡕࡒࠨ࿉"), bstack1lll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ࿊"): _str})
    def reset(self):
        if not self._started:
            return
        self._started = False
        sys.stdout.write = self._111lll11ll_opy_
        sys.stderr.write = self._111lll1111_opy_