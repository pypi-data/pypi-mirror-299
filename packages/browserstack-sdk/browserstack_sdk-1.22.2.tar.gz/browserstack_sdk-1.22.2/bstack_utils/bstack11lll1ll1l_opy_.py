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
from uuid import uuid4
from bstack_utils.helper import bstack1l11lll111_opy_, bstack1111lll11l_opy_
from bstack_utils.bstack11l11ll1l_opy_ import bstack1lll11l11ll_opy_
class bstack11ll11111l_opy_:
    def __init__(self, name=None, code=None, uuid=None, file_path=None, bstack11lll11lll_opy_=None, framework=None, tags=[], scope=[], bstack1ll1llll11l_opy_=None, bstack1ll1ll1lll1_opy_=True, bstack1ll1lll1ll1_opy_=None, bstack1lll11ll_opy_=None, result=None, duration=None, bstack11ll111lll_opy_=None, meta={}):
        self.bstack11ll111lll_opy_ = bstack11ll111lll_opy_
        self.name = name
        self.code = code
        self.file_path = file_path
        self.uuid = uuid
        if not self.uuid and bstack1ll1ll1lll1_opy_:
            self.uuid = uuid4().__str__()
        self.bstack11lll11lll_opy_ = bstack11lll11lll_opy_
        self.framework = framework
        self.tags = tags
        self.scope = scope
        self.bstack1ll1llll11l_opy_ = bstack1ll1llll11l_opy_
        self.bstack1ll1lll1ll1_opy_ = bstack1ll1lll1ll1_opy_
        self.bstack1lll11ll_opy_ = bstack1lll11ll_opy_
        self.result = result
        self.duration = duration
        self.meta = meta
    def bstack11ll11l1ll_opy_(self):
        if self.uuid:
            return self.uuid
        self.uuid = uuid4().__str__()
        return self.uuid
    def bstack11lll111ll_opy_(self, meta):
        self.meta = meta
    def bstack1ll1lll1l11_opy_(self):
        bstack1ll1ll1llll_opy_ = os.path.relpath(self.file_path, start=os.getcwd())
        return {
            bstack1lll1l1_opy_ (u"ࠨࡨ࡬ࡰࡪࡥ࡮ࡢ࡯ࡨࠫᘋ"): bstack1ll1ll1llll_opy_,
            bstack1lll1l1_opy_ (u"ࠩ࡯ࡳࡨࡧࡴࡪࡱࡱࠫᘌ"): bstack1ll1ll1llll_opy_,
            bstack1lll1l1_opy_ (u"ࠪࡺࡨࡥࡦࡪ࡮ࡨࡴࡦࡺࡨࠨᘍ"): bstack1ll1ll1llll_opy_
        }
    def set(self, **kwargs):
        for key, val in kwargs.items():
            if not hasattr(self, key):
                raise TypeError(bstack1lll1l1_opy_ (u"࡚ࠦࡴࡥࡹࡲࡨࡧࡹ࡫ࡤࠡࡣࡵ࡫ࡺࡳࡥ࡯ࡶ࠽ࠤࠧᘎ") + key)
            setattr(self, key, val)
    def bstack1ll1ll1l1l1_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᘏ"): self.name,
            bstack1lll1l1_opy_ (u"࠭ࡢࡰࡦࡼࠫᘐ"): {
                bstack1lll1l1_opy_ (u"ࠧ࡭ࡣࡱ࡫ࠬᘑ"): bstack1lll1l1_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᘒ"),
                bstack1lll1l1_opy_ (u"ࠩࡦࡳࡩ࡫ࠧᘓ"): self.code
            },
            bstack1lll1l1_opy_ (u"ࠪࡷࡨࡵࡰࡦࡵࠪᘔ"): self.scope,
            bstack1lll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩᘕ"): self.tags,
            bstack1lll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᘖ"): self.framework,
            bstack1lll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘗ"): self.bstack11lll11lll_opy_
        }
    def bstack1ll1llll111_opy_(self):
        return {
         bstack1lll1l1_opy_ (u"ࠧ࡮ࡧࡷࡥࠬᘘ"): self.meta
        }
    def bstack1ll1ll1l1ll_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠨࡥࡸࡷࡹࡵ࡭ࡓࡧࡵࡹࡳࡖࡡࡳࡣࡰࠫᘙ"): {
                bstack1lll1l1_opy_ (u"ࠩࡵࡩࡷࡻ࡮ࡠࡰࡤࡱࡪ࠭ᘚ"): self.bstack1ll1llll11l_opy_
            }
        }
    def bstack1ll1ll1l111_opy_(self, bstack1ll1ll11lll_opy_, details):
        step = next(filter(lambda st: st[bstack1lll1l1_opy_ (u"ࠪ࡭ࡩ࠭ᘛ")] == bstack1ll1ll11lll_opy_, self.meta[bstack1lll1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘜ")]), None)
        step.update(details)
    def bstack11ll1l1ll_opy_(self, bstack1ll1ll11lll_opy_):
        step = next(filter(lambda st: st[bstack1lll1l1_opy_ (u"ࠬ࡯ࡤࠨᘝ")] == bstack1ll1ll11lll_opy_, self.meta[bstack1lll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᘞ")]), None)
        step.update({
            bstack1lll1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫᘟ"): bstack1l11lll111_opy_()
        })
    def bstack11lll11ll1_opy_(self, bstack1ll1ll11lll_opy_, result, duration=None):
        bstack1ll1lll1ll1_opy_ = bstack1l11lll111_opy_()
        if bstack1ll1ll11lll_opy_ is not None and self.meta.get(bstack1lll1l1_opy_ (u"ࠨࡵࡷࡩࡵࡹࠧᘠ")):
            step = next(filter(lambda st: st[bstack1lll1l1_opy_ (u"ࠩ࡬ࡨࠬᘡ")] == bstack1ll1ll11lll_opy_, self.meta[bstack1lll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᘢ")]), None)
            step.update({
                bstack1lll1l1_opy_ (u"ࠫ࡫࡯࡮ࡪࡵ࡫ࡩࡩࡥࡡࡵࠩᘣ"): bstack1ll1lll1ll1_opy_,
                bstack1lll1l1_opy_ (u"ࠬࡪࡵࡳࡣࡷ࡭ࡴࡴࠧᘤ"): duration if duration else bstack1111lll11l_opy_(step[bstack1lll1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪᘥ")], bstack1ll1lll1ll1_opy_),
                bstack1lll1l1_opy_ (u"ࠧࡳࡧࡶࡹࡱࡺࠧᘦ"): result.result,
                bstack1lll1l1_opy_ (u"ࠨࡨࡤ࡭ࡱࡻࡲࡦࠩᘧ"): str(result.exception) if result.exception else None
            })
    def add_step(self, bstack1ll1lll111l_opy_):
        if self.meta.get(bstack1lll1l1_opy_ (u"ࠩࡶࡸࡪࡶࡳࠨᘨ")):
            self.meta[bstack1lll1l1_opy_ (u"ࠪࡷࡹ࡫ࡰࡴࠩᘩ")].append(bstack1ll1lll111l_opy_)
        else:
            self.meta[bstack1lll1l1_opy_ (u"ࠫࡸࡺࡥࡱࡵࠪᘪ")] = [ bstack1ll1lll111l_opy_ ]
    def bstack1ll1lll11ll_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠬࡻࡵࡪࡦࠪᘫ"): self.bstack11ll11l1ll_opy_(),
            **self.bstack1ll1ll1l1l1_opy_(),
            **self.bstack1ll1lll1l11_opy_(),
            **self.bstack1ll1llll111_opy_()
        }
    def bstack1ll1ll1l11l_opy_(self):
        if not self.result:
            return {}
        data = {
            bstack1lll1l1_opy_ (u"࠭ࡦࡪࡰ࡬ࡷ࡭࡫ࡤࡠࡣࡷࠫᘬ"): self.bstack1ll1lll1ll1_opy_,
            bstack1lll1l1_opy_ (u"ࠧࡥࡷࡵࡥࡹ࡯࡯࡯ࡡ࡬ࡲࡤࡳࡳࠨᘭ"): self.duration,
            bstack1lll1l1_opy_ (u"ࠨࡴࡨࡷࡺࡲࡴࠨᘮ"): self.result.result
        }
        if data[bstack1lll1l1_opy_ (u"ࠩࡵࡩࡸࡻ࡬ࡵࠩᘯ")] == bstack1lll1l1_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࠪᘰ"):
            data[bstack1lll1l1_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡷࡵࡩࡤࡺࡹࡱࡧࠪᘱ")] = self.result.bstack11l11lll1l_opy_()
            data[bstack1lll1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡸࡶࡪ࠭ᘲ")] = [{bstack1lll1l1_opy_ (u"࠭ࡢࡢࡥ࡮ࡸࡷࡧࡣࡦࠩᘳ"): self.result.bstack111111ll11_opy_()}]
        return data
    def bstack1ll1ll1ll11_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠧࡶࡷ࡬ࡨࠬᘴ"): self.bstack11ll11l1ll_opy_(),
            **self.bstack1ll1ll1l1l1_opy_(),
            **self.bstack1ll1lll1l11_opy_(),
            **self.bstack1ll1ll1l11l_opy_(),
            **self.bstack1ll1llll111_opy_()
        }
    def bstack11ll1111l1_opy_(self, event, result=None):
        if result:
            self.result = result
        if bstack1lll1l1_opy_ (u"ࠨࡕࡷࡥࡷࡺࡥࡥࠩᘵ") in event:
            return self.bstack1ll1lll11ll_opy_()
        elif bstack1lll1l1_opy_ (u"ࠩࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫᘶ") in event:
            return self.bstack1ll1ll1ll11_opy_()
    def bstack11ll1ll111_opy_(self):
        pass
    def stop(self, time=None, duration=None, result=None):
        self.bstack1ll1lll1ll1_opy_ = time if time else bstack1l11lll111_opy_()
        self.duration = duration if duration else bstack1111lll11l_opy_(self.bstack11lll11lll_opy_, self.bstack1ll1lll1ll1_opy_)
        if result:
            self.result = result
class bstack11lll1ll11_opy_(bstack11ll11111l_opy_):
    def __init__(self, hooks=[], bstack11ll1ll1l1_opy_={}, *args, **kwargs):
        self.hooks = hooks
        self.bstack11ll1ll1l1_opy_ = bstack11ll1ll1l1_opy_
        super().__init__(*args, **kwargs, bstack1lll11ll_opy_=bstack1lll1l1_opy_ (u"ࠪࡸࡪࡹࡴࠨᘷ"))
    @classmethod
    def bstack1ll1lll1111_opy_(cls, scenario, feature, test, **kwargs):
        steps = []
        for step in scenario.steps:
            steps.append({
                bstack1lll1l1_opy_ (u"ࠫ࡮ࡪࠧᘸ"): id(step),
                bstack1lll1l1_opy_ (u"ࠬࡺࡥࡹࡶࠪᘹ"): step.name,
                bstack1lll1l1_opy_ (u"࠭࡫ࡦࡻࡺࡳࡷࡪࠧᘺ"): step.keyword,
            })
        return bstack11lll1ll11_opy_(
            **kwargs,
            meta={
                bstack1lll1l1_opy_ (u"ࠧࡧࡧࡤࡸࡺࡸࡥࠨᘻ"): {
                    bstack1lll1l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭ᘼ"): feature.name,
                    bstack1lll1l1_opy_ (u"ࠩࡳࡥࡹ࡮ࠧᘽ"): feature.filename,
                    bstack1lll1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᘾ"): feature.description
                },
                bstack1lll1l1_opy_ (u"ࠫࡸࡩࡥ࡯ࡣࡵ࡭ࡴ࠭ᘿ"): {
                    bstack1lll1l1_opy_ (u"ࠬࡴࡡ࡮ࡧࠪᙀ"): scenario.name
                },
                bstack1lll1l1_opy_ (u"࠭ࡳࡵࡧࡳࡷࠬᙁ"): steps,
                bstack1lll1l1_opy_ (u"ࠧࡦࡺࡤࡱࡵࡲࡥࡴࠩᙂ"): bstack1lll11l11ll_opy_(test)
            }
        )
    def bstack1ll1lll1lll_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠨࡪࡲࡳࡰࡹࠧᙃ"): self.hooks
        }
    def bstack1ll1ll1ll1l_opy_(self):
        if self.bstack11ll1ll1l1_opy_:
            return {
                bstack1lll1l1_opy_ (u"ࠩ࡬ࡲࡹ࡫ࡧࡳࡣࡷ࡭ࡴࡴࡳࠨᙄ"): self.bstack11ll1ll1l1_opy_
            }
        return {}
    def bstack1ll1ll1ll11_opy_(self):
        return {
            **super().bstack1ll1ll1ll11_opy_(),
            **self.bstack1ll1lll1lll_opy_()
        }
    def bstack1ll1lll11ll_opy_(self):
        return {
            **super().bstack1ll1lll11ll_opy_(),
            **self.bstack1ll1ll1ll1l_opy_()
        }
    def bstack11ll1ll111_opy_(self):
        return bstack1lll1l1_opy_ (u"ࠪࡸࡪࡹࡴࡠࡴࡸࡲࠬᙅ")
class bstack11llll111l_opy_(bstack11ll11111l_opy_):
    def __init__(self, hook_type, *args, **kwargs):
        self.hook_type = hook_type
        self.bstack1ll1lll11l1_opy_ = None
        super().__init__(*args, **kwargs, bstack1lll11ll_opy_=bstack1lll1l1_opy_ (u"ࠫ࡭ࡵ࡯࡬ࠩᙆ"))
    def bstack11ll1lll11_opy_(self):
        return self.hook_type
    def bstack1ll1lll1l1l_opy_(self):
        return {
            bstack1lll1l1_opy_ (u"ࠬ࡮࡯ࡰ࡭ࡢࡸࡾࡶࡥࠨᙇ"): self.hook_type
        }
    def bstack1ll1ll1ll11_opy_(self):
        return {
            **super().bstack1ll1ll1ll11_opy_(),
            **self.bstack1ll1lll1l1l_opy_()
        }
    def bstack1ll1lll11ll_opy_(self):
        return {
            **super().bstack1ll1lll11ll_opy_(),
            bstack1lll1l1_opy_ (u"࠭ࡴࡦࡵࡷࡣࡷࡻ࡮ࡠ࡫ࡧࠫᙈ"): self.bstack1ll1lll11l1_opy_,
            **self.bstack1ll1lll1l1l_opy_()
        }
    def bstack11ll1ll111_opy_(self):
        return bstack1lll1l1_opy_ (u"ࠧࡩࡱࡲ࡯ࡤࡸࡵ࡯ࠩᙉ")
    def bstack11llll1lll_opy_(self, bstack1ll1lll11l1_opy_):
        self.bstack1ll1lll11l1_opy_ = bstack1ll1lll11l1_opy_