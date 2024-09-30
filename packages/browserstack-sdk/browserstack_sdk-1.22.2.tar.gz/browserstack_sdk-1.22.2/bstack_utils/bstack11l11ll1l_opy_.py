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
import re
from bstack_utils.bstack1l1l111lll_opy_ import bstack1lll11ll1l1_opy_
def bstack1lll11l1l1l_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖢ")):
        return bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᖣ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠪࡣࡽࡻ࡮ࡪࡶࡢࡷࡪࡺࡵࡱࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖤ")):
        return bstack1lll1l1_opy_ (u"ࠫࡸ࡫ࡴࡶࡲ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖥ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡺࡥࡢࡴࡧࡳࡼࡴ࡟ࡧࡷࡱࡧࡹ࡯࡯࡯ࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖦ")):
        return bstack1lll1l1_opy_ (u"࠭ࡴࡦࡣࡵࡨࡴࡽ࡮࠮ࡨࡸࡲࡨࡺࡩࡰࡰࠪᖧ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡩࡹࡳࡩࡴࡪࡱࡱࡣ࡫࡯ࡸࡵࡷࡵࡩࠬᖨ")):
        return bstack1lll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖩ")
def bstack1lll11l1ll1_opy_(fixture_name):
    return bool(re.match(bstack1lll1l1_opy_ (u"ࠩࡡࡣࡽࡻ࡮ࡪࡶࡢࠬࡸ࡫ࡴࡶࡲࡿࡸࡪࡧࡲࡥࡱࡺࡲ࠮ࡥࠨࡧࡷࡱࡧࡹ࡯࡯࡯ࡾࡰࡳࡩࡻ࡬ࡦࠫࡢࡪ࡮ࡾࡴࡶࡴࡨࡣ࠳࠰ࠧᖪ"), fixture_name))
def bstack1lll11l1111_opy_(fixture_name):
    return bool(re.match(bstack1lll1l1_opy_ (u"ࠪࡢࡤࡾࡵ࡯࡫ࡷࡣ࠭ࡹࡥࡵࡷࡳࢀࡹ࡫ࡡࡳࡦࡲࡻࡳ࠯࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᖫ"), fixture_name))
def bstack1lll11ll11l_opy_(fixture_name):
    return bool(re.match(bstack1lll1l1_opy_ (u"ࠫࡣࡥࡸࡶࡰ࡬ࡸࡤ࠮ࡳࡦࡶࡸࡴࢁࡺࡥࡢࡴࡧࡳࡼࡴࠩࡠࡥ࡯ࡥࡸࡹ࡟ࡧ࡫ࡻࡸࡺࡸࡥࡠ࠰࠭ࠫᖬ"), fixture_name))
def bstack1lll11l1lll_opy_(fixture_name):
    if fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠬࡥࡸࡶࡰ࡬ࡸࡤࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳࡥࡦࡪࡺࡷࡹࡷ࡫ࠧᖭ")):
        return bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴ࠲࡬ࡵ࡯ࡥࡷ࡭ࡴࡴࠧᖮ"), bstack1lll1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖯ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠨࡡࡻࡹࡳ࡯ࡴࡠࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫࡟ࡧ࡫ࡻࡸࡺࡸࡥࠨᖰ")):
        return bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰ࠮࡯ࡲࡨࡺࡲࡥࠨᖱ"), bstack1lll1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᖲ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠫࡤࡾࡵ࡯࡫ࡷࡣࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࡠࡨ࡬ࡼࡹࡻࡲࡦࠩᖳ")):
        return bstack1lll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࠭ࡧࡷࡱࡧࡹ࡯࡯࡯ࠩᖴ"), bstack1lll1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᖵ")
    elif fixture_name.startswith(bstack1lll1l1_opy_ (u"ࠧࡠࡺࡸࡲ࡮ࡺ࡟ࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࡡࡩ࡭ࡽࡺࡵࡳࡧࠪᖶ")):
        return bstack1lll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰ࠰ࡱࡴࡪࡵ࡭ࡧࠪᖷ"), bstack1lll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᖸ")
    return None, None
