"""Fördefinierade mötesmallar för LSS och vårdplanering."""

TEMPLATES = {
    "lss_utredning": {
        "namn": "LSS-utredning",
        "ikon": "🔍",
        "beskrivning": "Mall för LSS-utredning och behovsbedömning",
        "punkter": [
            {"text": "Presentation av deltagare", "ikon": "👋"},
            {"text": "Genomgång av aktuell situation", "ikon": "📋"},
            {"text": "Behov och önskemål", "ikon": "💬"},
            {"text": "Bedömning av insatser", "ikon": "✅"},
            {"text": "Beslut om insatser", "ikon": "📝"},
            {"text": "Uppföljning - när och hur", "ikon": "📅"},
        ],
    },
    "vardplanering": {
        "namn": "Vårdplanering",
        "ikon": "🏥",
        "beskrivning": "Mall för samordnad vårdplanering",
        "punkter": [
            {"text": "Presentation av deltagare", "ikon": "👋"},
            {"text": "Medicinsk status", "ikon": "🏥"},
            {"text": "Omvårdnadsbehov", "ikon": "❤️"},
            {"text": "Rehabilitering", "ikon": "💪"},
            {"text": "Hjälpmedel", "ikon": "🦽"},
            {"text": "Sociala insatser", "ikon": "🤝"},
            {"text": "Beslut och åtgärder", "ikon": "✅"},
            {"text": "Nästa möte", "ikon": "📅"},
        ],
    },
    "uppfoljning": {
        "namn": "Uppföljningsmöte",
        "ikon": "🔄",
        "beskrivning": "Mall för uppföljning av pågående insatser",
        "punkter": [
            {"text": "Presentation av deltagare", "ikon": "👋"},
            {"text": "Hur har det gått sedan sist?", "ikon": "📊"},
            {"text": "Vad fungerar bra?", "ikon": "👍"},
            {"text": "Vad behöver ändras?", "ikon": "🔧"},
            {"text": "Nya beslut", "ikon": "📝"},
            {"text": "Nästa uppföljning", "ikon": "📅"},
        ],
    },
    "genomforandeplan": {
        "namn": "Genomförandeplan",
        "ikon": "📑",
        "beskrivning": "Mall för upprättande av genomförandeplan",
        "punkter": [
            {"text": "Presentation av deltagare", "ikon": "👋"},
            {"text": "Personens mål och önskemål", "ikon": "🎯"},
            {"text": "Dagliga rutiner", "ikon": "🕐"},
            {"text": "Stöd och hjälp", "ikon": "🤝"},
            {"text": "Aktiviteter och fritid", "ikon": "⚽"},
            {"text": "Hälsa och välmående", "ikon": "❤️"},
            {"text": "Överenskommelser", "ikon": "✅"},
            {"text": "Datum för uppföljning", "ikon": "📅"},
        ],
    },
}
