"""MeetingHelper - Huvudapplikation."""

import json
import os
from datetime import datetime

import gi
from meetinghelper.i18n import _

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Adw, Gio, Gtk, Pango  # noqa: E402

from .templates import TEMPLATES  # noqa: E402

DATA_DIR = os.path.join(os.path.expanduser("~"), ".local", "share", "meetinghelper")


class MeetingHelperApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="se.meetinghelper.app")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.win = MeetingHelperWindow(application=app)
        self.win.present()


class MeetingHelperWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, title="MeetingHelper", default_width=800, default_height=700)

        self.current_template = None
        self.checkbuttons = []
        self.notes = {}

        # Huvudlayout
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.set_content(self.main_box)

        # Headerbar
        header = Adw.HeaderBar()
        self.main_box.append(header)

        # Exportknapp i header
        export_btn = Gtk.Button(label=_("💾 Exportera")
        export_btn.add_css_class("suggested-action")
        export_btn.connect("clicked", self.on_export)
        header.pack_end(export_btn)

        # Ladda-knapp i header
        load_btn = Gtk.Button(label=_("📂 Open")
        load_btn.connect("clicked", self.on_load)
        header.pack_end(load_btn)

        # Navigationsstack
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.main_box.append(self.stack)

        self._build_template_chooser()

    def _build_template_chooser(self):
        """Bygg mallväljaren (startsida)."""
        scroll = Gtk.ScrolledWindow(vexpand=True)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        box.set_margin_top(24)
        box.set_margin_bottom(24)
        box.set_margin_start(24)
        box.set_margin_end(24)

        # Rubrik
        title = Gtk.Label(label=_("Select mötestyp")
        title.add_css_class("title-1")
        box.append(title)

        desc = Gtk.Label(label=_("Tryck på den typ av möte du ska ha")
        desc.add_css_class("dim-label")
        box.append(desc)

        # Mallknappar
        for key, tmpl in TEMPLATES.items():
            btn = Gtk.Button()
            btn.set_margin_top(8)
            btn.add_css_class("card")

            btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            btn_box.set_margin_top(16)
            btn_box.set_margin_bottom(16)
            btn_box.set_margin_start(16)
            btn_box.set_margin_end(16)

            icon_label = Gtk.Label(label=tmpl["ikon"])
            icon_label.set_attributes(self._large_font())
            btn_box.append(icon_label)

            text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            name_label = Gtk.Label(label=tmpl["namn"], xalign=0)
            name_label.add_css_class("title-3")
            text_box.append(name_label)

            desc_label = Gtk.Label(label=tmpl["beskrivning"], xalign=0)
            desc_label.add_css_class("dim-label")
            text_box.append(desc_label)

            btn_box.append(text_box)
            btn.set_child(btn_box)
            btn.connect("clicked", self.on_template_chosen, key)
            box.append(btn)

        scroll.set_child(box)
        self.stack.add_named(scroll, "chooser")

    def _large_font(self):
        attrs = Pango.AttrList()
        attrs.insert(Pango.attr_scale_new(2.5))
        return attrs

    def on_template_chosen(self, button, template_key):
        """Användaren har valt en mall."""
        self.current_template = template_key
        self.checkbuttons = []
        self.notes = {}
        self._build_meeting_view(TEMPLATES[template_key])

    def _build_meeting_view(self, tmpl):
        """Bygg mötesvyn med checkboxar och anteckningsfält."""
        # Ta bort gammal vy om den finns
        old = self.stack.get_child_by_name("meeting")
        if old:
            self.stack.remove(old)

        scroll = Gtk.ScrolledWindow(vexpand=True)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        box.set_margin_start(16)
        box.set_margin_end(16)

        # Tillbaka-knapp
        back_btn = Gtk.Button(label=_("← Tillbaka till mallväljaren")
        back_btn.set_halign(Gtk.Align.START)
        back_btn.connect("clicked", lambda b: self.stack.set_visible_child_name("chooser"))
        box.append(back_btn)

        # Mötesrubrik
        header_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        header_box.set_margin_top(8)
        icon = Gtk.Label(label=tmpl["ikon"])
        icon.set_attributes(self._large_font())
        header_box.append(icon)

        title = Gtk.Label(label=tmpl["namn"], xalign=0)
        title.add_css_class("title-1")
        header_box.append(title)
        box.append(header_box)

        # Datum
        today = datetime.now().strftime("%Y-%m-%d")
        date_label = Gtk.Label(label=f"📅 Datum: {today}", xalign=0)
        date_label.add_css_class("title-4")
        box.append(date_label)

        # Deltagarfält
        box.append(self._section_label("👋 Deltagare"))
        self.deltagare_entry = Gtk.Entry()
        self.deltagare_entry.set_placeholder_text(_("Skriv namn på deltagare, separera med komma")
        box.append(self.deltagare_entry)

        # Separator
        box.append(Gtk.Separator())

        # Mötespunkter med checkboxar
        box.append(self._section_label("📋 Mötespunkter"))

        for i, punkt in enumerate(tmpl["punkter"]):
            punkt_frame = Gtk.Frame()
            punkt_frame.add_css_class("card")
            punkt_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
            punkt_box.set_margin_top(12)
            punkt_box.set_margin_bottom(12)
            punkt_box.set_margin_start(12)
            punkt_box.set_margin_end(12)

            # Checkbox-rad
            check_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
            cb = Gtk.CheckButton()
            # Gör checkboxen större via CSS
            cb.set_name(f"big-check-{i}")
            self.checkbuttons.append(cb)
            check_row.append(cb)

            punkt_label = Gtk.Label(label=f"{punkt['ikon']}  {punkt['text']}", xalign=0)
            punkt_label.add_css_class("title-3")
            check_row.append(punkt_label)
            punkt_box.append(check_row)

            # Anteckningsfält
            note_label = Gtk.Label(label=_("Anteckningar:", xalign=0)
            note_label.add_css_class("dim-label")
            punkt_box.append(note_label)

            tv = Gtk.TextView()
            tv.set_wrap_mode(Gtk.WrapMode.WORD)
            tv.set_top_margin(8)
            tv.set_bottom_margin(8)
            tv.set_left_margin(8)
            tv.set_right_margin(8)
            tv.set_size_request(-1, 80)
            tv.add_css_class("card")
            self.notes[i] = tv
            punkt_box.append(tv)

            punkt_frame.set_child(punkt_box)
            box.append(punkt_frame)

        # Övriga anteckningar
        box.append(Gtk.Separator())
        box.append(self._section_label("📝 Övriga anteckningar"))
        self.extra_notes = Gtk.TextView()
        self.extra_notes.set_wrap_mode(Gtk.WrapMode.WORD)
        self.extra_notes.set_top_margin(8)
        self.extra_notes.set_bottom_margin(8)
        self.extra_notes.set_left_margin(8)
        self.extra_notes.set_right_margin(8)
        self.extra_notes.set_size_request(-1, 120)
        self.extra_notes.add_css_class("card")
        box.append(self.extra_notes)

        # Beslut-sektion
        box.append(Gtk.Separator())
        box.append(self._section_label("✅ Beslut"))
        self.beslut_tv = Gtk.TextView()
        self.beslut_tv.set_wrap_mode(Gtk.WrapMode.WORD)
        self.beslut_tv.set_top_margin(8)
        self.beslut_tv.set_bottom_margin(8)
        self.beslut_tv.set_left_margin(8)
        self.beslut_tv.set_right_margin(8)
        self.beslut_tv.set_size_request(-1, 100)
        self.beslut_tv.add_css_class("card")
        box.append(self.beslut_tv)

        scroll.set_child(box)
        self.stack.add_named(scroll, "meeting")
        self.stack.set_visible_child_name("meeting")

        self._apply_css()

    def _section_label(self, text):
        label = Gtk.Label(label=text, xalign=0)
        label.add_css_class("title-2")
        label.set_margin_top(8)
        return label

    def _apply_css(self):
        css = b"""
        checkbutton indicator {
            min-width: 32px;
            min-height: 32px;
        }
        """
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_display(
            self.get_display(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def _get_text(self, textview):
        buf = textview.get_buffer()
        return buf.get_text(buf.get_start_iter(), buf.get_end_iter(), False)

    def _collect_data(self):
        """Samla in all mötesdata."""
        if not self.current_template:
            return None
        tmpl = TEMPLATES[self.current_template]
        punkter = []
        for i, punkt in enumerate(tmpl["punkter"]):
            punkter.append({
                "text": punkt["text"],
                "ikon": punkt["ikon"],
                "avklarad": self.checkbuttons[i].get_active(),
                "anteckningar": self._get_text(self.notes[i]),
            })
        return {
            "mall": tmpl["namn"],
            "datum": datetime.now().strftime("%Y-%m-%d"),
            "tid": datetime.now().strftime("%H:%M"),
            "deltagare": self.deltagare_entry.get_text(),
            "punkter": punkter,
            "ovriga_anteckningar": self._get_text(self.extra_notes),
            "beslut": self._get_text(self.beslut_tv),
        }

    def on_export(self, button):
        """Exportera mötesprotokoll."""
        data = self._collect_data()
        if not data:
            self._show_message("Välj en mall och fyll i mötesprotokollet först.")
            return

        dialog = Gtk.FileDialog()
        dialog.set_initial_name(f"motesprotokoll_{data['datum']}.txt")

        txt_filter = Gtk.FileFilter()
        txt_filter.set_name("Textfil (.txt)")
        txt_filter.add_pattern("*.txt")

        json_filter = Gtk.FileFilter()
        json_filter.set_name("JSON (.json)")
        json_filter.add_pattern("*.json")

        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(txt_filter)
        filters.append(json_filter)
        dialog.set_filters(filters)

        dialog.save(self, None, self._on_export_response, data)

    def _on_export_response(self, dialog, result, data):
        try:
            file = dialog.save_finish(result)
            path = file.get_path()
        except Exception:
            return

        if path.endswith(".json"):
            content = json.dumps(data, ensure_ascii=False, indent=2)
        else:
            content = self._format_text(data)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        self._show_message(f"Sparat till:\n{path}")

    def _format_text(self, data):
        """Formatera mötesprotokoll som text."""
        lines = [
            "═" * 50,
            f"  MÖTESPROTOKOLL - {data['mall']}",
            "═" * 50,
            f"  📅 Datum: {data['datum']}   🕐 Tid: {data['tid']}",
            f"  👋 Deltagare: {data['deltagare']}",
            "─" * 50,
            "",
            "  📋 MÖTESPUNKTER",
            "─" * 50,
        ]
        for p in data["punkter"]:
            status = "✅" if p["avklarad"] else "⬜"
            lines.append(f"  {status} {p['ikon']} {p['text']}")
            if p["anteckningar"].strip():
                for line in p["anteckningar"].strip().split("\n"):
                    lines.append(f"      {line}")
            lines.append("")

        if data["ovriga_anteckningar"].strip():
            lines.append("─" * 50)
            lines.append("  📝 ÖVRIGA ANTECKNINGAR")
            lines.append("─" * 50)
            lines.append(f"  {data['ovriga_anteckningar']}")
            lines.append("")

        if data["beslut"].strip():
            lines.append("─" * 50)
            lines.append("  ✅ BESLUT")
            lines.append("─" * 50)
            lines.append(f"  {data['beslut']}")
            lines.append("")

        lines.append("═" * 50)
        return "\n".join(lines) + "\n"

    def on_load(self, button):
        """Ladda ett sparat mötesprotokoll."""
        dialog = Gtk.FileDialog()
        json_filter = Gtk.FileFilter()
        json_filter.set_name("JSON-filer (.json)")
        json_filter.add_pattern("*.json")
        filters = Gio.ListStore.new(Gtk.FileFilter)
        filters.append(json_filter)
        dialog.set_filters(filters)
        dialog.open(self, None, self._on_load_response)

    def _on_load_response(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            path = file.get_path()
        except Exception:
            return

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Hitta rätt mall
        for key, tmpl in TEMPLATES.items():
            if tmpl["namn"] == data.get("mall"):
                self.current_template = key
                self.checkbuttons = []
                self.notes = {}
                self._build_meeting_view(tmpl)
                # Fyll i data
                self.deltagare_entry.set_text(data.get("deltagare", ""))
                for i, p in enumerate(data.get("punkter", [])):
                    if i < len(self.checkbuttons):
                        self.checkbuttons[i].set_active(p.get("avklarad", False))
                    if i in self.notes and p.get("anteckningar"):
                        self.notes[i].get_buffer().set_text(p["anteckningar"])
                if data.get("ovriga_anteckningar"):
                    self.extra_notes.get_buffer().set_text(data["ovriga_anteckningar"])
                if data.get("beslut"):
                    self.beslut_tv.get_buffer().set_text(data["beslut"])
                return

        self._show_message("Kunde inte hitta matchande mall för detta protokoll.")

    def _show_message(self, text):
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading="MeetingHelper",
            body=text,
        )
        dialog.add_response("ok", "OK")
        dialog.present()


def main():
    app = MeetingHelperApp()
    app.run()
