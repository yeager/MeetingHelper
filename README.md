# MeetingHelper

**Visuellt mötesprotokoll för LSS/vårdplanering**

MeetingHelper är en enkel GTK4-app designad för att göra mötesprotokoll tillgängliga för personer med kognitiva funktionshinder. Appen använder piktogram, stora checkboxar och tydlig layout.

## Funktioner

- 🔍 **LSS-utredning** - Mall för behovsbedömning
- 🏥 **Vårdplanering** - Mall för samordnad vårdplanering
- 🔄 **Uppföljningsmöte** - Mall för uppföljning
- 📑 **Genomförandeplan** - Mall för genomförandeplan
- ✅ Stora checkboxar för mötespunkter
- 📝 Anteckningsfält för varje punkt
- 💾 Export till text eller JSON
- 📂 Öppna sparade protokoll

## Installation

### Krav

- Python 3.8+
- GTK4
- libadwaita
- PyGObject

### Linux (Debian/Ubuntu)

```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1
pip install .
```

### Kör utan installation

```bash
python -m meetinghelper
```

## Användning

1. Starta appen
2. Välj mötestyp genom att trycka på ett kort
3. Fyll i deltagare
4. Bocka av punkter och skriv anteckningar
5. Exportera med 💾-knappen

## Filstruktur

```
meetinghelper/
├── __init__.py      # Paketinfo
├── __main__.py      # Startpunkt
├── app.py           # Huvudapplikation (GTK4/Adwaita)
└── templates.py     # Mötesmallar
setup.py             # Installation
se.meetinghelper.app.desktop  # Skrivbordsgenväg
```

## Licens

MIT
