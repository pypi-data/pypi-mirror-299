preeti_to_unicode_map = {
    'å': 'क',   # क
    'ß': 'ख',   # ख
    'á': 'ग',   # ग
    'ç': 'घ',   # घ
    'é': 'ङ',   # ङ
    '¨': 'च',   # च
    'è': 'छ',   # छ
    'í': 'ज',   # ज
    'ì': 'झ',   # झ
    'ï': 'ञ',   # ञ
    'ó': 'ट',   # ट
    'ô': 'ठ',   # ठ
    'ö': 'ड',   # ड
    'õ': 'ढ',   # ढ
    'Ú': 'ण',   # ण
    '÷': 'त',   # त
    'ø': 'थ',   # थ
    'ü': 'द',   # द
    'ý': 'ध',   # ध
    'þ': 'न',   # न
    'u': 'प',   # प
    'û': 'फ',   # फ
    '¶': 'ब',   # ब
    '¿': 'भ',   # भ
    'l': 'म',   # म
    'º': 'य',   # य
    '›': 'र',   # र
    '‹': 'ल',   # ल
    'Á': 'व',   # व
    '¤': 'श',   # श
    '»': 'ष',   # ष
    '¼': 'स',   # स
    '½': 'ह',   # ह
    '¾': 'क्ष', # क्ष
}

def convert_preeti_to_unicode(preeti_text):
    """
    Convert a Preeti encoded string to its Unicode equivalent.
    :param preeti_text: str
    :return: str
    """
    unicode_text = ""
    for char in preeti_text:
        unicode_text += preeti_to_unicode_map.get(char, char)
    return unicode_text