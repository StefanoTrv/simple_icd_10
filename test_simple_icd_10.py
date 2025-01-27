import unittest
import simple_icd_10 as icd

class TestSimpleICD10(unittest.TestCase):

    def test_is_valid_item(self):
        self.assertFalse(icd.is_valid_item("dinosaur"))
        self.assertTrue(icd.is_valid_item("XII"))
        self.assertTrue(icd.is_valid_item("G10-G14"))
        self.assertTrue(icd.is_valid_item("C00"))
        self.assertTrue(icd.is_valid_item("H60.1"))

    def test_is_category_or_subcategory(self):
        self.assertFalse(icd.is_category_or_subcategory("dinosaur"))
        self.assertFalse(icd.is_category_or_subcategory("XII"))
        self.assertFalse(icd.is_category_or_subcategory("G10-G14"))
        self.assertTrue(icd.is_category_or_subcategory("C00"))

    def test_is_chapter_or_block(self):
        self.assertFalse(icd.is_chapter_or_block("dinosaur"))
        self.assertTrue(icd.is_chapter_or_block("XII"))
        self.assertTrue(icd.is_chapter_or_block("G10-G14"))
        self.assertFalse(icd.is_chapter_or_block("C00"))

    def test_is_chapter(self):
        self.assertFalse(icd.is_chapter("dinosaur"))
        self.assertTrue(icd.is_chapter("XII"))
        self.assertFalse(icd.is_chapter("G10-G14"))
        self.assertFalse(icd.is_chapter("C00"))

    def test_is_block(self):
        self.assertFalse(icd.is_block("dinosaur"))
        self.assertFalse(icd.is_block("XII"))
        self.assertTrue(icd.is_block("G10-G14"))
        self.assertFalse(icd.is_block("C00"))

    def test_is_category(self):
        self.assertFalse(icd.is_category("dinosaur"))
        self.assertFalse(icd.is_category("XII"))
        self.assertFalse(icd.is_category("G10-G14"))
        self.assertTrue(icd.is_category("C00"))

    def test_is_subcategory(self):
        self.assertFalse(icd.is_subcategory("dinosaur"))
        self.assertFalse(icd.is_subcategory("XII"))
        self.assertFalse(icd.is_subcategory("G10-G14"))
        self.assertFalse(icd.is_subcategory("C00"))

    def test_get_description(self):
        self.assertEqual(icd.get_description("XII"),"Diseases of the skin and subcutaneous tissue")
        self.assertEqual(icd.get_description("G10-G14"),"Systemic atrophies primarily affecting the central nervous system")
        self.assertEqual(icd.get_description("C00"),"Malignant neoplasm of lip")
        self.assertEqual(icd.get_description("H60.1"),"Cellulitis of external ear")
    
    def test_get_parent(self):
        self.assertEqual(icd.get_parent("XII"),"")
        self.assertEqual(icd.get_parent("G10-G14"),"VI")
        self.assertEqual(icd.get_parent("C00"),"C00-C14")
        self.assertEqual(icd.get_parent("H60.1"),"H60")

    def test_get_children(self):
        self.assertEqual(icd.get_children("XII"),['L00-L08', 'L10-L14', 'L20-L30', 'L40-L45', 'L50-L54', 'L55-L59', 'L60-L75', 'L80-L99'])
        self.assertEqual(icd.get_children("G10-G14"),['G10', 'G11', 'G12', 'G13', 'G14'])
        self.assertEqual(icd.get_children("C00"),['C00.0', 'C00.1', 'C00.2', 'C00.3', 'C00.4', 'C00.5', 'C00.6', 'C00.8', 'C00.9'])
        self.assertEqual(icd.get_children("H60.1"),[])

    def test_get_ancestors(self):
        self.assertEqual(icd.get_ancestors("XII"),[])
        self.assertEqual(icd.get_ancestors("G10-G14"),['VI'])
        self.assertEqual(icd.get_ancestors("C00"),['C00-C14', 'C00-C75', 'C00-C97', 'II'])
        self.assertEqual(icd.get_ancestors("H60.1"),['H60', 'H60-H62', 'VIII'])

    def test_get_descendants(self):
        self.assertEqual(icd.get_descendants("G10-G14"),['G10', 'G11', 'G11.0', 'G11.1', 'G11.2', 'G11.3', 'G11.4', 'G11.8', 'G11.9', 'G12', 'G12.0', 'G12.1', 'G12.2', 'G12.8', 'G12.9', 'G13', 'G13.0', 'G13.1', 'G13.2', 'G13.8', 'G14'])
        self.assertEqual(icd.get_descendants("C00"),['C00.0', 'C00.1', 'C00.2', 'C00.3', 'C00.4', 'C00.5', 'C00.6', 'C00.8', 'C00.9'])
        self.assertEqual(icd.get_descendants("H60.1"),[])
        
    def test_is_descendant(self):
        self.assertTrue(icd.is_descendant("H60.1","H60-H62"))
        self.assertFalse(icd.is_descendant("H60-H62","H60.1"))
        self.assertFalse(icd.is_descendant("E15-E16","E15-E16"))
        
    def test_is_ancestor(self):
        self.assertFalse(icd.is_ancestor("H60.1","H60-H62"))
        self.assertTrue(icd.is_ancestor("H60-H62","H60.1"))
        self.assertFalse(icd.is_ancestor("E15-E16","E15-E16"))
        
    def test_get_nearest_common_ancestor(self):
        self.assertEqual(icd.get_nearest_common_ancestor("J950","J998"),"J95-J99")
        
    def test_is_leaf(self):
        self.assertFalse(icd.is_leaf("XII"))
        self.assertFalse(icd.is_leaf("G10-G14"))
        self.assertFalse(icd.is_leaf("C00"))
        self.assertTrue(icd.is_leaf("H60.1"))
        self.assertTrue(icd.is_leaf("O94"))
    
    def test_get_all_codes(self):
        self.assertEqual(icd.get_all_codes()[:15], ['I', 'A00-A09', 'A00', 'A00.0', 'A00.1', 'A00.9', 'A01', 'A01.0', 'A01.1', 'A01.2', 'A01.3', 'A01.4', 'A02', 'A02.0', 'A02.1'])
        self.assertEqual(icd.get_all_codes(False)[:15], ['I', 'A00-A09', 'A00', 'A000', 'A001', 'A009', 'A01', 'A010', 'A011', 'A012', 'A013', 'A014', 'A02', 'A020', 'A021'])
        self.assertEqual([code for code in icd.get_all_codes(False) if not icd.is_chapter_or_block(code)][:15],['A00', 'A000', 'A001', 'A009', 'A01', 'A010', 'A011', 'A012', 'A013', 'A014', 'A02', 'A020', 'A021', 'A022', 'A028'])
        self.assertEqual(icd.get_all_codes()[7159],'P00')
        self.assertEqual(icd.get_description(icd.get_all_codes()[7159]),'Fetus and newborn affected by maternal conditions that may be unrelated to present pregnancy')
        
    def test_get_index(self):
        self.assertEqual(icd.get_index("P00"),7159)
    
    def test_remove_dot(self):
        self.assertEqual(icd.remove_dot("XII"),"XII")
        self.assertEqual(icd.remove_dot("G10-G14"),"G10-G14")
        self.assertEqual(icd.remove_dot("H60.1"),"H601")
        self.assertEqual(icd.remove_dot("H601"),"H601")
    
    def test_add_dot(self):
        self.assertEqual(icd.add_dot("XII"),"XII")
        self.assertEqual(icd.add_dot("G10-G14"),"G10-G14")
        self.assertEqual(icd.add_dot("H60.1"),"H60.1")
        self.assertEqual(icd.add_dot("H601"),"H60.1")