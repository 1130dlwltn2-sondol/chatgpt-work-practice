#!/usr/bin/env python3
"""ChatGPT 업무 활용 실전 - PIL 기반 이미지 생성 스크립트."""
import os
import math
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(os.path.dirname(HERE), "assets")
os.makedirs(ASSETS, exist_ok=True)

BOLD = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
REG = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

BG = (13, 20, 44)          # 딥 네이비
PANEL = (24, 33, 63)
CORAL = (240, 128, 78)
TEAL = (64, 196, 178)
BLUE = (104, 156, 252)
GOLD = (238, 190, 92)
GREEN = (108, 196, 120)
WHITE = (246, 248, 251)
MUTED = (152, 165, 196)
LINE = (70, 88, 140)
LIGHT_BG = (248, 249, 252)
INK = (28, 38, 58)
SUB = (98, 114, 138)
CARD_LINE = (205, 214, 228)


def font(path, size):
    return ImageFont.truetype(path, size, index=1)


def text_center(d, cx, y, s, f, fill):
    bb = d.textbbox((0, 0), s, font=f)
    w = bb[2] - bb[0]
    d.text((cx - w / 2 - bb[0], y), s, font=f, fill=fill)


def text_left(d, x, y, s, f, fill):
    d.text((x, y), s, font=f, fill=fill)


def rrect(d, box, radius, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def arrow(d, x1, y1, x2, y2, fill=CORAL, width=4, head=14):
    d.line([x1, y1, x2, y2], fill=fill, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    for da in (2.62, -2.62):
        d.line([x2, y2, x2 + head * math.cos(ang + da),
                y2 + head * math.sin(ang + da)], fill=fill, width=width)


# ---------------------------------------------------------------- 표지 1000x1300
def make_cover():
    W, H = 1000, 1300
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(13 + (30 - 13) * t)
        g = int(20 + (48 - 20) * t)
        b = int(44 + (86 - 44) * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))
    # 채팅 말풍선 장식 (본문과 겹치지 않게 배치)
    d.ellipse([410, 640, 590, 820], outline=TEAL, width=7)
    d.polygon([(455, 695), (455, 755), (525, 725)], fill=TEAL)
    # 작은 말풍선 장식 (여백에만 배치)
    for (cx, cy, c) in ((120, 660, BLUE), (880, 660, CORAL), (900, 1000, GOLD)):
        d.ellipse([cx - 34, cy - 30, cx + 34, cy + 30], outline=c, width=5)

    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 160, "W I K I D O C S   T E C H   B O O K", fr(26), TEAL)
    d.line([(120, 208), (880, 208)], fill=LINE, width=2)

    text_center(d, W / 2, 250, "ChatGPT", fb(108), WHITE)
    text_center(d, W / 2, 396, "업무 활용 실전", fb(84), TEAL)

    text_center(d, W / 2, 500, "보고서, 이메일, 엑셀부터", fb(40), WHITE)
    text_center(d, W / 2, 560, "GPTs와 자동화까지", fb(40), WHITE)

    topics = [
        "프롬프트 기본기: 역할·맥락·형식·예시",
        "이메일·보고서·기획서 문서 작성",
        "데이터 정리와 엑셀 작업",
        "GPTs·메모리·음성 기능 활용",
        "관심 주제: 자영업자 사장님의 하루",
    ]
    y = 838
    text_center(d, W / 2, y, "이 책에서 다루는 내용", fr(26), MUTED)
    y += 42
    for i, t in enumerate(topics):
        rrect(d, [150, y, 850, y + 48], 24, (18, 27, 56), outline=(64, 80, 128), width=1)
        d.ellipse([174, y + 12, 208, y + 46], fill=TEAL)
        num = str(i + 1)
        bb = d.textbbox((0, 0), num, font=fb(26))
        d.text((191 - (bb[2] - bb[0]) / 2 - bb[0], y + 14), num, font=fb(26), fill=(255, 255, 255))
        d.text((224, y + 16), t, font=fr(24), fill=WHITE)
        y += 56

    d.line([(120, 1196), (880, 1196)], fill=LINE, width=2)
    text_center(d, W / 2, 1220, "저자  이준수", fr(30), MUTED)
    text_center(d, W / 2, 1260, "기준일  2026-10-09", fr(26), MUTED)

    img.save(os.path.join(ASSETS, "cover.png"))
    print("cover.png saved")


