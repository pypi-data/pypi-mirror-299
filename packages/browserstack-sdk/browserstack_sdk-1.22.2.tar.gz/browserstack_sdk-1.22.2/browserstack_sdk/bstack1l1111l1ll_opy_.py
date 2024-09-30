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
logger = logging.getLogger(__name__)
class BrowserStackSdk:
    def get_current_platform():
        bstack1l11l111ll_opy_ = {}
        bstack11lllll11l_opy_ = os.environ.get(bstack1lll1l1_opy_ (u"ࠬࡉࡕࡓࡔࡈࡒ࡙ࡥࡐࡍࡃࡗࡊࡔࡘࡍࡠࡆࡄࡘࡆ࠭ග"), bstack1lll1l1_opy_ (u"࠭ࠧඝ"))
        if not bstack11lllll11l_opy_:
            return bstack1l11l111ll_opy_
        try:
            bstack11lllll1l1_opy_ = json.loads(bstack11lllll11l_opy_)
            if bstack1lll1l1_opy_ (u"ࠢࡰࡵࠥඞ") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠣࡱࡶࠦඟ")] = bstack11lllll1l1_opy_[bstack1lll1l1_opy_ (u"ࠤࡲࡷࠧච")]
            if bstack1lll1l1_opy_ (u"ࠥࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠢඡ") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠦࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠢජ") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠧࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠣඣ")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠨ࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠥඤ"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠢࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠥඥ")))
            if bstack1lll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࠤඦ") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠢට") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠣඨ")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࠧඩ"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠥඪ")))
            if bstack1lll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠣණ") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠣඬ") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠤත")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠦථ"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠦද")))
            if bstack1lll1l1_opy_ (u"ࠦࡩ࡫ࡶࡪࡥࡨࠦධ") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠧࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠤන") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠨࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠥ඲")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠢࡥࡧࡹ࡭ࡨ࡫ࠢඳ"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠣࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠧප")))
            if bstack1lll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࠦඵ") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤබ") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥභ")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࠢම"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧඹ")))
            if bstack1lll1l1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠥය") in bstack11lllll1l1_opy_ or bstack1lll1l1_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥර") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ඼")] = bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠨල"), bstack11lllll1l1_opy_.get(bstack1lll1l1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨ඾")))
            if bstack1lll1l1_opy_ (u"ࠧࡩࡵࡴࡶࡲࡱ࡛ࡧࡲࡪࡣࡥࡰࡪࡹࠢ඿") in bstack11lllll1l1_opy_:
                bstack1l11l111ll_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠣව")] = bstack11lllll1l1_opy_[bstack1lll1l1_opy_ (u"ࠢࡤࡷࡶࡸࡴࡳࡖࡢࡴ࡬ࡥࡧࡲࡥࡴࠤශ")]
        except Exception as error:
            logger.error(bstack1lll1l1_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣ࡫ࡪࡺࡴࡪࡰࡪࠤࡨࡻࡲࡳࡧࡱࡸࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡣࡷࡥ࠿ࠦࠢෂ") +  str(error))
        return bstack1l11l111ll_opy_