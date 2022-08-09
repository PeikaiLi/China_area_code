import re
import pandas as pd
from tqdm import trange
import matplotlib.pyplot as plt


def find_city(acode):
    if acode//100*100 in dic_area_code:
        return dic_area_code[acode//100*100]
    else:
        return ""


def find_province(acode):
    if acode//10000*10000 in dic_area_code:
        return dic_area_code[acode//10000*10000]
    else:
        return ""
    

def drop_ethnic_noun(sen = ""):
    """
    把名字民族字符去掉，

    Parameters
    ----------
    sen : str, optional
        一个名字. The default is "".

    Returns
    -------
    sen : str
        精简过的名字.

    """
    sen.strip().replace("  "," ")
    ethnic_minorities = ['蒙古族','回族','藏族','苗族','维吾尔族','彝族','壮族','布依族','白族','朝鲜族','侗族','哈尼族','哈萨克族','满族','土家族','瑶族','达斡尔族','东乡族','高山族','景颇族','柯尔克孜族','拉祜族','纳西族','畲族','傣族','黎族','傈僳族','仫佬族','羌族','水族','土族','佤族','阿昌族','布朗族','毛南族','普米族','撒拉族','塔吉克族','锡伯族','仡佬族','保安族','德昂族','俄罗斯族','鄂温克族','京族','怒族','乌孜别克族','裕固族','独龙族','鄂伦春族','赫哲族','基诺族','珞巴族','门巴族','塔塔尔族','汉族']
    for i in ethnic_minorities:
        sen = sen.replace(i,"")
        
    ethnic_minorities = ['维吾尔', '哈萨克', '达斡尔', '柯尔克孜', '塔吉克', '俄罗斯', '鄂温克', '乌孜别克', '鄂伦春', '塔塔尔']
    for i in ethnic_minorities:
        sen = sen.replace(i,"")
        
    return sen


# 前缀处理
def drop_prefix(s= '西瓜自治县',pattern_prefix = '西瓜|毛病'):
    """
    去掉前缀：
    """
    s = drop_ethnic_noun(s)
    pattern_prefix = re.compile(pattern_prefix)
    prefix = re.match(pattern_prefix , s) # 从头匹配
    if bool(prefix) == True:
        prefix_string = prefix.group()
        prefix_index = len(prefix_string)
        _drop = s[prefix_index:]
    else:
        _drop = s
    return _drop


def drop_suffix(s= '西县'):
    """
    去掉后缀：
    """
    raws = s
    s = drop_ethnic_noun(s)
    if len(s)<3:
        return s
    wss_suffix = ['自治区','自治州',"自治县","自治旗","市辖区","县级市","林区","特区",'区',"县","旗","盟","市","省","族"]
    wss_suffix = [i[::-1] for i in wss_suffix]
    wss_suffix = "|".join(wss_suffix)
    pattern_suffix = re.compile(wss_suffix)
    s = drop_prefix(s[::-1],pattern_suffix)[::-1]
    # 如果把s弄没了
    if s=="":
        s = raws
        s = s.replace("族自治旗","").replace("自治旗","").replace("自治县","")
    return s




if __name__ == '__main__':
    area_code = pd.read_excel("2020年12月中国县以上行政区划代码.xlsx")
    area_code = area_code[area_code["代码"]<710000]
    dic_area_code = {}
    for i in range(len(area_code)):
        dic_area_code[area_code.iloc[i]['代码']] = area_code.iloc[i]['名称']
        
        
    county = area_code[area_code['代码'] %100 != 0].copy()
    county["市级"] = county['代码'].apply(find_city)
    county["省级"] = county['代码'].apply(find_province)
    county = county[['代码','省级','市级','名称']]
    county = county.rename(columns={'名称':'县区级'})
    county.to_excel('2020年12月中国县以上行政区划代码处理版本.xlsx',index = False)

    print("""drop_suffix(s= '鄂温克族自治旗')""")
    print(drop_suffix(s= '鄂温克族自治旗'))


    county_search_list = county.copy()
    county_search_list['省级_简'] = county_search_list['省级'].apply(drop_suffix)
    county_search_list['市级_简'] = county_search_list['市级'].apply(drop_suffix)
    county_search_list['县区级_简'] = county_search_list['县区级'].apply(drop_suffix)

    county_search_list['名称'] = county_search_list['省级_简']+" "+county_search_list['市级_简']+" "+county_search_list['县区级_简']
    county_search_list['名称'] = county_search_list['名称'].apply(lambda x : x.replace("  "," ").strip())
    county_search_list.to_excel("简写对应表.xlsx",index = False)