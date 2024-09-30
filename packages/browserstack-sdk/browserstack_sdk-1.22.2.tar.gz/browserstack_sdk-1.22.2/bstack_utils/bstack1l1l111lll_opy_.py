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
import os
import threading
from bstack_utils.config import Config
from bstack_utils.helper import bstack11111llll1_opy_, bstack11llllll11_opy_, bstack1llll1l1ll_opy_, bstack11l111ll1_opy_, \
    bstack11111lll1l_opy_
def bstack111l1ll1l_opy_(bstack1ll1lllll1l_opy_):
    for driver in bstack1ll1lllll1l_opy_:
        try:
            driver.quit()
        except Exception as e:
            pass
def bstack1l11ll11l1_opy_(driver, status, reason=bstack1lll1l1_opy_ (u"ࠬ࠭ᗗ")):
    bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
    if bstack1lll11l1ll_opy_.bstack11l1l1lll1_opy_():
        return
    bstack1l111111l_opy_ = bstack1l1111l1l1_opy_(bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᗘ"), bstack1lll1l1_opy_ (u"ࠧࠨᗙ"), status, reason, bstack1lll1l1_opy_ (u"ࠨࠩᗚ"), bstack1lll1l1_opy_ (u"ࠩࠪᗛ"))
    driver.execute_script(bstack1l111111l_opy_)
def bstack11lll1ll1_opy_(page, status, reason=bstack1lll1l1_opy_ (u"ࠪࠫᗜ")):
    try:
        if page is None:
            return
        bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
        if bstack1lll11l1ll_opy_.bstack11l1l1lll1_opy_():
            return
        bstack1l111111l_opy_ = bstack1l1111l1l1_opy_(bstack1lll1l1_opy_ (u"ࠫࡸ࡫ࡴࡔࡧࡶࡷ࡮ࡵ࡮ࡔࡶࡤࡸࡺࡹࠧᗝ"), bstack1lll1l1_opy_ (u"ࠬ࠭ᗞ"), status, reason, bstack1lll1l1_opy_ (u"࠭ࠧᗟ"), bstack1lll1l1_opy_ (u"ࠧࠨᗠ"))
        page.evaluate(bstack1lll1l1_opy_ (u"ࠣࡡࠣࡁࡃࠦࡻࡾࠤᗡ"), bstack1l111111l_opy_)
    except Exception as e:
        print(bstack1lll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡶࡩࡸࡹࡩࡰࡰࠣࡷࡹࡧࡴࡶࡵࠣࡪࡴࡸࠠࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷࠤࢀࢃࠢᗢ"), e)
def bstack1l1111l1l1_opy_(type, name, status, reason, bstack111ll1l11_opy_, bstack1l1l1l1111_opy_):
    bstack1l111ll11l_opy_ = {
        bstack1lll1l1_opy_ (u"ࠪࡥࡨࡺࡩࡰࡰࠪᗣ"): type,
        bstack1lll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗤ"): {}
    }
    if type == bstack1lll1l1_opy_ (u"ࠬࡧ࡮࡯ࡱࡷࡥࡹ࡫ࠧᗥ"):
        bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᗦ")][bstack1lll1l1_opy_ (u"ࠧ࡭ࡧࡹࡩࡱ࠭ᗧ")] = bstack111ll1l11_opy_
        bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᗨ")][bstack1lll1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᗩ")] = json.dumps(str(bstack1l1l1l1111_opy_))
    if type == bstack1lll1l1_opy_ (u"ࠪࡷࡪࡺࡓࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫᗪ"):
        bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗫ")][bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᗬ")] = name
    if type == bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡖࡩࡸࡹࡩࡰࡰࡖࡸࡦࡺࡵࡴࠩᗭ"):
        bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᗮ")][bstack1lll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᗯ")] = status
        if status == bstack1lll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࠩᗰ") and str(reason) != bstack1lll1l1_opy_ (u"ࠥࠦᗱ"):
            bstack1l111ll11l_opy_[bstack1lll1l1_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᗲ")][bstack1lll1l1_opy_ (u"ࠬࡸࡥࡢࡵࡲࡲࠬᗳ")] = json.dumps(str(reason))
    bstack1lllllll11_opy_ = bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࡽࢀࠫᗴ").format(json.dumps(bstack1l111ll11l_opy_))
    return bstack1lllllll11_opy_
def bstack1llll11lll_opy_(url, config, logger, bstack11111l1l1_opy_=False):
    hostname = bstack11llllll11_opy_(url)
    is_private = bstack11l111ll1_opy_(hostname)
    try:
        if is_private or bstack11111l1l1_opy_:
            file_path = bstack11111llll1_opy_(bstack1lll1l1_opy_ (u"ࠧ࠯ࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧᗵ"), bstack1lll1l1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᗶ"), logger)
            if os.environ.get(bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡎࡒࡇࡆࡒ࡟ࡏࡑࡗࡣࡘࡋࡔࡠࡇࡕࡖࡔࡘࠧᗷ")) and eval(
                    os.environ.get(bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࡠࡐࡒࡘࡤ࡙ࡅࡕࡡࡈࡖࡗࡕࡒࠨᗸ"))):
                return
            if (bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨᗹ") in config and not config[bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࠩᗺ")]):
                os.environ[bstack1lll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡒࡏࡄࡃࡏࡣࡓࡕࡔࡠࡕࡈࡘࡤࡋࡒࡓࡑࡕࠫᗻ")] = str(True)
                bstack1ll1llll1ll_opy_ = {bstack1lll1l1_opy_ (u"ࠧࡩࡱࡶࡸࡳࡧ࡭ࡦࠩᗼ"): hostname}
                bstack11111lll1l_opy_(bstack1lll1l1_opy_ (u"ࠨ࠰ࡥࡷࡹࡧࡣ࡬࠯ࡦࡳࡳ࡬ࡩࡨ࠰࡭ࡷࡴࡴࠧᗽ"), bstack1lll1l1_opy_ (u"ࠩࡱࡹࡩ࡭ࡥࡠ࡮ࡲࡧࡦࡲࠧᗾ"), bstack1ll1llll1ll_opy_, logger)
    except Exception as e:
        pass
def bstack1ll1llllll_opy_(caps, bstack1ll1lllll11_opy_):
    if bstack1lll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᗿ") in caps:
        caps[bstack1lll1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᘀ")][bstack1lll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯ࠫᘁ")] = True
        if bstack1ll1lllll11_opy_:
            caps[bstack1lll1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘂ")][bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩᘃ")] = bstack1ll1lllll11_opy_
    else:
        caps[bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮࡭ࡱࡦࡥࡱ࠭ᘄ")] = True
        if bstack1ll1lllll11_opy_:
            caps[bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᘅ")] = bstack1ll1lllll11_opy_
def bstack1lll11ll1l1_opy_(bstack11l1ll1l11_opy_):
    bstack1ll1llll1l1_opy_ = bstack1llll1l1ll_opy_(threading.current_thread(), bstack1lll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡔࡶࡤࡸࡺࡹࠧᘆ"), bstack1lll1l1_opy_ (u"ࠫࠬᘇ"))
    if bstack1ll1llll1l1_opy_ == bstack1lll1l1_opy_ (u"ࠬ࠭ᘈ") or bstack1ll1llll1l1_opy_ == bstack1lll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳࡴࡪࡪࠧᘉ"):
        threading.current_thread().testStatus = bstack11l1ll1l11_opy_
    else:
        if bstack11l1ll1l11_opy_ == bstack1lll1l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪࠧᘊ"):
            threading.current_thread().testStatus = bstack11l1ll1l11_opy_