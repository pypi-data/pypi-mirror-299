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
import re
bstack1ll11ll1l_opy_ = {
	bstack1lll1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ࿐"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࠧ࿑"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ࿒"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡰ࡫ࡹࠨ࿓"),
  bstack1lll1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ࿔"): bstack1lll1l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫ࿕"),
  bstack1lll1l1_opy_ (u"ࠨࡷࡶࡩ࡜࠹ࡃࠨ࿖"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡤࡽ࠳ࡤࠩ࿗"),
  bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ࿘"): bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࠬ࿙"),
  bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ࿚"): bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࠬ࿛"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡧࡶࡷ࡮ࡵ࡮ࡏࡣࡰࡩࠬ࿜"): bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭࿝"),
  bstack1lll1l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨ࿞"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡧࡩࡧࡻࡧࠨ࿟"),
  bstack1lll1l1_opy_ (u"ࠫࡨࡵ࡮ࡴࡱ࡯ࡩࡑࡵࡧࡴࠩ࿠"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡮ࡴࡱ࡯ࡩࠬ࿡"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ࿢"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡌࡰࡩࡶࠫ࿣"),
  bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ࿤"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡳࡴ࡮ࡻ࡭ࡍࡱࡪࡷࠬ࿥"),
  bstack1lll1l1_opy_ (u"ࠪࡺ࡮ࡪࡥࡰࠩ࿦"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡺ࡮ࡪࡥࡰࠩ࿧"),
  bstack1lll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࿨"): bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡌࡰࡩࡶࠫ࿩"),
  bstack1lll1l1_opy_ (u"ࠧࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ࿪"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡵࡧ࡯ࡩࡲ࡫ࡴࡳࡻࡏࡳ࡬ࡹࠧ࿫"),
  bstack1lll1l1_opy_ (u"ࠩࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ࿬"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡪࡩࡴࡒ࡯ࡤࡣࡷ࡭ࡴࡴࠧ࿭"),
  bstack1lll1l1_opy_ (u"ࠫࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭࿮"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡹ࡯࡭ࡦࡼࡲࡲࡪ࠭࿯"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ࿰"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ࿱"),
  bstack1lll1l1_opy_ (u"ࠨ࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࿲"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡯ࡤࡷࡰࡉ࡯࡮࡯ࡤࡲࡩࡹࠧ࿳"),
  bstack1lll1l1_opy_ (u"ࠪ࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ࿴"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱࡭ࡩࡲࡥࡕ࡫ࡰࡩࡴࡻࡴࠨ࿵"),
  bstack1lll1l1_opy_ (u"ࠬࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ࿶"): bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡳࡡࡴ࡭ࡅࡥࡸ࡯ࡣࡂࡷࡷ࡬ࠬ࿷"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ࿸"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧࡱࡨࡐ࡫ࡹࡴࠩ࿹"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ࿺"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡹࡹࡵࡗࡢ࡫ࡷࠫ࿻"),
  bstack1lll1l1_opy_ (u"ࠫ࡭ࡵࡳࡵࡵࠪ࿼"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲࡭ࡵࡳࡵࡵࠪ࿽"),
  bstack1lll1l1_opy_ (u"࠭ࡢࡧࡥࡤࡧ࡭࡫ࠧ࿾"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡢࡧࡥࡤࡧ࡭࡫ࠧ࿿"),
  bstack1lll1l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩက"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩခ"),
  bstack1lll1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ဂ"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡨ࡮ࡹࡡࡣ࡮ࡨࡇࡴࡸࡳࡓࡧࡶࡸࡷ࡯ࡣࡵ࡫ࡲࡲࡸ࠭ဃ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩင"): bstack1lll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭စ"),
  bstack1lll1l1_opy_ (u"ࠧࡳࡧࡤࡰࡒࡵࡢࡪ࡮ࡨࠫဆ"): bstack1lll1l1_opy_ (u"ࠨࡴࡨࡥࡱࡥ࡭ࡰࡤ࡬ࡰࡪ࠭ဇ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩဈ"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪဉ"),
  bstack1lll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫည"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡻࡳࡵࡱࡰࡒࡪࡺࡷࡰࡴ࡮ࠫဋ"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧဌ"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴࡮ࡦࡶࡺࡳࡷࡱࡐࡳࡱࡩ࡭ࡱ࡫ࠧဍ"),
  bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡶࡴࡊࡰࡶࡩࡨࡻࡲࡦࡅࡨࡶࡹࡹࠧဎ"): bstack1lll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡕࡶࡰࡈ࡫ࡲࡵࡵࠪဏ"),
  bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬတ"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡕࡇࡏࠬထ"),
  bstack1lll1l1_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬဒ"): bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡹ࡯ࡶࡴࡦࡩࠬဓ"),
  bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩန"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩပ"),
  bstack1lll1l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫဖ"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡫ࡳࡸࡺࡎࡢ࡯ࡨࠫဗ"),
  bstack1lll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧဘ"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡪࡴࡡࡣ࡮ࡨࡗ࡮ࡳࠧမ"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪယ"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪရ"),
  bstack1lll1l1_opy_ (u"ࠨࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭လ"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡳࡰࡴࡧࡤࡎࡧࡧ࡭ࡦ࠭ဝ")
}
bstack111ll1111l_opy_ = [
  bstack1lll1l1_opy_ (u"ࠪࡳࡸ࠭သ"),
  bstack1lll1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧဟ"),
  bstack1lll1l1_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧဠ"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡦࡵࡶ࡭ࡴࡴࡎࡢ࡯ࡨࠫအ"),
  bstack1lll1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫဢ"),
  bstack1lll1l1_opy_ (u"ࠨࡴࡨࡥࡱࡓ࡯ࡣ࡫࡯ࡩࠬဣ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩဤ"),
]
bstack11ll1lll1_opy_ = {
  bstack1lll1l1_opy_ (u"ࠪࡹࡸ࡫ࡲࡏࡣࡰࡩࠬဥ"): [bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢ࡙ࡘࡋࡒࡏࡃࡐࡉࠬဦ"), bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡡࡑࡅࡒࡋࠧဧ")],
  bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸࡑࡥࡺࠩဨ"): bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪဩ"),
  bstack1lll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫဪ"): bstack1lll1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡏࡃࡐࡉࠬါ"),
  bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨာ"): bstack1lll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡔࡗࡕࡊࡆࡅࡗࡣࡓࡇࡍࡆࠩိ"),
  bstack1lll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡍࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧီ"): bstack1lll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨု"),
  bstack1lll1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧူ"): bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡑࡃࡕࡅࡑࡒࡅࡍࡕࡢࡔࡊࡘ࡟ࡑࡎࡄࡘࡋࡕࡒࡎࠩေ"),
  bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭ဲ"): bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡏࡓࡈࡇࡌࠨဳ"),
  bstack1lll1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨဴ"): bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࡢࡘࡊ࡙ࡔࡔࠩဵ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࠪံ"): [bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡑࡒࡢࡍࡉ့࠭"), bstack1lll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡂࡒࡓࠫး")],
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯္ࠫ"): bstack1lll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡖࡈࡐࡥࡌࡐࡉࡏࡉ࡛ࡋࡌࠨ်"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨျ"): bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡆ࡛ࡔࡐࡏࡄࡘࡎࡕࡎࠨြ"),
  bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪွ"): bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡔࡈࡓࡆࡔ࡙ࡅࡇࡏࡌࡊࡖ࡜ࠫှ")
}
bstack11l11l111_opy_ = {
  bstack1lll1l1_opy_ (u"ࠨࡷࡶࡩࡷࡔࡡ࡮ࡧࠪဿ"): [bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡷࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ၀"), bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡸࡷࡪࡸࡎࡢ࡯ࡨࠫ၁")],
  bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧ၂"): [bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡣࡰ࡫ࡹࠨ၃"), bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷࡐ࡫ࡹࠨ၄")],
  bstack1lll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ၅"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ၆"),
  bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ၇"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ၈"),
  bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭၉"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭၊"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭။"): [bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡰࡱࡲࠪ၌"), bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ၍")],
  bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡍࡱࡦࡥࡱ࠭၎"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰࡯ࡳࡨࡧ࡬ࠨ၏"),
  bstack1lll1l1_opy_ (u"ࠫࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨၐ"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡷ࡫ࡲࡶࡰࡗࡩࡸࡺࡳࠨၑ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࠪၒ"): bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡱࡲࠪၓ"),
  bstack1lll1l1_opy_ (u"ࠨ࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪၔ"): bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯࡮ࡲ࡫ࡑ࡫ࡶࡦ࡮ࠪၕ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧၖ"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧၗ")
}
bstack111111l1_opy_ = {
  bstack1lll1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨၘ"): bstack1lll1l1_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪၙ"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩၚ"): [bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪၛ"), bstack1lll1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬၜ")],
  bstack1lll1l1_opy_ (u"ࠪࡷࡪࡹࡳࡪࡱࡱࡒࡦࡳࡥࠨၝ"): bstack1lll1l1_opy_ (u"ࠫࡳࡧ࡭ࡦࠩၞ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩၟ"): bstack1lll1l1_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ၠ"),
  bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬၡ"): [bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩၢ"), bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨၣ")],
  bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫၤ"): bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ၥ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩၦ"): bstack1lll1l1_opy_ (u"࠭ࡲࡦࡣ࡯ࡣࡲࡵࡢࡪ࡮ࡨࠫၧ"),
  bstack1lll1l1_opy_ (u"ࠧࡢࡲࡳ࡭ࡺࡳࡖࡦࡴࡶ࡭ࡴࡴࠧၨ"): [bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡲࡳ࡭ࡺࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨၩ"), bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵ࡯ࡵ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠪၪ")],
  bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡱࡶࡌࡲࡸ࡫ࡣࡶࡴࡨࡇࡪࡸࡴࡴࠩၫ"): [bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡗࡸࡲࡃࡦࡴࡷࡷࠬၬ"), bstack1lll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡳࡸࡘࡹ࡬ࡄࡧࡵࡸࠬၭ")]
}
bstack1ll1111111_opy_ = [
  bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡴࡹࡏ࡮ࡴࡧࡦࡹࡷ࡫ࡃࡦࡴࡷࡷࠬၮ"),
  bstack1lll1l1_opy_ (u"ࠧࡱࡣࡪࡩࡑࡵࡡࡥࡕࡷࡶࡦࡺࡥࡨࡻࠪၯ"),
  bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࠧၰ"),
  bstack1lll1l1_opy_ (u"ࠩࡶࡩࡹ࡝ࡩ࡯ࡦࡲࡻࡗ࡫ࡣࡵࠩၱ"),
  bstack1lll1l1_opy_ (u"ࠪࡸ࡮ࡳࡥࡰࡷࡷࡷࠬၲ"),
  bstack1lll1l1_opy_ (u"ࠫࡸࡺࡲࡪࡥࡷࡊ࡮ࡲࡥࡊࡰࡷࡩࡷࡧࡣࡵࡣࡥ࡭ࡱ࡯ࡴࡺࠩၳ"),
  bstack1lll1l1_opy_ (u"ࠬࡻ࡮ࡩࡣࡱࡨࡱ࡫ࡤࡑࡴࡲࡱࡵࡺࡂࡦࡪࡤࡺ࡮ࡵࡲࠨၴ"),
  bstack1lll1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫၵ"),
  bstack1lll1l1_opy_ (u"ࠧ࡮ࡱࡽ࠾࡫࡯ࡲࡦࡨࡲࡼࡔࡶࡴࡪࡱࡱࡷࠬၶ"),
  bstack1lll1l1_opy_ (u"ࠨ࡯ࡶ࠾ࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩၷ"),
  bstack1lll1l1_opy_ (u"ࠩࡶࡩ࠿࡯ࡥࡐࡲࡷ࡭ࡴࡴࡳࠨၸ"),
  bstack1lll1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫࠱ࡳࡵࡺࡩࡰࡰࡶࠫၹ"),
]
bstack111lll111_opy_ = [
  bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡏࡳࡨࡧ࡬ࠨၺ"),
  bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩၻ"),
  bstack1lll1l1_opy_ (u"࠭࡬ࡰࡥࡤࡰࡔࡶࡴࡪࡱࡱࡷࠬၼ"),
  bstack1lll1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧၽ"),
  bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫၾ"),
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡒࡥࡷࡧ࡯ࠫၿ"),
  bstack1lll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ႀ"),
  bstack1lll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡵࡓࡶࡴࡾࡹࠨႁ"),
  bstack1lll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨႂ"),
  bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡇࡴࡴࡴࡦࡺࡷࡓࡵࡺࡩࡰࡰࡶࠫႃ"),
  bstack1lll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫႄ"),
  bstack1lll1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡗࡣࡵ࡭ࡦࡨ࡬ࡦࡵࠪႅ"),
  bstack1lll1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡖࡤ࡫ࠬႆ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧႇ"),
  bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ႈ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥࡳࡷࡱࡘࡪࡹࡴࡴࠩႉ"),
  bstack1lll1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠵ࠬႊ"),
  bstack1lll1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠷࠭ႋ"),
  bstack1lll1l1_opy_ (u"ࠨࡅࡘࡗ࡙ࡕࡍࡠࡖࡄࡋࡤ࠹ࠧႌ"),
  bstack1lll1l1_opy_ (u"ࠩࡆ࡙ࡘ࡚ࡏࡎࡡࡗࡅࡌࡥ࠴ࠨႍ"),
  bstack1lll1l1_opy_ (u"ࠪࡇ࡚࡙ࡔࡐࡏࡢࡘࡆࡍ࡟࠶ࠩႎ"),
  bstack1lll1l1_opy_ (u"ࠫࡈ࡛ࡓࡕࡑࡐࡣ࡙ࡇࡇࡠ࠸ࠪႏ"),
  bstack1lll1l1_opy_ (u"ࠬࡉࡕࡔࡖࡒࡑࡤ࡚ࡁࡈࡡ࠺ࠫ႐"),
  bstack1lll1l1_opy_ (u"࠭ࡃࡖࡕࡗࡓࡒࡥࡔࡂࡉࡢ࠼ࠬ႑"),
  bstack1lll1l1_opy_ (u"ࠧࡄࡗࡖࡘࡔࡓ࡟ࡕࡃࡊࡣ࠾࠭႒"),
  bstack1lll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ႓"),
  bstack1lll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ႔"),
  bstack1lll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࡅࡤࡴࡹࡻࡲࡦࡏࡲࡨࡪ࠭႕"),
  bstack1lll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭႖")
]
bstack111ll1l111_opy_ = [
  bstack1lll1l1_opy_ (u"ࠬࡻࡰ࡭ࡱࡤࡨࡒ࡫ࡤࡪࡣࠪ႗"),
  bstack1lll1l1_opy_ (u"࠭ࡵࡴࡧࡵࡒࡦࡳࡥࠨ႘"),
  bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡋࡦࡻࠪ႙"),
  bstack1lll1l1_opy_ (u"ࠨࡵࡨࡷࡸ࡯࡯࡯ࡐࡤࡱࡪ࠭ႚ"),
  bstack1lll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡐࡳ࡫ࡲࡶ࡮ࡺࡹࠨႛ"),
  bstack1lll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ႜ"),
  bstack1lll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡗࡥ࡬࠭ႝ"),
  bstack1lll1l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ႞"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ႟"),
  bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬႠ"),
  bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩႡ"),
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࠨႢ"),
  bstack1lll1l1_opy_ (u"ࠪࡳࡸ࠭Ⴃ"),
  bstack1lll1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧႤ"),
  bstack1lll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡶࠫႥ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡶࡶࡲ࡛ࡦ࡯ࡴࠨႦ"),
  bstack1lll1l1_opy_ (u"ࠧࡳࡧࡪ࡭ࡴࡴࠧႧ"),
  bstack1lll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࢀ࡯࡯ࡧࠪႨ"),
  bstack1lll1l1_opy_ (u"ࠩࡰࡥࡨ࡮ࡩ࡯ࡧࠪႩ"),
  bstack1lll1l1_opy_ (u"ࠪࡶࡪࡹ࡯࡭ࡷࡷ࡭ࡴࡴࠧႪ"),
  bstack1lll1l1_opy_ (u"ࠫ࡮ࡪ࡬ࡦࡖ࡬ࡱࡪࡵࡵࡵࠩႫ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡔࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩႬ"),
  bstack1lll1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳࠬႭ"),
  bstack1lll1l1_opy_ (u"ࠧ࡯ࡱࡓࡥ࡬࡫ࡌࡰࡣࡧࡘ࡮ࡳࡥࡰࡷࡷࠫႮ"),
  bstack1lll1l1_opy_ (u"ࠨࡤࡩࡧࡦࡩࡨࡦࠩႯ"),
  bstack1lll1l1_opy_ (u"ࠩࡧࡩࡧࡻࡧࠨႰ"),
  bstack1lll1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯ࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡹࠧႱ"),
  bstack1lll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰࡗࡪࡴࡤࡌࡧࡼࡷࠬႲ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥࡢ࡮ࡐࡳࡧ࡯࡬ࡦࠩႳ"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡰࡒ࡬ࡴࡪࡲࡩ࡯ࡧࠪႴ"),
  bstack1lll1l1_opy_ (u"ࠧࡤࡪࡨࡧࡰ࡛ࡒࡍࠩႵ"),
  bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪႶ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡰࡵࡅࡲࡳࡰ࡯ࡥࡴࠩႷ"),
  bstack1lll1l1_opy_ (u"ࠪࡧࡦࡶࡴࡶࡴࡨࡇࡷࡧࡳࡩࠩႸ"),
  bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨႹ"),
  bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱ࡫ࡸࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬႺ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰ࡙ࡩࡷࡹࡩࡰࡰࠪႻ"),
  bstack1lll1l1_opy_ (u"ࠧ࡯ࡱࡅࡰࡦࡴ࡫ࡑࡱ࡯ࡰ࡮ࡴࡧࠨႼ"),
  bstack1lll1l1_opy_ (u"ࠨ࡯ࡤࡷࡰ࡙ࡥ࡯ࡦࡎࡩࡾࡹࠧႽ"),
  bstack1lll1l1_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡎࡲ࡫ࡸ࠭Ⴞ"),
  bstack1lll1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡌࡨࠬႿ"),
  bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡤࡪࡥࡤࡸࡪࡪࡄࡦࡸ࡬ࡧࡪ࠭Ⴠ"),
  bstack1lll1l1_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡕࡧࡲࡢ࡯ࡶࠫჁ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡩࡱࡱࡩࡓࡻ࡭ࡣࡧࡵࠫჂ"),
  bstack1lll1l1_opy_ (u"ࠧ࡯ࡧࡷࡻࡴࡸ࡫ࡍࡱࡪࡷࠬჃ"),
  bstack1lll1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡎࡲ࡫ࡸࡕࡰࡵ࡫ࡲࡲࡸ࠭Ⴤ"),
  bstack1lll1l1_opy_ (u"ࠩࡦࡳࡳࡹ࡯࡭ࡧࡏࡳ࡬ࡹࠧჅ"),
  bstack1lll1l1_opy_ (u"ࠪࡹࡸ࡫ࡗ࠴ࡅࠪ჆"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡶࡰࡪࡷࡰࡐࡴ࡭ࡳࠨჇ"),
  bstack1lll1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡇ࡯࡯࡮ࡧࡷࡶ࡮ࡩࠧ჈"),
  bstack1lll1l1_opy_ (u"࠭ࡶࡪࡦࡨࡳ࡛࠸ࠧ჉"),
  bstack1lll1l1_opy_ (u"ࠧ࡮࡫ࡧࡗࡪࡹࡳࡪࡱࡱࡍࡳࡹࡴࡢ࡮࡯ࡅࡵࡶࡳࠨ჊"),
  bstack1lll1l1_opy_ (u"ࠨࡧࡶࡴࡷ࡫ࡳࡴࡱࡖࡩࡷࡼࡥࡳࠩ჋"),
  bstack1lll1l1_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࡐࡴ࡭ࡳࠨ჌"),
  bstack1lll1l1_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࡈࡪࡰࠨჍ"),
  bstack1lll1l1_opy_ (u"ࠫࡹ࡫࡬ࡦ࡯ࡨࡸࡷࡿࡌࡰࡩࡶࠫ჎"),
  bstack1lll1l1_opy_ (u"ࠬࡹࡹ࡯ࡥࡗ࡭ࡲ࡫ࡗࡪࡶ࡫ࡒ࡙ࡖࠧ჏"),
  bstack1lll1l1_opy_ (u"࠭ࡧࡦࡱࡏࡳࡨࡧࡴࡪࡱࡱࠫა"),
  bstack1lll1l1_opy_ (u"ࠧࡨࡲࡶࡐࡴࡩࡡࡵ࡫ࡲࡲࠬბ"),
  bstack1lll1l1_opy_ (u"ࠨࡰࡨࡸࡼࡵࡲ࡬ࡒࡵࡳ࡫࡯࡬ࡦࠩგ"),
  bstack1lll1l1_opy_ (u"ࠩࡦࡹࡸࡺ࡯࡮ࡐࡨࡸࡼࡵࡲ࡬ࠩდ"),
  bstack1lll1l1_opy_ (u"ࠪࡪࡴࡸࡣࡦࡅ࡫ࡥࡳ࡭ࡥࡋࡣࡵࠫე"),
  bstack1lll1l1_opy_ (u"ࠫࡽࡳࡳࡋࡣࡵࠫვ"),
  bstack1lll1l1_opy_ (u"ࠬࡾ࡭ࡹࡌࡤࡶࠬზ"),
  bstack1lll1l1_opy_ (u"࠭࡭ࡢࡵ࡮ࡇࡴࡳ࡭ࡢࡰࡧࡷࠬთ"),
  bstack1lll1l1_opy_ (u"ࠧ࡮ࡣࡶ࡯ࡇࡧࡳࡪࡥࡄࡹࡹ࡮ࠧი"),
  bstack1lll1l1_opy_ (u"ࠨࡹࡶࡐࡴࡩࡡ࡭ࡕࡸࡴࡵࡵࡲࡵࠩკ"),
  bstack1lll1l1_opy_ (u"ࠩࡧ࡭ࡸࡧࡢ࡭ࡧࡆࡳࡷࡹࡒࡦࡵࡷࡶ࡮ࡩࡴࡪࡱࡱࡷࠬლ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶࡖࡦࡴࡶ࡭ࡴࡴࠧმ"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡲࡷࡍࡳࡹࡥࡤࡷࡵࡩࡈ࡫ࡲࡵࡵࠪნ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥࡴ࡫ࡪࡲࡆࡶࡰࠨო"),
  bstack1lll1l1_opy_ (u"࠭ࡤࡪࡵࡤࡦࡱ࡫ࡁ࡯࡫ࡰࡥࡹ࡯࡯࡯ࡵࠪპ"),
  bstack1lll1l1_opy_ (u"ࠧࡤࡣࡱࡥࡷࡿࠧჟ"),
  bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡶࡪ࡬࡯ࡹࠩრ"),
  bstack1lll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩს"),
  bstack1lll1l1_opy_ (u"ࠪ࡭ࡪ࠭ტ"),
  bstack1lll1l1_opy_ (u"ࠫࡪࡪࡧࡦࠩუ"),
  bstack1lll1l1_opy_ (u"ࠬࡹࡡࡧࡣࡵ࡭ࠬფ"),
  bstack1lll1l1_opy_ (u"࠭ࡱࡶࡧࡸࡩࠬქ"),
  bstack1lll1l1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡴࡡ࡭ࠩღ"),
  bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴࡘࡺ࡯ࡳࡧࡆࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠩყ"),
  bstack1lll1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡅࡤࡱࡪࡸࡡࡊ࡯ࡤ࡫ࡪࡏ࡮࡫ࡧࡦࡸ࡮ࡵ࡮ࠨშ"),
  bstack1lll1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡐࡴ࡭ࡳࡆࡺࡦࡰࡺࡪࡥࡉࡱࡶࡸࡸ࠭ჩ"),
  bstack1lll1l1_opy_ (u"ࠫࡳ࡫ࡴࡸࡱࡵ࡯ࡑࡵࡧࡴࡋࡱࡧࡱࡻࡤࡦࡊࡲࡷࡹࡹࠧც"),
  bstack1lll1l1_opy_ (u"ࠬࡻࡰࡥࡣࡷࡩࡆࡶࡰࡔࡧࡷࡸ࡮ࡴࡧࡴࠩძ"),
  bstack1lll1l1_opy_ (u"࠭ࡲࡦࡵࡨࡶࡻ࡫ࡄࡦࡸ࡬ࡧࡪ࠭წ"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧჭ"),
  bstack1lll1l1_opy_ (u"ࠨࡵࡨࡲࡩࡑࡥࡺࡵࠪხ"),
  bstack1lll1l1_opy_ (u"ࠩࡨࡲࡦࡨ࡬ࡦࡒࡤࡷࡸࡩ࡯ࡥࡧࠪჯ"),
  bstack1lll1l1_opy_ (u"ࠪࡹࡵࡪࡡࡵࡧࡌࡳࡸࡊࡥࡷ࡫ࡦࡩࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ჰ"),
  bstack1lll1l1_opy_ (u"ࠫࡪࡴࡡࡣ࡮ࡨࡅࡺࡪࡩࡰࡋࡱ࡮ࡪࡩࡴࡪࡱࡱࠫჱ"),
  bstack1lll1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡆࡶࡰ࡭ࡧࡓࡥࡾ࠭ჲ"),
  bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧჳ"),
  bstack1lll1l1_opy_ (u"ࠧࡸࡦ࡬ࡳࡘ࡫ࡲࡷ࡫ࡦࡩࠬჴ"),
  bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡓࡅࡍࠪჵ"),
  bstack1lll1l1_opy_ (u"ࠩࡳࡶࡪࡼࡥ࡯ࡶࡆࡶࡴࡹࡳࡔ࡫ࡷࡩ࡙ࡸࡡࡤ࡭࡬ࡲ࡬࠭ჶ"),
  bstack1lll1l1_opy_ (u"ࠪ࡬࡮࡭ࡨࡄࡱࡱࡸࡷࡧࡳࡵࠩჷ"),
  bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡔࡷ࡫ࡦࡦࡴࡨࡲࡨ࡫ࡳࠨჸ"),
  bstack1lll1l1_opy_ (u"ࠬ࡫࡮ࡢࡤ࡯ࡩࡘ࡯࡭ࠨჹ"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡪ࡯ࡒࡴࡹ࡯࡯࡯ࡵࠪჺ"),
  bstack1lll1l1_opy_ (u"ࠧࡳࡧࡰࡳࡻ࡫ࡉࡐࡕࡄࡴࡵ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࡌࡰࡥࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬ჻"),
  bstack1lll1l1_opy_ (u"ࠨࡪࡲࡷࡹࡔࡡ࡮ࡧࠪჼ"),
  bstack1lll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫჽ"),
  bstack1lll1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࠬჾ"),
  bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪჿ"),
  bstack1lll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᄀ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡢࡩࡨࡐࡴࡧࡤࡔࡶࡵࡥࡹ࡫ࡧࡺࠩᄁ"),
  bstack1lll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࠭ᄂ"),
  bstack1lll1l1_opy_ (u"ࠨࡶ࡬ࡱࡪࡵࡵࡵࡵࠪᄃ"),
  bstack1lll1l1_opy_ (u"ࠩࡸࡲ࡭ࡧ࡮ࡥ࡮ࡨࡨࡕࡸ࡯࡮ࡲࡷࡆࡪ࡮ࡡࡷ࡫ࡲࡶࠬᄄ")
]
bstack11lll11ll_opy_ = {
  bstack1lll1l1_opy_ (u"ࠪࡺࠬᄅ"): bstack1lll1l1_opy_ (u"ࠫࡻ࠭ᄆ"),
  bstack1lll1l1_opy_ (u"ࠬ࡬ࠧᄇ"): bstack1lll1l1_opy_ (u"࠭ࡦࠨᄈ"),
  bstack1lll1l1_opy_ (u"ࠧࡧࡱࡵࡧࡪ࠭ᄉ"): bstack1lll1l1_opy_ (u"ࠨࡨࡲࡶࡨ࡫ࠧᄊ"),
  bstack1lll1l1_opy_ (u"ࠩࡲࡲࡱࡿࡡࡶࡶࡲࡱࡦࡺࡥࠨᄋ"): bstack1lll1l1_opy_ (u"ࠪࡳࡳࡲࡹࡂࡷࡷࡳࡲࡧࡴࡦࠩᄌ"),
  bstack1lll1l1_opy_ (u"ࠫ࡫ࡵࡲࡤࡧ࡯ࡳࡨࡧ࡬ࠨᄍ"): bstack1lll1l1_opy_ (u"ࠬ࡬࡯ࡳࡥࡨࡰࡴࡩࡡ࡭ࠩᄎ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽ࡭ࡵࡳࡵࠩᄏ"): bstack1lll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾࡎ࡯ࡴࡶࠪᄐ"),
  bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡰࡰࡴࡷࠫᄑ"): bstack1lll1l1_opy_ (u"ࠩࡳࡶࡴࡾࡹࡑࡱࡵࡸࠬᄒ"),
  bstack1lll1l1_opy_ (u"ࠪࡴࡷࡵࡸࡺࡷࡶࡩࡷ࠭ᄓ"): bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᄔ"),
  bstack1lll1l1_opy_ (u"ࠬࡶࡲࡰࡺࡼࡴࡦࡹࡳࠨᄕ"): bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡕࡧࡳࡴࠩᄖ"),
  bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼ࡬ࡴࡹࡴࠨᄗ"): bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽࡍࡵࡳࡵࠩᄘ"),
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡱࡴࡲࡼࡾࡶ࡯ࡳࡶࠪᄙ"): bstack1lll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡰࡴࡷࠫᄚ"),
  bstack1lll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡶࡵࡨࡶࠬᄛ"): bstack1lll1l1_opy_ (u"ࠬ࠳࡬ࡰࡥࡤࡰࡕࡸ࡯ࡹࡻࡘࡷࡪࡸࠧᄜ"),
  bstack1lll1l1_opy_ (u"࠭࠭࡭ࡱࡦࡥࡱࡶࡲࡰࡺࡼࡹࡸ࡫ࡲࠨᄝ"): bstack1lll1l1_opy_ (u"ࠧ࠮࡮ࡲࡧࡦࡲࡐࡳࡱࡻࡽ࡚ࡹࡥࡳࠩᄞ"),
  bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡰࡳࡱࡻࡽࡵࡧࡳࡴࠩᄟ"): bstack1lll1l1_opy_ (u"ࠩ࠰ࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫᄠ"),
  bstack1lll1l1_opy_ (u"ࠪ࠱ࡱࡵࡣࡢ࡮ࡳࡶࡴࡾࡹࡱࡣࡶࡷࠬᄡ"): bstack1lll1l1_opy_ (u"ࠫ࠲ࡲ࡯ࡤࡣ࡯ࡔࡷࡵࡸࡺࡒࡤࡷࡸ࠭ᄢ"),
  bstack1lll1l1_opy_ (u"ࠬࡨࡩ࡯ࡣࡵࡽࡵࡧࡴࡩࠩᄣ"): bstack1lll1l1_opy_ (u"࠭ࡢࡪࡰࡤࡶࡾࡶࡡࡵࡪࠪᄤ"),
  bstack1lll1l1_opy_ (u"ࠧࡱࡣࡦࡪ࡮ࡲࡥࠨᄥ"): bstack1lll1l1_opy_ (u"ࠨ࠯ࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄦ"),
  bstack1lll1l1_opy_ (u"ࠩࡳࡥࡨ࠳ࡦࡪ࡮ࡨࠫᄧ"): bstack1lll1l1_opy_ (u"ࠪ࠱ࡵࡧࡣ࠮ࡨ࡬ࡰࡪ࠭ᄨ"),
  bstack1lll1l1_opy_ (u"ࠫ࠲ࡶࡡࡤ࠯ࡩ࡭ࡱ࡫ࠧᄩ"): bstack1lll1l1_opy_ (u"ࠬ࠳ࡰࡢࡥ࠰ࡪ࡮ࡲࡥࠨᄪ"),
  bstack1lll1l1_opy_ (u"࠭࡬ࡰࡩࡩ࡭ࡱ࡫ࠧᄫ"): bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡪࡪ࡮ࡲࡥࠨᄬ"),
  bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡲࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪᄭ"): bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫᄮ"),
}
bstack111ll1ll1l_opy_ = bstack1lll1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴ࠼࠲࠳࡬࡯ࡴࡩࡷࡥ࠲ࡨࡵ࡭࠰ࡲࡨࡶࡨࡿ࠯ࡤ࡮࡬࠳ࡷ࡫࡬ࡦࡣࡶࡩࡸ࠵࡬ࡢࡶࡨࡷࡹ࠵ࡤࡰࡹࡱࡰࡴࡧࡤࠣᄯ")
bstack111l1lllll_opy_ = bstack1lll1l1_opy_ (u"ࠦ࠴ࡶࡥࡳࡥࡼ࠳࡭࡫ࡡ࡭ࡶ࡫ࡧ࡭࡫ࡣ࡬ࠤᄰ")
bstack1l11l1l1l_opy_ = bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡷࡥ࠱࡫ࡹࡧ࠭ᄱ")
bstack1lll11l1l_opy_ = bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳ࠾࠴࠵ࡨࡶࡤ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲࡀ࠸࠱࠱ࡺࡨ࠴࡮ࡵࡣࠩᄲ")
bstack11ll1ll11_opy_ = bstack1lll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡀ࠯࠰ࡪࡸࡦ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡨࡵ࡭࠰ࡰࡨࡼࡹࡥࡨࡶࡤࡶࠫᄳ")
bstack111ll111l1_opy_ = {
  bstack1lll1l1_opy_ (u"ࠨࡥࡵ࡭ࡹ࡯ࡣࡢ࡮ࠪᄴ"): 50,
  bstack1lll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᄵ"): 40,
  bstack1lll1l1_opy_ (u"ࠪࡻࡦࡸ࡮ࡪࡰࡪࠫᄶ"): 30,
  bstack1lll1l1_opy_ (u"ࠫ࡮ࡴࡦࡰࠩᄷ"): 20,
  bstack1lll1l1_opy_ (u"ࠬࡪࡥࡣࡷࡪࠫᄸ"): 10
}
bstack1llll111_opy_ = bstack111ll111l1_opy_[bstack1lll1l1_opy_ (u"࠭ࡩ࡯ࡨࡲࠫᄹ")]
bstack1ll1l1ll11_opy_ = bstack1lll1l1_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᄺ")
bstack1ll1lll1l_opy_ = bstack1lll1l1_opy_ (u"ࠨࡴࡲࡦࡴࡺ࠭ࡱࡻࡷ࡬ࡴࡴࡡࡨࡧࡱࡸ࠴࠭ᄻ")
bstack1ll1llll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦ࠯ࡳࡽࡹ࡮࡯࡯ࡣࡪࡩࡳࡺ࠯ࠨᄼ")
bstack1lll1lll1_opy_ = bstack1lll1l1_opy_ (u"ࠪࡴࡾࡺࡥࡴࡶ࠰ࡴࡾࡺࡨࡰࡰࡤ࡫ࡪࡴࡴ࠰ࠩᄽ")
bstack1111llll_opy_ = bstack1lll1l1_opy_ (u"ࠫࡕࡲࡥࡢࡵࡨࠤ࡮ࡴࡳࡵࡣ࡯ࡰࠥࡶࡹࡵࡧࡶࡸࠥࡧ࡮ࡥࠢࡳࡽࡹ࡫ࡳࡵ࠯ࡶࡩࡱ࡫࡮ࡪࡷࡰࠤࡵࡧࡣ࡬ࡣࡪࡩࡸ࠴ࠠࡡࡲ࡬ࡴࠥ࡯࡮ࡴࡶࡤࡰࡱࠦࡰࡺࡶࡨࡷࡹࠦࡰࡺࡶࡨࡷࡹ࠳ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࡡࠩᄾ")
bstack111ll1l1l1_opy_ = [bstack1lll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᄿ"), bstack1lll1l1_opy_ (u"࡙࠭ࡐࡗࡕࡣ࡚࡙ࡅࡓࡐࡄࡑࡊ࠭ᅀ")]
bstack111ll11ll1_opy_ = [bstack1lll1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᅁ"), bstack1lll1l1_opy_ (u"ࠨ࡛ࡒ࡙ࡗࡥࡁࡄࡅࡈࡗࡘࡥࡋࡆ࡛ࠪᅂ")]
bstack11lllllll_opy_ = re.compile(bstack1lll1l1_opy_ (u"ࠩࡡ࡟ࡡࡢࡷ࠮࡟࠮࠾࠳࠰ࠤࠨᅃ"))
bstack1l111llll1_opy_ = [
  bstack1lll1l1_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࡎࡢ࡯ࡨࠫᅄ"),
  bstack1lll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᅅ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᅆ"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡦࡹࡆࡳࡲࡳࡡ࡯ࡦࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅇ"),
  bstack1lll1l1_opy_ (u"ࠧࡢࡲࡳࠫᅈ"),
  bstack1lll1l1_opy_ (u"ࠨࡷࡧ࡭ࡩ࠭ᅉ"),
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᅊ"),
  bstack1lll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡧࠪᅋ"),
  bstack1lll1l1_opy_ (u"ࠫࡴࡸࡩࡦࡰࡷࡥࡹ࡯࡯࡯ࠩᅌ"),
  bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡱ࡚ࡩࡧࡼࡩࡦࡹࠪᅍ"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡰࡔࡨࡷࡪࡺࠧᅎ"), bstack1lll1l1_opy_ (u"ࠧࡧࡷ࡯ࡰࡗ࡫ࡳࡦࡶࠪᅏ"),
  bstack1lll1l1_opy_ (u"ࠨࡥ࡯ࡩࡦࡸࡓࡺࡵࡷࡩࡲࡌࡩ࡭ࡧࡶࠫᅐ"),
  bstack1lll1l1_opy_ (u"ࠩࡨࡺࡪࡴࡴࡕ࡫ࡰ࡭ࡳ࡭ࡳࠨᅑ"),
  bstack1lll1l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧࡓࡩࡷ࡬࡯ࡳ࡯ࡤࡲࡨ࡫ࡌࡰࡩࡪ࡭ࡳ࡭ࠧᅒ"),
  bstack1lll1l1_opy_ (u"ࠫࡴࡺࡨࡦࡴࡄࡴࡵࡹࠧᅓ"),
  bstack1lll1l1_opy_ (u"ࠬࡶࡲࡪࡰࡷࡔࡦ࡭ࡥࡔࡱࡸࡶࡨ࡫ࡏ࡯ࡈ࡬ࡲࡩࡌࡡࡪ࡮ࡸࡶࡪ࠭ᅔ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡱࡲࡄࡧࡹ࡯ࡶࡪࡶࡼࠫᅕ"), bstack1lll1l1_opy_ (u"ࠧࡢࡲࡳࡔࡦࡩ࡫ࡢࡩࡨࠫᅖ"), bstack1lll1l1_opy_ (u"ࠨࡣࡳࡴ࡜ࡧࡩࡵࡃࡦࡸ࡮ࡼࡩࡵࡻࠪᅗ"), bstack1lll1l1_opy_ (u"ࠩࡤࡴࡵ࡝ࡡࡪࡶࡓࡥࡨࡱࡡࡨࡧࠪᅘ"), bstack1lll1l1_opy_ (u"ࠪࡥࡵࡶࡗࡢ࡫ࡷࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᅙ"),
  bstack1lll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡖࡪࡧࡤࡺࡖ࡬ࡱࡪࡵࡵࡵࠩᅚ"),
  bstack1lll1l1_opy_ (u"ࠬࡧ࡬࡭ࡱࡺࡘࡪࡹࡴࡑࡣࡦ࡯ࡦ࡭ࡥࡴࠩᅛ"),
  bstack1lll1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࡃࡰࡸࡨࡶࡦ࡭ࡥࠨᅜ"), bstack1lll1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࡄࡱࡹࡩࡷࡧࡧࡦࡇࡱࡨࡎࡴࡴࡦࡰࡷࠫᅝ"),
  bstack1lll1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࡆࡨࡺ࡮ࡩࡥࡓࡧࡤࡨࡾ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᅞ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡨࡧࡖ࡯ࡳࡶࠪᅟ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡈࡪࡼࡩࡤࡧࡖࡳࡨࡱࡥࡵࠩᅠ"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࡎࡴࡳࡵࡣ࡯ࡰ࡙࡯࡭ࡦࡱࡸࡸࠬᅡ"),
  bstack1lll1l1_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩࡏ࡮ࡴࡶࡤࡰࡱࡖࡡࡵࡪࠪᅢ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡷࡦࠪᅣ"), bstack1lll1l1_opy_ (u"ࠧࡢࡸࡧࡐࡦࡻ࡮ࡤࡪࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅤ"), bstack1lll1l1_opy_ (u"ࠨࡣࡹࡨࡗ࡫ࡡࡥࡻࡗ࡭ࡲ࡫࡯ࡶࡶࠪᅥ"), bstack1lll1l1_opy_ (u"ࠩࡤࡺࡩࡇࡲࡨࡵࠪᅦ"),
  bstack1lll1l1_opy_ (u"ࠪࡹࡸ࡫ࡋࡦࡻࡶࡸࡴࡸࡥࠨᅧ"), bstack1lll1l1_opy_ (u"ࠫࡰ࡫ࡹࡴࡶࡲࡶࡪࡖࡡࡵࡪࠪᅨ"), bstack1lll1l1_opy_ (u"ࠬࡱࡥࡺࡵࡷࡳࡷ࡫ࡐࡢࡵࡶࡻࡴࡸࡤࠨᅩ"),
  bstack1lll1l1_opy_ (u"࠭࡫ࡦࡻࡄࡰ࡮ࡧࡳࠨᅪ"), bstack1lll1l1_opy_ (u"ࠧ࡬ࡧࡼࡔࡦࡹࡳࡸࡱࡵࡨࠬᅫ"),
  bstack1lll1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡅࡹࡧࡦࡹࡹࡧࡢ࡭ࡧࠪᅬ"), bstack1lll1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡦࡵ࡭ࡻ࡫ࡲࡂࡴࡪࡷࠬᅭ"), bstack1lll1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡧࡶ࡮ࡼࡥࡳࡇࡻࡩࡨࡻࡴࡢࡤ࡯ࡩࡉ࡯ࡲࠨᅮ"), bstack1lll1l1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡨࡷ࡯ࡶࡦࡴࡆ࡬ࡷࡵ࡭ࡦࡏࡤࡴࡵ࡯࡮ࡨࡈ࡬ࡰࡪ࠭ᅯ"), bstack1lll1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡩࡸࡩࡷࡧࡵ࡙ࡸ࡫ࡓࡺࡵࡷࡩࡲࡋࡸࡦࡥࡸࡸࡦࡨ࡬ࡦࠩᅰ"),
  bstack1lll1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡪࡲࡪࡸࡨࡶࡕࡵࡲࡵࠩᅱ"), bstack1lll1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡤࡳ࡫ࡹࡩࡷࡖ࡯ࡳࡶࡶࠫᅲ"),
  bstack1lll1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡥࡴ࡬ࡺࡪࡸࡄࡪࡵࡤࡦࡱ࡫ࡂࡶ࡫࡯ࡨࡈ࡮ࡥࡤ࡭ࠪᅳ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵࡗࡦࡤࡹ࡭ࡪࡽࡔࡪ࡯ࡨࡳࡺࡺࠧᅴ"),
  bstack1lll1l1_opy_ (u"ࠪ࡭ࡳࡺࡥ࡯ࡶࡄࡧࡹ࡯࡯࡯ࠩᅵ"), bstack1lll1l1_opy_ (u"ࠫ࡮ࡴࡴࡦࡰࡷࡇࡦࡺࡥࡨࡱࡵࡽࠬᅶ"), bstack1lll1l1_opy_ (u"ࠬ࡯࡮ࡵࡧࡱࡸࡋࡲࡡࡨࡵࠪᅷ"), bstack1lll1l1_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡧ࡬ࡊࡰࡷࡩࡳࡺࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᅸ"),
  bstack1lll1l1_opy_ (u"ࠧࡥࡱࡱࡸࡘࡺ࡯ࡱࡃࡳࡴࡔࡴࡒࡦࡵࡨࡸࠬᅹ"),
  bstack1lll1l1_opy_ (u"ࠨࡷࡱ࡭ࡨࡵࡤࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᅺ"), bstack1lll1l1_opy_ (u"ࠩࡵࡩࡸ࡫ࡴࡌࡧࡼࡦࡴࡧࡲࡥࠩᅻ"),
  bstack1lll1l1_opy_ (u"ࠪࡲࡴ࡙ࡩࡨࡰࠪᅼ"),
  bstack1lll1l1_opy_ (u"ࠫ࡮࡭࡮ࡰࡴࡨ࡙ࡳ࡯࡭ࡱࡱࡵࡸࡦࡴࡴࡗ࡫ࡨࡻࡸ࠭ᅽ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡇ࡮ࡥࡴࡲ࡭ࡩ࡝ࡡࡵࡥ࡫ࡩࡷࡹࠧᅾ"),
  bstack1lll1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᅿ"),
  bstack1lll1l1_opy_ (u"ࠧࡳࡧࡦࡶࡪࡧࡴࡦࡅ࡫ࡶࡴࡳࡥࡅࡴ࡬ࡺࡪࡸࡓࡦࡵࡶ࡭ࡴࡴࡳࠨᆀ"),
  bstack1lll1l1_opy_ (u"ࠨࡰࡤࡸ࡮ࡼࡥࡘࡧࡥࡗࡨࡸࡥࡦࡰࡶ࡬ࡴࡺࠧᆁ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࡖࡧࡷ࡫ࡥ࡯ࡵ࡫ࡳࡹࡖࡡࡵࡪࠪᆂ"),
  bstack1lll1l1_opy_ (u"ࠪࡲࡪࡺࡷࡰࡴ࡮ࡗࡵ࡫ࡥࡥࠩᆃ"),
  bstack1lll1l1_opy_ (u"ࠫ࡬ࡶࡳࡆࡰࡤࡦࡱ࡫ࡤࠨᆄ"),
  bstack1lll1l1_opy_ (u"ࠬ࡯ࡳࡉࡧࡤࡨࡱ࡫ࡳࡴࠩᆅ"),
  bstack1lll1l1_opy_ (u"࠭ࡡࡥࡤࡈࡼࡪࡩࡔࡪ࡯ࡨࡳࡺࡺࠧᆆ"),
  bstack1lll1l1_opy_ (u"ࠧ࡭ࡱࡦࡥࡱ࡫ࡓࡤࡴ࡬ࡴࡹ࠭ᆇ"),
  bstack1lll1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡊࡥࡷ࡫ࡦࡩࡎࡴࡩࡵ࡫ࡤࡰ࡮ࢀࡡࡵ࡫ࡲࡲࠬᆈ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵࡇࡳࡣࡱࡸࡕ࡫ࡲ࡮࡫ࡶࡷ࡮ࡵ࡮ࡴࠩᆉ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࡒࡦࡺࡵࡳࡣ࡯ࡓࡷ࡯ࡥ࡯ࡶࡤࡸ࡮ࡵ࡮ࠨᆊ"),
  bstack1lll1l1_opy_ (u"ࠫࡸࡿࡳࡵࡧࡰࡔࡴࡸࡴࠨᆋ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡆࡪࡢࡉࡱࡶࡸࠬᆌ"),
  bstack1lll1l1_opy_ (u"࠭ࡳ࡬࡫ࡳ࡙ࡳࡲ࡯ࡤ࡭ࠪᆍ"), bstack1lll1l1_opy_ (u"ࠧࡶࡰ࡯ࡳࡨࡱࡔࡺࡲࡨࠫᆎ"), bstack1lll1l1_opy_ (u"ࠨࡷࡱࡰࡴࡩ࡫ࡌࡧࡼࠫᆏ"),
  bstack1lll1l1_opy_ (u"ࠩࡤࡹࡹࡵࡌࡢࡷࡱࡧ࡭࠭ᆐ"),
  bstack1lll1l1_opy_ (u"ࠪࡷࡰ࡯ࡰࡍࡱࡪࡧࡦࡺࡃࡢࡲࡷࡹࡷ࡫ࠧᆑ"),
  bstack1lll1l1_opy_ (u"ࠫࡺࡴࡩ࡯ࡵࡷࡥࡱࡲࡏࡵࡪࡨࡶࡕࡧࡣ࡬ࡣࡪࡩࡸ࠭ᆒ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪ࡝ࡩ࡯ࡦࡲࡻࡆࡴࡩ࡮ࡣࡷ࡭ࡴࡴࠧᆓ"),
  bstack1lll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨ࡙ࡵ࡯࡭ࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᆔ"),
  bstack1lll1l1_opy_ (u"ࠧࡦࡰࡩࡳࡷࡩࡥࡂࡲࡳࡍࡳࡹࡴࡢ࡮࡯ࠫᆕ"),
  bstack1lll1l1_opy_ (u"ࠨࡧࡱࡷࡺࡸࡥࡘࡧࡥࡺ࡮࡫ࡷࡴࡊࡤࡺࡪࡖࡡࡨࡧࡶࠫᆖ"), bstack1lll1l1_opy_ (u"ࠩࡺࡩࡧࡼࡩࡦࡹࡇࡩࡻࡺ࡯ࡰ࡮ࡶࡔࡴࡸࡴࠨᆗ"), bstack1lll1l1_opy_ (u"ࠪࡩࡳࡧࡢ࡭ࡧ࡚ࡩࡧࡼࡩࡦࡹࡇࡩࡹࡧࡩ࡭ࡵࡆࡳࡱࡲࡥࡤࡶ࡬ࡳࡳ࠭ᆘ"),
  bstack1lll1l1_opy_ (u"ࠫࡷ࡫࡭ࡰࡶࡨࡅࡵࡶࡳࡄࡣࡦ࡬ࡪࡒࡩ࡮࡫ࡷࠫᆙ"),
  bstack1lll1l1_opy_ (u"ࠬࡩࡡ࡭ࡧࡱࡨࡦࡸࡆࡰࡴࡰࡥࡹ࠭ᆚ"),
  bstack1lll1l1_opy_ (u"࠭ࡢࡶࡰࡧࡰࡪࡏࡤࠨᆛ"),
  bstack1lll1l1_opy_ (u"ࠧ࡭ࡣࡸࡲࡨ࡮ࡔࡪ࡯ࡨࡳࡺࡺࠧᆜ"),
  bstack1lll1l1_opy_ (u"ࠨ࡮ࡲࡧࡦࡺࡩࡰࡰࡖࡩࡷࡼࡩࡤࡧࡶࡉࡳࡧࡢ࡭ࡧࡧࠫᆝ"), bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࡗࡪࡸࡶࡪࡥࡨࡷࡆࡻࡴࡩࡱࡵ࡭ࡿ࡫ࡤࠨᆞ"),
  bstack1lll1l1_opy_ (u"ࠪࡥࡺࡺ࡯ࡂࡥࡦࡩࡵࡺࡁ࡭ࡧࡵࡸࡸ࠭ᆟ"), bstack1lll1l1_opy_ (u"ࠫࡦࡻࡴࡰࡆ࡬ࡷࡲ࡯ࡳࡴࡃ࡯ࡩࡷࡺࡳࠨᆠ"),
  bstack1lll1l1_opy_ (u"ࠬࡴࡡࡵ࡫ࡹࡩࡎࡴࡳࡵࡴࡸࡱࡪࡴࡴࡴࡎ࡬ࡦࠬᆡ"),
  bstack1lll1l1_opy_ (u"࠭࡮ࡢࡶ࡬ࡺࡪ࡝ࡥࡣࡖࡤࡴࠬᆢ"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯ࡉ࡯࡫ࡷ࡭ࡦࡲࡕࡳ࡮ࠪᆣ"), bstack1lll1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡂ࡮࡯ࡳࡼࡖ࡯ࡱࡷࡳࡷࠬᆤ"), bstack1lll1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪࡋࡪࡲࡴࡸࡥࡇࡴࡤࡹࡩ࡝ࡡࡳࡰ࡬ࡲ࡬࠭ᆥ"), bstack1lll1l1_opy_ (u"ࠪࡷࡦ࡬ࡡࡳ࡫ࡒࡴࡪࡴࡌࡪࡰ࡮ࡷࡎࡴࡂࡢࡥ࡮࡫ࡷࡵࡵ࡯ࡦࠪᆦ"),
  bstack1lll1l1_opy_ (u"ࠫࡰ࡫ࡥࡱࡍࡨࡽࡈ࡮ࡡࡪࡰࡶࠫᆧ"),
  bstack1lll1l1_opy_ (u"ࠬࡲ࡯ࡤࡣ࡯࡭ࡿࡧࡢ࡭ࡧࡖࡸࡷ࡯࡮ࡨࡵࡇ࡭ࡷ࠭ᆨ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡦࡩࡸࡹࡁࡳࡩࡸࡱࡪࡴࡴࡴࠩᆩ"),
  bstack1lll1l1_opy_ (u"ࠧࡪࡰࡷࡩࡷࡑࡥࡺࡆࡨࡰࡦࡿࠧᆪ"),
  bstack1lll1l1_opy_ (u"ࠨࡵ࡫ࡳࡼࡏࡏࡔࡎࡲ࡫ࠬᆫ"),
  bstack1lll1l1_opy_ (u"ࠩࡶࡩࡳࡪࡋࡦࡻࡖࡸࡷࡧࡴࡦࡩࡼࠫᆬ"),
  bstack1lll1l1_opy_ (u"ࠪࡻࡪࡨ࡫ࡪࡶࡕࡩࡸࡶ࡯࡯ࡵࡨࡘ࡮ࡳࡥࡰࡷࡷࠫᆭ"), bstack1lll1l1_opy_ (u"ࠫࡸࡩࡲࡦࡧࡱࡷ࡭ࡵࡴࡘࡣ࡬ࡸ࡙࡯࡭ࡦࡱࡸࡸࠬᆮ"),
  bstack1lll1l1_opy_ (u"ࠬࡸࡥ࡮ࡱࡷࡩࡉ࡫ࡢࡶࡩࡓࡶࡴࡾࡹࠨᆯ"),
  bstack1lll1l1_opy_ (u"࠭ࡥ࡯ࡣࡥࡰࡪࡇࡳࡺࡰࡦࡉࡽ࡫ࡣࡶࡶࡨࡊࡷࡵ࡭ࡉࡶࡷࡴࡸ࠭ᆰ"),
  bstack1lll1l1_opy_ (u"ࠧࡴ࡭࡬ࡴࡑࡵࡧࡄࡣࡳࡸࡺࡸࡥࠨᆱ"),
  bstack1lll1l1_opy_ (u"ࠨࡹࡨࡦࡰ࡯ࡴࡅࡧࡥࡹ࡬ࡖࡲࡰࡺࡼࡔࡴࡸࡴࠨᆲ"),
  bstack1lll1l1_opy_ (u"ࠩࡩࡹࡱࡲࡃࡰࡰࡷࡩࡽࡺࡌࡪࡵࡷࠫᆳ"),
  bstack1lll1l1_opy_ (u"ࠪࡻࡦ࡯ࡴࡇࡱࡵࡅࡵࡶࡓࡤࡴ࡬ࡴࡹ࠭ᆴ"),
  bstack1lll1l1_opy_ (u"ࠫࡼ࡫ࡢࡷ࡫ࡨࡻࡈࡵ࡮࡯ࡧࡦࡸࡗ࡫ࡴࡳ࡫ࡨࡷࠬᆵ"),
  bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱࡐࡤࡱࡪ࠭ᆶ"),
  bstack1lll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡙ࡓࡍࡅࡨࡶࡹ࠭ᆷ"),
  bstack1lll1l1_opy_ (u"ࠧࡵࡣࡳ࡛࡮ࡺࡨࡔࡪࡲࡶࡹࡖࡲࡦࡵࡶࡈࡺࡸࡡࡵ࡫ࡲࡲࠬᆸ"),
  bstack1lll1l1_opy_ (u"ࠨࡵࡦࡥࡱ࡫ࡆࡢࡥࡷࡳࡷ࠭ᆹ"),
  bstack1lll1l1_opy_ (u"ࠩࡺࡨࡦࡒ࡯ࡤࡣ࡯ࡔࡴࡸࡴࠨᆺ"),
  bstack1lll1l1_opy_ (u"ࠪࡷ࡭ࡵࡷ࡙ࡥࡲࡨࡪࡒ࡯ࡨࠩᆻ"),
  bstack1lll1l1_opy_ (u"ࠫ࡮ࡵࡳࡊࡰࡶࡸࡦࡲ࡬ࡑࡣࡸࡷࡪ࠭ᆼ"),
  bstack1lll1l1_opy_ (u"ࠬࡾࡣࡰࡦࡨࡇࡴࡴࡦࡪࡩࡉ࡭ࡱ࡫ࠧᆽ"),
  bstack1lll1l1_opy_ (u"࠭࡫ࡦࡻࡦ࡬ࡦ࡯࡮ࡑࡣࡶࡷࡼࡵࡲࡥࠩᆾ"),
  bstack1lll1l1_opy_ (u"ࠧࡶࡵࡨࡔࡷ࡫ࡢࡶ࡫࡯ࡸ࡜ࡊࡁࠨᆿ"),
  bstack1lll1l1_opy_ (u"ࠨࡲࡵࡩࡻ࡫࡮ࡵ࡙ࡇࡅࡆࡺࡴࡢࡥ࡫ࡱࡪࡴࡴࡴࠩᇀ"),
  bstack1lll1l1_opy_ (u"ࠩࡺࡩࡧࡊࡲࡪࡸࡨࡶࡆ࡭ࡥ࡯ࡶࡘࡶࡱ࠭ᇁ"),
  bstack1lll1l1_opy_ (u"ࠪ࡯ࡪࡿࡣࡩࡣ࡬ࡲࡕࡧࡴࡩࠩᇂ"),
  bstack1lll1l1_opy_ (u"ࠫࡺࡹࡥࡏࡧࡺ࡛ࡉࡇࠧᇃ"),
  bstack1lll1l1_opy_ (u"ࠬࡽࡤࡢࡎࡤࡹࡳࡩࡨࡕ࡫ࡰࡩࡴࡻࡴࠨᇄ"), bstack1lll1l1_opy_ (u"࠭ࡷࡥࡣࡆࡳࡳࡴࡥࡤࡶ࡬ࡳࡳ࡚ࡩ࡮ࡧࡲࡹࡹ࠭ᇅ"),
  bstack1lll1l1_opy_ (u"ࠧࡹࡥࡲࡨࡪࡕࡲࡨࡋࡧࠫᇆ"), bstack1lll1l1_opy_ (u"ࠨࡺࡦࡳࡩ࡫ࡓࡪࡩࡱ࡭ࡳ࡭ࡉࡥࠩᇇ"),
  bstack1lll1l1_opy_ (u"ࠩࡸࡴࡩࡧࡴࡦࡦ࡚ࡈࡆࡈࡵ࡯ࡦ࡯ࡩࡎࡪࠧᇈ"),
  bstack1lll1l1_opy_ (u"ࠪࡶࡪࡹࡥࡵࡑࡱࡗࡪࡹࡳࡪࡱࡱࡗࡹࡧࡲࡵࡑࡱࡰࡾ࠭ᇉ"),
  bstack1lll1l1_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨ࡙࡯࡭ࡦࡱࡸࡸࡸ࠭ᇊ"),
  bstack1lll1l1_opy_ (u"ࠬࡽࡤࡢࡕࡷࡥࡷࡺࡵࡱࡔࡨࡸࡷ࡯ࡥࡴࠩᇋ"), bstack1lll1l1_opy_ (u"࠭ࡷࡥࡣࡖࡸࡦࡸࡴࡶࡲࡕࡩࡹࡸࡹࡊࡰࡷࡩࡷࡼࡡ࡭ࠩᇌ"),
  bstack1lll1l1_opy_ (u"ࠧࡤࡱࡱࡲࡪࡩࡴࡉࡣࡵࡨࡼࡧࡲࡦࡍࡨࡽࡧࡵࡡࡳࡦࠪᇍ"),
  bstack1lll1l1_opy_ (u"ࠨ࡯ࡤࡼ࡙ࡿࡰࡪࡰࡪࡊࡷ࡫ࡱࡶࡧࡱࡧࡾ࠭ᇎ"),
  bstack1lll1l1_opy_ (u"ࠩࡶ࡭ࡲࡶ࡬ࡦࡋࡶ࡚࡮ࡹࡩࡣ࡮ࡨࡇ࡭࡫ࡣ࡬ࠩᇏ"),
  bstack1lll1l1_opy_ (u"ࠪࡹࡸ࡫ࡃࡢࡴࡷ࡬ࡦ࡭ࡥࡔࡵ࡯ࠫᇐ"),
  bstack1lll1l1_opy_ (u"ࠫࡸ࡮࡯ࡶ࡮ࡧ࡙ࡸ࡫ࡓࡪࡰࡪࡰࡪࡺ࡯࡯ࡖࡨࡷࡹࡓࡡ࡯ࡣࡪࡩࡷ࠭ᇑ"),
  bstack1lll1l1_opy_ (u"ࠬࡹࡴࡢࡴࡷࡍ࡜ࡊࡐࠨᇒ"),
  bstack1lll1l1_opy_ (u"࠭ࡡ࡭࡮ࡲࡻ࡙ࡵࡵࡤࡪࡌࡨࡊࡴࡲࡰ࡮࡯ࠫᇓ"),
  bstack1lll1l1_opy_ (u"ࠧࡪࡩࡱࡳࡷ࡫ࡈࡪࡦࡧࡩࡳࡇࡰࡪࡒࡲࡰ࡮ࡩࡹࡆࡴࡵࡳࡷ࠭ᇔ"),
  bstack1lll1l1_opy_ (u"ࠨ࡯ࡲࡧࡰࡒ࡯ࡤࡣࡷ࡭ࡴࡴࡁࡱࡲࠪᇕ"),
  bstack1lll1l1_opy_ (u"ࠩ࡯ࡳ࡬ࡩࡡࡵࡈࡲࡶࡲࡧࡴࠨᇖ"), bstack1lll1l1_opy_ (u"ࠪࡰࡴ࡭ࡣࡢࡶࡉ࡭ࡱࡺࡥࡳࡕࡳࡩࡨࡹࠧᇗ"),
  bstack1lll1l1_opy_ (u"ࠫࡦࡲ࡬ࡰࡹࡇࡩࡱࡧࡹࡂࡦࡥࠫᇘ"),
  bstack1lll1l1_opy_ (u"ࠬࡪࡩࡴࡣࡥࡰࡪࡏࡤࡍࡱࡦࡥࡹࡵࡲࡂࡷࡷࡳࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠨᇙ")
]
bstack1l11ll1ll1_opy_ = bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷ࠿࠵࠯ࡢࡲ࡬࠱ࡨࡲ࡯ࡶࡦ࠱ࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡦࡳࡲ࠵ࡡࡱࡲ࠰ࡥࡺࡺ࡯࡮ࡣࡷࡩ࠴ࡻࡰ࡭ࡱࡤࡨࠬᇚ")
bstack1ll1l1l111_opy_ = [bstack1lll1l1_opy_ (u"ࠧ࠯ࡣࡳ࡯ࠬᇛ"), bstack1lll1l1_opy_ (u"ࠨ࠰ࡤࡥࡧ࠭ᇜ"), bstack1lll1l1_opy_ (u"ࠩ࠱࡭ࡵࡧࠧᇝ")]
bstack11ll11l11_opy_ = [bstack1lll1l1_opy_ (u"ࠪ࡭ࡩ࠭ᇞ"), bstack1lll1l1_opy_ (u"ࠫࡵࡧࡴࡩࠩᇟ"), bstack1lll1l1_opy_ (u"ࠬࡩࡵࡴࡶࡲࡱࡤ࡯ࡤࠨᇠ"), bstack1lll1l1_opy_ (u"࠭ࡳࡩࡣࡵࡩࡦࡨ࡬ࡦࡡ࡬ࡨࠬᇡ")]
bstack11l11lll1_opy_ = {
  bstack1lll1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᇢ"): bstack1lll1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇣ"),
  bstack1lll1l1_opy_ (u"ࠩࡩ࡭ࡷ࡫ࡦࡰࡺࡒࡴࡹ࡯࡯࡯ࡵࠪᇤ"): bstack1lll1l1_opy_ (u"ࠪࡱࡴࢀ࠺ࡧ࡫ࡵࡩ࡫ࡵࡸࡐࡲࡷ࡭ࡴࡴࡳࠨᇥ"),
  bstack1lll1l1_opy_ (u"ࠫࡪࡪࡧࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇦ"): bstack1lll1l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇧ"),
  bstack1lll1l1_opy_ (u"࠭ࡩࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇨ"): bstack1lll1l1_opy_ (u"ࠧࡴࡧ࠽࡭ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇩ"),
  bstack1lll1l1_opy_ (u"ࠨࡵࡤࡪࡦࡸࡩࡐࡲࡷ࡭ࡴࡴࡳࠨᇪ"): bstack1lll1l1_opy_ (u"ࠩࡶࡥ࡫ࡧࡲࡪ࠰ࡲࡴࡹ࡯࡯࡯ࡵࠪᇫ")
}
bstack1lll1l11l_opy_ = [
  bstack1lll1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᇬ"),
  bstack1lll1l1_opy_ (u"ࠫࡲࡵࡺ࠻ࡨ࡬ࡶࡪ࡬࡯ࡹࡑࡳࡸ࡮ࡵ࡮ࡴࠩᇭ"),
  bstack1lll1l1_opy_ (u"ࠬࡳࡳ࠻ࡧࡧ࡫ࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᇮ"),
  bstack1lll1l1_opy_ (u"࠭ࡳࡦ࠼࡬ࡩࡔࡶࡴࡪࡱࡱࡷࠬᇯ"),
  bstack1lll1l1_opy_ (u"ࠧࡴࡣࡩࡥࡷ࡯࠮ࡰࡲࡷ࡭ࡴࡴࡳࠨᇰ"),
]
bstack1l111ll11_opy_ = bstack111lll111_opy_ + bstack111ll1l111_opy_ + bstack1l111llll1_opy_
bstack1l11111ll1_opy_ = [
  bstack1lll1l1_opy_ (u"ࠨࡠ࡯ࡳࡨࡧ࡬ࡩࡱࡶࡸࠩ࠭ᇱ"),
  bstack1lll1l1_opy_ (u"ࠩࡡࡦࡸ࠳࡬ࡰࡥࡤࡰ࠳ࡩ࡯࡮ࠦࠪᇲ"),
  bstack1lll1l1_opy_ (u"ࠪࡢ࠶࠸࠷࠯ࠩᇳ"),
  bstack1lll1l1_opy_ (u"ࠫࡣ࠷࠰࠯ࠩᇴ"),
  bstack1lll1l1_opy_ (u"ࠬࡤ࠱࠸࠴࠱࠵ࡠ࠼࠭࠺࡟࠱ࠫᇵ"),
  bstack1lll1l1_opy_ (u"࠭࡞࠲࠹࠵࠲࠷ࡡ࠰࠮࠻ࡠ࠲ࠬᇶ"),
  bstack1lll1l1_opy_ (u"ࠧ࡟࠳࠺࠶࠳࠹࡛࠱࠯࠴ࡡ࠳࠭ᇷ"),
  bstack1lll1l1_opy_ (u"ࠨࡠ࠴࠽࠷࠴࠱࠷࠺࠱ࠫᇸ")
]
bstack111ll1l1ll_opy_ = bstack1lll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳ࠻࠱࠲ࡥࡵ࡯࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡣࡰ࡯ࠪᇹ")
bstack11ll1ll1_opy_ = bstack1lll1l1_opy_ (u"ࠪࡷࡩࡱ࠯ࡷ࠳࠲ࡩࡻ࡫࡮ࡵࠩᇺ")
bstack11ll111ll_opy_ = [ bstack1lll1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ᇻ") ]
bstack11ll1ll1l_opy_ = [ bstack1lll1l1_opy_ (u"ࠬࡧࡰࡱ࠯ࡤࡹࡹࡵ࡭ࡢࡶࡨࠫᇼ") ]
bstack1llllllll_opy_ = [ bstack1lll1l1_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭ᇽ") ]
bstack1l11ll111l_opy_ = bstack1lll1l1_opy_ (u"ࠧࡔࡆࡎࡗࡪࡺࡵࡱࠩᇾ")
bstack1l1111l1l_opy_ = bstack1lll1l1_opy_ (u"ࠨࡕࡇࡏ࡙࡫ࡳࡵࡃࡷࡸࡪࡳࡰࡵࡧࡧࠫᇿ")
bstack1ll11l11ll_opy_ = bstack1lll1l1_opy_ (u"ࠩࡖࡈࡐ࡚ࡥࡴࡶࡖࡹࡨࡩࡥࡴࡵࡩࡹࡱ࠭ሀ")
bstack1l11lll1l1_opy_ = bstack1lll1l1_opy_ (u"ࠪ࠸࠳࠶࠮࠱ࠩሁ")
bstack1lll1111ll_opy_ = [
  bstack1lll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡈࡄࡍࡑࡋࡄࠨሂ"),
  bstack1lll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡗࡍࡒࡋࡄࡠࡑࡘࡘࠬሃ"),
  bstack1lll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡆࡑࡕࡃࡌࡇࡇࡣࡇ࡟࡟ࡄࡎࡌࡉࡓ࡚ࠧሄ"),
  bstack1lll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡋࡔࡘࡑࡕࡏࡤࡉࡈࡂࡐࡊࡉࡉ࠭ህ"),
  bstack1lll1l1_opy_ (u"ࠨࡇࡕࡖࡤ࡙ࡏࡄࡍࡈࡘࡤࡔࡏࡕࡡࡆࡓࡓࡔࡅࡄࡖࡈࡈࠬሆ"),
  bstack1lll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡃࡐࡐࡑࡉࡈ࡚ࡉࡐࡐࡢࡇࡑࡕࡓࡆࡆࠪሇ"),
  bstack1lll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡗࡋࡓࡆࡖࠪለ"),
  bstack1lll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡘࡅࡇࡗࡖࡉࡉ࠭ሉ"),
  bstack1lll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡁࡃࡑࡕࡘࡊࡊࠧሊ"),
  bstack1lll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧላ"),
  bstack1lll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡓࡇࡍࡆࡡࡑࡓ࡙ࡥࡒࡆࡕࡒࡐ࡛ࡋࡄࠨሌ"),
  bstack1lll1l1_opy_ (u"ࠨࡇࡕࡖࡤࡇࡄࡅࡔࡈࡗࡘࡥࡉࡏࡘࡄࡐࡎࡊࠧል"),
  bstack1lll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡁࡅࡆࡕࡉࡘ࡙࡟ࡖࡐࡕࡉࡆࡉࡈࡂࡄࡏࡉࠬሎ"),
  bstack1lll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡕࡗࡑࡒࡊࡒ࡟ࡄࡑࡑࡒࡊࡉࡔࡊࡑࡑࡣࡋࡇࡉࡍࡇࡇࠫሏ"),
  bstack1lll1l1_opy_ (u"ࠫࡊࡘࡒࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤ࡚ࡉࡎࡇࡇࡣࡔ࡛ࡔࠨሐ"),
  bstack1lll1l1_opy_ (u"ࠬࡋࡒࡓࡡࡖࡓࡈࡑࡓࡠࡅࡒࡒࡓࡋࡃࡕࡋࡒࡒࡤࡌࡁࡊࡎࡈࡈࠬሑ"),
  bstack1lll1l1_opy_ (u"࠭ࡅࡓࡔࡢࡗࡔࡉࡋࡔࡡࡆࡓࡓࡔࡅࡄࡖࡌࡓࡓࡥࡈࡐࡕࡗࡣ࡚ࡔࡒࡆࡃࡆࡌࡆࡈࡌࡆࠩሒ"),
  bstack1lll1l1_opy_ (u"ࠧࡆࡔࡕࡣࡕࡘࡏ࡙࡛ࡢࡇࡔࡔࡎࡆࡅࡗࡍࡔࡔ࡟ࡇࡃࡌࡐࡊࡊࠧሓ"),
  bstack1lll1l1_opy_ (u"ࠨࡇࡕࡖࡤࡔࡁࡎࡇࡢࡒࡔ࡚࡟ࡓࡇࡖࡓࡑ࡜ࡅࡅࠩሔ"),
  bstack1lll1l1_opy_ (u"ࠩࡈࡖࡗࡥࡎࡂࡏࡈࡣࡗࡋࡓࡐࡎࡘࡘࡎࡕࡎࡠࡈࡄࡍࡑࡋࡄࠨሕ"),
  bstack1lll1l1_opy_ (u"ࠪࡉࡗࡘ࡟ࡎࡃࡑࡈࡆ࡚ࡏࡓ࡛ࡢࡔࡗࡕࡘ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡࡉࡅࡎࡒࡅࡅࠩሖ"),
]
bstack111111ll_opy_ = bstack1lll1l1_opy_ (u"ࠫ࠳࠵ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠲ࡧࡲࡵ࡫ࡩࡥࡨࡺࡳ࠰ࠩሗ")
bstack1llllllll1_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠬࢄࠧመ")), bstack1lll1l1_opy_ (u"࠭࠮ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭ሙ"), bstack1lll1l1_opy_ (u"ࠧ࠯ࡤࡶࡸࡦࡩ࡫࠮ࡥࡲࡲ࡫࡯ࡧ࠯࡬ࡶࡳࡳ࠭ሚ"))
bstack11l111lll1_opy_ = bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹ࠺࠰࠱ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺ࠰ࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡥࡲࡱ࠴ࡧࡰࡪࠩማ")
bstack111ll11l1l_opy_ = [ bstack1lll1l1_opy_ (u"ࠩࡳࡽࡹ࡫ࡳࡵࠩሜ"), bstack1lll1l1_opy_ (u"ࠪࡶࡴࡨ࡯ࡵࠩም"), bstack1lll1l1_opy_ (u"ࠫࡵࡧࡢࡰࡶࠪሞ"), bstack1lll1l1_opy_ (u"ࠬࡨࡥࡩࡣࡹࡩࠬሟ")]
bstack1lll111ll1_opy_ = [ bstack1lll1l1_opy_ (u"࠭ࡰࡺࡶࡨࡷࡹ࠭ሠ"), bstack1lll1l1_opy_ (u"ࠧࡳࡱࡥࡳࡹ࠭ሡ"), bstack1lll1l1_opy_ (u"ࠨࡲࡤࡦࡴࡺࠧሢ"), bstack1lll1l1_opy_ (u"ࠩࡥࡩ࡭ࡧࡶࡦࠩሣ") ]
bstack11ll1111ll_opy_ = {
  bstack1lll1l1_opy_ (u"ࠪࡔࡆ࡙ࡓࠨሤ"): bstack1lll1l1_opy_ (u"ࠫࡵࡧࡳࡴࡧࡧࠫሥ"),
  bstack1lll1l1_opy_ (u"ࠬࡌࡁࡊࡎࠪሦ"): bstack1lll1l1_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩ࠭ሧ"),
  bstack1lll1l1_opy_ (u"ࠧࡔࡍࡌࡔࠬረ"): bstack1lll1l1_opy_ (u"ࠨࡵ࡮࡭ࡵࡶࡥࡥࠩሩ")
}
bstack1l1111ll1_opy_ = [
  bstack1lll1l1_opy_ (u"ࠤࡪࡩࡹࠨሪ"),
  bstack1lll1l1_opy_ (u"ࠥ࡫ࡴࡈࡡࡤ࡭ࠥራ"),
  bstack1lll1l1_opy_ (u"ࠦ࡬ࡵࡆࡰࡴࡺࡥࡷࡪࠢሬ"),
  bstack1lll1l1_opy_ (u"ࠧࡸࡥࡧࡴࡨࡷ࡭ࠨር"),
  bstack1lll1l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧሮ"),
  bstack1lll1l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦሯ"),
  bstack1lll1l1_opy_ (u"ࠣࡵࡸࡦࡲ࡯ࡴࡆ࡮ࡨࡱࡪࡴࡴࠣሰ"),
  bstack1lll1l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࡘࡴࡋ࡬ࡦ࡯ࡨࡲࡹࠨሱ"),
  bstack1lll1l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨሲ"),
  bstack1lll1l1_opy_ (u"ࠦࡨࡲࡥࡢࡴࡈࡰࡪࡳࡥ࡯ࡶࠥሳ"),
  bstack1lll1l1_opy_ (u"ࠧࡧࡣࡵ࡫ࡲࡲࡸࠨሴ"),
  bstack1lll1l1_opy_ (u"ࠨࡥࡹࡧࡦࡹࡹ࡫ࡓࡤࡴ࡬ࡴࡹࠨስ"),
  bstack1lll1l1_opy_ (u"ࠢࡦࡺࡨࡧࡺࡺࡥࡂࡵࡼࡲࡨ࡙ࡣࡳ࡫ࡳࡸࠧሶ"),
  bstack1lll1l1_opy_ (u"ࠣࡥ࡯ࡳࡸ࡫ࠢሷ"),
  bstack1lll1l1_opy_ (u"ࠤࡴࡹ࡮ࡺࠢሸ"),
  bstack1lll1l1_opy_ (u"ࠥࡴࡪࡸࡦࡰࡴࡰࡘࡴࡻࡣࡩࡃࡦࡸ࡮ࡵ࡮ࠣሹ"),
  bstack1lll1l1_opy_ (u"ࠦࡵ࡫ࡲࡧࡱࡵࡱࡒࡻ࡬ࡵ࡫ࡗࡳࡺࡩࡨࠣሺ"),
  bstack1lll1l1_opy_ (u"ࠧࡹࡨࡢ࡭ࡨࠦሻ"),
  bstack1lll1l1_opy_ (u"ࠨࡣ࡭ࡱࡶࡩࡆࡶࡰࠣሼ")
]
bstack111ll1ll11_opy_ = [
  bstack1lll1l1_opy_ (u"ࠢࡤ࡮࡬ࡧࡰࠨሽ"),
  bstack1lll1l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧሾ"),
  bstack1lll1l1_opy_ (u"ࠤࡤࡹࡹࡵࠢሿ"),
  bstack1lll1l1_opy_ (u"ࠥࡱࡦࡴࡵࡢ࡮ࠥቀ"),
  bstack1lll1l1_opy_ (u"ࠦࡹ࡫ࡳࡵࡥࡤࡷࡪࠨቁ")
]
bstack1l1l1lll1l_opy_ = {
  bstack1lll1l1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦቂ"): [bstack1lll1l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧቃ")],
  bstack1lll1l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦቄ"): [bstack1lll1l1_opy_ (u"ࠣࡵࡦࡶࡪ࡫࡮ࡴࡪࡲࡸࠧቅ")],
  bstack1lll1l1_opy_ (u"ࠤࡤࡹࡹࡵࠢቆ"): [bstack1lll1l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡅ࡭ࡧࡰࡩࡳࡺࠢቇ"), bstack1lll1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸ࡚࡯ࡂࡥࡷ࡭ࡻ࡫ࡅ࡭ࡧࡰࡩࡳࡺࠢቈ"), bstack1lll1l1_opy_ (u"ࠧࡹࡣࡳࡧࡨࡲࡸ࡮࡯ࡵࠤ቉"), bstack1lll1l1_opy_ (u"ࠨࡣ࡭࡫ࡦ࡯ࡊࡲࡥ࡮ࡧࡱࡸࠧቊ")],
  bstack1lll1l1_opy_ (u"ࠢ࡮ࡣࡱࡹࡦࡲࠢቋ"): [bstack1lll1l1_opy_ (u"ࠣ࡯ࡤࡲࡺࡧ࡬ࠣቌ")],
  bstack1lll1l1_opy_ (u"ࠤࡷࡩࡸࡺࡣࡢࡵࡨࠦቍ"): [bstack1lll1l1_opy_ (u"ࠥࡸࡪࡹࡴࡤࡣࡶࡩࠧ቎")],
}
bstack111ll111ll_opy_ = {
  bstack1lll1l1_opy_ (u"ࠦࡨࡲࡩࡤ࡭ࡈࡰࡪࡳࡥ࡯ࡶࠥ቏"): bstack1lll1l1_opy_ (u"ࠧࡩ࡬ࡪࡥ࡮ࠦቐ"),
  bstack1lll1l1_opy_ (u"ࠨࡳࡤࡴࡨࡩࡳࡹࡨࡰࡶࠥቑ"): bstack1lll1l1_opy_ (u"ࠢࡴࡥࡵࡩࡪࡴࡳࡩࡱࡷࠦቒ"),
  bstack1lll1l1_opy_ (u"ࠣࡵࡨࡲࡩࡑࡥࡺࡵࡗࡳࡊࡲࡥ࡮ࡧࡱࡸࠧቓ"): bstack1lll1l1_opy_ (u"ࠤࡶࡩࡳࡪࡋࡦࡻࡶࠦቔ"),
  bstack1lll1l1_opy_ (u"ࠥࡷࡪࡴࡤࡌࡧࡼࡷ࡙ࡵࡁࡤࡶ࡬ࡺࡪࡋ࡬ࡦ࡯ࡨࡲࡹࠨቕ"): bstack1lll1l1_opy_ (u"ࠦࡸ࡫࡮ࡥࡍࡨࡽࡸࠨቖ"),
  bstack1lll1l1_opy_ (u"ࠧࡺࡥࡴࡶࡦࡥࡸ࡫ࠢ቗"): bstack1lll1l1_opy_ (u"ࠨࡴࡦࡵࡷࡧࡦࡹࡥࠣቘ")
}
bstack11ll1l1ll1_opy_ = {
  bstack1lll1l1_opy_ (u"ࠧࡃࡇࡉࡓࡗࡋ࡟ࡂࡎࡏࠫ቙"): bstack1lll1l1_opy_ (u"ࠨࡕࡸ࡭ࡹ࡫ࠠࡔࡧࡷࡹࡵ࠭ቚ"),
  bstack1lll1l1_opy_ (u"ࠩࡄࡊ࡙ࡋࡒࡠࡃࡏࡐࠬቛ"): bstack1lll1l1_opy_ (u"ࠪࡗࡺ࡯ࡴࡦࠢࡗࡩࡦࡸࡤࡰࡹࡱࠫቜ"),
  bstack1lll1l1_opy_ (u"ࠫࡇࡋࡆࡐࡔࡈࡣࡊࡇࡃࡉࠩቝ"): bstack1lll1l1_opy_ (u"࡚ࠬࡥࡴࡶࠣࡗࡪࡺࡵࡱࠩ቞"),
  bstack1lll1l1_opy_ (u"࠭ࡁࡇࡖࡈࡖࡤࡋࡁࡄࡊࠪ቟"): bstack1lll1l1_opy_ (u"ࠧࡕࡧࡶࡸ࡚ࠥࡥࡢࡴࡧࡳࡼࡴࠧበ")
}
bstack111ll1l11l_opy_ = 65536
bstack111ll11l11_opy_ = bstack1lll1l1_opy_ (u"ࠨ࠰࠱࠲ࡠ࡚ࡒࡖࡐࡆࡅ࡙ࡋࡄ࡞ࠩቡ")
bstack111ll11lll_opy_ = [
      bstack1lll1l1_opy_ (u"ࠩࡸࡷࡪࡸࡎࡢ࡯ࡨࠫቢ"), bstack1lll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵࡎࡩࡾ࠭ባ"), bstack1lll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧቤ"), bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩብ"), bstack1lll1l1_opy_ (u"࠭ࡣࡶࡵࡷࡳࡲ࡜ࡡࡳ࡫ࡤࡦࡱ࡫ࡳࠨቦ"),
      bstack1lll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡛ࡳࡦࡴࠪቧ"), bstack1lll1l1_opy_ (u"ࠨࡲࡵࡳࡽࡿࡐࡢࡵࡶࠫቨ"), bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧ࡬ࡑࡴࡲࡼࡾ࡛ࡳࡦࡴࠪቩ"), bstack1lll1l1_opy_ (u"ࠪࡰࡴࡩࡡ࡭ࡒࡵࡳࡽࡿࡐࡢࡵࡶࠫቪ"),
      bstack1lll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡹࡸ࡫ࡲࡏࡣࡰࡩࠬቫ"), bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶࡏࡪࡿࠧቬ"), bstack1lll1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩቭ")
    ]
