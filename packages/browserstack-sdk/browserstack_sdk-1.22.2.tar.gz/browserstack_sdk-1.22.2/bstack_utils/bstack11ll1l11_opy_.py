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
from collections import deque
from bstack_utils.constants import *
class bstack1l11l11l1l_opy_:
    def __init__(self):
        self._1lll1ll1111_opy_ = deque()
        self._1lll1l1l1l1_opy_ = {}
        self._1lll1l1lll1_opy_ = False
    def bstack1lll1l1ll1l_opy_(self, test_name, bstack1lll1l11l1l_opy_):
        bstack1lll1l1l111_opy_ = self._1lll1l1l1l1_opy_.get(test_name, {})
        return bstack1lll1l1l111_opy_.get(bstack1lll1l11l1l_opy_, 0)
    def bstack1lll1l111ll_opy_(self, test_name, bstack1lll1l11l1l_opy_):
        bstack1lll1l1l1ll_opy_ = self.bstack1lll1l1ll1l_opy_(test_name, bstack1lll1l11l1l_opy_)
        self.bstack1lll1ll111l_opy_(test_name, bstack1lll1l11l1l_opy_)
        return bstack1lll1l1l1ll_opy_
    def bstack1lll1ll111l_opy_(self, test_name, bstack1lll1l11l1l_opy_):
        if test_name not in self._1lll1l1l1l1_opy_:
            self._1lll1l1l1l1_opy_[test_name] = {}
        bstack1lll1l1l111_opy_ = self._1lll1l1l1l1_opy_[test_name]
        bstack1lll1l1l1ll_opy_ = bstack1lll1l1l111_opy_.get(bstack1lll1l11l1l_opy_, 0)
        bstack1lll1l1l111_opy_[bstack1lll1l11l1l_opy_] = bstack1lll1l1l1ll_opy_ + 1
    def bstack11ll111l1_opy_(self, bstack1lll1l1l11l_opy_, bstack1lll1l11ll1_opy_):
        bstack1lll1l1llll_opy_ = self.bstack1lll1l111ll_opy_(bstack1lll1l1l11l_opy_, bstack1lll1l11ll1_opy_)
        bstack1lll1l11l11_opy_ = bstack111ll111ll_opy_[bstack1lll1l11ll1_opy_]
        bstack1lll1l11lll_opy_ = bstack1lll1l1_opy_ (u"ࠦࢀࢃ࠭ࡼࡿ࠰ࡿࢂࠨᕻ").format(bstack1lll1l1l11l_opy_, bstack1lll1l11l11_opy_, bstack1lll1l1llll_opy_)
        self._1lll1ll1111_opy_.append(bstack1lll1l11lll_opy_)
    def bstack1ll111l1_opy_(self):
        return len(self._1lll1ll1111_opy_) == 0
    def bstack1l11l1l11l_opy_(self):
        bstack1lll1l1ll11_opy_ = self._1lll1ll1111_opy_.popleft()
        return bstack1lll1l1ll11_opy_
    def capturing(self):
        return self._1lll1l1lll1_opy_
    def bstack11lll11l1_opy_(self):
        self._1lll1l1lll1_opy_ = True
    def bstack11ll1lll_opy_(self):
        self._1lll1l1lll1_opy_ = False