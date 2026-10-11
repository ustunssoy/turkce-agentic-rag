import re
from typing import List, Set

TURKISH_STOPWORDS: Set[str] = {
    "acaba", "altı", "ama", "ancak", "arada", "artık", "asla", "aslında", "ayrıca", "bana",
    "bazen", "bazı", "bazıları", "belki", "ben", "benden", "beni", "benim", "beri", "beş",
    "bile", "bin", "bir", "biraz", "biri", "birkaç", "birkaçı", "birlikte", "birçok", "biri",
    "böyle", "böylece", "bu", "buna", "bunda", "bundan", "bunlar", "bunları", "bunların",
    "bunu", "bunun", "burada", "bütün", "çoğu", "çoğunlukla", "çok", "çünkü", "da", "daha",
    "dahi", "de", "defa", "değil", "diğer", "diye", "dokuz", "dolayı", "dolayısıyla", "dört",
    "edecek", "eden", "ederek", "edilecek", "ediliyor", "edilmesi", "ediyor", "eğer", "elli",
    "en", "etmesi", "etti", "ettiği", "ettiğini", "gibi", "göre", "halen", "hangi", "hangisi",
    "hani", "hatta", "hem", "henüz", "hep", "hepsi", "her", "herhangi", "herkes", "herkese",
    "hiç", "hiçbir", "hiçbiri", "için", "içinde", "iki", "ile", "ilgili", "ise", "işte",
    "itibaren", "itibariyle", "kadar", "karşın", "katrilyon", "kendi", "kendine", "kendini",
    "kendisi", "kendisine", "kendisini", "kez", "ki", "kim", "kime", "kimi", "kimse", "kırk",
    "mı", "mi", "mu", "mü", "nasıl", "ne", "neden", "nedenle", "nerde", "nerede", "nereye",
    "nitekim", "ona", "ondan", "onlar", "onlara", "onlardan", "onların", "onu", "onun", "orada",
    "oysa", "oysaki", "öyle", "pek", "rağmen", "sadece", "sanki", "sekiz", "seksen", "sen",
    "senden", "seni", "senin", "siz", "sizden", "sizi", "sizin", "sonra", "şayet", "şey",
    "şeyler", "şu", "şuna", "şunda", "şundan", "şunlar", "şunu", "şunun", "tabii", "tam",
    "tamam", "tarafından", "tüm", "üç", "üzere", "var", "vardı", "ve", "veya", "veyahut",
    "ya", "yani", "yapacak", "yapılan", "yapılması", "yapıyor", "yedi", "yetmiş", "yine",
    "yok", "yoksa", "yüz", "zaten"
}

TURKISH_LOWERCASE_MAP = {
    ord("I"): "ı",
    ord("İ"): "i",
    ord("Ç"): "ç",
    ord("Ş"): "ş",
    ord("Ğ"): "ğ",
    ord("Ü"): "ü",
    ord("Ö"): "ö",
}


def turkish_lower(text: str) -> str:
    """Accurately lowercases Turkish text respecting dotted and dotless I."""
    return text.translate(TURKISH_LOWERCASE_MAP).lower()


def simple_turkish_stem(token: str) -> str:
    """Lightweight rule-based suffix trimmer for Turkish legal terminology."""
    suffixes = [
        "lerinden", "larından", "lerindeki", "larındaki",
        "lerinin", "larının", "lerine", "larına", "lerini", "larını",
        "leriyle", "larıyla", "lerden", "lardan", "lerde", "larda",
        "lerin", "ların", "lere", "lara", "leri", "ları",
        "sinden", "sından", "sinde", "sında", "sinin", "sının", "sine", "sına", "sini", "sını",
        "imiz", "ımız", "ümüz", "umuz", "iniz", "ınız", "ünüz", "unuz",
        "miz", "mız", "müz", "muz", "niz", "nız", "nüz", "nuz",
        "den", "dan", "ten", "tan", "de", "da", "te", "ta",
        "nin", "nın", "nün", "nun", "in", "ın", "ün", "un",
        "ye", "ya", "e", "a", "yi", "yı", "yu", "yü", "i", "ı", "u", "ü",
        "lik", "lık", "lük", "luk", "ci", "cı", "cü", "cu",
        "le", "la"
    ]
    for suffix in suffixes:
        if token.endswith(suffix) and len(token) - len(suffix) >= 3:
            return token[:-len(suffix)]
    return token


def tokenize_turkish(text: str, stem: bool = True, remove_stop: bool = True) -> List[str]:
    """Tokenizes Turkish text with lowercasing, optional stop-word removal, and stemming."""
    text = turkish_lower(text)
    # Keep alphanumeric characters and numbers (law article numbers are vital, e.g. 'madde 25', '4857')
    raw_tokens = re.findall(r"\b[a-zçğıöşü0-9]+\b", text)
    tokens: List[str] = []
    for tok in raw_tokens:
        if remove_stop and tok in TURKISH_STOPWORDS:
            continue
        if stem and not tok.isdigit():
            tok = simple_turkish_stem(tok)
        if tok:
            tokens.append(tok)
    return tokens
