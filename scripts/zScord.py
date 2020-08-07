import http.client
import urllib.parse
import math
from bs4 import BeautifulSoup


# 通过第三方网站获取z值
# 计算过程未知
# 该网站的算法是基于日本儿童的冠脉管径数据库
def get_z_score(gender, height, weight, rca, lmca):
    conn = http.client.HTTPConnection("cgi.geocities.jp")
    headers = {
        'content-type': "application/x-www-form-urlencoded",
        'dnt': "1"
    }
    post_data = {
        'methodology': 'LMS_4',
        'mode': 'calc_z',
        'gender': gender,
        'height': height,
        'weight': weight,
        'Seg1': rca,
        'Seg5': lmca
    }
    payload = urllib.parse.urlencode(post_data)

    rca_z = 0
    lmca_z = 0
    try:
        conn.request("POST", "/kawasaki_disease_z/zsp_form.cgi", payload, headers)
        res = conn.getresponse()
        data = BeautifulSoup(res.read(), 'html.parser').find_all('td')
        rca_z = float(data[6].get_text())
        lmca_z = float(data[10].get_text())
    except http.client.HTTPException as e:
        print(e)
    finally:
        if conn:
            conn.close()
    return rca_z, lmca_z


# 计算BSA
def calc_bsa(height, weight):
    if weight <= 30:
        return weight * 0.035 + 0.1
    else:
        return 0.024265 * height ** 0.3964 * weight ** 0.5378
    # math.sqrt(echo.patient.weight * echo.patient.height / 3600)


# 另一种根据性别区分的BSA算法
def calc_bsa_with_gender(gender, height, weight):
    if gender == 'F':
        return 0.0073 * height + 0.0127 * weight - 0.2106
    elif gender == 'M':
        return 0.0057 * height + 0.0121 * weight + 0.0882
    else:
        return 0.0061 * height + 0.0124 * weight - 0.0099


# 基于BSA标准z值的算法
# 算法的常数来自上海的数据库？
# 该算法得出的数据参考价值可能不高
def calc_z_score(bsa, rca, lmca):
    z_rca = (rca - (5.032 * math.sqrt(bsa) - 2.189 * bsa - 0.577)) / 0.332
    z_lmca = (lmca - (4.898 * math.sqrt(bsa) - 1.761 * bsa - 0.368)) / 0.324
    return round(z_lmca, 2), round(z_rca, 2)



