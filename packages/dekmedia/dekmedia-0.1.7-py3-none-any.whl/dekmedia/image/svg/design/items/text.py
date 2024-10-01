import math
from ..base import Element, Manager
from .utils.path import path_text


class TextPath(Element):
    spec = dict(
        ff='', fs='', fw='',
        f='black',
        t='',
    )

    def path(self, proxy):
        raise NotImplementedError()

    def draw(self, proxy):
        result = {}
        for i, (c, (x, y, a)) in enumerate(path_text(self.path(proxy), proxy.t, )):
            result["text" + "-" * i] = {
                "x": x,
                "y": y,
                "transform": f"rotate({a}, {x}, {y})",
                "text-anchor": "middle",
                "dominant-baseline": "central",
                "font-family": proxy.ff,
                "font-size": self._pv(proxy.fs),
                "font-weight": self._pv(proxy.fw),
                "fill": proxy.f,
                "+": c
            }
        return result


@Manager.element
class TextPathCircle(TextPath):
    spec = dict(
        **TextPath.spec,
        x=lambda w: w / 2, y=lambda _, h: h / 2,
        a=lambda w: w / 2, b=lambda _, h: h / 2,
        p=1,  # percent
    )

    def path(self, proxy):
        rx = proxy.a * proxy.p
        ry = proxy.b * proxy.p
        alpha = 0.001
        return (
            f"M{proxy.x} {proxy.y + ry}"
            f"A{rx} {ry} 0 1 1 {proxy.x + rx * math.sin(alpha)} {proxy.y + ry * math.cos(alpha)}"
        )
