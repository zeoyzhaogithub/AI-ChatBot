from datetime import datetime
import openai
import pytz

# ----------------------
# 八字排盘模块（简化版）
# 注意：此为简化逻辑，真实排盘需考虑节气、时辰换算等复杂因素
# ----------------------

TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
WUXING_MAP = {
    "甲": "木", "乙": "木", "寅": "木", "卯": "木",
    "丙": "火", "丁": "火", "巳": "火", "午": "火",
    "戊": "土", "己": "土", "辰": "土", "戌": "土", "丑": "土", "未": "土",
    "庚": "金", "辛": "金", "申": "金", "酉": "金",
    "壬": "水", "癸": "水", "亥": "水", "子": "水"
}

def get_bazi_simplified(birth_time):
    """简化版八字排盘（示例用，实际需要完整排盘逻辑）"""
    year = (birth_time.year - 3) % 60 % 10
    month = (birth_time.month + 1) % 12
    day = (birth_time.day + 30) % 60 % 10
    hour = birth_time.hour // 2 % 12
    
    return [
        TIANGAN[year] + DIZHI[(birth_time.year - 3) % 60 % 12],
        TIANGAN[month] + DIZHI[(birth_time.month + 1) % 12],
        TIANGAN[day] + DIZHI[(birth_time.day + 30) % 60 % 12],
        TIANGAN[hour] + DIZHI[birth_time.hour // 2 % 12]
    ]

# ----------------------
# 分析模块
# ----------------------

def analyze_wuxing(bazi):
    """五行统计"""
    wuxing = {"木":0, "火":0, "土":0, "金":0, "水":0}
    for pillar in bazi:
        for c in pillar:
            element = WUXING_MAP.get(c, None)
            if element:
                wuxing[element] += 1
    return wuxing

def analyze_shishen(bazi):
    """十神分析（示例逻辑）"""
    # 日干取日柱的天干
    ri_gan = bazi[2][0]
    shishen_map = {
        "甲": {"甲":"比肩", "乙":"劫财", "丙":"食神", "丁":"伤官", "戊":"偏财", 
              "己":"正财", "庚":"七杀", "辛":"正官", "壬":"偏印", "癸":"正印"},
        # 其他日干的映射需补充完整
    }
    return {"七杀":2, "正官":1, "正印":3}  # 示例返回

# ----------------------
# 职业建议生成
# ----------------------

CAREER_MAPPING = {
    "木": ["教育", "出版", "文化"],
    "火": ["艺术", "娱乐", "能源"],
    "土": ["房地产", "农业", "建筑"],
    "金": ["金融", "机械", "法律"],
    "水": ["物流", "旅游", "医疗"],
    "七杀": ["创业", "军警"],
    "正官": ["公务员", "管理"],
    "正印": ["教育", "研究"]
}

def get_career_suggestions(wuxing, shishen):
    """获取职业建议关键词"""
    suggestions = []
    
    # 五行建议
    max_element = max(wuxing, key=wuxing.get)
    suggestions.extend(CAREER_MAPPING.get(max_element, []))
    
    # 十神建议
    for key in shishen:
        if shishen[key] > 1:
            suggestions.extend(CAREER_MAPPING.get(key, []))
    
    return list(set(suggestions))[:5]

# ----------------------
# 大模型接口
# ----------------------

def generate_advice_with_llm(suggestions, bazi):
    """调用大模型生成详细建议"""
    prompt = f"""请根据以下八字分析和职业建议，生成一份详细的职业咨询报告：
八字：{bazi}
建议方向：{', '.join(suggestions)}

要求：
1. 用专业但易懂的中文描述
2. 包含适合的行业和岗位建议
3. 分析性格优势和注意事项
4. 最后给出发展建议"""
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# ----------------------
# 主程序
# ----------------------

def main():
    # 配置OpenAI API密钥
    openai.api_key = "sk-your-api-key"
    
    # 获取输入
    birth_time = input("请输入出生时间（北京时间，格式YYYY-MM-DD HH:MM）：")
    local_time = datetime.strptime(birth_time, "%Y-%m-%d %H:%M")
    
    # 八字排盘
    bazi = get_bazi_simplified(local_time)
    print("\n您的八字命盘：", " ".join(bazi))
    
    # 分析阶段
    wuxing = analyze_wuxing(bazi)
    shishen = analyze_shishen(bazi)
    
    # 生成建议
    suggestions = get_career_suggestions(wuxing, shishen)
    print("\n生成建议关键词：", ", ".join(suggestions))
    
    # 大模型生成报告
    print("\n生成详细分析报告...")
    report = generate_advice_with_llm(suggestions, bazi)
    print("\n=== 职业发展建议报告 ===")
    print(report)

if __name__ == "__main__":
    main()