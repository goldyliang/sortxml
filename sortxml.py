#! /usr/bin/env python

##
# A simple program to normalized an XML file by sorting all elements and/or the attributes
# This is useful when comparing two XML files such as REST WADL files.
#
import sys
from lxml import etree
from copy import deepcopy
from collections import OrderedDict

##
# Compare two XML element (by comparing the string)
#
def cmp_elements(a, b):
    str_a = etree.tostring(a)
    str_b = etree.tostring(b)
    if str_a > str_b:
        return 1
    elif str_a == str_b:
        return 0
    else:
        return -1

##
# Sort the attribute dictionary, and return an OrderedDict
#
def sortedAttributes ( attrib ):
    ordered_attrib_list = []
    
    for key,value in attrib.iteritems():
        ordered_attrib_list.append ( (key,value) )

    ordered_attrib_list.sort ()
    
    return OrderedDict(ordered_attrib_list)

##
# Sort all sub-elements and attributes of a given XML root element
#
def sort (ele_root, bSortEle=True, bSortAttr=True):
    
    # Construct a copy of the root element,
    # with the same tag and ordered attributes,
    # And set the namespace map the same as original

    # Get a sorted or unsorted attribute list
    if (bSortAttr):
        attrib = sortedAttributes(ele_root.attrib)
    else:
        attrib = ele_root.attrib

    sorted_root = etree.Element(ele_root.tag, attrib, nsmap=ele_root.nsmap)

    # Set the constructed copy with the same text
    sorted_root.text = ele_root.text

    # Get all children
    subs = ele_root.findall ('./*')

    # Sort all the children recursively, and fill into a list
    sorted_subs = []
    for ele in subs:
       new_ele = sort (ele)
       sorted_subs.append (new_ele)

    # Sort all the children if bSortEle is true
    if (bSortEle):
        sorted_subs.sort (cmp_elements)


    # Append the sorted children to the copy of the root
    for ele in sorted_subs:
       sorted_root.append (ele)

    return sorted_root


# Read argument as input xml file, and sorted xml file
if (len(sys.argv) < 3):
   print "Normalize an XML file by sorting all elements and attributes"
   print "Usage: sortxml.py <input_file>, <output_file> [-ne] [-na]"
   print "   -ne  Not sorting elements"
   print "   -na  Not sorting attributes"
   sys.exit(1)

in_file = sys.argv[1]
out_file = sys.argv[2]
bSortEle = True
bSortAttr = True

if (len(sys.argv) > 3):
    if sys.argv[3] == '-ne':
       bSortEle = False
    elif (sys.argv[3] == '-na'):
       bSortAttr = False

if len(sys.argv) > 4:
    if sys.argv[4] == '-ne':
        bSortEle = False
    elif sys.argv[4] == '-na':
        bSortAttr = False

# Parse the input by removing all blank text (in order not to get conflict with pretty print)
parser = etree.XMLParser(remove_blank_text=True)
tree = etree.parse(in_file, parser)

# Get sorted XML root
sorted_root = sort (tree.getroot(), bSortEle, bSortAttr)

# Output
f = open(out_file, 'w')
f.write(etree.tostring(sorted_root, pretty_print=True))
f.close()

print "Sorted XML generated."

