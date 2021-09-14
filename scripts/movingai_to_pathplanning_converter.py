"""
Converts maps and benchmarks from the format of MovingAI's https://movingai.com/benchmarks/index.html
to the format of PathPlanning's https://github.com/PathPlanning/Push-and-Rotate--CBS--PrioritizedPlanning
"""
import os
import xml.etree.ElementTree as ET
from collections import defaultdict
from typing import List

SHOULD_GENERATE_AGENTS_FILES = True
AGENT_ATTRIBUTES = ['id', 'start_j', 'start_i', 'goal_j', 'goal_i']

HEIGHT_LINE = 1
WIDTH_LINE = 2
MAP_FIRST_LINE = 4

SHOULD_PARALLELIZE_PATHS = [False, False]
algorithm_fields = {
    'planner': 'push_and_rotate',
    'low_level': 'astar',
    'parallelize_paths_1': str(SHOULD_PARALLELIZE_PATHS[0]).lower(),
    'parallelize_paths_2': str(SHOULD_PARALLELIZE_PATHS[1]).lower()
}

RUNNING_TIME_IN_MS = 1000
SHOULD_AGGREGATE_RESULTS = False
options_fields = {
    'maxtime': str(RUNNING_TIME_IN_MS),
    'aggregated_results': str(SHOULD_AGGREGATE_RESULTS).lower()
}


def append_options_section(root, map_scenes: List[str], scene_type):
    scene_prefix = map_scenes[0].rsplit('-', 1)[0]
    agents_file_prefix = os.path.join(scene_type, scene_prefix)
    tasks_count = len(map_scenes)
    max_agents = get_max_agents(agents_file_prefix, tasks_count)

    options = ET.SubElement(root, 'options')
    options_fields.update({'agents_file': os.path.join('out', agents_file_prefix), 'tasks_count': str(tasks_count)})
    for tag, text in options_fields.items():
        element = ET.SubElement(options, tag)
        element.text = text
    agents_range = ET.SubElement(options, 'agents_range')
    agents_range.set('min', '1')
    agents_range.set('max', str(max_agents))


def append_algorithm_section(root):
    algorithm = ET.SubElement(root, 'algorithm')
    for tag, text in algorithm_fields.items():
        element = ET.SubElement(algorithm, tag)
        element.text = text
    return algorithm


def main():
    scenes_by_type = get_scenes()
    for scene_type, scenes in scenes_by_type.items():
        for map_name, map_scenes in scenes.items():
            map_path = os.path.join('maps', map_name + '.map')
            if not os.path.exists(map_path):
                print(f"skipping {map_name}, couldn't find map file")
                continue
            print(f'generating map xml: {map_name}')
            generate_map_xml(map_name, map_path, map_scenes, scene_type)
            generate_agents_xmls(map_scenes, scene_type)


def generate_agents_xmls(map_scenes, scene_type):
    for scene in map_scenes:
        print(f'generating agents xml: {scene}')
        agent_xml_root = ET.Element('root')
        with open(os.path.join(scene_type, scene)) as scene_file:
            for agent_id, agent_line in enumerate(scene_file, -1):
                if agent_id < 0:
                    continue
                agent_coordinates = [coord for coord in agent_line.split()[4:-1]]
                attributes_values = [agent_id] + agent_coordinates
                agent_element = ET.SubElement(agent_xml_root, 'agent')
                for attribute, value in zip(AGENT_ATTRIBUTES, attributes_values):
                    agent_element.set(attribute, str(value))
                    xml_path = os.path.join('out', scene_type, f'{os.path.splitext(scene)[0]}.xml')
                    ET.ElementTree(agent_xml_root).write(xml_path)


def generate_map_xml(map_name, map_path, map_scenes, scene_type):
    map_xml_root = ET.Element('root')
    append_map_section(map_xml_root, map_path)
    append_algorithm_section(map_xml_root)
    append_options_section(map_xml_root, map_scenes, scene_type)
    ET.ElementTree(map_xml_root).write(os.path.join('out', f'{map_name}.{scene_type}.xml'))


def get_max_agents(agents_file_prefix, tasks_count):
    agents_counts = []
    for i in range(1, tasks_count + 1):
        with open(f'{agents_file_prefix}-{i}.scen') as agents_file:
            line_count_with_header = sum(1 for _ in agents_file)
            agents_counts.append(line_count_with_header - 1)
    max_agents = max(agents_counts)
    if max_agents != min(agents_counts):
        print(f'different agent count in {agents_file_prefix}')
    return max_agents


def get_scenes():
    scenes = {}
    for scene_type in ['scen-random', 'scen-even']:
        scenes[scene_type] = defaultdict(list)
        for random_file_name in os.listdir(scene_type):
            map_name = random_file_name.rsplit('-', 2)[0]
            scenes[scene_type][map_name].append(random_file_name)
    return scenes


def append_map_section(root, map_path):
    with open(map_path) as map_file:
        map_lines = map_file.readlines()
    _, height = map_lines[HEIGHT_LINE].split()
    _, width = map_lines[WIDTH_LINE].split()
    actual_map_lines = map_lines[MAP_FIRST_LINE:]

    map_element = ET.SubElement(root, 'map')
    grid = ET.SubElement(map_element, 'grid')
    grid.set('height', height)
    grid.set('width', width)
    for line in actual_map_lines:
        row_content = line.replace('.', '0 ').replace('@', '1 ').replace('T', '1 ').strip()
        row_element = ET.SubElement(grid, 'row')
        row_element.text = row_content
    return map_element


if __name__ == '__main__':
    main()
