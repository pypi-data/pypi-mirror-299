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
class bstack1l11l1lll1_opy_:
    def __init__(self, handler):
        self._1lll111111l_opy_ = None
        self.handler = handler
        self._1ll1lllllll_opy_ = self.bstack1lll1111111_opy_()
        self.patch()
    def patch(self):
        self._1lll111111l_opy_ = self._1ll1lllllll_opy_.execute
        self._1ll1lllllll_opy_.execute = self.bstack1ll1llllll1_opy_()
    def bstack1ll1llllll1_opy_(self):
        def execute(this, driver_command, *args, **kwargs):
            self.handler(bstack1lll1l1_opy_ (u"ࠥࡦࡪ࡬࡯ࡳࡧࠥᗕ"), driver_command, None, this, args)
            response = self._1lll111111l_opy_(this, driver_command, *args, **kwargs)
            self.handler(bstack1lll1l1_opy_ (u"ࠦࡦ࡬ࡴࡦࡴࠥᗖ"), driver_command, response)
            return response
        return execute
    def reset(self):
        self._1ll1lllllll_opy_.execute = self._1lll111111l_opy_
    @staticmethod
    def bstack1lll1111111_opy_():
        from selenium.webdriver.remote.webdriver import WebDriver
        return WebDriver