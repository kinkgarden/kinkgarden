from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def icon_svg():
    from xml.dom import minidom

    impl = minidom.getDOMImplementation()
    icons = ["heart", "check", "tilde", "no"]
    doc = impl.createDocument("http://www.w3.org/2000/svg", "svg", None)
    doc.documentElement.setAttribute("style", "display:none;")
    for name in icons:
        with minidom.parse(f"kinks/assets/{name}.svg") as orig:
            symbol = doc.createElement("symbol")
            symbol.setAttribute("id", name)
            symbol.setAttribute("viewBox", orig.documentElement.getAttribute("viewBox"))
            orig = orig.getElementsByTagName("g")[0]
            for child in list(orig.childNodes):
                if isinstance(child, minidom.Text):
                    orig.removeChild(child)
            orig.removeAttribute("id")
            orig.firstChild.removeAttribute("id")
            orig.firstChild.removeAttribute("style")
            symbol.appendChild(orig)
            doc.documentElement.appendChild(symbol)
    data = doc.toxml(encoding="UTF-8")
    data = data.replace(b'<?xml version="1.0" encoding="UTF-8"?>', b"")
    return mark_safe(data.decode("utf-8"))
