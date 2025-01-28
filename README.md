# simple_icd_10
A simple python library for ICD-10 codes

## Index
* [Release notes](#release-notes)
* [Introduction](#introduction)
* [Setup](#setup)
* [What a code is and how it looks like](#what-a-code-is-and-how-it-looks-like)
* [Documentation](#documentation)
  * [is_valid_item(code)](#is_valid_itemcode)
  * [is_category_or_subcategory(code)](#is_category_or_subcategorycode)
  * [is_chapter_or_block(code)](#is_chapter_or_blockcode)
  * [is_chapter(code)](#is_chaptercode)
  * [is_block(code)](#is_blockcode)
  * [is_category(code)](#is_categorycode)
  * [is_subcategory(code)](#is_subcategorycode)
  * [get_description(code)](#get_descriptioncode)
  * [get_parent(code)](#get_parentcode)
  * [get_children(code)](#get_childrencode)
  * [get_ancestors(code)](#get_ancestorscode)
  * [get_descendants(code)](#get_descendantscode)
  * [is_ancestor(a,b)](#is_ancestorab)
  * [is_descendant(a,b)](#is_descendantab)
  * [get_nearest_common_ancestor(a,b)](#get_nearest_common_ancestorab)
  * [is_leaf(code)](#is_leafcode)
  * [get_all_codes(with_dots=True)](#get_all_codeswith_dotstrue)
  * [get_index(code)](#get_indexcode)
  * [remove_dot(code)](#remove_dotcode)
  * [add_dot(code)](#add_dotcode)
* [Conclusion](#conclusion)

## Release notes
* **2.1.1**: Fixed X85-Y09 being a child instead of a sibling of X60-X84.
* **2.1.0**: Added type hints. It now requires Python 3.9 or a later version. Renamed internal variables to discourage direct access. Dropped conda support (old versions are still available).
* **2.0.1**: Fixed a minor bug that affected get_nearest_common_ancestor(a,b) when a and b were the same code but written in different formats.
* **2.0.0**: **Major update**
  * Completely rewritten the library, making the code simpler, easier to understand and customize and less prone to errors!
  * **Important**: from now on, the default format of the codes returned by the functions in this library will be the one **with** the dot instead of the one **without** the dot. Please consider how this could impact your project before updating the package.
  * The results of "get_descendants" are now always ordered.
  * The argument in "get_all_codes" (now renamed to "with_dots") is now optional and is True by default.
  * **Removed the memoization**: thanks to the new implementation of the library, memoization is no longer needed.
* **1.6.3**: Fixed a bug relative to the descendants of block "X85-Y09".
* **1.6.2**: Fixed a bug that caused incorrect results when working with some of the codes in chapter XX.
* **1.6.1**: Added functions that were missing from release 1.6.0.
* **1.6.0**: Added the functions "get_parent", "get_children", "remove_dot" and "add_dot". These functions could be optimized for better performance: contact me if you feel that such improvement is needed.
* **1.5.0**: Added the function "is_leaf", renamed the function "is_valid_code" to "is_category_or_subcategory" (the old name can still be used for backward compatibility), removed from the README a section rendered obsolete by this renaming.
* **1.4.0**: Added the functions "is_chapter", "is_block", "is_category" and "is_subcategory"
* **1.3.2**: Re-release of the previous version (pretend this doesn't exist)
* **1.3.1**: Huge performance improvements, bug fix
* **1.3.0**: Additional major performance improvements
* **1.2.1**: Minor fix to ensure the integrity of the data
* **1.2.0**: Added memoization to achieve high performance improvements
* **1.1**: Added the function "get_nearest_common_ancestor"
* **1.0**: Initial release

## Introduction
The scope of this library is to provide a simple instrument for dealing with ICD-10 codes in your Python projects. It provides ways to check whether a code exists, to find its ancestors and descendants, to see its description and much more.  
The codes and their descriptions were taken from [this page](https://icd.who.int/browse10/2019/en#) in the WHO's website and are referred to the **2019 version of ICD-10**.  
If you are looking for a library that deals with ICD-10-CM codes instead of ICD-10 codes, you can check the [simple_icd_10_CM library](https://github.com/StefanoTrv/simple_icd_10_CM). If you are interested in the ICD-11 MMS classification, you can check out instead the [simple_icd_11 library](https://github.com/StefanoTrv/simple_icd_11).  
There is also a Java version of this library, [SimpleICD10-Java-edition](https://github.com/StefanoTrv/SimpleICD10-Java-edition).

You can find all the codes and their descriptions in plain text in the ["data" folder](https://github.com/StefanoTrv/simple_icd_10/tree/master/data), as well as an XML file that contains the entire ICD-10 classification.

## Setup
You can either use the "simple_icd_10.py" file, which contains all the source code, in conjunction with the XML file in the "data" folder (you can find them in the [GitHub repository](https://github.com/StefanoTrv/simple_icd_10)), or install the package with pip, using this command:
```bash
pip install simple-icd-10
```
The distribution files are also available as [releases in the Github repository](https://github.com/StefanoTrv/simple_icd_10/releases).

## What a code is and how it looks like
We need to start by clarifying what a code is for us. The [ICD-10 instruction manual](https://icd.who.int/browse10/Content/statichtml/ICD10Volume2_en_2019.pdf) makes a distinction between **chapters**, **block of categories**, **three-character categories** and **four-character subcategories** (which from now on we'll refer to as chapters, blocks, categories and subcategories), with a few additional five-character subcategories: we will consider all these items as codes.

Generally speaking, the codes of subcategories can be written in two different ways: with a dot (for example "I13.1") and without the dot (for example "I131"). The functions in this library can receive as input codes in both these formats. The codes returned by the functions will always be in the format with the dot. You can easily change the format of a code by using the [`remove_dot`](#remove_dotcode) and [`add_dot`](#add_dotcode) functions.

## Documentation
Here I will list all the functions provided by this library and describe how to use them. If you are interested in a more interactive introduction to simple_icd_10, please take a look at the Jupyter Notebook ["Showcase notebook.ipynb"](https://github.com/StefanoTrv/simple_icd_10/blob/master/Showcase%20notebook.ipynb); there you can also find more examples.

Here we suppose we have imported the library as follows:
```python
import simple_icd_10 as icd
```
### is_valid_item(code)
This function takes a string as input and returns True if the string is a valid chapter, block, category or subcategory in ICD-10, False otherwise.
```python
icd.is_valid_item("cat")
#False
icd.is_valid_item("B99")
#True
```
### is_category_or_subcategory(code)
This function takes a string as input and returns True if the string is a valid category or subcategory in ICD-10, False otherwise.
```python
icd.is_category_or_subcategory("A00-B99")
#False
icd.is_category_or_subcategory("B99")
#True
```
### is_chapter_or_block(code)
This function takes a string as input and returns True if the string is a valid chapter or block in ICD-10, False otherwise.
```python
icd.is_chapter_or_block("A00-B99")
#True
icd.is_chapter_or_block("B99")
#False
```
### is_chapter(code)
This function takes a string as input and returns True if the string is a valid chapter in ICD-10, False otherwise.
```python
icd.is_chapter("XII")
#True
icd.is_chapter("B99")
#False
```
### is_block(code)
This function takes a string as input and returns True if the string is a valid block in ICD-10, False otherwise.
```python
icd.is_block("A00-B99")
#True
icd.is_block("B99")
#False
```
### is_category(code)
This function takes a string as input and returns True if the string is a valid category in ICD-10, False otherwise.
```python
icd.is_category("B99")
#True
icd.is_category("XIV")
#False
```
### is_subcategory(code)
This function takes a string as input and returns True if the string is a valid subcategory in ICD-10, False otherwise.
```python
icd.is_subcategory("B95.1")
#True
icd.is_subcategory("B99")
#False
```
### get_description(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns a string with its short description, otherwise it raises a ValueError.
```python
icd.get_description("XII")
#"Diseases of the skin and subcutaneous tissue"
icd.get_description("F00")
#"Dementia in Alzheimer disease"
```
### get_parent(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns a string containing its parent, otherwise it raises a ValueError. If the code doesn't have a parent (that is, if it's a chapter), it returns an empty string.
```python
icd.get_parent("C00")
#"C00-C14"
icd.get_parent("XII")
#""
```
### get_children(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns a list of strings containing its children, otherwise it raises a ValueError. If the code doesn't have children, it returns an empty list.
```python
icd.get_children("XII")
#['L00-L08', 'L10-L14', 'L20-L30', 'L40-L45', 'L50-L54', 'L55-L59', 'L60-L75', 'L80-L99']
icd.get_children("H60.1")
#[]
```
### get_ancestors(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns a list containing all its ancestors in the ICD-10 classification, otherwise it raises a ValueError. The results are ordered from its parent to its most distant ancestor.
```python
icd.get_ancestors("H60.1")
#['H60', 'H60-H62', 'VIII']
```
### get_descendants(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns a list containing all its descendants in the ICD-10 classification, otherwise it raises a ValueError. The returned codes are ordered as in a pre-order depth-first traversal of the tree containing the ICD-10 classification.
```python
icd.get_descendants("C00")
#['C00.0', 'C00.1', 'C00.2', 'C00.3', 'C00.4', 'C00.5', 'C00.6', 'C00.8', 'C00.9']
```
### is_ancestor(a,b)
This function takes two strings as input. If both strings are valid ICD-10 codes, it returns True if the first string is an ancestor of the second string. If at least one of the strings is not a valid ICD-10 code, it raises a ValueError.
```python
icd.is_ancestor("XVIII","R01.0")
#True
icd.is_ancestor("K00-K14","M31")
#False
```
### is_descendant(a,b)
This function takes two strings as input. If both strings are valid ICD-10 codes, it returns True if the first string is a descendant of the second string. If at least one of the strings is not a valid ICD-10 code, it raises a ValueError.
```python
icd.is_descendant("R01.0","XVIII")
#True
icd.is_descendant("M31","K00-K14")
#False
```
### get_nearest_common_ancestor(a,b)
This function takes two strings as input. If both strings are valid ICD-10 codes, it returns their nearest common ancestor if it exists, an empty string if it doesn't exist. If at least one of the strings is not a valid ICD-10 code, it raises a ValueError.
```python
icd.get_nearest_common_ancestor("H28.0","H25.1")
#"H25-H28"
icd.get_nearest_common_ancestor("K35","E21.0")
#""
```
### is_leaf(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns True if the code is a leaf in the ICD-10 classification (that is, it has no descendants), False otherwise. If the string is not a valid ICD-10 code it raises a ValueError.
```python
icd.is_leaf("H28")
#False
icd.is_leaf("H28.0")
#True
#""
```
### get_all_codes(with_dots=True)
This function takes a boolean for input and returns the list of all items in the ICD-10 classification. If the optional argument 'with_dots' is True (its default value), the subcategories in the list will have a dot in them, if it's set to False the subcategories won't have a dot in them.
```python
icd.get_all_codes()
#['I', 'A00-A09', 'A00', 'A00.0', 'A00.1', 'A00.9', 'A01', 'A01.0', ...
icd.get_all_codes(with_dots=False)
#['I', 'A00-A09', 'A00', 'A000', 'A001', 'A009', 'A01', 'A010', ...
```
### get_index(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns its index in the list returned by `get_all_codes`, otherwise it raises a ValueError.
```python
icd.get_index("P00")
#7159
icd.get_all_codes(True)[7159]
#"P00"
```
### remove_dot(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns the same code in the notation without the dot, otherwise it raises a ValueError.
```python
icd.remove_dot("H60.1")
#"H601"
icd.remove_dot("H601")
#"H601"
icd.remove_dot("G10-G14")
#"G10-G14"
```
### add_dot(code)
This function takes a string as input. If the string is a valid ICD-10 code, it returns the same code in the notation with the dot, otherwise it raises a ValueError.
```python
icd.add_dot("H60.1")
#"H60.1"
icd.add_dot("H601")
#"H60.1"
icd.add_dot("G10-G14")
#"G10-G14"
```
## Conclusion
This is everything you needed to know before using the simple_icd_10 library - please contact me if you feel I missed something or there's some passage that you think should be explained better or more. Also contact me if you find any errors in the library or in the documentation.  
I hope this library will save you some time; it definitely would have done it for me if I hadn't had to write it!

If you are feeling particularly thankful and/or generous and feel like leaving me a tip, **don't!**  
Donate instead to *Médecins Sans Frontières* to support their efforts to provides medical care to millions of people caught in crises around the world. Click on the logo below to open their "donate" page.

[![MSF Logo](https://www.msf.org/themes/custom/msf_theme/src/kss/components/icons/assets/logo-white-en.svg)](https://www.msf.org/donate)

If you end up making a donation because of this library, feel free to drop me an email: I'll be happy to read it!

*Stefano Travasci*
