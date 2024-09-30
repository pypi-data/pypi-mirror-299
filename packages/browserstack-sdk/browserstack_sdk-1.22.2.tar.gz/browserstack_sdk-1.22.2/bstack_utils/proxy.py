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
from urllib.parse import urlparse
from bstack_utils.config import Config
from bstack_utils.messages import bstack1lllll1l1ll_opy_
bstack1lll11l1ll_opy_ = Config.bstack1l1ll1111_opy_()
def bstack1lll11lllll_opy_(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
def bstack1lll1l111l1_opy_(bstack1lll11llll1_opy_, bstack1lll1l11111_opy_):
    from pypac import get_pac
    from pypac import PACSession
    from pypac.parser import PACFile
    import socket
    if os.path.isfile(bstack1lll11llll1_opy_):
        with open(bstack1lll11llll1_opy_) as f:
            pac = PACFile(f.read())
    elif bstack1lll11lllll_opy_(bstack1lll11llll1_opy_):
        pac = get_pac(url=bstack1lll11llll1_opy_)
    else:
        raise Exception(bstack1lll1l1_opy_ (u"ࠬࡖࡡࡤࠢࡩ࡭ࡱ࡫ࠠࡥࡱࡨࡷࠥࡴ࡯ࡵࠢࡨࡼ࡮ࡹࡴ࠻ࠢࡾࢁࠬᕼ").format(bstack1lll11llll1_opy_))
    session = PACSession(pac)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((bstack1lll1l1_opy_ (u"ࠨ࠸࠯࠺࠱࠼࠳࠾ࠢᕽ"), 80))
        bstack1lll1l1111l_opy_ = s.getsockname()[0]
        s.close()
    except:
        bstack1lll1l1111l_opy_ = bstack1lll1l1_opy_ (u"ࠧ࠱࠰࠳࠲࠵࠴࠰ࠨᕾ")
    proxy_url = session.get_pac().find_proxy_for_url(bstack1lll1l11111_opy_, bstack1lll1l1111l_opy_)
    return proxy_url
def bstack1lll1lll1l_opy_(config):
    return bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡖࡲࡰࡺࡼࠫᕿ") in config or bstack1lll1l1_opy_ (u"ࠩ࡫ࡸࡹࡶࡳࡑࡴࡲࡼࡾ࠭ᖀ") in config
def bstack1l1ll1ll11_opy_(config):
    if not bstack1lll1lll1l_opy_(config):
        return
    if config.get(bstack1lll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡑࡴࡲࡼࡾ࠭ᖁ")):
        return config.get(bstack1lll1l1_opy_ (u"ࠫ࡭ࡺࡴࡱࡒࡵࡳࡽࡿࠧᖂ"))
    if config.get(bstack1lll1l1_opy_ (u"ࠬ࡮ࡴࡵࡲࡶࡔࡷࡵࡸࡺࠩᖃ")):
        return config.get(bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࡕࡸ࡯ࡹࡻࠪᖄ"))
def bstack111111ll1_opy_(config, bstack1lll1l11111_opy_):
    proxy = bstack1l1ll1ll11_opy_(config)
    proxies = {}
    if config.get(bstack1lll1l1_opy_ (u"ࠧࡩࡶࡷࡴࡕࡸ࡯ࡹࡻࠪᖅ")) or config.get(bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࡐࡳࡱࡻࡽࠬᖆ")):
        if proxy.endswith(bstack1lll1l1_opy_ (u"ࠩ࠱ࡴࡦࡩࠧᖇ")):
            proxies = bstack1ll1ll1l1_opy_(proxy, bstack1lll1l11111_opy_)
        else:
            proxies = {
                bstack1lll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖈ"): proxy
            }
    bstack1lll11l1ll_opy_.bstack11111lll1_opy_(bstack1lll1l1_opy_ (u"ࠫࡵࡸ࡯ࡹࡻࡖࡩࡹࡺࡩ࡯ࡩࡶࠫᖉ"), proxies)
    return proxies
def bstack1ll1ll1l1_opy_(bstack1lll11llll1_opy_, bstack1lll1l11111_opy_):
    proxies = {}
    global bstack1lll11lll1l_opy_
    if bstack1lll1l1_opy_ (u"ࠬࡖࡁࡄࡡࡓࡖࡔ࡞࡙ࠨᖊ") in globals():
        return bstack1lll11lll1l_opy_
    try:
        proxy = bstack1lll1l111l1_opy_(bstack1lll11llll1_opy_, bstack1lll1l11111_opy_)
        if bstack1lll1l1_opy_ (u"ࠨࡄࡊࡔࡈࡇ࡙ࠨᖋ") in proxy:
            proxies = {}
        elif bstack1lll1l1_opy_ (u"ࠢࡉࡖࡗࡔࠧᖌ") in proxy or bstack1lll1l1_opy_ (u"ࠣࡊࡗࡘࡕ࡙ࠢᖍ") in proxy or bstack1lll1l1_opy_ (u"ࠤࡖࡓࡈࡑࡓࠣᖎ") in proxy:
            bstack1lll11lll11_opy_ = proxy.split(bstack1lll1l1_opy_ (u"ࠥࠤࠧᖏ"))
            if bstack1lll1l1_opy_ (u"ࠦ࠿࠵࠯ࠣᖐ") in bstack1lll1l1_opy_ (u"ࠧࠨᖑ").join(bstack1lll11lll11_opy_[1:]):
                proxies = {
                    bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖒ"): bstack1lll1l1_opy_ (u"ࠢࠣᖓ").join(bstack1lll11lll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖔ"): str(bstack1lll11lll11_opy_[0]).lower() + bstack1lll1l1_opy_ (u"ࠤ࠽࠳࠴ࠨᖕ") + bstack1lll1l1_opy_ (u"ࠥࠦᖖ").join(bstack1lll11lll11_opy_[1:])
                }
        elif bstack1lll1l1_opy_ (u"ࠦࡕࡘࡏ࡙࡛ࠥᖗ") in proxy:
            bstack1lll11lll11_opy_ = proxy.split(bstack1lll1l1_opy_ (u"ࠧࠦࠢᖘ"))
            if bstack1lll1l1_opy_ (u"ࠨ࠺࠰࠱ࠥᖙ") in bstack1lll1l1_opy_ (u"ࠢࠣᖚ").join(bstack1lll11lll11_opy_[1:]):
                proxies = {
                    bstack1lll1l1_opy_ (u"ࠨࡪࡷࡸࡵࡹࠧᖛ"): bstack1lll1l1_opy_ (u"ࠤࠥᖜ").join(bstack1lll11lll11_opy_[1:])
                }
            else:
                proxies = {
                    bstack1lll1l1_opy_ (u"ࠪ࡬ࡹࡺࡰࡴࠩᖝ"): bstack1lll1l1_opy_ (u"ࠦ࡭ࡺࡴࡱ࠼࠲࠳ࠧᖞ") + bstack1lll1l1_opy_ (u"ࠧࠨᖟ").join(bstack1lll11lll11_opy_[1:])
                }
        else:
            proxies = {
                bstack1lll1l1_opy_ (u"࠭ࡨࡵࡶࡳࡷࠬᖠ"): proxy
            }
    except Exception as e:
        print(bstack1lll1l1_opy_ (u"ࠢࡴࡱࡰࡩࠥ࡫ࡲࡳࡱࡵࠦᖡ"), bstack1lllll1l1ll_opy_.format(bstack1lll11llll1_opy_, str(e)))
    bstack1lll11lll1l_opy_ = proxies
    return proxies