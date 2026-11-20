import hashlib
import os
from pathlib import Path
import flet as ft
import httpx

APP_NAME = "Shield AI Hub"
APP_VERSION = "1.0.0"

# قائمة المزودين للتبديل التلقائي عند نفاد التوكنز أو عدم توفر الشبكة
AI_PROVIDERS = [
    {"name": "OpenRouter (Free)", "url": "https://openrouter.ai/api/v1/chat/completions", "model": "deepseek/deepseek-chat:free"},
    {"name": "Qwen Studio", "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions", "model": "qwen-turbo"},
    {"name": "Offline Local Engine", "url": None, "model": "local-index"},
]

TRANSLATIONS = {
    "ar": {
        "title": "درع الملفات والبحث الذكي",
        "search_hint": "ابحث بالاسم أو اسأل الذكاء الاصطناعي...",
        "scan_btn": "فحص الملفات والمكرر",
        "dir_label": "مسار المجلد",
        "lang_btn": "English",
        "status_ready": "النظام جاهز (يعمل بدون خدمات جوجل)",
        "duplicates_found": "ملفات مكررة",
        "corrupt_found": "ملفات تالفة / فارغة",
        "total_files": "إجمالي الملفات",
    },
    "en": {
        "title": "Shield AI & File Search",
        "search_hint": "Search files or ask AI...",
        "scan_btn": "Scan & Check Duplicates",
        "dir_label": "Folder Path",
        "lang_btn": "العربية",
        "status_ready": "Ready (No Google Play Services required)",
        "duplicates_found": "Duplicate Files",
        "corrupt_found": "Corrupt / Empty Files",
        "total_files": "Total Files",
    },
}


def file_sha256(filepath: Path, chunk_size: int = 65536) -> str:
    h = hashlib.sha256()
    with filepath.open("rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()


def scan_directory(target_dir: str) -> dict:
    root = Path(target_dir)
    if not root.exists() or not root.is_dir():
        return {"error": f"Path not found: {target_dir}", "files": [], "duplicates": [], "corrupt": []}

    seen_hashes = {}
    duplicates = []
    corrupt = []
    all_files = []

    for item in root.rglob("*"):
        if item.is_file():
            all_files.append(str(item))
            try:
                if item.stat().st_size == 0:
                    corrupt.append(str(item))
                    continue
                digest = file_sha256(item)
                if digest in seen_hashes:
                    duplicates.append((str(item), seen_hashes[digest]))
                else:
                    seen_hashes[digest] = str(item)
            except OSError:
                corrupt.append(str(item))

    return {
        "error": None,
        "files": all_files,
        "duplicates": duplicates,
        "corrupt": corrupt,
    }


async def query_ai_with_fallback(prompt: str, api_key: str = "") -> str:
    for provider in AI_PROVIDERS:
        if provider["url"] is None:
            return f"[Offline Mode] البحث المحلي عن: {prompt}"
        if not api_key:
            continue
        try:
            async with httpx.AsyncClient(timeout=12.0) as client:
                resp = await client.post(
                    provider["url"],
                    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
                    json={"model": provider["model"], "messages": [{"role": "user", "content": prompt}]},
                )
                if resp.status_code == 200:
                    data = resp.json()
                    return f"[{provider['name']}]\n" + data["choices"][0]["message"]["content"]
        except Exception:
            continue
    return "[Offline Fallback] تعذر الاتصال بالمزودين، تم التحويل للبحث المحلي."


def main(page: ft.Page):
    state = {"lang": "ar"}
    page.title = f"{APP_NAME} v{APP_VERSION}"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.rtl = True
    page.padding = 16

    default_path = "/storage/emulated/0/Download" if os.path.exists("/storage/emulated/0") else str(Path.home())

    title_text = ft.Text(size=22, weight=ft.FontWeight.BOLD)
    status_text = ft.Text(size=12, color=ft.Colors.GREEN_400)
    dir_input = ft.TextField(value=default_path, expand=True)
    search_input = ft.TextField(expand=True)
    api_key_input = ft.TextField(label="API Key (Optional)", password=True, can_reveal_password=True)
    results_list = ft.ListView(expand=True, spacing=8)

    def refresh_ui():
        t = TRANSLATIONS[state["lang"]]
        page.rtl = state["lang"] == "ar"
        title_text.value = t["title"]
        status_text.value = t["status_ready"]
        dir_input.label = t["dir_label"]
        search_input.hint_text = t["search_hint"]
        scan_btn.text = t["scan_btn"]
        lang_btn.text = t["lang_btn"]
        page.update()

    def toggle_lang(e):
        state["lang"] = "en" if state["lang"] == "ar" else "ar"
        refresh_ui()

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT if page.theme_mode == ft.ThemeMode.DARK else ft.ThemeMode.DARK
        )
        page.update()

    def run_scan(e):
        t = TRANSLATIONS[state["lang"]]
        results_list.controls.clear()
        res = scan_directory(dir_input.value.strip())
        if res["error"]:
            results_list.controls.append(ft.Text(res["error"], color=ft.Colors.RED_400))
        else:
            results_list.controls.append(
                ft.Text(
                    f"{t['total_files']}: {len(res['files'])} | "
                    f"{t['duplicates_found']}: {len(res['duplicates'])} | "
                    f"{t['corrupt_found']}: {len(res['corrupt'])}",
                    weight=ft.FontWeight.BOLD,
                )
            )
            for dup, orig in res["duplicates"][:20]:
                results_list.controls.append(ft.Text(f"DUP: {dup} == {orig}", size=12, color=ft.Colors.AMBER_400))
            for bad in res["corrupt"][:20]:
                results_list.controls.append(ft.Text(f"CORRUPT: {bad}", size=12, color=ft.Colors.RED_400))
        page.update()

    async def run_search(e):
        query = search_input.value.strip()
        if not query:
            return
        results_list.controls.clear()
        results_list.controls.append(ft.ProgressRing())
        page.update()

        # بحث سريع بالاسم في المسار المحدد + استعلام AI
        root = Path(dir_input.value.strip())
        matches = []
        if root.exists():
            matches = [str(p) for p in root.rglob("*") if query.lower() in p.name.lower()][:15]

        ai_reply = await query_ai_with_fallback(query, api_key_input.value.strip())
        results_list.controls.clear()
        results_list.controls.append(ft.Container(content=ft.Text(ai_reply), padding=10, bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST, border_radius=8))
        for m in matches:
            results_list.controls.append(ft.Text(f"FILE: {m}", size=12))
        page.update()

    lang_btn = ft.OutlinedButton(on_click=toggle_lang)
    theme_btn = ft.IconButton(icon=ft.Icons.BRIGHTNESS_6_OUTLINED, on_click=toggle_theme)
    scan_btn = ft.FilledButton(icon=ft.Icons.FOLDER_OPEN_OUTLINED, on_click=run_scan)
    search_btn = ft.IconButton(icon=ft.Icons.SEARCH, on_click=run_search)

    page.add(
        ft.Row([title_text, ft.Row([lang_btn, theme_btn])], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        status_text,
        ft.Row([dir_input, scan_btn]),
        api_key_input,
        ft.Row([search_input, search_btn]),
        ft.Divider(),
        results_list,
    )
    refresh_ui()


if __name__ == "__main__":
    ft.app(target=main)