def bstack1lll111lll1_opy_(hook_name):
    if hook_name in [bstack1lll1l1_opy_ (u"ࠪࡷࡪࡺࡵࡱࠩᖹ"), bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳ࠭ᖺ")]:
        return hook_name.capitalize()
    return hook_name
def bstack1lll11l111l_opy_(hook_name):
    if hook_name in [bstack1lll1l1_opy_ (u"ࠬࡹࡥࡵࡷࡳࡣ࡫ࡻ࡮ࡤࡶ࡬ࡳࡳ࠭ᖻ"), bstack1lll1l1_opy_ (u"࠭ࡳࡦࡶࡸࡴࡤࡳࡥࡵࡪࡲࡨࠬᖼ")]:
        return bstack1lll1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡆࡃࡆࡌࠬᖽ")
    elif hook_name in [bstack1lll1l1_opy_ (u"ࠨࡵࡨࡸࡺࡶ࡟࡮ࡱࡧࡹࡱ࡫ࠧᖾ"), bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹࡻࡰࡠࡥ࡯ࡥࡸࡹࠧᖿ")]:
        return bstack1lll1l1_opy_ (u"ࠪࡆࡊࡌࡏࡓࡇࡢࡅࡑࡒࠧᗀ")
    elif hook_name in [bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡡࡳࡦࡲࡻࡳࡥࡦࡶࡰࡦࡸ࡮ࡵ࡮ࠨᗁ"), bstack1lll1l1_opy_ (u"ࠬࡺࡥࡢࡴࡧࡳࡼࡴ࡟࡮ࡧࡷ࡬ࡴࡪࠧᗂ")]:
        return bstack1lll1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪᗃ")
    elif hook_name in [bstack1lll1l1_opy_ (u"ࠧࡵࡧࡤࡶࡩࡵࡷ࡯ࡡࡰࡳࡩࡻ࡬ࡦࠩᗄ"), bstack1lll1l1_opy_ (u"ࠨࡶࡨࡥࡷࡪ࡯ࡸࡰࡢࡧࡱࡧࡳࡴࠩᗅ")]:
        return bstack1lll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬᗆ")
    return hook_name
def bstack1lll11l1l11_opy_(node, scenario):
    if hasattr(node, bstack1lll1l1_opy_ (u"ࠪࡧࡦࡲ࡬ࡴࡲࡨࡧࠬᗇ")):
        parts = node.nodeid.rsplit(bstack1lll1l1_opy_ (u"ࠦࡠࠨᗈ"))
        params = parts[-1]
        return bstack1lll1l1_opy_ (u"ࠧࢁࡽࠡ࡝ࡾࢁࠧᗉ").format(scenario.name, params)
    return scenario.name
def bstack1lll11l11ll_opy_(node):
    try:
        examples = []
        if hasattr(node, bstack1lll1l1_opy_ (u"࠭ࡣࡢ࡮࡯ࡷࡵ࡫ࡣࠨᗊ")):
            examples = list(node.callspec.params[bstack1lll1l1_opy_ (u"ࠧࡠࡲࡼࡸࡪࡹࡴࡠࡤࡧࡨࡤ࡫ࡸࡢ࡯ࡳࡰࡪ࠭ᗋ")].values())
        return examples
    except:
        return []
def bstack1lll11l11l1_opy_(feature, scenario):
    return list(feature.tags) + list(scenario.tags)
def bstack1lll11ll111_opy_(report):
    try:
        status = bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱ࡫ࡤࠨᗌ")
        if report.passed or (report.failed and hasattr(report, bstack1lll1l1_opy_ (u"ࠤࡺࡥࡸࡾࡦࡢ࡫࡯ࠦᗍ"))):
            status = bstack1lll1l1_opy_ (u"ࠪࡴࡦࡹࡳࡦࡦࠪᗎ")
        elif report.skipped:
            status = bstack1lll1l1_opy_ (u"ࠫࡸࡱࡩࡱࡲࡨࡨࠬᗏ")
        bstack1lll11ll1l1_opy_(status)
    except:
        pass
def bstack1l11l11l_opy_(status):
    try:
        bstack1lll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࠬᗐ")
        if status == bstack1lll1l1_opy_ (u"࠭ࡰࡢࡵࡶࡩࡩ࠭ᗑ"):
            bstack1lll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠧࡱࡣࡶࡷࡪࡪࠧᗒ")
        elif status == bstack1lll1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩᗓ"):
            bstack1lll11ll1ll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡶ࡯࡮ࡶࡰࡦࡦࠪᗔ")
        bstack1lll11ll1l1_opy_(bstack1lll11ll1ll_opy_)
    except:
        pass
def bstack1lll111llll_opy_(item=None, report=None, summary=None, extra=None):
    return