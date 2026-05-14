import os
import time
from playwright.sync_api import sync_playwright

def run_automation():
    # 현재 스크립트가 있는 폴더에 'browser_data'라는 이름으로 세션(로그인 정보)을 저장할 경로 지정
    user_data_dir = os.path.join(os.getcwd(), "browser_data")

    with sync_playwright() as p:
        # 1. 브라우저 실행 (로그인 세션 유지 모드)
        # headless=False 로 설정하면 화면을 직접 볼 수 있습니다. (나중에 완성되면 True로 변경)
        print("브라우저를 실행합니다...")
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            headless=False, 
            args=["--start-maximized"] # 브라우저 창 크기 최대화
        )
        
        page = browser.new_page()

        try:
            # ---------------------------------------------------------
            # [여기에 타겟 웹사이트 주소를 입력하세요]
            # ---------------------------------------------------------
            target_url = "https://app.cloudtype.io/@super8114/yuhan-food-menu:main" # 예시: "https://naver.com"
            print(f"{target_url} 로 이동 중...")
            page.goto(target_url)


            # [최초 1회 로그인 대기 로직]
            # 만약 처음 실행해서 로그인이 안 되어 있다면, 사용자가 직접 로그인할 시간을 줍니다.
            # (로그인 버튼이나 내 정보 텍스트가 화면에 있는지 확인하여 분기처리 할 수 있습니다)
            # 여기서는 간단히 페이지 이동 후 잠시 대기하는 것으로 가정합니다.
            page.wait_for_load_state("networkidle") # 페이지 로딩이 완료될 때까지 대기


            # ---------------------------------------------------------
            # 2. 특정 아이콘(버튼) 클릭
            # .x-navbar.space-x-2 (부모 상자) 안에 있는 첫 번째 a 태그(버튼)를 의미합니다.
            target_button_selector = ".x-navbar.space-x-2 > a:nth-child(1)"
            
            print("재생 버튼을 찾는 중...")
            # 재생 버튼이 화면에 보일 때까지 대기 후 클릭
            page.wait_for_selector(target_button_selector, state="visible", timeout=10000)
            page.click(target_button_selector)
            print("재생 버튼 클릭 완료!")


            # '실행 중'이라는 글자가 포함된 span 태그를 찾습니다.
            status_text_selector = "span:has-text('실행 중')"
            
            print("상태 결과를 기다리는 중...")
            # 클릭 후 결과가 렌더링될 때까지 대기
            page.wait_for_selector(status_text_selector, timeout=10000)
            
            # 상태 텍스트 가져오기
            status_result = page.locator(status_text_selector).inner_text()
            print(f"========== 최종 상태 확인 ==========")
            print(f"결과: {status_result}")
            print("====================================")

            # (선택) 여기서 status_result 값을 조건문으로 체크하여
            # Discord 웹훅이나 텔레그램으로 메시지를 보낼 수 있습니다.

        except Exception as e:
            print(f"에러가 발생했습니다: {e}")

        finally:
            # 4. 종료
            print("작업이 완료되어 브라우저를 종료합니다. (3초 후 꺼짐)")
            time.sleep(3) # 결과를 눈으로 확인하기 위한 잠깐의 대기
            browser.close()

if __name__ == "__main__":
    run_automation()