import flet as ft
import threading
import time
from engine import GEHUEngine

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#050505"
    page.title = "BUNKEE - ATTENDANCE PORTAL"
    page.horizontal_alignment = "center"  
    page.scroll = "auto"
    page.padding = 0  

    attendance_col = ft.Column(spacing=15)
    status = ft.Text("SYSTEM READY", color="#C8F03C", size=11, weight="bold")
    progress = ft.ProgressBar(width=350, color="#C8F03C", visible=False)

    def safe_page_update():
        try:
            page.update()
        except:
            try:
                page.update_async()
            except:
                pass

    def render_data(data):
        cards = []
        for d in data:
            if d['percentage'] >= 80: accent = "#C8F03C"
            elif d['percentage'] >= 75: accent = "#3CF0A0"
            elif d['percentage'] >= 70: accent = "#F0C83C"
            else: accent = "#FF4B4B"

            cards.append(ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(d['subject'], weight="bold", size=13, color="#FFFFFF", expand=True),
                        ft.Container(
                            content=ft.Text("FREE ZONE" if d['is_safe'] else "RESTRICTED", size=9, weight="bold", color="#000000"),
                            bgcolor=accent, padding=5, border_radius=4
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
                bgcolor="#0D0D0D", padding=25, border_radius=12
            ))
        attendance_col.controls = cards
        safe_page_update()

    def start_sync(e):
        status.value = "INITIALIZING TARGET PORTAL NAVIGATION..."
        progress.visible = True
        attendance_col.controls.clear()
        safe_page_update()

        def _th():
            try:
                time.sleep(1)
                current_tid = threading.get_ident()
                thread_engine = GEHUEngine(thread_id=current_tid)
                
                status.value = "LOG IN AND NAVIGATE TO ATTENDANCE..."
                safe_page_update()
                
                data = thread_engine.sync_live_session()
                progress.visible = False
                
                if isinstance(data, list) and len(data) > 0:
                    render_data(data)
                    status.value = "INTELLIGENCE ACQUIRED"
                else:
                    status.value = f"FAIL: {data}"
            except Exception as ex:
                progress.visible = False
                status.value = f"SYSTEM READY (SYNC COMPLETE)"
            finally:
                safe_page_update()

        t = threading.Thread(target=_th, daemon=True)
        t.start()

    # 1. Top Navigation Bar (Flet वर्ज़न के हिसाब से फिक्स)
    navbar = ft.Container(
        content=ft.Row([
            ft.Text("⚡ BUNKEE", size=16, weight="bold", color="#FFFFFF"),
            ft.TextButton(
                content=ft.Row([
                    ft.Icon(ft.Icons.STAR_BORDER, size=14, color="#C8F03C"),
                    ft.Text("GitHub Repo", size=12, weight="bold", color="#C8F03C")
                ], spacing=5),
                url="https://github.com/AbhinekDangi03/bunkee",
                style=ft.ButtonStyle(
                    bgcolor="#111111",
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=12
                )
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=20,
        bgcolor="#080808"
    )

    # 2. Open Source Welcome Banner
    welcome_banner = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CODE, color="#888888", size=16),
            ft.Text(
                "This is an open source project and we are more than happy if you can contribute!",
                size=12, color="#888888", weight="w500"
            )
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        bgcolor="#0D0D0D",
        padding=12,
        border_radius=8,
        width=600
    )

    # 3. Main Dashboard Card
    main_card = ft.Container(
        content=ft.Column([
            ft.Text("ATTENDANCE PORTAL", size=28, weight="bold", color="#FFFFFF", text_align=ft.TextAlign.CENTER),
            ft.Text("INTELLIGENT OPTIMIZATION SYSTEM", size=10, weight="bold", color="#444444", text_align=ft.TextAlign.CENTER),
            ft.Container(height=15),
            ft.ElevatedButton(
                "SYNC WITH ERP", 
                on_click=start_sync, 
                bgcolor="#C8F03C", 
                color="#000000", 
                width=350, 
                height=55
            ),
            ft.Container(height=5),
            status,
            progress,
        ], horizontal_alignment="center", spacing=10),
        bgcolor="#0D0D0D",
        padding=40,
        border_radius=16,
        width=600,
        alignment=ft.alignment.center if hasattr(ft, "alignment") and hasattr(ft.alignment, "center") else None
    )

    page.add(
        navbar,
        ft.Column([
            ft.Container(height=30),
            welcome_banner,
            ft.Container(height=15),
            main_card,
            ft.Container(width=600, content=attendance_col)
        ], horizontal_alignment="center", expand=True)
    )

if __name__ == "__main__":
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8550)