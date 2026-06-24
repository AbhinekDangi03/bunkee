from playwright.sync_api import sync_playwright
import os, math

class GEHUEngine:
    def __init__(self, thread_id=None):
        self.base_url = "https://student.gehu.ac.in"
        # Isolate thread profiles to completely prevent cross-thread lock violations
        suffix = f"_{thread_id}" if thread_id is not None else ""
        self.user_data_dir = os.path.join(os.getcwd(), f"nek_profile{suffix}")

    def sync_live_session(self):
        # The context manager automatically allocates and frees resources perfectly
        with sync_playwright() as p:
            try:
                context = p.chromium.launch_persistent_context(
                    self.user_data_dir,
                    headless=False,
                    args=["--no-sandbox", "--disable-setuid-sandbox"]
                )
                page = context.new_page()
                
                print("ACTION: INITIALIZING TARGET PORTAL NAVIGATION")
                page.goto(self.base_url, timeout=45000, wait_until="domcontentloaded")
                
                print("ACTION: LOG IN AND NAVIGATE TO ATTENDANCE")
                page.wait_for_url("**/Cyborg_StudentAttendanceAcademic*", timeout=120000)
                
                data = None
                for _ in range(10): 
                    page.wait_for_timeout(2000)
                    
                    for frame in page.frames:
                        try:
                            if frame.is_detached(): continue
                            
                            raw_data = frame.evaluate("""() => {
                                if (typeof jQuery !== 'undefined') {
                                    const grid = jQuery(".ui-jqgrid-btable:visible");
                                    return grid.length > 0 ? grid.jqGrid('getGridParam', 'data') : null;
                                }
                                return null;
                            }""")
                            
                            if raw_data and len(raw_data) > 0:
                                data = raw_data
                                break
                        except:
                            continue 
                    
                    if data: break

                if data:
                    return self._process(data)
                return "ERR: TABLE_NOT_FOUND (Ensure attendance is open)"
                
            except Exception as e:
                return f"CRASH: {str(e)[:50]}"
            # The manual close is completely removed. Python cleans up here.

    def _process(self, data):
        res = []
        for i in data:
            subj = i.get("Faculty") or i.get("Subject") or "Unknown"
            if "TOTAL" in str(subj).upper(): continue
            
            try:
                tot = int(float(str(i.get("TotalLecture", 0))))
                att = int(float(str(i.get("TotalPresent", 0))))
                per = float(str(i.get("Percentage", 0)).replace('%', ''))
                
                bunk_70 = max(0, math.floor((att - 0.70 * tot) / 0.70)) if per >= 70 else 0
                need_70 = max(0, math.ceil((0.70 * tot - att) / 0.30)) if per < 70 else 0
                need_75 = max(0, math.ceil((0.75 * tot - att) / 0.25)) if per < 75 else 0

                res.append({
                    "subject": str(subj).upper(),
                    "percentage": per,
                    "attended": att,
                    "conducted": tot,
                    "leave_prop": bunk_70,
                    "need_70": need_70,
                    "need_75": need_75,
                    "is_safe": per >= 80
                })
            except:
                continue
        return res
