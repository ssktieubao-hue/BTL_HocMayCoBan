"""Script tạo slide PowerPoint (PPTX) báo cáo Bài tập lớn Học Máy:
Hệ thống Gợi ý Mua kèm Bán lẻ (Retail Recommender System)
"""
import os
import sys
from pathlib import Path
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# 1. BẢNG MÀU CHUẨN DESIGN HIỆN ĐẠI
COLOR_PRIMARY = RGBColor(13, 92, 86)       # Xanh ngọc lục bảo đậm #0d5c56
COLOR_PRIMARY_DARK = RGBColor(8, 61, 57)  # #083d39
COLOR_PRIMARY_LIGHT = RGBColor(20, 130, 121) # #148279
COLOR_INK = RGBColor(15, 23, 42)          # Xanh than đậm #0f172a
COLOR_MUTED = RGBColor(100, 116, 139)     # Xám thanh lịch #64748b
COLOR_CARD_BG = RGBColor(248, 250, 252)   # Trắng xám nhạt #f8fafc
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_LINE = RGBColor(226, 232, 240)      # Viền mỏng #e2e8f0
COLOR_GOLD = RGBColor(217, 119, 6)        # Vàng cam nhấn #d97706
COLOR_GREEN = RGBColor(16, 185, 129)      # Xanh lá điểm nhấn
COLOR_HEADER_BG = RGBColor(241, 245, 249) # #f1f5f9

FONT_TITLE = "Segoe UI"
FONT_BODY = "Segoe UI"

