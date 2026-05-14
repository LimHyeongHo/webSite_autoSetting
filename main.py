import os
import time
from dotenv import load_dotenv # [추가된 부분 1] .env 파일을 읽기 위한 라이브러리
from playwright.sync_api import sync_playwright

# [추가된 부분 2] 프로그램 시작 시 .env 파일의 내용을 불러옵니다.
load_dotenv()

def run_automation():
    user_data_dir = os.path.join(os.getcwd(), "browser_data")
    
    # [추가된 부분 3] .env에서 아이디와 비밀번호를 변수에 저장합니다.
    USER_ID = os.getenv("USER_ID")
    USER_PW = os.getenv("USER_PW")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, 
            args=["--start-maximized"]
        )
        
        page = browser.new_page()

        try:
            # 1. 사이트 접속
            target_url = "https://app.cloudtype.io/@super8114/yuhan-food-menu:main"
            print("서버를 켜기 위해 접속 중입니다...")
            page.goto(target_url)
            page.wait_for_load_state("networkidle")

            # ---------------------------------------------------------
            # [새로 추가된 로직 시작: 로그인 상태 체크 및 자동 로그인]
            print("로그인 상태를 확인합니다...")
            
            # 이메일 입력칸의 선택자 (Cloudtype 기준에 맞춰 수정 필요)
            login_email_selector = "input[type='email']" 
            
            try:
                # 사이트 접속 후 딱 '3초'만 로그인 창이 있는지 찾아봅니다.
                page.wait_for_selector(login_email_selector, state="visible", timeout=3000)
                
                print("로그인이 풀려있습니다. .env 정보로 로그인을 시도합니다.")
                
                # 아이디 입력
                page.fill(login_email_selector, USER_ID)
                
                # 비밀번호 입력
                page.fill("input[type='password']", USER_PW)
                
                # 로그인 버튼 클릭
                page.click("button:has-text('로그인')")
                
                # 로그인 처리가 완료되고 대시보드가 뜰 때까지 잠시 대기
                page.wait_for_load_state("networkidle")
                time.sleep(2) 
                print("로그인 완료! 대시보드로 진입했습니다.")
                
            except Exception:
                # 3초 동안 로그인 창을 못 찾았을 경우 실행됩니다.
                print("이미 로그인되어 있습니다. 다음 작업으로 넘어갑니다.")
            #-----------
            # (요청하신 추가된 부분의 마지막 줄 표시입니다!)


            # 2. 재생 버튼 클릭 (.x-navbar.space-x-2 상자 안의 첫 번째 버튼)
            target_button_selector = ".x-navbar.space-x-2 > a:nth-child(1)"
            print("재생 버튼을 클릭합니다...")
            page.wait_for_selector(target_button_selector, state="visible", timeout=10000)
            page.click(target_button_selector)

            # 3. 상태 확인
            status_text_selector = "span:has-text('실행 중')"
            print("서버가 켜지기를 기다리는 중 (최대 30초)...")
            page.wait_for_selector(status_text_selector, timeout=30000)
            
            print("====================================")
            print("✅ 결과: 정상적으로 서버가 켜졌습니다 (실행 중)!")
            print("====================================")

        except Exception as e:
            print("====================================")
            print(f"❌ 에러 발생: {e}")
            print("====================================")

        finally:
            print("프로그램을 종료합니다. (3초 뒤 창이 닫힙니다)")
            os._exit(0)

if __name__ == "__main__":
    run_automation()