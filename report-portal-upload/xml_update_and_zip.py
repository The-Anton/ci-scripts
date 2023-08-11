import xml.etree.ElementTree as ET
import os
import zipfile
import sys


def update_xml_file(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    testsuites = root.findall('testsuite')
    if 'file' in testsuites[0].attrib and testsuites[0].attrib['failures'] != "0":
        return
    elif 'file' in testsuites[0].attrib:
        root.remove(testsuites[0])


    for testsuite in testsuites:
        if len(list(testsuite)) == 0:
            root.remove(testsuite)


    parent_testsuite = testsuites[1]
    for testsuite in testsuites[2:]:
        parent_testsuite.append(testsuite)
        root.remove(testsuite)

    tree.write(xml_file, encoding='utf-8', xml_declaration=True)


def create_zip_file(directory):
    # Get all the xml files starting with "junit"
    xml_files = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.startswith('junit')]

    # Process each XML file
    for xml_file in xml_files:
        update_xml_file(xml_file)

    # Create a zip file and add the updated XML files
    zip_file = os.path.join(directory, 'periodic-job.zip')
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        for modified_file in xml_files:
            zipf.write(modified_file, os.path.basename(modified_file))

    return zip_file


# Directory path containing junit xml files
directory = sys.argv[1]

zip_file = create_zip_file(directory)
print(zip_file)