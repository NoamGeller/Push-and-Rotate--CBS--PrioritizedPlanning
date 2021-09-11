"""
Converts maps and benchmarks from the format of MovingAI's https://movingai.com/benchmarks/index.html
to the format of PathPlanning's https://github.com/PathPlanning/Push-and-Rotate--CBS--PrioritizedPlanning
"""
import os
import xml.etree.ElementTree as ET

HEIGHT_LINE = 1
WIDTH_LINE = 2
MAP_FIRST_LINE = 4


def main():
    for map_file_name in os.listdir('maps'):
        with open(os.path.join('maps', map_file_name)) as map_file:
            map_lines = map_file.readlines()
        _, height = map_lines[HEIGHT_LINE].split()
        _, width = map_lines[WIDTH_LINE].split()
        actual_map_lines = map_lines[MAP_FIRST_LINE:]
        map_name, _ = os.path.splitext(map_file_name)

        # benchmarks = os.listdir('scen-even') + os.listdir('scen-random')
        # for benchmark_file_name in benchmarks:

        create_map_xml(map_name, actual_map_lines, height, width)


def create_map_xml(map_name, map_lines, height, width):
    root = ET.Element('root')
    map_element = ET.SubElement(root, 'map')
    grid = ET.SubElement(map_element, 'grid')
    grid.set('height', height)
    grid.set('width', width)
    for line in map_lines:
        row_content = line.replace('.', '0 ').replace('@', '1 ').replace('T', '1 ').strip()
        row_element = ET.SubElement(grid, 'row')
        row_element.text = row_content
    ET.ElementTree(root).write(os.path.join('out', map_name + '.xml'), )


if __name__ == '__main__':
    main()

