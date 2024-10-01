import math
from ..base import Element, Manager


class TextPath(Element):
    spec = dict(
        ff='', fs='', fw='', f='black',
        t='',
        ta='', ab='', so='',
    )

    def path(self, proxy):
        raise NotImplementedError()

    def draw(self, proxy):
        eid = self.manager.new_id()
        return {
            "defs": {
                "+": {
                    "path": {
                        "id": eid,
                        'd': self.path(proxy)
                    }
                }
            },
            "text": {
                "font-family": proxy.ff,
                "font-size": proxy.fs,
                "font-weight": proxy.fw,
                "fill": proxy.f,
                "text-anchor": proxy.ta,
                "+": {
                    "textPath": {
                        "xlink:href": "#" + eid,
                        "alignment-baseline": proxy.ab,
                        "startOffset": f"{100 * proxy.so}%" if isinstance(proxy.so, float) else proxy.so,
                        "+": proxy.t
                    }
                }
            }
        }


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
