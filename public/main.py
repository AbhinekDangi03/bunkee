import flet as ft
import threading
from engine import GEHUEngine

def main(page: ft.Page):
    # REMOVED: Shared global engine instance that caused file lock contention
    
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.title = "ATTENDANCE-PORTAL"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "auto"
    page.padding = 30

    attendance_col = ft.Column(spacing=15)
    status = ft.Text("SYSTEM READY", color="#C8F03C", size=12, weight="bold")
    progress = ft.ProgressBar(width=350, color="#C8F03C", visible=False)

    def render_data(data):
        cards = []
        for d in data:
            # Color Coding
            if d['percentage'] >= 80: accent = "#C8F03C" # Free Zone (Lime)
            elif d['percentage'] >= 75: accent = "#3CF0A0" # Mandatory (Green)
            elif d['percentage'] >= 70: accent = "#F0C83C" # Warning (Yellow)
            else: accent = "#FF4B4B" # Danger (Red)

            cards.append(ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(d['subject'], weight="bold", size=12, color="#FFFFFF", expand=True),
                        ft.Container(
                            content=ft.Text("FREE ZONE" if d['is_safe'] else "RESTRICTED", size=9, weight="bold", color="#000000"),
                            bgcolor=accent, padding=ft.padding.symmetric(horizontal=8, vertical=2), border_radius=4
                        )
                    ]),
                    ft.Row([
                        ft.Column([
                            ft.Text(f"STATS: {d['attended']} / {d['conducted']}", size=11, color="#888888"),
                            ft.Text(
                                f"LEAVE PROBABILITY: {d['leave_prop']} Classes" if d['percentage'] >= 70 else f"CLASSES NEEDED (70%): {d['need_70']}",
                                size=11, weight="bold", color=accent
                            ),
                            ft.Text(f"NEED FOR 75%: {d['need_75']}", size=10, color="#444444") if d['percentage'] < 75 else ft.Container()
                        ], spacing=2),
                        ft.Text(f"{int(d['percentage'])}%", size=35, weight="black", color=accent)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ]),
                bgcolor="#0D0D0D", padding=25, border_radius=12, border=ft.border.all(1, "#1A1A1A")
            ))
        attendance_col.controls = cards
        page.update()

    def start_sync(e):
        status.value = "FETCHING YOUR DATA FROM THE COLLEGE'S ERP SYSTEM....."
        progress.visible = True
        attendance_col.controls.clear()
        page.update()
        
        def _th():
            # Acquire current OS/Runtime thread identifier
            current_tid = threading.get_ident()
            
            # Spin up a completely isolated engine profile context for this run
            thread_engine = GEHUEngine(thread_id=current_tid)
            
            data = thread_engine.sync_live_session()
            progress.visible = False
            if isinstance(data, list) and len(data) > 0:
                render_data(data)
                status.value = "INTELLIGENCE ACQUIRED"
            else:
                status.value = f"FAIL: {data}"
            page.update()
            
        threading.Thread(target=_th, daemon=True).start()

    # ---- INDENTATION FIXED: Functions and Objects live in the main function scope ----
    def open_github(e):
        page.launch_url("https://github.com/AbhinekDangi03/bunkee")

    oss_banner = ft.Container(
        content=ft.Column([
            ft.Text(
                "This is an open source project and we are more than happy if you can contribute!",
                size=12,
                color="#888888",
                text_align=ft.TextAlign.CENTER
            ),
            ft.TextButton(
                text="Contribute on GitHub",
                icon=ft.Icons.CODE,
                icon_color="#C8F03C",
                style=ft.ButtonStyle(color="#FFFFFF"),
                on_click=open_github
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=15,
        bgcolor="#0D0D0D",
        border_radius=8,
        border=ft.border.all(1, "#1A1A1A"),
        width=400
    )

    page.add(
        ft.Container(height=20),
        ft.Text("ATTENDANCE-PORTAL", size=45, weight="bold", color="#FFFFFF"),
        ft.Text("INTELLIGENT OPTIMIZATION SYSTEM", size=10, weight="bold", color="#444444"),
        ft.Container(height=10),
        
        # Injected banner here
        oss_banner, 
        
        ft.Container(height=10),
        ft.ElevatedButton("SYNC WITH ERP", on_click=start_sync, bgcolor="#C8F03C", color="#000000", width=350, height=60),
        status, progress,
        ft.Divider(height=50, color="#1A1A1A"),
        attendance_col
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)
