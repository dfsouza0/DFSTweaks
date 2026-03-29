#!/usr/bin/env python3
"""DFSTweaks - Ferramenta de Otimização de PC para Windows"""

import customtkinter as ctk
import subprocess
import threading
import sys
import ctypes
import os
from tkinter import BooleanVar

from tweaks import TWEAKS

# ─── Admin ────────────────────────────────────────────────────────────────────

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def request_admin():
    if not is_admin():
        script = os.path.abspath(sys.argv[0])
        args = " ".join(f'"{a}"' for a in sys.argv[1:])
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", script, args, None, 1)
        if ret > 32:
            sys.exit(0)


# ─── Theme ────────────────────────────────────────────────────────────────────

C = {
    "bg":         "#1c1c1c",
    "sidebar":    "#212121",
    "card":       "#2a2a2a",
    "card_hover": "#303030",
    "active":     "#313131",
    "border":     "#383838",
    "accent":     "#4a7de8",
    "accent_h":   "#3a6bd8",
    "text":       "#f0f0f0",
    "text_dim":   "#969696",
    "text_muted": "#555555",
    "success":    "#4caf50",
    "success_h":  "#388e3c",
    "warning":    "#ff9800",
}

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ─── TweakCard ────────────────────────────────────────────────────────────────

class TweakCard(ctk.CTkFrame):
    def __init__(self, parent, tweak: dict, **kwargs):
        super().__init__(
            parent,
            fg_color=C["card"],
            corner_radius=8,
            border_width=1,
            border_color=C["border"],
            **kwargs,
        )
        self.tweak = tweak
        self.var = BooleanVar(value=False)
        self._build()

    def _build(self):
        self.columnconfigure(1, weight=1)

        # Left accent bar
        bar = ctk.CTkFrame(self, fg_color=C["accent"], width=3, corner_radius=2)
        bar.grid(row=0, column=0, rowspan=2, padx=(10, 10), pady=10, sticky="ns")

        # Name
        ctk.CTkLabel(
            self,
            text=self.tweak["name"],
            text_color=C["text"],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).grid(row=0, column=1, sticky="ew", padx=(0, 8), pady=(12, 2))

        # Description
        ctk.CTkLabel(
            self,
            text=self.tweak["desc"],
            text_color=C["text_dim"],
            font=ctk.CTkFont(size=11),
            anchor="w",
            wraplength=580,
            justify="left",
        ).grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(0, 12))

        # Toggle switch
        ctk.CTkSwitch(
            self,
            text="",
            variable=self.var,
            width=46,
            height=24,
            button_color=C["accent"],
            button_hover_color=C["accent_h"],
            progress_color=C["accent"],
            fg_color=C["border"],
        ).grid(row=0, column=2, rowspan=2, padx=(8, 14), pady=10)


# ─── Main App ─────────────────────────────────────────────────────────────────

class DFSTweaksApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DFSTweaks")
        self.geometry("1240x740")
        self.minsize(960, 600)
        self.configure(fg_color=C["bg"])

        try:
            if os.path.exists("assets/icon.ico"):
                self.iconbitmap("assets/icon.ico")
        except Exception:
            pass

        self.current_cat = list(TWEAKS.keys())[0]
        self.nav_btns: dict[str, ctk.CTkButton] = {}
        self.all_cards: dict[str, list[TweakCard]] = {}

        self._build_layout()
        self._build_sidebar()
        self._build_content()
        self._pre_build_cards()
        self._select_cat(self.current_cat)

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar_frame = ctk.CTkFrame(
            self, fg_color=C["sidebar"], corner_radius=0, width=268,
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.sidebar_frame.columnconfigure(0, weight=1)

        self.content_frame = ctk.CTkFrame(self, fg_color=C["bg"], corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nsew")
        self.content_frame.grid_rowconfigure(1, weight=1)
        self.content_frame.columnconfigure(0, weight=1)

    # ── Sidebar ───────────────────────────────────────────────────────────────

    def _build_sidebar(self):
        # ── Logo ──────────────────────────────────────────────────────
        logo_row = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_row.grid(row=0, column=0, sticky="ew", padx=18, pady=(22, 4))

        # Diamond icon
        diamond = ctk.CTkFrame(logo_row, fg_color=C["accent"], width=38, height=38, corner_radius=6)
        diamond.pack(side="left", padx=(0, 10))
        diamond.pack_propagate(False)
        ctk.CTkLabel(
            diamond, text="◆", text_color="#ffffff",
            font=ctk.CTkFont(size=16, weight="bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")

        name_col = ctk.CTkFrame(logo_row, fg_color="transparent")
        name_col.pack(side="left")

        title_row = ctk.CTkFrame(name_col, fg_color="transparent")
        title_row.pack(anchor="w")
        ctk.CTkLabel(
            title_row, text="DFS", text_color=C["accent"],
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(side="left")
        ctk.CTkLabel(
            title_row, text="Tweaks", text_color=C["text"],
            font=ctk.CTkFont(size=18, weight="bold"),
        ).pack(side="left", padx=(2, 0))

        ctk.CTkLabel(
            name_col, text="github.com/dfsouza0/DFSTweaks",
            text_color=C["text_muted"],
            font=ctk.CTkFont(size=10),
        ).pack(anchor="w")

        # ── Action buttons ────────────────────────────────────────────
        btn_outer = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        btn_outer.grid(row=1, column=0, sticky="ew", padx=12, pady=(14, 4))
        btn_outer.columnconfigure((0, 1), weight=1)

        def _sbtn(parent, text, cmd, row, col, colspan=1, color=None, hcolor=None, tcolor=None):
            ctk.CTkButton(
                parent, text=text,
                fg_color=color or C["card"],
                hover_color=hcolor or C["active"],
                text_color=tcolor or C["text_dim"],
                height=32, corner_radius=6,
                font=ctk.CTkFont(size=11),
                command=cmd,
            ).grid(row=row, column=col, columnspan=colspan, sticky="ew", padx=3, pady=3)

        _sbtn(btn_outer, "✓  Marcar Todos",    self._select_all,           0, 0, 2, tcolor=C["text"])
        _sbtn(btn_outer, "✗  Desmarcar Todos", self._deselect_all,         1, 0)
        _sbtn(btn_outer, "☑  Marcar Categoria",self._select_cat_all,       1, 1)

        # ── Separator ─────────────────────────────────────────────────
        ctk.CTkFrame(self.sidebar_frame, fg_color=C["border"], height=1
                     ).grid(row=2, column=0, sticky="ew", padx=12, pady=(8, 4))

        # ── Nav scroll ────────────────────────────────────────────────
        nav = ctk.CTkScrollableFrame(
            self.sidebar_frame, fg_color="transparent",
            scrollbar_button_color=C["border"],
            scrollbar_button_hover_color=C["active"],
        )
        nav.grid(row=3, column=0, sticky="nsew", padx=6, pady=4)
        nav.columnconfigure(0, weight=1)

        for i, (cat, data) in enumerate(TWEAKS.items()):
            n = len(data["items"])
            btn = ctk.CTkButton(
                nav,
                text=f"  {data['icon']}  {cat}",
                anchor="w",
                fg_color="transparent",
                hover_color=C["active"],
                text_color=C["text_dim"],
                height=40,
                corner_radius=6,
                font=ctk.CTkFont(size=13),
                command=lambda c=cat: self._select_cat(c),
            )
            btn.grid(row=i, column=0, sticky="ew", padx=4, pady=2)
            self.nav_btns[cat] = btn

        # ── Run button ────────────────────────────────────────────────
        ctk.CTkFrame(self.sidebar_frame, fg_color=C["border"], height=1
                     ).grid(row=4, column=0, sticky="ew", padx=12, pady=(4, 0))

        self.run_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="▶   Executar Selecionados",
            fg_color=C["accent"],
            hover_color=C["accent_h"],
            text_color="#ffffff",
            height=42,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._run_selected,
        )
        self.run_btn.grid(row=5, column=0, sticky="ew", padx=12, pady=(8, 18))

    # ── Content area ──────────────────────────────────────────────────────────

    def _build_content(self):
        header = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=72)
        header.grid(row=0, column=0, sticky="ew", padx=28, pady=(20, 0))
        header.grid_propagate(False)

        self.cat_title = ctk.CTkLabel(
            header, text="",
            text_color=C["text"],
            font=ctk.CTkFont(size=28, weight="bold"),
            anchor="w",
        )
        self.cat_title.pack(anchor="w")

        self.cat_sub = ctk.CTkLabel(
            header, text="",
            text_color=C["text_dim"],
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        self.cat_sub.pack(anchor="w")

        self.scroll = ctk.CTkScrollableFrame(
            self.content_frame,
            fg_color="transparent",
            scrollbar_button_color=C["border"],
            scrollbar_button_hover_color=C["active"],
        )
        self.scroll.grid(row=1, column=0, sticky="nsew", padx=18, pady=(10, 18))
        self.scroll.columnconfigure(0, weight=1)

    def _pre_build_cards(self):
        for cat, data in TWEAKS.items():
            cards = []
            for tweak in data["items"]:
                card = TweakCard(self.scroll, tweak)
                cards.append(card)
            self.all_cards[cat] = cards

    # ── Category switching ────────────────────────────────────────────────────

    def _select_cat(self, cat: str):
        for c, btn in self.nav_btns.items():
            if c == cat:
                btn.configure(fg_color=C["active"], text_color=C["text"])
            else:
                btn.configure(fg_color="transparent", text_color=C["text_dim"])

        self.current_cat = cat
        data = TWEAKS[cat]
        n = len(data["items"])
        self.cat_title.configure(text=f"{data['icon']}  {cat}")
        self.cat_sub.configure(text=f"{n} otimização{'ões' if n != 1 else 'ão'} disponíve{'is' if n != 1 else 'l'}")

        for child in self.scroll.winfo_children():
            child.grid_forget()

        for i, card in enumerate(self.all_cards[cat]):
            card.grid(row=i, column=0, sticky="ew", padx=6, pady=5)

    # ── Select / deselect ─────────────────────────────────────────────────────

    def _select_all(self):
        for cards in self.all_cards.values():
            for c in cards:
                c.var.set(True)

    def _deselect_all(self):
        for cards in self.all_cards.values():
            for c in cards:
                c.var.set(False)

    def _select_cat_all(self):
        for c in self.all_cards[self.current_cat]:
            c.var.set(True)

    # ── Execution ─────────────────────────────────────────────────────────────

    def _run_selected(self):
        selected = [
            (cat, card.tweak)
            for cat, cards in self.all_cards.items()
            for card in cards
            if card.var.get()
        ]

        if not selected:
            self._dialog(
                "Nenhum item selecionado",
                "Ative pelo menos uma otimização antes de executar.",
            )
            return

        self._exec_window(selected)

    def _exec_window(self, selected: list):
        win = ctk.CTkToplevel(self)
        win.title("DFSTweaks — Executando")
        win.geometry("760x520")
        win.configure(fg_color=C["bg"])
        win.grab_set()

        ctk.CTkLabel(
            win, text="Aplicando otimizações...",
            text_color=C["text"],
            font=ctk.CTkFont(size=16, weight="bold"),
        ).pack(anchor="w", padx=18, pady=(16, 6))

        log = ctk.CTkTextbox(
            win, fg_color=C["card"],
            text_color=C["text"],
            font=ctk.CTkFont(family="Consolas", size=11),
            state="disabled",
            border_color=C["border"],
            border_width=1,
        )
        log.pack(fill="both", expand=True, padx=18, pady=(0, 8))

        prog = ctk.CTkProgressBar(
            win, fg_color=C["card"],
            progress_color=C["accent"],
            height=8, corner_radius=4,
        )
        prog.pack(fill="x", padx=18, pady=(0, 8))
        prog.set(0)

        close_btn = ctk.CTkButton(
            win, text="Aguarde...",
            state="disabled",
            fg_color=C["card"],
            hover_color=C["active"],
            text_color=C["text_dim"],
            command=win.destroy,
        )
        close_btn.pack(pady=(0, 16))

        def log_write(msg: str):
            log.configure(state="normal")
            log.insert("end", msg + "\n")
            log.see("end")
            log.configure(state="disabled")

        def run_thread():
            total = len(selected)
            for idx, (cat, tweak) in enumerate(selected):
                win.after(0, log_write, f"\n[{cat}] {tweak['name']}")
                win.after(0, log_write, "─" * 56)

                script = "\n".join(tweak["cmds"])
                try:
                    proc = subprocess.Popen(
                        [
                            "powershell", "-NoProfile", "-NonInteractive",
                            "-ExecutionPolicy", "Bypass", "-Command", script,
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                        creationflags=subprocess.CREATE_NO_WINDOW,
                    )
                    for line in proc.stdout:
                        line = line.strip()
                        if line:
                            win.after(0, log_write, f"  {line}")
                    proc.wait()
                    win.after(0, log_write, "  ✓ Concluído")
                except Exception as e:
                    win.after(0, log_write, f"  ✗ Erro: {e}")

                win.after(0, prog.set, (idx + 1) / total)

            win.after(0, log_write, "\n✓ Todas as otimizações foram aplicadas com sucesso!")
            win.after(
                0,
                lambda: close_btn.configure(
                    text="Fechar", state="normal",
                    fg_color=C["success"], hover_color=C["success_h"],
                    text_color="#ffffff",
                ),
            )

        threading.Thread(target=run_thread, daemon=True).start()

    # ── Dialog ────────────────────────────────────────────────────────────────

    def _dialog(self, title: str, msg: str):
        win = ctk.CTkToplevel(self)
        win.title(title)
        win.geometry("420x160")
        win.configure(fg_color=C["bg"])
        win.grab_set()

        ctk.CTkLabel(
            win, text=title,
            text_color=C["text"],
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(padx=20, pady=(20, 6))

        ctk.CTkLabel(
            win, text=msg,
            text_color=C["text_dim"],
            font=ctk.CTkFont(size=12),
        ).pack(padx=20, pady=(0, 12))

        ctk.CTkButton(
            win, text="OK",
            fg_color=C["accent"],
            hover_color=C["accent_h"],
            command=win.destroy,
        ).pack(pady=(0, 18))


# ─── Entry point ──────────────────────────────────────────────────────────────

def main():
    if sys.platform == "win32":
        request_admin()
    app = DFSTweaksApp()
    app.mainloop()


if __name__ == "__main__":
    main()