FIG_DIR = Path("reports/figures")

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def add_header(slide, category, title):
        # Category badge
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        tf_cat.margin_left = tf_cat.margin_top = tf_cat.margin_right = tf_cat.margin_bottom = 0
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category.upper()
        p_cat.font.name = FONT_TITLE
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_GOLD

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11), Inches(0.6))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = FONT_TITLE
        p_t.font.size = Pt(22)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_INK

        # Divider line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_LINE
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=COLOR_WHITE, border_color=COLOR_LINE):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = bg_color
        if border_color:
            shape.line.color.rgb = border_color
            shape.line.width = Pt(1.2)
        else:
            shape.line.fill.background()
        return shape

    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ
    # =========================================================================
    # =========================================================================
    # SLIDE 1: TRANG TIÊU ĐỀ (MODERN EXECUTIVE TITLE SLIDE)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)

    # 1. Background: Deep Midnight Emerald
    bg = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = RGBColor(6, 38, 35)  # #062623 - Chiều sâu sang trọng
    bg.line.fill.background()

    # 2. Decorative Top Accent Strip
    strip = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.12))
    strip.fill.solid()
    strip.fill.fore_color.rgb = COLOR_GOLD
    strip.line.fill.background()

    # 3. Decorative subtle circular backdrop shape (top-right aura)
    circle = s1.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.8), Inches(-1.5), Inches(5.2), Inches(5.2))
    circle.fill.solid()
    circle.fill.fore_color.rgb = RGBColor(12, 58, 52)
    circle.line.fill.background()

    # 4. Pill Badge: Course / Class Tag
    tag_bg = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(0.75), Inches(6.8), Inches(0.42))
    tag_bg.fill.solid()
    tag_bg.fill.fore_color.rgb = RGBColor(15, 68, 62)
    tag_bg.line.color.rgb = RGBColor(217, 119, 6)
    tag_bg.line.width = Pt(1.2)
    
    tf_tag = tag_bg.text_frame
    tf_tag.word_wrap = True
    tf_tag.margin_top = tf_tag.margin_bottom = tf_tag.margin_left = tf_tag.margin_right = 0
    p_tag = tf_tag.paragraphs[0]
    p_tag.text = "★  BÀI TẬP LỚN MÔN HỌC MÁY  •  LỚP 12523W.1"
    p_tag.font.name = FONT_TITLE
    p_tag.font.size = Pt(11)
    p_tag.font.bold = True
    p_tag.font.color.rgb = RGBColor(254, 243, 199)
    p_tag.alignment = PP_ALIGN.CENTER

    # 5. Main Title & Subtitle in Hero Box
    hero_box = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.333), Inches(2.6))
    tf_hero = hero_box.text_frame
    tf_hero.word_wrap = True
    tf_hero.margin_left = tf_hero.margin_right = tf_hero.margin_top = tf_hero.margin_bottom = 0

    p_t1 = tf_hero.paragraphs[0]
    p_t1.text = "HỆ THỐNG GỢI Ý MUA KÈM BÁN LẺ"
    p_t1.font.name = FONT_TITLE
    p_t1.font.size = Pt(36)
    p_t1.font.bold = True
    p_t1.font.color.rgb = COLOR_WHITE
    p_t1.space_after = Pt(4)

    p_t2 = tf_hero.add_paragraph()
    p_t2.text = "Dựa Trên Ma Trận Đồng Xuất Hiện Cosine Nhị Phân"
    p_t2.font.name = FONT_TITLE
    p_t2.font.size = Pt(22)
    p_t2.font.bold = True
    p_t2.font.color.rgb = RGBColor(245, 158, 11)  # Vàng hổ phách sáng #f59e0b
    p_t2.space_after = Pt(10)

    p_sub = tf_hero.add_paragraph()
    p_sub.text = "Retail Cross-Selling Recommender System using Binary Item–Invoice Cosine Modeling"
    p_sub.font.name = FONT_TITLE
    p_sub.font.size = Pt(13.5)
    p_sub.font.italic = True
    p_sub.font.color.rgb = RGBColor(148, 163, 184)  # Slate nhạt sang trọng

    # 6. Subtle Divider Line
    div = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.0), Inches(4.2), Inches(11.333), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = RGBColor(26, 92, 85)
    div.line.fill.background()

    # 7. 4 Modern Executive Meta Cards at Bottom
    cards_meta = [
        {
            "icon": "👨‍🏫",
            "tag": "GIẢNG VIÊN HƯỚNG DẪN",
            "val": "PGS.TS. Nguyễn Văn Hậu",
            "sub": "Bộ môn Học máy & Trí tuệ nhân tạo"
        },
        {
            "icon": "👥",
            "tag": "NHÓM SINH VIÊN",
            "val": "Nhóm 2 Thành Viên",
            "sub": "Lớp 12523W.1 • Khoa CNTT"
        },
        {
            "icon": "📊",
            "tag": "DỮ LIỆU NGHIÊN CỨU",
            "val": "UCI Online Retail II",
            "sub": "1.067.371 giao dịch • CC BY 4.0"
        },
        {
            "icon": "🔒",
            "tag": "CHỐNG RÒ RỈ DỮ LIỆU",
            "val": "frozen-before-test",
            "sub": "Tag Git đóng băng • Test độc lập"
        }
    ]

    card_w = Inches(2.65)
    card_h = Inches(2.2)
    card_y = Inches(4.5)
    gap = Inches(0.24)

    for i, m in enumerate(cards_meta):
        cx = Inches(1.0) + i * (card_w + gap)
        # Card container
        c_shape = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, card_y, card_w, card_h)
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = RGBColor(11, 48, 43)  # Dark glassmorphic teal
        c_shape.line.color.rgb = RGBColor(28, 92, 84)
        c_shape.line.width = Pt(1.2)

        # Text inside card
        tb = s1.shapes.add_textbox(cx + Inches(0.18), card_y + Inches(0.2), card_w - Inches(0.36), card_h - Inches(0.4))
        tf_c = tb.text_frame
        tf_c.word_wrap = True
        tf_c.margin_left = tf_c.margin_right = tf_c.margin_top = tf_c.margin_bottom = 0

        p1 = tf_c.paragraphs[0]
        p1.text = f"{m['icon']}  {m['tag']}"
        p1.font.name = FONT_TITLE
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = RGBColor(245, 158, 11)  # Gold
        p1.space_after = Pt(8)

        p2 = tf_c.add_paragraph()
        p2.text = m["val"]
        p2.font.name = FONT_TITLE
        p2.font.size = Pt(14.5)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE
        p2.space_after = Pt(6)

        p3 = tf_c.add_paragraph()
        p3.text = m["sub"]
        p3.font.name = FONT_BODY
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = RGBColor(148, 163, 184)

    # =========================================================================
    # SLIDE 2: ĐẶT VẤN ĐỀ & MỤC TIÊU NGHIÊN CỨU
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Tổng quan bài toán", "Đặt Vấn Đề & Mục Tiêu Nghiên Cứu")

    # Card 1: Bối cảnh
    add_card(s2, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b1 = s2.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b1.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Bối Cảnh Thương Mại"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(12)
    p = tf.add_paragraph()
    p.text = "• Trong bán lẻ trực tuyến, gợi ý mua kèm (Cross-sell / Next-Basket) giúp khách hàng khám phá sản phẩm và tăng giá trị đơn hàng (AOV).\n\n" \
             "• Khác với gợi ý cá nhân hóa dài hạn, bài toán giỏ hàng cần phản hồi ngay theo ngữ cảnh các món đang chọn trong phiên mua sắm hiện tại."
    p.font.size = Pt(13.5)
    p.font.color.rgb = COLOR_INK

    # Card 2: Câu hỏi nghiên cứu
    add_card(s2, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b2 = s2.shapes.add_textbox(Inches(5.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b2.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Câu Hỏi Nghiên Cứu"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(12)
    p = tf.add_paragraph()
    p.text = "• Câu hỏi cốt lõi: Ma trận đồng xuất hiện nhị phân (Item-Invoice) kết hợp độ đo Cosine có tạo ra gợi ý mua kèm chất lượng và vượt trội so với Top bán chạy không?\n\n" \
             "• So sánh với Item-Customer: Vector theo khách hàng hay vector theo hóa đơn mang lại hiệu quả tốt hơn?\n\n" \
             "• Đơn vị quan sát: Sản phẩm (StockCode) trong không gian các hóa đơn."
    p.font.size = Pt(13.5)
    p.font.color.rgb = COLOR_INK

    # Card 3: 3 Nguyên tắc bắt buộc
    add_card(s2, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b3 = s2.shapes.add_textbox(Inches(9.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b3.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3 Nguyên Tắc Bắt Buộc"
    p.font.bold = True
    p.font.size = Pt(18)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(12)
    p = tf.add_paragraph()
    p.text = "1. Chặn rò rỉ dữ liệu (No Leakage): Chia theo hóa đơn & theo thời gian; đóng băng cấu hình trước test.\n\n" \
             "2. Đánh giá nghiêm ngặt: Test chỉ chạy duy nhất 1 lần, có khoảng tin cậy 95% (ci95) và kiểm thử độ nhạy 20 seed.\n\n" \
             "3. Triển khai chuẩn kỹ thuật: Tách train offline khỏi serving online; phản hồi API <2ms."
    p.font.size = Pt(13.5)
    p.font.color.rgb = COLOR_INK

    # =========================================================================
    # SLIDE 3: KHÁM PHÁ DỮ LIỆU (EDA)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Dữ liệu & EDA", "Tập Dữ Liệu UCI Online Retail II & Đặc Thù Thực Tế")

    # Left: Details
    add_card(s3, Inches(0.8), Inches(1.65), Inches(6.0), Inches(5.2))
    b = s3.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.6), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Tổng Quan Dữ Liệu Giao Dịch"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Nguồn: UCI Online Retail II (Daqing Chen, 2019, CC BY 4.0, DOI: 10.24432/C5CG6D).\n" \
             "• Quy mô: 1.067.371 dòng giao dịch, 8 biến, diễn ra từ 01/12/2009 đến 09/12/2011.\n" \
             "• Bản chất cửa hàng: Doanh nghiệp bán đồ lưu niệm/quà tặng tại Anh (92.6% khách UK), có nhiều đơn bán sỉ số lượng lớn."
    p.font.size = Pt(13.5)
    p.space_after = Pt(12)

    p = tf.add_paragraph()
    p.text = "3 Phát Hiện Quan Trọng Từ EDA:"
    p.font.bold = True
    p.font.size = Pt(15)
    p.font.color.rgb = COLOR_GOLD
    p.space_after = Pt(6)

    p = tf.add_paragraph()
    p.text = "1. Phân phối đuôi dài (Long-tail): 25% sản phẩm chỉ xuất hiện <= 17 hóa đơn. Sản phẩm top 1 xuất hiện trong 15.4% hóa đơn.\n" \
             "2. Giỏ hàng biến động mạnh: Trung vị 15 sản phẩm/hóa đơn, nhưng có hóa đơn lên tới 673 sản phẩm (khách sỉ).\n" \
             "3. Nhóm túi quà tặng: Top 20 sản phẩm bán chạy có tới 7 loại túi quà (Bag, Shopper)."
    p.font.size = Pt(13)

    # Right: Embed EDA chart
    chart_path = FIG_DIR / "eda_basket_size.png"
    if chart_path.exists():
        add_card(s3, Inches(7.1), Inches(1.65), Inches(5.4), Inches(5.2))
        s3.shapes.add_picture(str(chart_path), Inches(7.25), Inches(1.85), width=Inches(5.1))
        # Label
        lbl = s3.shapes.add_textbox(Inches(7.25), Inches(6.3), Inches(5.1), Inches(0.4))
        p = lbl.text_frame.paragraphs[0]
        p.text = "Hình 1: Phân phối kích thước giỏ hàng (Số sản phẩm / Hóa đơn)"
        p.font.size = Pt(11)
        p.font.italic = True
        p.font.color.rgb = COLOR_MUTED
        p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 4: TIỀN XỬ LÝ & CHỐNG RÒ RỈ DỮ LIỆU
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Tiền xử lý & Chia tập", "Chiến Lược Làm Sạch & Chặn Rò Rỉ Dữ Liệu (No Leakage)")

    # Left: Cleaning rules table
    add_card(s4, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s4.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Luật Làm Sạch Cố Định (Fixed Rules)"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "Chỉ áp dụng luật kinh doanh cố định, TUYỆT ĐỐI KHÔNG học bất kỳ thông tin nào từ dữ liệu ở bước này:\n\n" \
             "• Loại hóa đơn hủy (Invoice bắt đầu bằng C): Loại 19.494 dòng\n" \
             "• Loại Quantity <= 0: Loại 3.457 dòng\n" \
             "• Loại Price <= 0: Loại 2.750 dòng\n" \
             "• Loại mã phi sản phẩm (POST, D, M, BANK CHARGES...): Loại 4.794 dòng\n" \
             "• Kiểm tra Description thiếu: 0 dòng\n\n" \
             "-> Tổng cộng loại 30.495 dòng (2.86%), còn lại 1.036.876 dòng sạch."
    p.font.size = Pt(13.5)

    # Right: Split strategy
    add_card(s4, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s4.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Phân Chia 70 / 15 / 15 Không Rò Rỉ"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Chia theo HÓA ĐƠN: Mọi dòng của cùng một hóa đơn phải nằm trọn vẹn trong một tập (có unit test kiểm tra giao rỗng: A ∩ B = ∅).\n\n" \
             "• Chia theo THỜI GIAN: Train (cũ nhất, 70%) -> Validation (tiếp theo, 15%) -> Test (mới nhất, 15%). Mô phỏng thực tế: Dùng quá khứ dự đoán tương lai.\n\n" \
             "• Ngưỡng tần suất chỉ đếm trên Train: Không đếm trên tập tổng để tránh rò rỉ từ vựng.\n\n" \
             "• Đóng băng mô hình: Toàn bộ cấu hình và code test được gắn tag Git frozen-before-test trước khi xem tập Test."
    p.font.size = Pt(13.5)

    # =========================================================================
    # SLIDE 5: CƠ SỞ LÝ THUYẾT: MÔ HÌNH COSINE NHỊ PHÂN
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. Mô hình học máy", "Cơ Sở Lý Thuyết: Cosine Trên Vector Nhị Phân Item–Invoice")

    add_card(s5, Inches(0.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s5.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Bản Chất Vector Nhị Phân"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Mỗi sản phẩm i là một vector nhị phân x_i ∈ {0, 1}^M trên M hóa đơn huấn luyện (vị trí j = 1 nếu hóa đơn j có chứa sản phẩm i).\n\n" \
             "• Tại sao nhị phân hóa?\n" \
             "  + Loại bỏ ảnh hưởng cực đoan của các đơn mua sỉ số lượng lớn (mua 1 món hay 100 món đều là 'có nhu cầu').\n" \
             "  + Dễ giải thích, tính toán cực nhanh qua ma trận thưa (Scipy CSR Matrix)."
    p.font.size = Pt(13.5)

    add_card(s5, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s5.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Công Thức Cosine & Điểm Giỏ Hàng"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Độ tương đồng giữa 2 sản phẩm A và B:\n" \
             "   cos(A, B) = |H_A ∩ H_B| / ( căn(|H_A|) × căn(|H_B|) )\n" \
             "   -> Tử số: Số hóa đơn chứa cả 2 sản phẩm.\n" \
             "   -> Mẫu số: Chuẩn hóa theo tần suất của từng món -> Tự động phạt hàng đại trà, ưu tiên liên kết thực chất.\n\n" \
             "2. Điểm gợi ý cho giỏ hàng nhiều món:\n" \
             "   Score(c) = ∑_{q ∈ Basket} cos(c, q)  với c ∉ Basket\n" \
             "   (Loại trừ các món đã có trong giỏ, không gợi ý món điểm 0).\n\n" \
             "3. Mô hình cơ sở (Baseline): Gợi ý Top sản phẩm có số lượng hóa đơn cao nhất toàn cục."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 6: GIAO THỨC ĐÁNH GIÁ (EVALUATION PROTOCOL)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Phương pháp đánh giá", "Giao Thức Leave-One-Out & Bộ Chỉ Số Toàn Diện")

    # Card 1: Giao thức
    add_card(s6, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s6.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Giao Thức Leave-One-Out"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Với mỗi hóa đơn đánh giá có ít nhất 2 sản phẩm:\n" \
             "  1. Giấu ngẫu nhiên 1 sản phẩm đã từng xuất hiện ở Train (nhãn ground-truth, cố định seed = 42).\n" \
             "  2. Dùng các sản phẩm còn lại làm đầu vào (Query) để mô hình dự đoán Top-K.\n" \
             "  3. Ghi nhận 'Trúng' (Hit) nếu sản phẩm bị giấu nằm trong Top-K gợi ý.\n\n" \
             "• Bản chất Hit-rate: Vì giỏ hàng có thể có nhiều món hợp lý khác nhưng chỉ giấu 1 món, Hit-rate là CẬN DƯỚI của chất lượng thực tế. Do đó phải đọc cùng Baseline."
    p.font.size = Pt(13.5)

    # Card 2: 3 chỉ số
    add_card(s6, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s6.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Bộ Chỉ Số Đánh Giá Toàn Diện"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Hit-rate@K (K = 5, 10, 20):\n" \
             "   Tỷ lệ ca mà món bị giấu nằm trong Top-K. K chính báo cáo = 10.\n\n" \
             "2. Độ phủ danh mục (Coverage@K):\n" \
             "   Tỷ lệ sản phẩm khác nhau trong kho được gợi ý ít nhất một lần. Đánh giá mô hình có phủ rộng danh mục hay chỉ loanh quanh vài món quen thuộc.\n\n" \
             "3. Tỷ lệ hàng phổ biến (Popularity Share):\n" \
             "   Tỷ lệ lượt gợi ý thuộc Top 100 sản phẩm bán chạy nhất. Đánh giá mức độ thiên lệch của mô hình.\n\n" \
             "4. Khoảng tin cậy 95% (ci95):\n" \
             "   ci95 = 1.96 × căn(p(1 - p) / n) để xác nhận chênh lệch có ý nghĩa thống kê hay chỉ do ngẫu nhiên."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 7: THÍ NGHIỆM 1, 2 & 3 TRÊN VALIDATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Thí nghiệm Validation", "Thí Nghiệm 1, 2 & 3: Lựa Chọn Cấu Hình Mô Hình Tối Ưu")

    # Left: Thí nghiệm 2 & 3
    add_card(s7, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s7.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Thí Nghiệm 2 & 3: Baseline & Ngưỡng Lọc"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "• THÍ NGHIỆM 2: Cosine vs Baseline (trên Validation, K = 10):\n" \
             "  + Hit-rate@10: Cosine đạt 25.52% vs Baseline 4.78% (gấp 5.3 lần).\n" \
             "  + Coverage: Cosine phủ 43.49% danh mục vs Baseline chỉ 0.59% (gấp 74 lần!).\n" \
             "  + Tỷ lệ phổ biến: Cosine giảm từ 100% của Baseline xuống 44.18%.\n\n" \
             "• THÍ NGHIỆM 3: Khảo sát ngưỡng min_count ∈ {1, 5, 10, 20, 50}:\n" \
             "  + Hit-rate giữa min_count=1 (25.52%) và min_count=50 (24.63%) chỉ chênh 0.89%, nằm gọn trong ci95 (±1.16%).\n" \
             "  + Nhưng Coverage giảm mạnh từ 43.49% xuống 34.68% (mất 20% danh mục gợi ý).\n\n" \
             "-> Quyết định: Chọn min_count = 1 (Không lọc) theo nguyên tắc Parsimony."
    p.font.size = Pt(12.5)

    # Right: Thí nghiệm 1
    add_card(s7, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s7.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Thí Nghiệm 1: Item–Invoice vs Item–Customer"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(8)

    p = tf.add_paragraph()
    p.text = "So sánh vector theo Hóa đơn với vector theo Khách hàng (trên cùng bộ 5.424 ca validation):\n\n" \
             "• Hit-rate@10: Ngang nhau hoàn toàn (cùng 25.52%).\n\n" \
             "• Thiên lệch phổ biến: Item-Customer thiên lệch hàng phổ biến nghiêm trọng hơn nhiều (63.0% vs 44.2%). Do một khách mua nhiều đợt nên hàng phổ biến đồng xuất hiện với hầu hết các món khác.\n\n" \
             "• Khả năng phục vụ thực tế: Dữ liệu thiếu 22.6% Customer ID (khách vãng lai). Item-Customer không có vector cho các đơn này.\n\n" \
             "-> Quyết định: Giữ Item–Invoice làm mô hình chính vì bao phủ toàn bộ hóa đơn, gợi ý đa dạng hơn và ít thiên lệch hàng đại trà."
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 8: THÍ NGHIỆM 4: PHÂN TÍCH NHÓM TÚI QUÀ
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Thí nghiệm chuyên sâu", "Thí Nghiệm 4: Phân Tích Nhóm Túi Quà Tặng (Nhóm G)")

    add_card(s8, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s8.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Đặc Điểm Của Nhóm Túi (Nhóm G)"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Định nghĩa: G = 27 sản phẩm trong Top 100 bán chạy của train có mô tả chứa BAG, SHOPPER, WRAP, GIFT, RIBBON, TISSUE.\n\n" \
             "• Tỷ lệ xuất hiện:\n" \
             "  + Trong danh mục sản phẩm: 0.6%\n" \
             "  + Trong giỏ hàng thật: 6.5%\n" \
             "  + Trong gợi ý Top-10 của Cosine: 22.1% (Gấp 3.4 lần thực tế!)\n\n" \
             "• Khi món bị giấu thuộc G: Hit-rate@10 đạt tới 66.8% ±4.6 (vượt xa mức trung bình 25.5%). Mô hình cực kỳ nhạy với nhóm túi."
    p.font.size = Pt(13.5)

    add_card(s8, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s8.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Khảo Sát Loại Bỏ & Quyết Định"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Hiệu ứng cơ học:\n" \
             "  + Trên các ca giấu món ngoài G: Bỏ G làm Hit-rate tăng khoảng 2 điểm (từ 22.2% lên 24.4%), nhưng đây chỉ là hiệu ứng cơ học vì loại bớt suất trượt chắc chắn.\n" \
             "  + Trên toàn bộ ca đánh giá: Bỏ G làm Hit-rate@10 GIẢM 3 điểm (từ 25.5% xuống khoảng 22.5%).\n" \
             "  + Bỏ G khỏi đầu vào chỉ chênh 0.2 - 0.8 điểm (nhỏ hơn ci95).\n\n" \
             "-> Quyết định: KHÔNG LỌC NHÓM G trong mô hình chính. Ghi nhận xu hướng gợi ý túi là một giới hạn tự nhiên phản ánh thói quen mua túi kèm quà của cửa hàng."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 9: KẾT QUẢ TEST ĐỘC LẬP
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. Kết quả Test", "Đánh Giá Độc Lập Trên Tập Test (5.461 Ca, Seed 42)")

    # KPI Summary Cards
    # KPI 1
    add_card(s9, Inches(0.8), Inches(1.65), Inches(3.7), Inches(1.6), bg_color=COLOR_PRIMARY_DARK)
    b = s9.shapes.add_textbox(Inches(1.0), Inches(1.75), Inches(3.3), Inches(1.4))
    tf = b.text_frame
    p = tf.paragraphs[0]
    p.text = "HIT-RATE@10 (TEST)"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_GOLD
    p = tf.add_paragraph()
    p.text = "21.59% ±1.09"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "Gấp 5.6 lần Baseline (3.85%)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(226, 232, 240)

    # KPI 2
    add_card(s9, Inches(4.8), Inches(1.65), Inches(3.7), Inches(1.6), bg_color=COLOR_PRIMARY)
    b = s9.shapes.add_textbox(Inches(5.0), Inches(1.75), Inches(3.3), Inches(1.4))
    tf = b.text_frame
    p = tf.paragraphs[0]
    p.text = "ĐỘ PHỦ (COVERAGE@10)"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_GOLD
    p = tf.add_paragraph()
    p.text = "40.86%"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p = tf.add_paragraph()
    p.text = "Baseline chỉ đạt 0.85% (Gấp 48 lần)"
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(226, 232, 240)

    # KPI 3
    add_card(s9, Inches(8.8), Inches(1.65), Inches(3.7), Inches(1.6), bg_color=COLOR_CARD_BG)
    b = s9.shapes.add_textbox(Inches(9.0), Inches(1.75), Inches(3.3), Inches(1.4))
    tf = b.text_frame
    p = tf.paragraphs[0]
    p.text = "TỶ LỆ HÀNG PHỔ BIẾN"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_MUTED
    p = tf.add_paragraph()
    p.text = "28.96%"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_INK
    p = tf.add_paragraph()
    p.text = "Baseline là 100% (Giảm thiên vị)"
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_PRIMARY

    # Full table
    table_shape = s9.shapes.add_table(4, 5, Inches(0.8), Inches(3.5), Inches(11.733), Inches(2.0))
    table = table_shape.table
    table.columns[0].width = Inches(1.5)
    table.columns[1].width = Inches(2.6)
    table.columns[2].width = Inches(2.6)
    table.columns[3].width = Inches(2.5)
    table.columns[4].width = Inches(2.5)

    headers = ["K", "Top Bán Chạy (Baseline)", "Cosine Item–Invoice", "Coverage (Cosine)", "Tỷ lệ phổ biến (Cosine)"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = COLOR_HEADER_BG
        for p in cell.text_frame.paragraphs:
            p.font.bold = True
            p.font.size = Pt(12)
            p.font.color.rgb = COLOR_INK

    rows = [
        ["K = 5", "2.38% ±0.40", "15.89% ±0.97", "33.13%", "29.00%"],
        ["K = 10", "3.85% ±0.51", "21.59% ±1.09", "40.86%", "28.96%"],
        ["K = 20", "5.68% ±0.61", "27.49% ±1.18", "49.38%", "29.87%"],
    ]
    for row_idx, r in enumerate(rows, 1):
        for col_idx, val in enumerate(r):
            cell = table.cell(row_idx, col_idx)
            cell.text = val
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                if col_idx == 2:
                    p.font.bold = True
                    p.font.color.rgb = COLOR_PRIMARY

    # Note below
    note = s9.shapes.add_textbox(Inches(0.8), Inches(5.8), Inches(11.733), Inches(1.0))
    tf = note.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "• Tiêu chí kết luận đã chốt: Cận dưới ci95 của Cosine (20.50%) > Cận trên ci95 của Baseline (4.36%) -> Cosine vượt trội hoàn toàn.\n" \
             "• Kiểm định 20 seed: Lặp lại 20 seed ngẫu nhiên khác nhau, Cosine duy trì trung bình 21.43% ±0.57 (ổn định từ 19.79% đến 22.38%)."
    p.font.size = Pt(12.5)
    p.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 10: PHÂN TÍCH LỖI ĐA CHIỀU (ERROR ANALYSIS)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Phân tích lỗi", "Phân Tích Lỗi Đa Chiều Trên Tập Test (Hit-rate@10)")

    # Left: Explanation of 3 dimensions
    add_card(s10, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s10.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3 Chiều Phân Khúc Lỗi Lớn"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Độ phổ biến của món bị giấu:\n" \
             "• Món >= 500 hóa đơn: Đạt 32.0% ±1.9 (chiếm tới 61% số lượt trúng của Cosine).\n" \
             "• Món < 20 hóa đơn: Đạt 15.9% ±5.1.\n" \
             "• Baseline CHỈ trúng ở nhóm >= 500 hóa đơn (9.3%), hoàn toàn bất lực ở các món còn lại.\n\n" \
             "2. Kích thước giỏ hàng (Basket Size):\n" \
             "• Giỏ 2 - 5 món: Hit-rate đạt 33.1% ±3.3.\n" \
             "• Giỏ > 40 món: Hit-rate GIẢM CÒN 9.2% ±1.8.\n" \
             "-> Điểm yếu lớn: Giỏ nhiều món làm tổng cosine bị dồn điểm vào các món liên kết rộng, gây loãng gợi ý.\n\n" \
             "3. Theo tháng giao dịch: Hiệu năng ổn định (21.1% - 21.4% từ T10-T12; T9 đạt 26.7%)."
    p.font.size = Pt(12.5)

    # Right: Embed error analysis chart
    err_chart = FIG_DIR / "error_analysis.png"
    if err_chart.exists():
        add_card(s10, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
        s10.shapes.add_picture(str(err_chart), Inches(6.95), Inches(1.85), width=Inches(5.4))
        lbl = s10.shapes.add_textbox(Inches(6.95), Inches(6.3), Inches(5.4), Inches(0.4))
        p = lbl.text_frame.paragraphs[0]
        p.text = "Hình 2: So sánh Hit-rate@10 giữa Cosine và Baseline theo các phân khúc"
        p.font.size = Pt(11)
        p.font.italic = True
        p.font.color.rgb = COLOR_MUTED
        p.alignment = PP_ALIGN.CENTER

    # =========================================================================
    # SLIDE 11: KIẾN TRÚC TRIỂN KHAI & NÂNG CẤP WEB/API
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. Triển khai & Ứng dụng", "Kiến Trúc Triển Khai Thực Tế & Các Điểm Nâng Cấp")

    # Left: Architecture
    add_card(s11, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s11.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Kiến Trúc Tách Rời (Offline - Online)"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Huấn luyện Offline (Batch Job):\n" \
             "  Script tính trước Top-50 láng giềng gần nhất cho từng món và lưu vào item_invoice_cosine.json (~2.9 MB).\n\n" \
             "• Phục vụ Trực Tuyến (FastAPI Serving):\n" \
             "  FastAPI nạp toàn bộ artifact vào bộ nhớ RAM khi server khởi động. Độ trễ mỗi request < 2ms, không tính toán lại mô hình trực tuyến.\n\n" \
             "• Kiểm thử tự động: 31 test cases bao phủ pipeline, model logic, evaluation và API endpoint (pytest 100% xanh)."
    p.font.size = Pt(13)

    # Right: Upgrades implemented
    add_card(s11, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s11.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Các Nâng Cấp Sản Phẩm Đã Thực Hiện"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Gợi ý theo CẢ GIỎ HÀNG nhiều món (/api/recommend-basket):\n" \
             "   Tổng hợp điểm tương đồng cho danh sách nhiều món cùng lúc (POST & GET).\n\n" \
             "2. Giao diện Cửa hàng E-Commerce (The Artisan Gift Shop):\n" \
             "   Thiết kế chuẩn sàn bán lẻ, hỗ trợ giỏ hàng, bảng tóm tắt đơn hàng.\n\n" \
             "3. Nhận diện hình ảnh tự động & Fallback an toàn:\n" \
             "   Gắn ảnh Unsplash theo từ khóa chủ đề (nến, bánh, túi, gốm sứ...); tự động chuyển sang logo pastel nếu offline.\n\n" \
             "4. Chuẩn hóa phông chữ tiếng Việt (Be Vietnam Pro):\n" \
             "   Hiển thị sắc nét, 100% chuẩn dấu Unicode.\n\n" \
             "5. Đóng gói Docker: Sẵn sàng chạy ngay với 1 lệnh."
    p.font.size = Pt(12.5)

    # =========================================================================
    # SLIDE 12: ĐÁNH GIÁ TRUNG THỰC: GIẢ ĐỊNH & GIỚI HẠN
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "11. Thảo luận khoa học", "Đánh Giá Trung Thực: Giả Định & Giới Hạn Của Mô Hình")

    # Left: Assumptions
    add_card(s12, Inches(0.8), Inches(1.65), Inches(5.6), Inches(5.2))
    b = s12.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(5.2), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Giả Định Cốt Lõi Của Phương Pháp"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "• Giả định đồng xuất hiện: Hai sản phẩm hay nằm chung hóa đơn thì có mối quan hệ bổ trợ hoặc quan tâm cùng lúc.\n\n" \
             "• Tương quan không phải nhân quả: Kết quả chỉ phản ánh hành vi mua kèm trong quá khứ, không khẳng định việc gợi ý món A sẽ gây ra hành vi mua món B.\n\n" \
             "• Tính đối xứng: Cosine(A, B) = Cosine(B, A), không phân biệt được chiều A kéo theo B hay ngược lại (như Luật kết hợp Association Rules)."
    p.font.size = Pt(13.5)

    # Right: Limitations
    add_card(s12, Inches(6.8), Inches(1.65), Inches(5.7), Inches(5.2))
    b = s12.shapes.add_textbox(Inches(7.0), Inches(1.85), Inches(5.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "4 Giới Hạn Đã Kiểm Chứng"
    p.font.bold = True
    p.font.size = Pt(17)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)

    p = tf.add_paragraph()
    p.text = "1. Vấn đề khởi đầu lạnh (Cold-Start): Không thể gợi ý cho sản phẩm mới tinh chưa từng có trong tập học (4.8% cặp ở test bị cold-start).\n\n" \
             "2. Yếu ở giỏ hàng lớn (>40 món): Chiếm tới 18.8% số ca test, nhưng Hit-rate chỉ đạt 9.2%.\n\n" \
             "3. Thiên lệch biến thể cùng dòng: Mô hình hay gợi ý biến thể khác màu/kích thước của cùng một mặt hàng (ví dụ mua tách hồng thì gợi ý 4 tách màu khác).\n\n" \
             "4. Đặc thù dữ liệu: Khách UK chiếm 92.6% và tập test rơi vào mùa cao điểm Giáng sinh cuối năm 2011."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 13: ĐỊNH HƯỚNG NÂNG CẤP TRONG TƯƠNG LAI
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "12. Hướng phát triển", "Định Hướng Nâng Cấp Thuật Toán Trong Tương Lai")

    # 3 Strategy Cards
    # Card 1: Basket Normalization
    add_card(s13, Inches(0.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b = s13.shapes.add_textbox(Inches(1.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "1. Trọng Số Kích Thước Giỏ (IDF / BM25)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "• Mục tiêu: Khắc phục sự sụt giảm Hit-rate từ 33.1% xuống 9.2% ở giỏ lớn.\n\n" \
             "• Giải pháp: Áp dụng trọng số nghịch đảo tần suất (IDF). Món hiếm trong giỏ nhận trọng số lớn hơn; hóa đơn dài bị suy giảm độ tin cậy kết nối giữa 2 món ngẫu nhiên."
    p.font.size = Pt(13)

    # Card 2: Re-ranking MMR
    add_card(s13, Inches(4.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b = s13.shapes.add_textbox(Inches(5.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "2. Tái Xếp Hạng Đa Dạng (MMR Re-ranking)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "• Mục tiêu: Tránh gợi ý trùng lặp các biến thể cùng dòng sản phẩm.\n\n" \
             "• Giải pháp: Áp dụng thuật toán Maximal Marginal Relevance (MMR). Phạt điểm các món có độ giống nhau quá cao trong danh sách gợi ý để tăng độ phủ và độ mới (Novelty / Diversity)."
    p.font.size = Pt(13)

    # Card 3: Hybrid Cold-start
    add_card(s13, Inches(8.8), Inches(1.65), Inches(3.7), Inches(5.2))
    b = s13.shapes.add_textbox(Inches(9.0), Inches(1.85), Inches(3.3), Inches(4.8))
    tf = b.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3. Mô Hình Lai Cho Cold-Start (Content-based)"
    p.font.bold = True
    p.font.size = Pt(16)
    p.font.color.rgb = COLOR_PRIMARY
    p.space_after = Pt(10)
    p = tf.add_paragraph()
    p.text = "• Mục tiêu: Xử lý 4.8% sản phẩm mới ở tập test chưa có giao dịch cũ.\n\n" \
             "• Giải pháp: Nhúng ngữ nghĩa văn bản của cột Description bằng TF-IDF hoặc Sentence-BERT. Khi gặp món mới, tự động Fallback sang gợi ý tương đồng ngữ nghĩa."
    p.font.size = Pt(13)

    # =========================================================================
    # SLIDE 14: TỔNG KẾT & Q&A
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    bg = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = COLOR_PRIMARY_DARK
    bg.line.fill.background()

    strip = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.2))
    strip.fill.solid()
    strip.fill.fore_color.rgb = COLOR_GOLD
    strip.line.fill.background()

    box = s14.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.5))
    tf = box.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "TỔNG KẾT BÀI BÁO CÁO"
    p.font.name = FONT_TITLE
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    p = tf.add_paragraph()
    p.text = "3 Thông Điệp Cốt Lõi Của Nhóm"
    p.font.name = FONT_TITLE
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(8)
    p.space_after = Pt(20)

    p = tf.add_paragraph()
    p.text = "1. Hiệu năng vượt trội: Cosine Item–Invoice đạt Hit-rate@10 là 21.59%, vượt baseline 5.6 lần và mở rộng độ phủ danh mục gấp 48 lần (40.86% so với 0.85%).\n\n" \
             "2. Phương pháp luận trung thực: Nghiêm túc chặn rò rỉ dữ liệu, đóng băng cấu hình bằng Git tag trước khi xem test, phân tích sai số đa chiều theo tinh thần khoa học.\n\n" \
             "3. Kỹ thuật hoàn thiện: Đạt đủ tiêu chuẩn từ thuật toán, kiểm thử tự động (31 unit tests) đến ứng dụng Web SPA gợi ý giỏ hàng thông minh và đóng gói Docker."
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(241, 245, 249)
    p.space_after = Pt(24)

    p = tf.add_paragraph()
    p.text = "XIN CHÂN THÀNH CẢM ƠN THẦY VÀ HỘI ĐỒNG ĐÃ LẮNG NGHE!\nSẴN SÀNG TRẢ LỜI CÁC CÂU HỎI VẤN ĐÁP."
    p.font.name = FONT_TITLE
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_GOLD

    out_file = "Bao_Cao_BTL_Hoc_May_Retail_Recommender.pptx"
    candidates = [
        out_file,
        "Bao_Cao_BTL_Hoc_May_Retail_Recommender_CapNhat.pptx",
        "Bao_Cao_BTL_Hoc_May_Retail_Recommender_v2.pptx",
        "Bao_Cao_BTL_Hoc_May_Retail_Recommender_MoiNhat.pptx"
    ]
    saved = False
    for target in candidates:
        try:
            prs.save(target)
            print(f"Đã tạo thành công file trình chiếu: {target} (14 slides)")
            saved = True
            break
        except PermissionError:
            continue
    if not saved:
        import time
        ts_file = f"Bao_Cao_BTL_Hoc_May_Retail_Recommender_{int(time.time())}.pptx"
        prs.save(ts_file)
        print(f"Các file chính đang mở trong PowerPoint, đã lưu vào: {ts_file} (14 slides)")

if __name__ == "__main__":
    create_deck()
