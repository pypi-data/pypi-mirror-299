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
import json
import logging
import os
import datetime
import threading
from bstack_utils.helper import bstack11l111111l_opy_, bstack111llllll1_opy_, bstack1l1ll1l11_opy_, bstack11ll111ll1_opy_, bstack1111ll1l1l_opy_, bstack1111l111l1_opy_, bstack11111ll1l1_opy_, bstack1l11lll111_opy_
from bstack_utils.bstack1lll111ll1l_opy_ import bstack1lll11111l1_opy_
import bstack_utils.bstack1llll1l11l_opy_ as bstack1ll1l1111_opy_
from bstack_utils.bstack1l1llll1ll_opy_ import bstack1llllll1ll_opy_
import bstack_utils.bstack1l1l1ll1ll_opy_ as bstack1111ll1l_opy_
from bstack_utils.bstack1l1lllllll_opy_ import bstack1l1lllllll_opy_
from bstack_utils.bstack11lll1ll1l_opy_ import bstack11ll11111l_opy_
bstack1ll1ll11ll1_opy_ = bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡦࡳࡱࡲࡥࡤࡶࡲࡶ࠲ࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭ࠨᙊ")
logger = logging.getLogger(__name__)
class bstack1l1lll1lll_opy_:
    bstack1lll111ll1l_opy_ = None
    bs_config = None
    bstack1l11llll1_opy_ = None
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def launch(cls, bs_config, bstack1l11llll1_opy_):
        cls.bs_config = bs_config
        cls.bstack1l11llll1_opy_ = bstack1l11llll1_opy_
        try:
            cls.bstack1ll1ll11111_opy_()
            bstack11l11111l1_opy_ = bstack11l111111l_opy_(bs_config)
            bstack11l1111111_opy_ = bstack111llllll1_opy_(bs_config)
            data = bstack1ll1l1111_opy_.bstack1ll1l1lll11_opy_(bs_config, bstack1l11llll1_opy_)
            config = {
                bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᙋ"): (bstack11l11111l1_opy_, bstack11l1111111_opy_),
                bstack1lll1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᙌ"): cls.default_headers()
            }
            response = bstack1l1ll1l11_opy_(bstack1lll1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩᙍ"), cls.request_url(bstack1lll1l1_opy_ (u"ࠬࡧࡰࡪ࠱ࡹ࠶࠴ࡨࡵࡪ࡮ࡧࡷࠬᙎ")), data, config)
            if response.status_code != 200:
                bstack1ll1l1lll1l_opy_ = response.json()
                if bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᙏ")] == False:
                    cls.bstack1ll1ll11l11_opy_(bstack1ll1l1lll1l_opy_)
                    return
                cls.bstack1ll1l1l1ll1_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᙐ")])
                cls.bstack1ll1l11ll1l_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙑ")])
                return None
            bstack1ll1l1llll1_opy_ = cls.bstack1ll1l1l1111_opy_(response)
            return bstack1ll1l1llll1_opy_
        except Exception as error:
            logger.error(bstack1lll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡢࡶ࡫࡯ࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࢀࢃࠢᙒ").format(str(error)))
            return None
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def stop(cls, bstack1ll1l1l11l1_opy_=None):
        if not bstack1llllll1ll_opy_.on() and not bstack1111ll1l_opy_.on():
            return
        if os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᙓ")) == bstack1lll1l1_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᙔ") or os.environ.get(bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᙕ")) == bstack1lll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᙖ"):
            logger.error(bstack1lll1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡱࡳࠤࡧࡻࡩ࡭ࡦࠣࡶࡪࡷࡵࡦࡵࡷࠤࡹࡵࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᙗ"))
            return {
                bstack1lll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙘ"): bstack1lll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᙙ"),
                bstack1lll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙚ"): bstack1lll1l1_opy_ (u"࡙ࠫࡵ࡫ࡦࡰ࠲ࡦࡺ࡯࡬ࡥࡋࡇࠤ࡮ࡹࠠࡶࡰࡧࡩ࡫࡯࡮ࡦࡦ࠯ࠤࡧࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥࡳࡩࡨࡪࡷࠤ࡭ࡧࡶࡦࠢࡩࡥ࡮ࡲࡥࡥࠩᙛ")
            }
        try:
            cls.bstack1lll111ll1l_opy_.shutdown()
            data = {
                bstack1lll1l1_opy_ (u"ࠬ࡬ࡩ࡯࡫ࡶ࡬ࡪࡪ࡟ࡢࡶࠪᙜ"): bstack1l11lll111_opy_()
            }
            if not bstack1ll1l1l11l1_opy_ is None:
                data[bstack1lll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠ࡯ࡨࡸࡦࡪࡡࡵࡣࠪᙝ")] = [{
                    bstack1lll1l1_opy_ (u"ࠧࡳࡧࡤࡷࡴࡴࠧᙞ"): bstack1lll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡥ࡫ࡪ࡮࡯ࡩࡩ࠭ᙟ"),
                    bstack1lll1l1_opy_ (u"ࠩࡶ࡭࡬ࡴࡡ࡭ࠩᙠ"): bstack1ll1l1l11l1_opy_
                }]
            config = {
                bstack1lll1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᙡ"): cls.default_headers()
            }
            bstack1111l11111_opy_ = bstack1lll1l1_opy_ (u"ࠫࡦࡶࡩ࠰ࡸ࠴࠳ࡧࡻࡩ࡭ࡦࡶ࠳ࢀࢃ࠯ࡴࡶࡲࡴࠬᙢ").format(os.environ[bstack1lll1l1_opy_ (u"ࠧࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠥᙣ")])
            bstack1ll1l1l11ll_opy_ = cls.request_url(bstack1111l11111_opy_)
            response = bstack1l1ll1l11_opy_(bstack1lll1l1_opy_ (u"࠭ࡐࡖࡖࠪᙤ"), bstack1ll1l1l11ll_opy_, data, config)
            if not response.ok:
                raise Exception(bstack1lll1l1_opy_ (u"ࠢࡔࡶࡲࡴࠥࡸࡥࡲࡷࡨࡷࡹࠦ࡮ࡰࡶࠣࡳࡰࠨᙥ"))
        except Exception as error:
            logger.error(bstack1lll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡲࡴࠥࡨࡵࡪ࡮ࡧࠤࡷ࡫ࡱࡶࡧࡶࡸࠥࡺ࡯ࠡࡖࡨࡷࡹࡎࡵࡣ࠼࠽ࠤࠧᙦ") + str(error))
            return {
                bstack1lll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᙧ"): bstack1lll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙨ"),
                bstack1lll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙩ"): str(error)
            }
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1ll1l1l1111_opy_(cls, response):
        bstack1ll1l1lll1l_opy_ = response.json()
        bstack1ll1l1llll1_opy_ = {}
        if bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠬࡰࡷࡵࠩᙪ")) is None:
            os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙫ")] = bstack1lll1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᙬ")
        else:
            os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ᙭")] = bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠩ࡭ࡻࡹ࠭᙮"), bstack1lll1l1_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᙯ"))
        os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᙰ")] = bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡭ࡧࡳࡩࡧࡧࡣ࡮ࡪࠧᙱ"), bstack1lll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᙲ"))
        if bstack1llllll1ll_opy_.bstack1ll1l1ll1ll_opy_(cls.bs_config, cls.bstack1l11llll1_opy_.get(bstack1lll1l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡹࡸ࡫ࡤࠨᙳ"), bstack1lll1l1_opy_ (u"ࠨࠩᙴ"))) is True:
            bstack1ll1l1l1l11_opy_, bstack1ll1l11ll11_opy_, bstack1ll1l1l1l1l_opy_ = cls.bstack1ll1l1lllll_opy_(bstack1ll1l1lll1l_opy_)
            if bstack1ll1l1l1l11_opy_ != None and bstack1ll1l11ll11_opy_ != None:
                bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩᙵ")] = {
                    bstack1lll1l1_opy_ (u"ࠪ࡮ࡼࡺ࡟ࡵࡱ࡮ࡩࡳ࠭ᙶ"): bstack1ll1l1l1l11_opy_,
                    bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᙷ"): bstack1ll1l11ll11_opy_,
                    bstack1lll1l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡣࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡴࠩᙸ"): bstack1ll1l1l1l1l_opy_
                }
            else:
                bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᙹ")] = {}
        else:
            bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᙺ")] = {}
        if bstack1111ll1l_opy_.bstack11l11ll11l_opy_(cls.bs_config) is True:
            bstack1ll1l1ll11l_opy_, bstack1ll1l11ll11_opy_ = cls.bstack1ll1l11l11l_opy_(bstack1ll1l1lll1l_opy_)
            if bstack1ll1l1ll11l_opy_ != None and bstack1ll1l11ll11_opy_ != None:
                bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᙻ")] = {
                    bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹ࡮࡟ࡵࡱ࡮ࡩࡳ࠭ᙼ"): bstack1ll1l1ll11l_opy_,
                    bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᙽ"): bstack1ll1l11ll11_opy_,
                }
            else:
                bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᙾ")] = {}
        else:
            bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᙿ")] = {}
        if bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ ")].get(bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡨࡢࡵ࡫ࡩࡩࡥࡩࡥࠩᚁ")) != None or bstack1ll1l1llll1_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚂ")].get(bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡪࡤࡷ࡭࡫ࡤࡠ࡫ࡧࠫᚃ")) != None:
            cls.bstack1ll1l11l111_opy_(bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠪ࡮ࡼࡺࠧᚄ")), bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚅ")))
        return bstack1ll1l1llll1_opy_
    @classmethod
    def bstack1ll1l1lllll_opy_(cls, bstack1ll1l1lll1l_opy_):
        if bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬᚆ")) == None:
            cls.bstack1ll1l1l1ll1_opy_()
            return [None, None, None]
        if bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᚇ")][bstack1lll1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᚈ")] != True:
            cls.bstack1ll1l1l1ll1_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨᚉ")])
            return [None, None, None]
        logger.debug(bstack1lll1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡐࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᚊ"))
        os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡃࡗࡌࡐࡉࡥࡃࡐࡏࡓࡐࡊ࡚ࡅࡅࠩᚋ")] = bstack1lll1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩᚌ")
        if bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠬࡰࡷࡵࠩᚍ")):
            os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡎ࡜࡚ࠧᚎ")] = bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠧ࡫ࡹࡷࠫᚏ")]
            os.environ[bstack1lll1l1_opy_ (u"ࠨࡅࡕࡉࡉࡋࡎࡕࡋࡄࡐࡘࡥࡆࡐࡔࡢࡇࡗࡇࡓࡉࡡࡕࡉࡕࡕࡒࡕࡋࡑࡋࠬᚐ")] = json.dumps({
                bstack1lll1l1_opy_ (u"ࠩࡸࡷࡪࡸ࡮ࡢ࡯ࡨࠫᚑ"): bstack11l111111l_opy_(cls.bs_config),
                bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡸࡱࡵࡨࠬᚒ"): bstack111llllll1_opy_(cls.bs_config)
            })
        if bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢ࡬ࡦࡹࡨࡦࡦࡢ࡭ࡩ࠭ᚓ")):
            os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᚔ")] = bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡮ࡡࡴࡪࡨࡨࡤ࡯ࡤࠨᚕ")]
        if bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧᚖ")].get(bstack1lll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚗ"), {}).get(bstack1lll1l1_opy_ (u"ࠩࡤࡰࡱࡵࡷࡠࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᚘ")):
            os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡂࡎࡏࡓ࡜ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࡖࠫᚙ")] = str(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫᚚ")][bstack1lll1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᚛")][bstack1lll1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻࡤࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࡵࠪ᚜")])
        return [bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠧ࡫ࡹࡷࠫ᚝")], bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡩࡣࡶ࡬ࡪࡪ࡟ࡪࡦࠪ᚞")], os.environ[bstack1lll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡁࡍࡎࡒ࡛ࡤ࡙ࡃࡓࡇࡈࡒࡘࡎࡏࡕࡕࠪ᚟")]]
    @classmethod
    def bstack1ll1l11l11l_opy_(cls, bstack1ll1l1lll1l_opy_):
        if bstack1ll1l1lll1l_opy_.get(bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚠ")) == None:
            cls.bstack1ll1l11ll1l_opy_()
            return [None, None]
        if bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚡ")][bstack1lll1l1_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᚢ")] != True:
            cls.bstack1ll1l11ll1l_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚣ")])
            return [None, None]
        if bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚤ")].get(bstack1lll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚥ")):
            logger.debug(bstack1lll1l1_opy_ (u"ࠩࡗࡩࡸࡺࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡕࡸࡧࡨ࡫ࡳࡴࡨࡸࡰࠦ࠭ᚦ"))
            parsed = json.loads(os.getenv(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᚧ"), bstack1lll1l1_opy_ (u"ࠫࢀࢃࠧᚨ")))
            capabilities = bstack1ll1l1111_opy_.bstack1ll1l11l1l1_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚩ")][bstack1lll1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᚪ")][bstack1lll1l1_opy_ (u"ࠧࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚫ")], bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᚬ"), bstack1lll1l1_opy_ (u"ࠩࡹࡥࡱࡻࡥࠨᚭ"))
            bstack1ll1l1ll11l_opy_ = capabilities[bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨᚮ")]
            os.environ[bstack1lll1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᚯ")] = bstack1ll1l1ll11l_opy_
            parsed[bstack1lll1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚰ")] = capabilities[bstack1lll1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚱ")]
            os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᚲ")] = json.dumps(parsed)
            scripts = bstack1ll1l1111_opy_.bstack1ll1l11l1l1_opy_(bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚳ")][bstack1lll1l1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᚴ")][bstack1lll1l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᚵ")], bstack1lll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩᚶ"), bstack1lll1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩ࠭ᚷ"))
            bstack1l1lllllll_opy_.bstack11l11111ll_opy_(scripts)
            commands = bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚸ")][bstack1lll1l1_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᚹ")][bstack1lll1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࡗࡳ࡜ࡸࡡࡱࠩᚺ")].get(bstack1lll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᚻ"))
            bstack1l1lllllll_opy_.bstack11l11l1l1l_opy_(commands)
            bstack1l1lllllll_opy_.store()
        return [bstack1ll1l1ll11l_opy_, bstack1ll1l1lll1l_opy_[bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡫ࡥࡸ࡮ࡥࡥࡡ࡬ࡨࠬᚼ")]]
    @classmethod
    def bstack1ll1l1l1ll1_opy_(cls, response=None):
        os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᚽ")] = bstack1lll1l1_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᚾ")
        os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡔࡡࡗࡉࡘ࡚ࡏࡑࡕࡢࡆ࡚ࡏࡌࡅࡡࡆࡓࡒࡖࡌࡆࡖࡈࡈࠬᚿ")] = bstack1lll1l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᛀ")
        os.environ[bstack1lll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᛁ")] = bstack1lll1l1_opy_ (u"ࠩࡱࡹࡱࡲࠧᛂ")
        os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡓࡕ࡙࡟ࡋ࡙ࡗࠫᛃ")] = bstack1lll1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛄ")
        os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡓࡠࡖࡈࡗ࡙ࡕࡐࡔࡡࡅ࡙ࡎࡒࡄࡠࡊࡄࡗࡍࡋࡄࡠࡋࡇࠫᛅ")] = bstack1lll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᛆ")
        os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡐࡒࡖࡣࡆࡒࡌࡐ࡙ࡢࡗࡈࡘࡅࡆࡐࡖࡌࡔ࡚ࡓࠨᛇ")] = bstack1lll1l1_opy_ (u"ࠣࡰࡸࡰࡱࠨᛈ")
        cls.bstack1ll1ll11l11_opy_(response, bstack1lll1l1_opy_ (u"ࠤࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠤᛉ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11ll1l_opy_(cls, response=None):
        os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨᛊ")] = bstack1lll1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᛋ")
        os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᛌ")] = bstack1lll1l1_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᛍ")
        os.environ[bstack1lll1l1_opy_ (u"ࠧࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᛎ")] = bstack1lll1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᛏ")
        cls.bstack1ll1ll11l11_opy_(response, bstack1lll1l1_opy_ (u"ࠤࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠤᛐ"))
        return [None, None, None]
    @classmethod
    def bstack1ll1l11l111_opy_(cls, bstack1ll1ll111l1_opy_, bstack1ll1l11ll11_opy_):
        os.environ[bstack1lll1l1_opy_ (u"ࠪࡆࡘࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛑ")] = bstack1ll1ll111l1_opy_
        os.environ[bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛒ")] = bstack1ll1l11ll11_opy_
    @classmethod
    def bstack1ll1ll11l11_opy_(cls, response=None, product=bstack1lll1l1_opy_ (u"ࠧࠨᛓ")):
        if response == None:
            logger.error(product + bstack1lll1l1_opy_ (u"ࠨࠠࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡨࡤ࡭ࡱ࡫ࡤࠣᛔ"))
        for error in response[bstack1lll1l1_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᛕ")]:
            bstack111l11l11l_opy_ = error[bstack1lll1l1_opy_ (u"ࠨ࡭ࡨࡽࠬᛖ")]
            error_message = error[bstack1lll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᛗ")]
            if error_message:
                if bstack111l11l11l_opy_ == bstack1lll1l1_opy_ (u"ࠥࡉࡗࡘࡏࡓࡡࡄࡇࡈࡋࡓࡔࡡࡇࡉࡓࡏࡅࡅࠤᛘ"):
                    logger.info(error_message)
                else:
                    logger.error(error_message)
            else:
                logger.error(bstack1lll1l1_opy_ (u"ࠦࡉࡧࡴࡢࠢࡸࡴࡱࡵࡡࡥࠢࡷࡳࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࠧᛙ") + product + bstack1lll1l1_opy_ (u"ࠧࠦࡦࡢ࡫࡯ࡩࡩࠦࡤࡶࡧࠣࡸࡴࠦࡳࡰ࡯ࡨࠤࡪࡸࡲࡰࡴࠥᛚ"))
    @classmethod
    def bstack1ll1ll11111_opy_(cls):
        if cls.bstack1lll111ll1l_opy_ is not None:
            return
        cls.bstack1lll111ll1l_opy_ = bstack1lll11111l1_opy_(cls.bstack1ll1l1l111l_opy_)
        cls.bstack1lll111ll1l_opy_.start()
    @classmethod
    def bstack11ll1llll1_opy_(cls):
        if cls.bstack1lll111ll1l_opy_ is None:
            return
        cls.bstack1lll111ll1l_opy_.shutdown()
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1ll1l1l111l_opy_(cls, bstack11ll1ll1ll_opy_, bstack1ll1ll111ll_opy_=bstack1lll1l1_opy_ (u"࠭ࡡࡱ࡫࠲ࡺ࠶࠵ࡢࡢࡶࡦ࡬ࠬᛛ")):
        config = {
            bstack1lll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᛜ"): cls.default_headers()
        }
        response = bstack1l1ll1l11_opy_(bstack1lll1l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᛝ"), cls.request_url(bstack1ll1ll111ll_opy_), bstack11ll1ll1ll_opy_, config)
        bstack11l111l1ll_opy_ = response.json()
    @classmethod
    def bstack11l1llll1l_opy_(cls, bstack11ll1ll1ll_opy_, bstack1ll1ll111ll_opy_=bstack1lll1l1_opy_ (u"ࠩࡤࡴ࡮࠵ࡶ࠲࠱ࡥࡥࡹࡩࡨࠨᛞ")):
        if not bstack1ll1l1111_opy_.bstack1ll1l11llll_opy_(bstack11ll1ll1ll_opy_[bstack1lll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᛟ")]):
            return
        bstack1l1l1l1ll_opy_ = bstack1ll1l1111_opy_.bstack1ll1l111lll_opy_(bstack11ll1ll1ll_opy_[bstack1lll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᛠ")], bstack11ll1ll1ll_opy_.get(bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴࠧᛡ")))
        if bstack1l1l1l1ll_opy_ != None:
            bstack11ll1ll1ll_opy_[bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡧࡹࡨࡺ࡟࡮ࡣࡳࠫᛢ")] = bstack1l1l1l1ll_opy_
        if bstack1ll1ll111ll_opy_ == bstack1lll1l1_opy_ (u"ࠧࡢࡲ࡬࠳ࡻ࠷࠯ࡣࡣࡷࡧ࡭࠭ᛣ"):
            cls.bstack1ll1ll11111_opy_()
            cls.bstack1lll111ll1l_opy_.add(bstack11ll1ll1ll_opy_)
        elif bstack1ll1ll111ll_opy_ == bstack1lll1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ࠭ᛤ"):
            cls.bstack1ll1l1l111l_opy_([bstack11ll1ll1ll_opy_], bstack1ll1ll111ll_opy_)
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1l11llll1l_opy_(cls, bstack11ll11ll11_opy_):
        bstack1ll1ll11l1l_opy_ = []
        for log in bstack11ll11ll11_opy_:
            bstack1ll1l1l1lll_opy_ = {
                bstack1lll1l1_opy_ (u"ࠩ࡮࡭ࡳࡪࠧᛥ"): bstack1lll1l1_opy_ (u"ࠪࡘࡊ࡙ࡔࡠࡎࡒࡋࠬᛦ"),
                bstack1lll1l1_opy_ (u"ࠫࡱ࡫ࡶࡦ࡮ࠪᛧ"): log[bstack1lll1l1_opy_ (u"ࠬࡲࡥࡷࡧ࡯ࠫᛨ")],
                bstack1lll1l1_opy_ (u"࠭ࡴࡪ࡯ࡨࡷࡹࡧ࡭ࡱࠩᛩ"): log[bstack1lll1l1_opy_ (u"ࠧࡵ࡫ࡰࡩࡸࡺࡡ࡮ࡲࠪᛪ")],
                bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡥࡲࡦࡵࡳࡳࡳࡹࡥࠨ᛫"): {},
                bstack1lll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᛬"): log[bstack1lll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᛭")],
            }
            if bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᛮ") in log:
                bstack1ll1l1l1lll_opy_[bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᛯ")] = log[bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᛰ")]
            elif bstack1lll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᛱ") in log:
                bstack1ll1l1l1lll_opy_[bstack1lll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡥࡲࡶࡰࡢࡹࡺ࡯ࡤࠨᛲ")] = log[bstack1lll1l1_opy_ (u"ࠩ࡫ࡳࡴࡱ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᛳ")]
            bstack1ll1ll11l1l_opy_.append(bstack1ll1l1l1lll_opy_)
        cls.bstack11l1llll1l_opy_({
            bstack1lll1l1_opy_ (u"ࠪࡩࡻ࡫࡮ࡵࡡࡷࡽࡵ࡫ࠧᛴ"): bstack1lll1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨᛵ"),
            bstack1lll1l1_opy_ (u"ࠬࡲ࡯ࡨࡵࠪᛶ"): bstack1ll1ll11l1l_opy_
        })
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1ll1l1ll111_opy_(cls, steps):
        bstack1ll1l11lll1_opy_ = []
        for step in steps:
            bstack1ll1l1ll1l1_opy_ = {
                bstack1lll1l1_opy_ (u"࠭࡫ࡪࡰࡧࠫᛷ"): bstack1lll1l1_opy_ (u"ࠧࡕࡇࡖࡘࡤ࡙ࡔࡆࡒࠪᛸ"),
                bstack1lll1l1_opy_ (u"ࠨ࡮ࡨࡺࡪࡲࠧ᛹"): step[bstack1lll1l1_opy_ (u"ࠩ࡯ࡩࡻ࡫࡬ࠨ᛺")],
                bstack1lll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡴࡶࡤࡱࡵ࠭᛻"): step[bstack1lll1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡵࡷࡥࡲࡶࠧ᛼")],
                bstack1lll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᛽"): step[bstack1lll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᛾")],
                bstack1lll1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࠩ᛿"): step[bstack1lll1l1_opy_ (u"ࠨࡦࡸࡶࡦࡺࡩࡰࡰࠪᜀ")]
            }
            if bstack1lll1l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡳࡷࡱࡣࡺࡻࡩࡥࠩᜁ") in step:
                bstack1ll1l1ll1l1_opy_[bstack1lll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࡤࡻࡵࡪࡦࠪᜂ")] = step[bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳࡥࡵࡶ࡫ࡧࠫᜃ")]
            elif bstack1lll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡶࡺࡴ࡟ࡶࡷ࡬ࡨࠬᜄ") in step:
                bstack1ll1l1ll1l1_opy_[bstack1lll1l1_opy_ (u"࠭ࡨࡰࡱ࡮ࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜅ")] = step[bstack1lll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪࠧᜆ")]
            bstack1ll1l11lll1_opy_.append(bstack1ll1l1ll1l1_opy_)
        cls.bstack11l1llll1l_opy_({
            bstack1lll1l1_opy_ (u"ࠨࡧࡹࡩࡳࡺ࡟ࡵࡻࡳࡩࠬᜇ"): bstack1lll1l1_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ᜈ"),
            bstack1lll1l1_opy_ (u"ࠪࡰࡴ࡭ࡳࠨᜉ"): bstack1ll1l11lll1_opy_
        })
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1l1111l1_opy_(cls, screenshot):
        cls.bstack11l1llll1l_opy_({
            bstack1lll1l1_opy_ (u"ࠫࡪࡼࡥ࡯ࡶࡢࡸࡾࡶࡥࠨᜊ"): bstack1lll1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩᜋ"),
            bstack1lll1l1_opy_ (u"࠭࡬ࡰࡩࡶࠫᜌ"): [{
                bstack1lll1l1_opy_ (u"ࠧ࡬࡫ࡱࡨࠬᜍ"): bstack1lll1l1_opy_ (u"ࠨࡖࡈࡗ࡙ࡥࡓࡄࡔࡈࡉࡓ࡙ࡈࡐࡖࠪᜎ"),
                bstack1lll1l1_opy_ (u"ࠩࡷ࡭ࡲ࡫ࡳࡵࡣࡰࡴࠬᜏ"): datetime.datetime.utcnow().isoformat() + bstack1lll1l1_opy_ (u"ࠪ࡞ࠬᜐ"),
                bstack1lll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᜑ"): screenshot[bstack1lll1l1_opy_ (u"ࠬ࡯࡭ࡢࡩࡨࠫᜒ")],
                bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠࡷࡸ࡭ࡩ࠭ᜓ"): screenshot[bstack1lll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡤࡸࡵ࡯ࡡࡸࡹ࡮ࡪ᜔ࠧ")]
            }]
        }, bstack1ll1ll111ll_opy_=bstack1lll1l1_opy_ (u"ࠨࡣࡳ࡭࠴ࡼ࠱࠰ࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࡸ᜕࠭"))
    @classmethod
    @bstack11ll111ll1_opy_(class_method=True)
    def bstack1lllll11_opy_(cls, driver):
        current_test_uuid = cls.current_test_uuid()
        if not current_test_uuid:
            return
        cls.bstack11l1llll1l_opy_({
            bstack1lll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡠࡶࡼࡴࡪ࠭᜖"): bstack1lll1l1_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ᜗"),
            bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡡࡵࡹࡳ࠭᜘"): {
                bstack1lll1l1_opy_ (u"ࠧࡻࡵࡪࡦࠥ᜙"): cls.current_test_uuid(),
                bstack1lll1l1_opy_ (u"ࠨࡩ࡯ࡶࡨ࡫ࡷࡧࡴࡪࡱࡱࡷࠧ᜚"): cls.bstack11l1llll11_opy_(driver)
            }
        })
    @classmethod
    def bstack11lll1l1l1_opy_(cls, event: str, bstack11ll1ll1ll_opy_: bstack11ll11111l_opy_):
        bstack11l1ll1111_opy_ = {
            bstack1lll1l1_opy_ (u"ࠧࡦࡸࡨࡲࡹࡥࡴࡺࡲࡨࠫ᜛"): event,
            bstack11ll1ll1ll_opy_.bstack11ll1ll111_opy_(): bstack11ll1ll1ll_opy_.bstack11ll1111l1_opy_(event)
        }
        cls.bstack11l1llll1l_opy_(bstack11l1ll1111_opy_)
    @classmethod
    def on(cls):
        if (os.environ.get(bstack1lll1l1_opy_ (u"ࠨࡄࡖࡣ࡙ࡋࡓࡕࡑࡓࡗࡤࡐࡗࡕࠩ᜜"), None) is None or os.environ[bstack1lll1l1_opy_ (u"ࠩࡅࡗࡤ࡚ࡅࡔࡖࡒࡔࡘࡥࡊࡘࡖࠪ᜝")] == bstack1lll1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣ᜞")) and (os.environ.get(bstack1lll1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᜟ"), None) is None or os.environ[bstack1lll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᜠ")] == bstack1lll1l1_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᜡ")):
            return False
        return True
    @staticmethod
    def bstack1ll1l11l1ll_opy_(func):
        def wrap(*args, **kwargs):
            if bstack1l1lll1lll_opy_.on():
                return func(*args, **kwargs)
            return
        return wrap
    @staticmethod
    def default_headers():
        headers = {
            bstack1lll1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᜢ"): bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᜣ"),
            bstack1lll1l1_opy_ (u"࡛ࠩ࠱ࡇ࡙ࡔࡂࡅࡎ࠱࡙ࡋࡓࡕࡑࡓࡗࠬᜤ"): bstack1lll1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᜥ")
        }
        if os.environ.get(bstack1lll1l1_opy_ (u"ࠫࡇ࡙࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᜦ"), None):
            headers[bstack1lll1l1_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᜧ")] = bstack1lll1l1_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࡻࡾࠩᜨ").format(os.environ[bstack1lll1l1_opy_ (u"ࠢࡃࡕࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠣᜩ")])
        return headers
    @staticmethod
    def request_url(url):
        return bstack1lll1l1_opy_ (u"ࠨࡽࢀ࠳ࢀࢃࠧᜪ").format(bstack1ll1ll11ll1_opy_, url)
    @staticmethod
    def current_test_uuid():
        return getattr(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠩࡦࡹࡷࡸࡥ࡯ࡶࡢࡸࡪࡹࡴࡠࡷࡸ࡭ࡩ࠭ᜫ"), None)
    @staticmethod
    def bstack11l1llll11_opy_(driver):
        return {
            bstack1111ll1l1l_opy_(): bstack1111l111l1_opy_(driver)
        }
    @staticmethod
    def bstack1ll1ll1111l_opy_(exception_info, report):
        return [{bstack1lll1l1_opy_ (u"ࠪࡦࡦࡩ࡫ࡵࡴࡤࡧࡪ࠭ᜬ"): [exception_info.exconly(), report.longreprtext]}]
    @staticmethod
    def bstack11l11lll1l_opy_(typename):
        if bstack1lll1l1_opy_ (u"ࠦࡆࡹࡳࡦࡴࡷ࡭ࡴࡴࠢᜭ") in typename:
            return bstack1lll1l1_opy_ (u"ࠧࡇࡳࡴࡧࡵࡸ࡮ࡵ࡮ࡆࡴࡵࡳࡷࠨᜮ")
        return bstack1lll1l1_opy_ (u"ࠨࡕ࡯ࡪࡤࡲࡩࡲࡥࡥࡇࡵࡶࡴࡸࠢᜯ")