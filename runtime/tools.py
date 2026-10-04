"""Registry + implementasi tools: web, file, shell, memory, skills."""
from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Callable

import requests
from bs4 import BeautifulSoup

from .config import Config
from .memory import Memory
from .skills import SkillStore

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) muse-assistant-runtime/0.1"}


# ---------------------------------------------------------------- helpers

def _safe_path(cfg: Config, path: str) -> Path:
    """Pastikan path tetap di dalam workspace (cegah path traversal)."""
    p = (cfg.workspace / path).resolve()
    if p != cfg.workspace and cfg.workspace not in p.parents:
        raise ValueError(f"Path di luar workspace: {path}")
    return p


def _html_to_text(html: str, limit: int = 8000) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    return "\n".join(lines)[:limit]


# ---------------------------------------------------------------- tool impls

def _parse_ddg(html: str, count: int) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for res in soup.select(".result")[:count]:
        a = res.select_one(".result__a")
        snip = res.select_one(".result__snippet")
        if not a:
            continue
        url = a.get("href", "")
        m = re.search(r"[?&]uddg=([^&]+)", url)
        if m:
            from urllib.parse import unquote
            url = unquote(m.group(1))
        out.append(f"- {a.get_text(strip=True)}\n  {url}\n  {(snip.get_text(strip=True) if snip else '')[:300]}")
    return out


def _parse_bing(html: str, count: int) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    out = []
    for res in soup.select(".b_algo")[:count]:
        h2 = res.select_one("h2")
        if not h2:
            continue
        a = h2.select_one("a")
        snip = res.select_one(".b_caption p") or res.select_one("p")
        title = h2.get_text(strip=True)
        url = a.get("href", "") if a else ""
        out.append(f"- {title}\n  {url}\n  {(snip.get_text(strip=True) if snip else '')[:300]}")
    return out


def tool_web_search(query: str, count: int = 5) -> str:
    """Cari web tanpa API key (coba DuckDuckGo, fallback ke Bing)."""
    count = max(1, min(count, 10))
    errors = []
    # 1) DuckDuckGo
    try:
        r = requests.post("https://html.duckduckgo.com/html/", data={"q": query},
                          headers=UA, timeout=15)
        r.raise_for_status()
        out = _parse_ddg(r.text, count)
        if out:
            return "\n".join(out)
    except Exception as e:
        errors.append(f"DDG: {e}")
    # 2) Bing (fallback)
    try:
        r = requests.get("https://www.bing.com/search",
                         params={"q": query}, headers=UA, timeout=20)
        r.raise_for_status()
        out = _parse_bing(r.text, count)
        if out:
            return "\n".join(out)
    except Exception as e:
        errors.append(f"Bing: {e}")
    return "Tidak ada hasil. (" + "; ".join(errors) + ")"


def tool_web_fetch(url: str, limit: int = 8000) -> str:
    """Ambil teks bersih dari sebuah URL (tanpa JavaScript)."""
    try:
        r = requests.get(url, headers=UA, timeout=25)
        r.raise_for_status()
    except Exception as e:
        return f"Gagal fetch {url}: {e}"
    text = _html_to_text(r.text, limit)
    return text or "(halaman kosong / tidak ada teks terbaca)"


