"""
学院名称映射：数据库/导入脚本 ↔ 小程序 UI
"""

# 小程序首页使用的学院名称
UI_COLLEGES = [
    '计算机学院',
    '电信学院',
    '机电学院',
    '经贸学院',
    '艺设学院',
    '人文学院',
    '材食学院',
    '外国语',
    '管理学院',
]

# 旧 category → UI category（一对一）
LEGACY_TO_UI = {
    '计算机学院': '计算机学院',
    '计算机': '计算机学院',
    '电子信息学院': '电信学院',
    '艺术设计学院': '艺设学院',
    '人文社会科学学院': '人文学院',
    '外国语学院': '外国语',
}

# 经济与管理学院按书名拆分
ECON_TITLE_TO_UI = {
    '管理学（第5版）': '管理学院',
    '财务管理学（第9版）': '管理学院',
}


def resolve_ui_category(category, title=''):
    """将数据库 category + 书名解析为小程序 UI 学院名"""
    if not category:
        return category
    if category == '经济与管理学院':
        return ECON_TITLE_TO_UI.get(title, '经贸学院')
    return LEGACY_TO_UI.get(category, category)


def ui_matches_book(ui_name, book_category, book_title=''):
    """判断某本书是否属于 UI 学院"""
    resolved = resolve_ui_category(book_category, book_title)
    return resolved == ui_name


def db_categories_for_ui(ui_name):
    """返回能匹配该 UI 学院的所有 DB category 值（用于 API 查询）"""
    cats = set()
    for legacy, ui in LEGACY_TO_UI.items():
        if ui == ui_name:
            cats.add(legacy)
    if ui_name == '经贸学院' or ui_name == '管理学院':
        cats.add('经济与管理学院')
    if ui_name == '计算机学院':
        cats.add('计算机')
    return list(cats)
