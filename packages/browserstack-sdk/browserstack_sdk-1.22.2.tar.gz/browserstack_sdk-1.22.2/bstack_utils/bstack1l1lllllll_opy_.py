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
class bstack111lll1l11_opy_(object):
  bstack111l11111_opy_ = os.path.join(os.path.expanduser(bstack1lll1l1_opy_ (u"ࠪࢂࠬྦྷ")), bstack1lll1l1_opy_ (u"ࠫ࠳ࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫྨ"))
  bstack111lll1lll_opy_ = os.path.join(bstack111l11111_opy_, bstack1lll1l1_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹ࠮࡫ࡵࡲࡲࠬྩ"))
  bstack111llll111_opy_ = None
  perform_scan = None
  bstack11lll11l_opy_ = None
  bstack11llllll1_opy_ = None
  bstack111lllll11_opy_ = None
  def __new__(cls):
    if not hasattr(cls, bstack1lll1l1_opy_ (u"࠭ࡩ࡯ࡵࡷࡥࡳࡩࡥࠨྪ")):
      cls.instance = super(bstack111lll1l11_opy_, cls).__new__(cls)
      cls.instance.bstack111lll1ll1_opy_()
    return cls.instance
  def bstack111lll1ll1_opy_(self):
    try:
      with open(self.bstack111lll1lll_opy_, bstack1lll1l1_opy_ (u"ࠧࡳࠩྫ")) as bstack1lll11l111_opy_:
        bstack111lll1l1l_opy_ = bstack1lll11l111_opy_.read()
        data = json.loads(bstack111lll1l1l_opy_)
        if bstack1lll1l1_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪྫྷ") in data:
          self.bstack11l11l1l1l_opy_(data[bstack1lll1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫྭ")])
        if bstack1lll1l1_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫྮ") in data:
          self.bstack11l11111ll_opy_(data[bstack1lll1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬྯ")])
    except:
      pass
  def bstack11l11111ll_opy_(self, scripts):
    if scripts != None:
      self.perform_scan = scripts[bstack1lll1l1_opy_ (u"ࠬࡹࡣࡢࡰࠪྰ")]
      self.bstack11lll11l_opy_ = scripts[bstack1lll1l1_opy_ (u"࠭ࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠪྱ")]
      self.bstack11llllll1_opy_ = scripts[bstack1lll1l1_opy_ (u"ࠧࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠫྲ")]
      self.bstack111lllll11_opy_ = scripts[bstack1lll1l1_opy_ (u"ࠨࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸ࠭ླ")]
  def bstack11l11l1l1l_opy_(self, bstack111llll111_opy_):
    if bstack111llll111_opy_ != None and len(bstack111llll111_opy_) != 0:
      self.bstack111llll111_opy_ = bstack111llll111_opy_
  def store(self):
    try:
      with open(self.bstack111lll1lll_opy_, bstack1lll1l1_opy_ (u"ࠩࡺࠫྴ")) as file:
        json.dump({
          bstack1lll1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࡷࠧྵ"): self.bstack111llll111_opy_,
          bstack1lll1l1_opy_ (u"ࠦࡸࡩࡲࡪࡲࡷࡷࠧྶ"): {
            bstack1lll1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥྷ"): self.perform_scan,
            bstack1lll1l1_opy_ (u"ࠨࡧࡦࡶࡕࡩࡸࡻ࡬ࡵࡵࠥྸ"): self.bstack11lll11l_opy_,
            bstack1lll1l1_opy_ (u"ࠢࡨࡧࡷࡖࡪࡹࡵ࡭ࡶࡶࡗࡺࡳ࡭ࡢࡴࡼࠦྐྵ"): self.bstack11llllll1_opy_,
            bstack1lll1l1_opy_ (u"ࠣࡵࡤࡺࡪࡘࡥࡴࡷ࡯ࡸࡸࠨྺ"): self.bstack111lllll11_opy_
          }
        }, file)
    except:
      pass
  def bstack1lll11ll11_opy_(self, bstack111llll11l_opy_):
    try:
      return any(command.get(bstack1lll1l1_opy_ (u"ࠩࡱࡥࡲ࡫ࠧྻ")) == bstack111llll11l_opy_ for command in self.bstack111llll111_opy_)
    except:
      return False
bstack1l1lllllll_opy_ = bstack111lll1l11_opy_()