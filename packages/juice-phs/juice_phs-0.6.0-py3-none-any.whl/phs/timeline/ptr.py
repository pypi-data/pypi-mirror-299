import xml.etree.ElementTree as ET
import csv

def insert_target_comment(input_ptr_path,
                          output_ptr_path=False,
                          target='JUPITER',
                          verbose=True):

    if not output_ptr_path:
        output_ptr_path = input_ptr_path + '.output'

    # Read the XML content from the file
    with open(input_ptr_path, 'r') as file:
        xml_input = file.read()

    root = ET.fromstring(xml_input)

    # Iterate through all 'block' elements and check for the target
    for block in root.iter('block'):
        attitude = block.find('attitude')
        if attitude is not None:
            metadata = block.find('metadata')
            if metadata is not None:
                comment_element = ET.Element('comment')
                comment_element.text = f'TARGET={target}'
                metadata.append(comment_element)

    # Convert the modified XML back to string
    modified_xml = ET.tostring(root, encoding='unicode')
    # Write the modified XML to a new file
    with open(output_ptr_path, 'w') as file:
        file.write(modified_xml)

    if verbose:
        print(modified_xml)

    return modified_xml


def set_obs_id(input_ptr_path,
               output_ptr_path=False,
               verbose=False):
    obs_id = 0

    if not output_ptr_path:
        output_ptr_path = input_ptr_path + '.output'

    # Read the XML content from the file
    with open(input_ptr_path, 'r') as file:
        xml_input = file.read()

    root = ET.fromstring(xml_input)

    # Iterate through all 'block' elements and check for the target
    for block in root.iter('block'):
        if block.attrib.get('ref') == 'OBS':
            obs_id += 1
            metadata = block.find('metadata')
            if metadata is not None:
                obs_id_present = False
                # Iterate through existing comments to find and update OBS_ID
                for comment in metadata.findall(".//comment"):
                    if 'OBS_ID' in comment.text:
                        comment.text = f' OBS_ID={obs_id:03d} '
                        obs_id_present = True

                # If OBS_ID comment element is not present, add it
                if not obs_id_present:
                    comment_element = ET.Element('comment')
                    comment_element.text = f' OBS_ID={obs_id:03d} '
                    metadata.append(comment_element)

    #  <comment> Track Power Optimised Jupiter </comment>
    #  <comment> PRIME=UVS </comment>
    #  <comment> OBS_ID=002 </comment>
    #  <comment> OBS_NAME=UVS_JUP_AP_SCAN_MAP </comment>
    #  <comment> TARGET=JUPITER </comment>

    # Convert the modified XML back to string
    modified_xml = ET.tostring(root, encoding='unicode')
    # Write the modified XML to a new file
    with open(output_ptr_path, 'w') as file:
        file.write(modified_xml)

    if verbose:
        print(modified_xml)

    return modified_xml


def check_obs_metadata(xml_file, output_ptr_path=False):
    # Read the XML content from the file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    if not output_ptr_path:
        output_ptr_path = xml_file + '.output'

    # List to store missing fields for each OBS
    missing_fields_report = []

    for block in root.iter('block'):
        if block.attrib.get('ref') == 'OBS':
            attitude = block.find('attitude')
            start_time =  block.find('startTime')
            end_time = block.find('endTime')
            try:
                start_time = start_time.text.strip()
            except:
                start_time = ''
            try:
                end_time = end_time.text.strip()
            except:
                end_time = ''
            if attitude is not None:
                metadata = block.find('metadata')
                if metadata is not None:
                    obs_info = {'OBS_NAME': '', 'OBS_ID': '',
                                'BLOCK_START': start_time, 'BLOCK_END': end_time}
                    obs_id_found = False

                    # Check for required fields and add if missing
                    for comment in metadata.iter('comment'):
                        for field in ['PRIME', 'OBS_NAME', 'TARGET', 'OBS_ID']:
                            if field in comment.text:
                                value = comment.text.split('=')[1].strip()
                                obs_info[field] = value

                    for field in ['PRIME', 'OBS_NAME', 'TARGET', 'OBS_ID']:
                        if field not in obs_info:
                            obs_info[field] = 'MISSING'
                            # Add the missing field with a placeholder value
                            comment_element = ET.Element('comment')
                            comment_element.text = f' {field}=PLACEHOLDER '
                            metadata.append(comment_element)

                            # Add the OBS information to the report
                            missing_fields_report.append(obs_info)
                if not obs_info['OBS_NAME']: obs_info['OBS_NAME'] = '???'
                if not obs_info['OBS_ID']: obs_info['OBS_ID'] = '???'

    # Convert the modified XML back to string
    modified_xml = ET.tostring(root, encoding='unicode')

    print("\nMissing Fields Report:")
    for obs_info in missing_fields_report:
        print(f"OBS_NAME: {obs_info['OBS_NAME']}, OBS_ID: {obs_info['OBS_ID']}")
        print(f"BLOCK_START: {obs_info['BLOCK_START']}, BLOCK_END: {obs_info['BLOCK_END']}")
        for field, status in obs_info.items():
            if status == 'MISSING':
                print(f"  - {field} is missing")
        print()

    # Write the modified XML to a new file
    with open(output_ptr_path, 'w') as file:
        file.write(modified_xml)

    return modified_xml

def export_ptr(xml_file, output_ptr_path=False):
    # Read the XML content from the file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    #output_ptr_path = 'output.csv'  # Desired output CSV file name


    if not output_ptr_path:
        output_ptr_path = xml_file + '.output'


    #for observations in root.iter('observations'):
    #    designer = observations.attrib.get('designer')

    # Open CSV file for writing
    with open(output_ptr_path, mode='w', newline='') as file:
        writer = csv.writer(file)

        # Extracting information
        for block in root.findall('.//block'):
            start_time = block.find('startTime').text.strip()
            end_time = block.find('endTime').text.strip()
            #print(f"Block Reference: {block.get('ref')}")
            #print(f"Start Time: {start_time}")
            #print(f"End Time: {end_time}")

            attitude = block.find('attitude')
            if attitude is not None:
                #print(f"Attitude Reference: {attitude.get('ref')}")
                phase_angle = attitude.find('phaseAngle')
                if phase_angle is not None:
                    y_dir = phase_angle.find('yDir').text.strip()
                    angle = phase_angle.find('angle').text.strip()
                    #print(f"Phase Angle - yDir: {y_dir}, Angle: {angle} degrees")

            # Extract metadata observations
            for observation in block.findall('.//observation'):
                obs_type = observation.find('type').text.strip()
                obs_type_upper = obs_type.upper()
                definition = observation.find('definition').text.strip()
                unit = observation.find('unit').text.strip()
                target = observation.find('target').text.strip()
                start_time_obs = observation.find('startTime').text.strip() + 'Z'
                end_time_obs = observation.find('endTime').text.strip() + 'Z'
                obs_type_output = unit + '_' + obs_type_upper + '_OBSERVATION'

                #print(f"{obs_type_output}, {start_time_obs}, {end_time_obs}, {definition}, {unit}")

                writer.writerow([
                    obs_type_output,
                    start_time_obs,
                    end_time_obs,
                    definition,
                    unit
                ])

