from playwright.sync_api import sync_playwright
import time
import random

def open_page(link, ques_amount):
    with sync_playwright() as p:
        # initialization
        browser = p.chromium.launch(
                   headless=False,
                   args=[
                       '--disable-blink-features=AutomationControlled',
                       '--no-sandbox',
                       '--disable-dev-shm-usage'
                   ]
               )
               
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            locale='ru-RU',
            timezone_id='Europe/Moscow'
        )
        
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
            Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
            Object.defineProperty(navigator, 'languages', { get: () => ['ru-RU', 'ru', 'en-US', 'en'] });
            window.chrome = { runtime: {} };
        """) 
        page = context.new_page()

        page.goto(link, wait_until="domcontentloaded", timeout=30000) # opens link

        try:
            page.wait_for_selector('span.prob_nums', timeout=15000)
            print("Page is succesfully opened")
        except Exception:
            page.screenshot(path="debug_sdamgia.png")
            print("Timeout. Check out debug_sdamgia.png screenshot")

            browser.close()
            return

        time.sleep(random.uniform(2, 4))

        print("Finding links\n")
        questions = []
        all_links = page.locator('span.prob_nums a').all()
        target_links = all_links[:ques_amount]

        for i, link_elem in enumerate(target_links):
            href = link_elem.get_attribute('href')
            questions.append(href)
            print(f"Question number {i+1}: {href}")
            time.sleep(random.uniform(0.5, 1.5))

        print('-'*70)
        print("Finding answers")

        answers = []
        ques_page = browser.new_page() # another browser page to parsing questions
        num = 0 
        for ques in questions:
            num += 1
            ques_page.goto(f"https://inf-ege.sdamgia.ru{ques}", wait_until="domcontentloaded", timeout=30000)

            try:
                ques_page.wait_for_selector('text="Ответ:"', timeout=10000)
            except Exception:
                print(f"Timeout on question {i+1}")
            time.sleep(random.uniform(1, 2))
            
            answer_blocks = ques_page.locator('p').filter(has_text='Ответ:').all()

            clean_answer = "Not found"
            for block in answer_blocks:
                raw_text = block.text_content()
                clean_answer = raw_text.replace('Ответ:', '').strip().rstrip('.')
                break

            print(f"Answer {num}: {clean_answer}")
            answers.append(clean_answer)
            time.sleep(random.uniform(1, 2))

        browser.close()

def main():
    link = input("Enter the link: ")
    ques_amount = int(input("Enter amount of questions: "))

    print('='*70)

    open_page(link, ques_amount)

if __name__ == "__main__":
    main()




