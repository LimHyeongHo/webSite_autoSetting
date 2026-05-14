import os
import time
import sys
import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()

def show_popup(title, message, is_error=False):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    
    if is_error:
        messagebox.showerror(title, message)
    else:
        messagebox.showinfo(title, message)
        
    root.destroy()

def run_automation():
    user_data_dir = os.path.join(os.getcwd(), "browser_data")
    USER_ID = os.getenv("USER_ID")
    USER_PW = os.getenv("USER_PW")

    # [수정된 부분 1] 결과를 저장할 변수를 미리 만들어 둡니다. (기본값은 성공)
    result_status = "success"
    result_message = "✅ 정상적으로 서버가 켜졌습니다 (실행 중)!"

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, 
            channel="chrome",
            args=["--start-maximized"]
        )
        
        page = browser.new_page()

        try:
            target_url = "https://app.cloudtype.io/@super8114/yuhan-food-menu:main"
            page.goto(target_url)
            page.wait_for_load_state("networkidle")

            # --- (자동 로그인 로직) ---
            login_email_selector = "input[type='email']" 
            try:
                page.wait_for_selector(login_email_selector, state="visible", timeout=3000)
                page.fill(login_email_selector, USER_ID)
                page.fill("input[type='password']", USER_PW)
                page.click("button:has-text('로그인')")
                page.wait_for_load_state("networkidle")
                time.sleep(2) 
            except Exception:
                pass
            # ------------------------

            target_button_selector = ".x-navbar.space-x-2 > a:nth-child(1)"
            page.wait_for_selector(target_button_selector, state="visible", timeout=10000)
            page.click(target_button_selector)

            status_text_selector = "span:has-text('실행 중')"
            page.wait_for_selector(status_text_selector, timeout=30000)
            
            # [수정된 부분 2] 여기서 팝업을 띄우지 않고 그냥 넘어갑니다. (성공 상태 유지)

        except Exception as e:
            # [수정된 부분 3] 에러가 났을 때도 팝업을 띄우지 않고, 결과 변수만 '에러'로 바꿔줍니다.
            result_status = "error"
            result_message = f"서버를 켜는 중 문제가 발생했습니다.\n\n상세 내용:\n{e}"

        finally:
            # [수정된 부분 4] 가장 먼저 브라우저부터 완벽하게 끕니다.
            try:
                page.goto("about:blank")
                page.close()
                browser.close()
            except Exception:
                pass
            
            # [수정된 부분 5] 브라우저가 다 꺼진 지금! 아까 저장해둔 결과에 맞춰 팝업을 띄웁니다.
            if result_status == "success":
                show_popup("서버 실행 완료", result_message)
            else:
                show_popup("실행 오류", result_message, is_error=True)
            
            sys.exit(0)

if __name__ == "__main__":
    run_automation()