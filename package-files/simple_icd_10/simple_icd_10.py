from __future__ import annotations
import xml.etree.ElementTree as ET

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources  # type: ignore

from . import data  # relative-import the "package" containing the data

_chapter_list : list[_CodeTree] = []

_code_to_node : dict[str,_CodeTree] = {}

_all_codes_list : list[str] = []

_all_codes_list_no_dots : list[str] = []

_code_to_index_dictionary : dict[str,int] = {}

class _CodeTree:
    def __init__(self, tree, parent = None):
        #initialize all the values
        self.name = ""
        self.description = ""
        self.type = ""
        self.parent = parent
        self.children = []
        
        #reads the data from the subtrees
        self.type=tree.attrib["type"]
        for subtree in tree:
            if subtree.tag=="name":
                self.name=subtree.text
            elif subtree.tag=="description":
                self.description=subtree.text
            else:
                self.children.append(_CodeTree(subtree, parent=self))
        
        #adds the new node to the dictionary
        _code_to_node[self.name]=self

def _load_codes() -> None:
    #creates the tree
    root = ET.fromstring(pkg_resources.read_text(data, 'icd_10_v2019.xml'))
    for child in root:
        _chapter_list.append(_CodeTree(child))

_load_codes()

def _add_dot_to_code(code) -> str:
    if len(code)<4 or code[3]==".":
        return code
    elif code[:3]+"."+code[3:] in _code_to_node:
        return code[:3]+"."+code[3:]
    else:
        return code

def is_valid_item(code) -> bool:
    return code in _code_to_node or len(code)>=4 and code[:3]+"."+code[3:] in _code_to_node

def is_chapter(code) -> bool:
    code = _add_dot_to_code(code)
    if code in _code_to_node:
        return _code_to_node[code].type=="chapter"
    else:
        return False

def is_block(code) -> bool:
    code = _add_dot_to_code(code)
    if code in _code_to_node:
        return _code_to_node[code].type=="block"
    else:
        return False

def is_category(code) -> bool:
    code = _add_dot_to_code(code)
    if code in _code_to_node:
        return _code_to_node[code].type=="category"
    else:
        return False

def is_subcategory(code) -> bool:
    code = _add_dot_to_code(code)
    if code in _code_to_node:
        return _code_to_node[code].type=="subcategory"
    else:
        return False
    
def is_category_or_subcategory(code) -> bool:
    return is_subcategory(code) or is_category(code)

def is_chapter_or_block(code) -> bool:
    return is_block(code) or is_chapter(code)

def get_description(code) -> str:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    return node.description

def get_parent(code) -> str:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    if node.parent!=None:
        return node.parent.name
    else:
        return ""

def get_children(code) -> list[str]:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    res = []
    for child in node.children:
        res.append(child.name)
    return res

def is_leaf(code) -> bool:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    return len(node.children)==0

def get_ancestors(code) -> list[str]:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    result = []
    while node.parent != None:
        result.append(node.parent.name)
        node=node.parent
    return result

def get_descendants(code) -> list[str]:
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(code)]
    result = []
    _add_children_to_list(node, result)
    return result

def _add_children_to_list(node, list) -> None:
    for child in node.children:
        list.append(child.name)
        _add_children_to_list(child,list)

def is_ancestor(a,b) -> bool:
    if not is_valid_item(a):
        raise ValueError("The code \""+a+"\" does not exist.")
    node = _code_to_node[_add_dot_to_code(a)]
    return a in get_ancestors(b) and a!=b

def is_descendant(a,b) -> bool:
    return is_ancestor(b,a)

def get_nearest_common_ancestor(a,b) -> str:
    anc_a = [_add_dot_to_code(a)] + get_ancestors(a)
    anc_b = [_add_dot_to_code(b)] + get_ancestors(b)
    if len(anc_b) > len(anc_a):
        temp = anc_a
        anc_a = anc_b
        anc_b = temp
    for anc in anc_a:
        if anc in anc_b:
            return anc
    return ""

def get_all_codes(with_dots=True) -> list[str]:
    if _all_codes_list==[]:
        for chapter in _chapter_list:
            _add_tree_to_list(chapter)
    if with_dots:
        return _all_codes_list.copy()
    else:
        return _all_codes_list_no_dots.copy()

def _add_tree_to_list(tree) -> None:
    _all_codes_list.append(tree.name)
    if(len(tree.name)>4 and tree.name[3]=="."):
        _all_codes_list_no_dots.append(tree.name[:3]+tree.name[4:])
    else:
        _all_codes_list_no_dots.append(tree.name)
    for child in tree.children:
        _add_tree_to_list(child)

def get_index(code) -> int: # type: ignore
    if not is_valid_item(code):
        raise ValueError("The code \""+code+"\" does not exist.")
    code = _add_dot_to_code(code)
    if _all_codes_list==[]:
        for chapter in _chapter_list:
            _add_tree_to_list(chapter)
    if code in _code_to_index_dictionary:
        return _code_to_index_dictionary[code]
    else:
        i=0
        for c in _all_codes_list:
            if c==code:
                _code_to_index_dictionary[code]=i
                return i
            else:
                i=i+1

def remove_dot(code) -> str:
    if _all_codes_list==[]:
        for chapter in _chapter_list:
            _add_tree_to_list(chapter)
    return _all_codes_list_no_dots[get_index(code)]

def add_dot(code) -> str:
    if _all_codes_list==[]:
        for chapter in _chapter_list:
            _add_tree_to_list(chapter)
    return _all_codes_list[get_index(code)]