# ------------------------------------- 프롬프트의 네 가지 요소 (OpenAI 가이드)
def make_prompt_four():
    W, H = 1500, 680
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "좋은 프롬프트의 네 가지 요소", fb(42), INK)

    items = [
        ("목표", "무엇을 얻고 싶은지", TEAL,
         "예: 다음 주 월요일 아침에\n보낼 거래처 이메일 초안"),
        ("맥락", "상황과 배경 정보", BLUE,
         "예: 계약금이 입금되지 않아\n납기가 일주일 늦어졌다"),
        ("출력 형식", "결과물의 형태와 분량", GOLD,
         "예: 정중한 말투, 세 단락,\n불릿 3개로 정리"),
        ("경계", "원하지 않는 것", CORAL,
         "예: 변명처럼 들리지 않게,\n법적 언급은 제외"),
    ]
    bw = 330
    gap = (W - bw * 4 - 120) / 3
    x = 60
    for title, sub, col, desc in items:
        rrect(d, [x, 110, x + bw, 590], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, 110, x + bw, 110 + 130], 24, col)
        rrect(d, [x, 110 + 106, x + bw, 110 + 130], 0, col)
        text_center(d, x + bw / 2, 132, title, fb(40), (255, 255, 255))
        text_center(d, x + bw / 2, 186, sub, fr(24), (255, 255, 255))
        yy = 292
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(27), INK)
            yy += 46
        x += bw + gap

    text_center(d, W / 2, 622, "네 가지가 꼭 다 필요하지는 않다. 짧고 분명한 요청이 긴 요구사항보다 낫다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-prompt-four.png"))
    print("fig-prompt-four.png saved")


# ---------------------------------------------------- 문서 작성 4단계
def make_doc_workflow():
    W, H = 1600, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "문서 작성 4단계 워크플로우", fb(42), INK)

    steps = [
        ("계획", "목적과 독자를 정한다\n핵심 메시지 한 줄", TEAL),
        ("초안", "거친 메모를 넘긴다\n형식을 지정해 받는다", BLUE),
        ("수정", "구체적으로 지적한다\n25% 줄여달라 식으로", GOLD),
        ("포장", "채널에 맞게 다듬는다\n메일·슬라이드·문서", CORAL),
    ]
    n = len(steps)
    bw, bh = 300, 370
    total = n * bw + (n - 1) * 50
    x = (W - total) / 2
    y = 120
    centers = []
    for title, desc, col in steps:
        rrect(d, [x, y, x + bw, y + bh], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, y, x + bw, y + 96], 24, col)
        rrect(d, [x, y + 72, x + bw, y + 96], 0, col)
        text_center(d, x + bw / 2, y + 30, title, fb(36), (255, 255, 255))
        yy = y + 130
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(26), INK)
            yy += 44
        centers.append(x + bw / 2)
        x += bw + 50
    for i in range(n - 1):
        arrow(d, centers[i] + 150, y + bh / 2, centers[i + 1] - 150, y + bh / 2, fill=SUB, width=4, head=12)

    text_center(d, W / 2, 546, "\"더 좋게 해줘\"가 아니라 \"두 번째 단락을 25% 줄여줘\"처럼 정확히 말하는 편이 효과적이다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-doc-workflow.png"))
    print("fig-doc-workflow.png saved")


# --------------------------------------------------- 데이터 업무 흐름
def make_data_flow():
    W, H = 1600, 620
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "ChatGPT로 하는 데이터 업무 흐름", fb(42), INK)

    steps = [
        ("파일 올리기", "엑셀·CSV를\n채팅창에 드래그", TEAL),
        ("정리", "날짜 형식 통일\n빈칸·오타 찾아내기", BLUE),
        ("분석", "월별 합계·평균\n증감률 계산", GOLD),
        ("시각화", "막대·선 그래프\n이미지로 받기", CORAL),
        ("보고서", "숫자 해석 문장\n메일·문서로 포장", (110, 140, 200)),
    ]
    n = len(steps)
    bw, bh = 240, 360
    total = n * bw + (n - 1) * 56
    x = (W - total) / 2
    y = 120
    centers = []
    for title, desc, col in steps:
        rrect(d, [x, y, x + bw, y + bh], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, y, x + bw, y + 96], 24, col)
        rrect(d, [x, y + 72, x + bw, y + 96], 0, col)
        text_center(d, x + bw / 2, y + 30, title, fb(32), (255, 255, 255))
        yy = y + 130
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(26), INK)
            yy += 44
        centers.append(x + bw / 2)
        x += bw + 56
    for i in range(n - 1):
        arrow(d, centers[i] + 120, y + bh / 2, centers[i + 1] - 120, y + bh / 2, fill=SUB, width=4, head=12)

    text_center(d, W / 2, 540, "숫자는 반드시 원본과 대조한다. AI 계산은 틀릴 수 있다는 전제로 검산이 마지막 단계다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-data-flow.png"))
    print("fig-data-flow.png saved")