class Browser:
    """Browser live (Playwright/Chromium) — dipakai tool_web_browse."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self._pw = None
        self._browser = None
        self._page = None

    def _ensure(self):
        if self._page:
            return self._page
        try:
            from playwright.sync_api import sync_playwright
        except ImportError:
            raise RuntimeError("playwright belum diinstal: pip install playwright && playwright install chromium")
        self._pw = sync_playwright().start()
        try:
            self._browser = self._pw.chromium.launch(headless=self.cfg.browser_headless)
        except Exception as e:
            raise RuntimeError(
                f"Gagal meluncurkan Chromium ({e}). Jalankan: playwright install chromium"
            )
        self._page = self._browser.new_page()
        self._page.set_default_timeout(self.cfg.browser_timeout)
        return self._page

    def act(self, action: str, **kw) -> str:
        page = self._ensure()
        try:
            if action == "goto":
                page.goto(kw["url"], wait_until="domcontentloaded")
                return f"Membuka {kw['url']} — judul: {page.title()}"
            if action == "text":
                return page.inner_text("body")[: int(kw.get("limit", 8000))]
            if action == "click":
                page.click(kw["selector"])
                page.wait_for_timeout(1000)
                return f"Klik {kw['selector']} — judul sekarang: {page.title()}"
            if action == "fill":
                page.fill(kw["selector"], kw["text"])
                return f"Mengisi {kw['selector']}"
            if action == "press":
                page.keyboard.press(kw["key"])
                page.wait_for_timeout(800)
                return f"Menekan {kw['key']}"
            if action == "url":
                return page.url
            if action == "screenshot":
                path = str(kw.get("path", "screenshot.png"))
                page.screenshot(path=path)
                return f"Screenshot tersimpan: {path}"
            if action == "wait":
                page.wait_for_timeout(int(kw.get("ms", 2000)))
                return "Menunggu selesai."
            return f"Aksi tidak dikenal: {action}"
        except Exception as e:
            return f"Gagal ({action}): {e}"

    def close(self):
        try:
            if self._browser:
                self._browser.close()
            if self._pw:
                self._pw.stop()
        except Exception:
            pass
        self._page = self._browser = self._pw = None


# ---------------------------------------------------------------- registry

def build_tools(cfg: Config, memory: Memory, skills: SkillStore, browser: Browser):
    def _read_file(path: str) -> str:
        try:
            p = _safe_path(cfg, path)
            return p.read_text(encoding="utf-8")[:20000]
        except Exception as e:
            return f"Gagal baca: {e}"

    def _write_file(path: str, content: str) -> str:
        try:
            p = _safe_path(cfg, path)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
            return f"Tersimpan: {p.relative_to(cfg.workspace)}"
        except Exception as e:
            return f"Gagal tulis: {e}"

    def _list_dir(path: str = ".") -> str:
        try:
            p = _safe_path(cfg, path)
            items = sorted(p.iterdir(), key=lambda x: (not x.is_dir(), x.name))
            return "\n".join(("📁 " if x.is_dir() else "📄 ") + x.name for x in items) or "(kosong)"
        except Exception as e:
            return f"Gagal list: {e}"

    def _shell(command: str) -> str:
        if not cfg.allow_shell:
            return ("Shell nonaktif. Nyalakan dengan ALLOW_SHELL=1 jika kamu sadar risikonya "
                    "(perintah shell bisa merusak sistem).")
        try:
            r = subprocess.run(command, shell=True, capture_output=True, text=True,
                               timeout=cfg.shell_timeout, cwd=cfg.workspace)
            out = (r.stdout + r.stderr).strip()[:8000]
            return f"[exit {r.returncode}]\n{out or '(tanpa output)'}"
        except subprocess.TimeoutExpired:
            return f"Timeout setelah {cfg.shell_timeout}s."
        except Exception as e:
            return f"Gagal: {e}"

    def _browse(action: str, args_json: str = "{}") -> str:
        try:
            args = json.loads(args_json) if isinstance(args_json, str) else {}
        except Exception:
            return "args_json bukan JSON valid."
        return browser.act(action, **args)

    tools: dict[str, tuple[dict, Callable[..., str]]] = {
        "web_search": ({
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Cari web (DuckDuckGo, tanpa API key). Kembalikan judul, URL, snippet.",
                "parameters": {"type": "object", "properties": {
                    "query": {"type": "string"},
                    "count": {"type": "integer", "default": 5}},
                    "required": ["query"]}}}, tool_web_search),
        "web_fetch": ({
            "type": "function",
            "function": {
                "name": "web_fetch",
                "description": "Ambil teks bersih dari URL (tanpa JavaScript; untuk situs JS pakai web_browse).",
                "parameters": {"type": "object", "properties": {
                    "url": {"type": "string"},
                    "limit": {"type": "integer", "default": 8000}},
                    "required": ["url"]}}}, tool_web_fetch),
        "web_browse": ({
            "type": "function",
            "function": {
                "name": "web_browse",
                "description": ("Browser live (Chromium). action: goto{url} | text{limit} | click{selector} | "
                                "fill{selector,text} | press{key} | url | screenshot{path} | wait{ms}. "
                                "args_json berisi parameter aksi sebagai JSON."),
                "parameters": {"type": "object", "properties": {
                    "action": {"type": "string"},
                    "args_json": {"type": "string", "default": "{}"}},
                    "required": ["action"]}}}, _browse),
        "read_file": ({
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Baca file di dalam workspace.",
                "parameters": {"type": "object", "properties": {
                    "path": {"type": "string", "description": "path relatif thd workspace"}},
                    "required": ["path"]}}}, _read_file),
        "write_file": ({
            "type": "function",
            "function": {
                "name": "write_file",
                "description": "Tulis/overwrite file di dalam workspace.",
                "parameters": {"type": "object", "properties": {
                    "path": {"type": "string"},
                    "content": {"type": "string"}},
                    "required": ["path", "content"]}}}, _write_file),
        "list_dir": ({
            "type": "function",
            "function": {
                "name": "list_dir",
                "description": "Lihat isi direktori di dalam workspace.",
                "parameters": {"type": "object", "properties": {
                    "path": {"type": "string", "default": "."}}}}}, _list_dir),
        "shell": ({
            "type": "function",
            "function": {
                "name": "shell",
                "description": "Jalankan perintah shell di workspace (perlu ALLOW_SHELL=1).",
                "parameters": {"type": "object", "properties": {
                    "command": {"type": "string"}},
                    "required": ["command"]}}}, _shell),
        "remember": ({
            "type": "function",
            "function": {
                "name": "remember",
                "description": "Simpan fakta tahan lama ke memori.",
                "parameters": {"type": "object", "properties": {
                    "fact": {"type": "string"}},
                    "required": ["fact"]}}}, memory.remember),
        "recall": ({
            "type": "function",
            "function": {
                "name": "recall",
                "description": "Cari ingatan yang relevan dengan query.",
                "parameters": {"type": "object", "properties": {
                    "query": {"type": "string"}},
                    "required": ["query"]}}}, memory.recall),
        "load_skill": ({
            "type": "function",
            "function": {
                "name": "load_skill",
                "description": ("Muat playbook lengkap sebuah skill. Katalog:\n" + skills.catalog_text()),
                "parameters": {"type": "object", "properties": {
                    "name": {"type": "string"}},
                    "required": ["name"]}}}, skills.load),
    }

    schemas = [schema for schema, _ in tools.values()]
    funcs = {name: fn for name, (_, fn) in tools.items()}
    return schemas, funcs


def check_playwright_browser() -> str:
    """Cek apakah Chromium Playwright tersedia (untuk pesan setup)."""
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True)
            b.close()
        return "ok"
    except Exception as e:
        return str(e)


def _tool_names_for_prompt() -> str:
    return "web_search, web_fetch, web_browse, read_file, write_file, list_dir, shell, remember, recall, load_skill"
