import xml.dom.minidom
import xml.etree.ElementTree as ET
from xml.dom.minidom import Node


def strip_xml(node: Node) -> None:
    """Strip XML of excess whitespace.

    Source: https://stackoverflow.com/a/16919069
    """
    for x in node.childNodes:
        if x.nodeType == Node.TEXT_NODE:
            if x.nodeValue:
                x.nodeValue = x.nodeValue.strip()
        elif x.nodeType == Node.ELEMENT_NODE:
            strip_xml(x)


def make_pretty_xml(root: ET.Element) -> bytes:
    """Make XML pretty."""
    xml_doc = xml.dom.minidom.parseString(ET.tostring(root))

    strip_xml(xml_doc)
    xml_doc.normalize()

    return xml_doc.toprettyxml(indent=" ", newl="\n", encoding="utf-8")