bstack111l1llll1_opy_= {
  bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡒ࡯ࡤࡣ࡯ࠫቮ"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡌࡰࡥࡤࡰࠬቯ"),
  bstack1lll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࡍࡱࡦࡥࡱࡕࡰࡵ࡫ࡲࡲࡸ࠭ተ"): bstack1lll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࡎࡲࡧࡦࡲࡏࡱࡶ࡬ࡳࡳࡹࠧቱ"),
  bstack1lll1l1_opy_ (u"ࠫࡱࡵࡣࡢ࡮ࡒࡴࡹ࡯࡯࡯ࡵࠪቲ"): bstack1lll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࡐࡴࡩࡡ࡭ࡑࡳࡸ࡮ࡵ࡮ࡴࠩታ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡢࡴࡤࡰࡱ࡫࡬ࡴࡒࡨࡶࡕࡲࡡࡵࡨࡲࡶࡲ࠭ቴ"): bstack1lll1l1_opy_ (u"ࠧࡱࡣࡵࡥࡱࡲࡥ࡭ࡵࡓࡩࡷࡖ࡬ࡢࡶࡩࡳࡷࡳࠧት"),
  bstack1lll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫቶ"): bstack1lll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬቷ"),
  bstack1lll1l1_opy_ (u"ࠪࡰࡴ࡭ࡌࡦࡸࡨࡰࠬቸ"): bstack1lll1l1_opy_ (u"ࠫࡱࡵࡧࡍࡧࡹࡩࡱ࠭ቹ"),
  bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡓࡶࡴࡾࡹࠨቺ"): bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡔࡷࡵࡸࡺࠩቻ"),
  bstack1lll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡸࡖࡲࡰࡺࡼࠫቼ"): bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬች"),
  bstack1lll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࠬቾ"): bstack1lll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ቿ"),
  bstack1lll1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡅࡲࡲࡹ࡫ࡸࡵࡑࡳࡸ࡮ࡵ࡮ࡴࠩኀ"): bstack1lll1l1_opy_ (u"ࠬࡺࡥࡴࡶࡆࡳࡳࡺࡥࡹࡶࡒࡴࡹ࡯࡯࡯ࡵࠪኁ"),
  bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡓࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪኂ"): bstack1lll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡔࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫኃ"),
  bstack1lll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡕࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬኄ"): bstack1lll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡏࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ኅ"),
  bstack1lll1l1_opy_ (u"ࠪࡧࡺࡹࡴࡰ࡯࡙ࡥࡷ࡯ࡡࡣ࡮ࡨࡷࠬኆ"): bstack1lll1l1_opy_ (u"ࠫࡨࡻࡳࡵࡱࡰ࡚ࡦࡸࡩࡢࡤ࡯ࡩࡸ࠭ኇ"),
  bstack1lll1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩኈ"): bstack1lll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ኉"),
  bstack1lll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩኊ"): bstack1lll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪኋ"),
  bstack1lll1l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡕࡧࡶࡸࡸ࠭ኌ"): bstack1lll1l1_opy_ (u"ࠪࡶࡪࡸࡵ࡯ࡖࡨࡷࡹࡹࠧኍ"),
  bstack1lll1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ኎"): bstack1lll1l1_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ኏"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࡔࡶࡴࡪࡱࡱࡷࠬነ"): bstack1lll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ኑ"),
  bstack1lll1l1_opy_ (u"ࠨࡲࡨࡶࡨࡿࡃࡢࡲࡷࡹࡷ࡫ࡍࡰࡦࡨࠫኒ"): bstack1lll1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࡄࡣࡳࡸࡺࡸࡥࡎࡱࡧࡩࠬና"),
  bstack1lll1l1_opy_ (u"ࠪࡨ࡮ࡹࡡࡣ࡮ࡨࡅࡺࡺ࡯ࡄࡣࡳࡸࡺࡸࡥࡍࡱࡪࡷࠬኔ"): bstack1lll1l1_opy_ (u"ࠫࡩ࡯ࡳࡢࡤ࡯ࡩࡆࡻࡴࡰࡅࡤࡴࡹࡻࡲࡦࡎࡲ࡫ࡸ࠭ን"),
  bstack1lll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬኖ"): bstack1lll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ኗ"),
  bstack1lll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧኘ"): bstack1lll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨኙ"),
  bstack1lll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ኚ"): bstack1lll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧኛ"),
  bstack1lll1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࡐࡲࡷ࡭ࡴࡴࡳࠨኜ"): bstack1lll1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩኝ"),
  bstack1lll1l1_opy_ (u"࠭ࡰࡳࡱࡻࡽࡘ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ኞ"): bstack1lll1l1_opy_ (u"ࠧࡱࡴࡲࡼࡾ࡙ࡥࡵࡶ࡬ࡲ࡬ࡹࠧኟ")
}
bstack111ll11111_opy_ = [bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸࡪࡹࡴࠨአ"), bstack1lll1l1_opy_ (u"ࠩࡵࡳࡧࡵࡴࠨኡ")]