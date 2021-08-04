import simple_icd_10 as icd

chapter_list = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX","XXI","XXII"]

def to_xml(item):
    result = "<item type=\""+get_type(item)+"\">"+"\n\t<name>"+icd.add_dot(item)+"</name>\n\t<description>"+icd.get_description(item)+"</description>"
    for child in icd.get_children(item):
        result = result + add_tabulation(to_xml(child))
    result = result +"\n</item>"
    return result


def get_type(item):
    if icd.is_chapter(item):
        return "chapter"
    elif icd.is_block(item):
        return "block"
    elif icd.is_category(item):
        return "category"
    else:
        return "subcategory"

def add_tabulation(string):
    result = ""
    for line in string.splitlines():
        result = result +"\n\t" + line
    return result


XML_output= ""
for chapter in chapter_list:
    XML_output=XML_output+"\n"+to_xml(chapter)
XML_output="<icd_10_v2019>"+add_tabulation(XML_output)+"\n</icd_10_v2019>"

f = open("icd_10_v2019.xml", "w", encoding="utf-8-sig")
f.write(XML_output)
f.close()