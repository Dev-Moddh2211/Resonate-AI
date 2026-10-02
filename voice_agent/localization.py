"""Small, explainable market localization layer shared by the Category 3 manager."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

def load_market(market):
    if market == "philippines": return ("Taglish", "neutral", "fil-PH", "taglish")
    if market == "indonesia": return ("Bahasa Indonesia", "formal", "id-ID", "formal")
    return ("English", "neutral", "en-US-neutral", "default")

def detect_language(market, text, previous="neutral"):
    t = text.casefold()
    if market == "philippines":
        tagalog = sum(w in t.split() for w in ("po", "opo", "salamat", "magkano", "kailangan", "ako", "ng", "para", "gusto"))
        english = sum(w in t.split() for w in ("premium", "policy", "coverage", "beneficiary", "rider", "bank", "please", "want"))
        return ("Taglish" if tagalog and english else "Tagalog" if tagalog else "English", "taglish" if tagalog and english else previous)
    colloquial = any(w in t.split() for w in ("nggak", "gak", "gue", "aku", "kapan", "dong", "aja", "kok"))
    english = any(w in t.split() for w in ("tenor", "installment", "loan", "finance", "payment", "follow-up"))
    return ("Bahasa Indonesia" if not english else "Bahasa + finance English", "colloquial" if colloquial else previous)

def localized_text(market, key, register="neutral", fallback=""):
    if market == "philippines":
        return {"greeting":"Hi po! I can help check your life-insurance interest for a preliminary review. Hindi ito approval. Okay po ba to continue?", "escalation":"Sige po, I’ll arrange a specialist callback. I’ll keep the details you shared so you won’t need to repeat everything.", "unauthorized":"Hindi po ako makakapag-guarantee ng approval. I can record the details for preliminary review or arrange a specialist callback.", "fallback":"Wala akong verified answer for that right now. I can record your question and arrange help from an insurance specialist.", "closing":"Salamat po. Kumpleto na ang initial details for preliminary review—this is not an approval or guarantee. Would you like a specialist to follow up?", "clarify":f"{fallback} po, para tama ang ma-record natin."}.get(key, fallback)
    if market == "indonesia":
        colloquial = register == "colloquial"
        return {"greeting":"Halo, saya bisa membantu follow-up pembiayaan dan cicilan Anda untuk peninjauan awal. Ini bukan persetujuan pinjaman. Apakah boleh kita lanjut?", "escalation":"Baik, saya akan catat dan teruskan ke petugas. Detail yang sudah Anda sampaikan akan ikut dalam handoff.", "unauthorized":"Saya tidak bisa menjamin approval atau mengambil keputusan kredit. Saya dapat mencatat informasi untuk peninjauan awal atau meneruskan ke petugas.", "fallback":"Maaf, saya belum punya jawaban yang terverifikasi untuk itu. Saya bisa mencatat pertanyaannya dan meneruskannya ke petugas.", "closing":"Terima kasih. Data awalnya sudah lengkap untuk peninjauan—ini bukan persetujuan. Apakah Anda ingin dihubungi petugas?", "clarify":f"{fallback}, ya." if colloquial else f"{fallback}, mohon."}.get(key, fallback)
    return fallback
