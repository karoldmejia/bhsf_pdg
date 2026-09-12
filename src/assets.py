import os as _os
import base64 as _b64

_LOGO_CACHE = {}


def _get_logo_b64(nombre="Logo_barco_sin_fondo.jpeg"):
    """Carga un logo desde img/ y lo retorna como (base64, mime) o None."""
    if nombre in _LOGO_CACHE:
        return _LOGO_CACHE[nombre]
    ruta = f"img/{nombre}"
    if not _os.path.exists(ruta):
        return None
    try:
        with open(ruta, 'rb') as f:
            data = f.read()
        ext = nombre.rsplit('.', 1)[-1].lower()
        mime = 'jpeg' if ext in ('jpg', 'jpeg') else ext
        b64 = _b64.b64encode(data).decode()
        _LOGO_CACHE[nombre] = (b64, mime)
        return (b64, mime)
    except Exception:
        return None


def logo_html(style="max-width:220px;height:auto;"):
    """Logo para sidebar."""
    r = _get_logo_b64()
    if r:
        b64, mime = r
        return f'<img src="data:image/{mime};base64,{b64}" style="{style}" />'
    return '<b style="color:#fff">Barco Hospital San Raffaele</b>'


def logo_hero():
    """Logo para el hero principal."""
    r = _get_logo_b64()
    if r:
        b64, mime = r
        return (f'<img src="data:image/{mime};base64,{b64}" '
                f'style="max-width:260px;height:auto;display:block;" />')
    return '<h1 class="hero-title">Barco Hospital San Raffaele</h1>'


def logo_eu_footer():
    """HTML del logo UE para el footer, o '' si no existe."""
    r = _get_logo_b64("ES-Funded by EU HA POS.png")
    if not r:
        return ''
    b64, mime = r
    return (f'<img src="data:image/{mime};base64,{b64}" '
            f'style="max-width:120px;height:auto;margin-bottom:0.5rem;" />')