# ------------------------------------------------- 자동화(Work·예약 작업) 흐름
def make_work_flow():
    W, H = 1600, 660
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "반복 업무를 맡기는 두 가지 방법 (기준일 2026-10-09)", fb(40), INK)

    boxes = [
        (60, 120, 750, 570, "예약 작업", TEAL,
         ["정해진 시간에 스스로 실행",
          "예: 매주 월요일 9시에",
          "업계 뉴스 요약 보고서 받기",
          "확인: chatgpt.com/schedules",
          "에서 실행 이력을 점검"]),
        (850, 120, 1540, 570, "ChatGPT Work", CORAL,
         ["여러 단계를 스스로 계획·실행",
          "예: 파일 정리 + 표 만들기 +",
          "보고서 초안까지 한 번에",
          "주의: 민감한 행동 앞에서는",
          "반드시 확인을 요청함"]),
    ]
    for x1, y1, x2, y2, title, col, lines in boxes:
        rrect(d, [x1, y1, x2, y2], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x1, y1, x2, y1 + 84], 24, col)
        rrect(d, [x1, y1 + 60, x2, y1 + 84], 0, col)
        text_center(d, (x1 + x2) / 2, y1 + 26, title, fb(36), (255, 255, 255))
        yy = y1 + 116
        for ln in lines:
            text_center(d, (x1 + x2) / 2, yy, ln, fr(28), SUB if ln.startswith("예:") or ln.startswith("확인:") or ln.startswith("주의:") else INK)
            yy += 52

    text_center(d, W / 2, 602, "기능은 자주 바뀌므로 사용 전 공식 도움말(help.openai.com)에서 현재 상태를 확인한다", fr(26), SUB)
    img.save(os.path.join(ASSETS, "fig-work-flow.png"))
    print("fig-work-flow.png saved")


# ------------------------------------------------- 자영업자 사장님의 하루
def make_shop_day():
    W, H = 1600, 660
    img = Image.new("RGB", (W, H), LIGHT_BG)
    d = ImageDraw.Draw(img)
    fb = lambda s: font(BOLD, s)
    fr = lambda s: font(REG, s)

    text_center(d, W / 2, 26, "자영업자 사장님의 하루: ChatGPT 실전 장면", fb(42), INK)

    items = [
        ("오전", "메뉴판·가격표 문구", "신메뉴 설명 한 줄,\n시즌 한정 포스터 문구", TEAL),
        ("점심", "리뷰 답글 쓰기", "별점별 답변 템플릿,\n악성 리뷰 정중 대응", BLUE),
        ("오후", "마케팅 문구", "SNS 업로드 문구,\n이벤트·할인 안내", GOLD),
        ("저녁", "매출 정리와 아이디어", "하루 매출표 정리,\n단골 관리 메시지", CORAL),
    ]
    bw = 350
    gap = (W - bw * 4 - 120) / 3
    x = 60
    for time, title, desc, col in items:
        rrect(d, [x, 110, x + bw, 580], 24, (255, 255, 255), outline=CARD_LINE, width=2)
        rrect(d, [x, 110, x + bw, 110 + 132], 24, col)
        rrect(d, [x, 110 + 108, x + bw, 110 + 132], 0, col)
        text_center(d, x + bw / 2, 132, time, fb(34), (255, 255, 255))
        text_center(d, x + bw / 2, 184, title, fr(26), (255, 255, 255))
        yy = 292
        for ln in desc.split("\n"):
            text_center(d, x + bw / 2, yy, ln, fr(26), INK)
            yy += 44
        x += bw + gap

    text_center(d, W / 2, 608, "스마트폰 하나면 된다. 핵심은 \"우리 가게 상황\"을 한 줄로 먼저 알려주는 것이다", fr(27), SUB)
    img.save(os.path.join(ASSETS, "fig-shop-day.png"))
    print("fig-shop-day.png saved")


if __name__ == "__main__":
    make_cover()
    make_prompt_four()
    make_doc_workflow()
    make_data_flow()
    make_work_flow()
    make_shop_day()
    print("done")
