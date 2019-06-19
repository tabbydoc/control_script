import os
import shutil
import subprocess
import xml.etree.ElementTree as ET
import copy
import configparser
from termcolor import colored
from sys import argv

_debug = 0
_copy_suffix = 1

try:
    param1 = argv[1]
    if param1 == "-d":
        _debug = 1
except IndexError:
    print('-r')


def create_config(path_config):
    """
    Create a config file
    """
    config = configparser.ConfigParser()
    config.add_section("datasets")
    config.set("datasets", "output_path", "")
    config.set("datasets", "local_path", "")
    config.set("datasets", "amount_of_reserve", "1")

    config.add_section("data1")
    config.set("data1", "name", "")
    config.set("data1", "path_to_dataset", "")
    config.set("data1", "script_to_convert", "")

    config.add_section("image-transform")
    config.set("image-transform", "script_to_transform", "")

    config.add_section("tuning-image")
    config.set("tuning-image", "script_to_tuning", "")

    config.add_section("records")
    config.set("records", "script_to_create_tf_records", "")
    config.set("records", "path_to_output", "")
    config.set("records", "path_to_label_map", "")

    with open(path_config, "w") as config_file:
        config.write(config_file)
        print(colored(" File " + path_config + " was created!", "blue"))


def error_message(error_type, text, text2, text3):
    if error_type == 0:
        print(colored('ERROR! File ' + text + ' not found!', 'red', attrs=['reverse', 'bold']))
    elif error_type == 3:
        print(colored('ERROR! Process ' + text + ' finished with exit code ' + str(text2), 'red',
                      attrs=['reverse', 'bold']))
        raise SystemExit(3)
    elif error_type == 2:
        print(colored('ERROR! Folder ' + text + ' not found!', 'red', attrs=['reverse', 'bold']))
        print(colored(
            "Proposal: Enter the correct path ('" + text2 + "') in the [" + text3 + "] section of the config.ini file.",
            'yellow'))
        raise SystemExit(2)
    elif error_type == 1:
        print(colored('ERROR! Script ' + text + ' not found!', 'red', attrs=['reverse', 'bold']))
        print(colored(
            "Proposal: Enter the correct path ('" + text2 + "') in the [" + text3 + "] section of the config.ini file.",
            'yellow'))
        raise SystemExit(1)


def move_files(in_path):
    files = os.listdir(in_path + '/annotations/xmls')
    for xml_file in files:
        if xml_file.endswith('.xml'):
            ann_path_in = os.path.join(in_path + '/annotations/xmls/', xml_file)
            if _debug == 1:
                print(colored("-File xml input - " + ann_path_in, 'green'))
            ann_path_out = os.path.join(xmls_path, xml_file)
            if _debug == 1:
                print(colored("-File xml output - " + ann_path_out, 'green'))
            file_name = xml_file[:-4]
            if os.path.exists(ann_path_out):
                if _debug == 1:
                    print(colored("-File exist! Run copy proc", 'green'))
                global _copy_suffix
                new_filename = file_name + '_' + str(_copy_suffix)
                ann_path_out = os.path.join(xmls_path, new_filename + '.xml')
                if _debug == 1:
                    print(colored("-New xml path - " + ann_path_out, 'green'))
                shutil.copyfile(ann_path_in, ann_path_out)

                xml_tree = ET.parse(ann_path_out)
                new_xml_tree = copy.deepcopy(xml_tree)
                filename_img = new_xml_tree.find('filename')
                filename_img.text = new_filename + '.jpeg'
                new_xml_tree.write(ann_path_out)

                img_path_in = os.path.join(in_path + '/images/', file_name + '.jpeg')
                img_path_out = os.path.join(images_path, new_filename + '.jpeg')
                shutil.copyfile(img_path_in, img_path_out)
                _copy_suffix += 1

            else:
                img_path_in = os.path.join(in_path + '/images/', file_name + '.jpeg')
                img_path_out = os.path.join(images_path, file_name + '.jpeg')
                shutil.copyfile(ann_path_in, ann_path_out)
                shutil.copyfile(img_path_in, img_path_out)


if __name__ == "__main__":
    print(colored('\n Starting the script', 'blue', attrs=['bold']) + '\n')
    path = "config.ini"
    if not os.path.exists(path):
        error_message(0, path, '', '')  # ERROR
        create_config(path)
    else:
        config = configparser.ConfigParser()
        config.read(path)
        print(colored(' - datasets -', 'blue'))
        output_dir = config.get("datasets", 'output_path')
        if not os.path.exists(output_dir):
            error_message(2, output_dir, 'output_path', "datasets")  # ERROR
        local_dir = config.get("datasets", 'local_path')
        if not os.path.exists(local_dir):
            error_message(2, local_dir, 'local_path', "datasets")  # ERROR

        annotations_path = os.path.join(local_dir, "annotations")
        xmls_path = os.path.join(annotations_path, "xmls")
        images_path = os.path.join(local_dir, "images")

        if os.path.exists(annotations_path):
            shutil.rmtree(annotations_path)
        if os.path.exists(images_path):
            shutil.rmtree(images_path)
        if os.path.exists(xmls_path):
            shutil.rmtree(xmls_path)

        os.makedirs(images_path)
        os.makedirs(annotations_path)
        os.makedirs(xmls_path)

        for i in range(int(config.get("datasets", 'amount_of_reserve'))):
            print(colored("= " + config.get('data' + str(i + 1), 'name') + " =", 'blue'))
            script = config.get('data' + str(i + 1), 'script_to_convert')
            data_dir = config.get('data' + str(i + 1), 'path_to_dataset')
            if os.path.exists(script) or script == "":
                if script != "":
                    print(colored('Running script', 'blue'), colored(script, 'blue', attrs=['underline']) + '\n',
                          colored('-i ' + data_dir + ' -o ' + output_dir, 'blue') + '\n')
                    code = subprocess.call(['python', script, '-i' + data_dir, '-o' + output_dir])
                    if code != 0:
                        error_message(3, script, code, '')
                else:
                    print(colored(' -Skip-', 'yellow') + '\n')
            else:
                error_message(1, script, 'script_to_convert', 'data' + str(i + 1))  # ERROR
            move_files(output_dir)

        shutil.rmtree(output_dir + '/annotations')
        shutil.rmtree(output_dir + '/images')
        print(colored(' - Some data conversions -', 'blue'))
        subprocess.call(['python', 'transform_data_dir.py', local_dir, output_dir, 'annotations/xmls', 'images', '0'])

        print(colored(" - Image Transform - ", 'blue'))
        script = config.get('image-transform', 'script_to_transform')
        data_dir = config.get("datasets", 'output_path')
        if os.path.exists(script) or script == "":
            if script != "":
                print(colored('Running script', 'blue'), colored(script, 'blue', attrs=['underline']) + '\n',
                      colored('-i ' + data_dir + ' -o ' + output_dir, 'blue') + '\n')
                code = subprocess.call(['python', script, '-i' + data_dir, '-o' + output_dir])
                if code != 0:
                    error_message(3, script, code, '')
            else:
                print(colored(' -Skip-', 'yellow') + '\n')
        else:
            error_message(1, script, 'script_to_transform', 'image-transform')  # ERROR

        print(colored(" - Tuning Image - ", 'blue'))
        script = config.get('tuning-image', 'script_to_tuning')
        data_dir = config.get("datasets", 'output_path')
        if os.path.exists(script) or script == "":
            if script != "":
                print(colored('Running script', 'blue'), colored(script, 'blue', attrs=['underline']) + '\n',
                      colored('-i ' + data_dir + ' -o ' + output_dir, 'blue') + '\n')
                code = subprocess.call(['python', script, '--data_dir=' + data_dir, '--output_dir=' + local_dir])
                if code != 0:
                    error_message(3, script, code, '')
            else:
                print(colored(' -Skip-', 'yellow') + '\n')
        else:
            error_message(1, script, 'script_to_tuning', 'tuning-image')  # ERROR
                
        if os.path.exists(os.path.join(output_dir, 'images')):
            shutil.rmtree(os.path.join(output_dir, 'images'))
        if os.path.exists(os.path.join(output_dir, 'annotations')):
            shutil.rmtree(os.path.join(output_dir, 'annotations'))

        print(colored(' - Some data conversions -', 'blue'))
        subprocess.call(['python', 'transform_data_dir.py', local_dir, output_dir, 'annotations/xmls', 'images', '0'])

        print(colored(" - Create tfRecords - ", 'blue'))
        script = config.get('records', 'script_to_create_tf_records')
        data_dir = config.get("datasets", 'output_path')
        output_path = config.get("records", 'path_to_output')
        label_map_path = config.get("records", 'path_to_label_map')
        if os.path.exists(script) or script == "":
            if script != "":
                print(colored('Running script', 'blue'), colored(script, 'blue', attrs=['underline']) + '\n',
                      colored('-i ' + data_dir + ' -o ' + output_dir, 'blue') + '\n')
                code = subprocess.call(['python', script, '--data_dir=' + data_dir, '--output_dir=' + output_path,
                                        '--label_map_path=' + label_map_path])
                if code != 0:
                    error_message(3, script, code, '')
            else:
                print(colored(' -Skip-', 'yellow') + '\n')
        else:
            error_message(1, script, 'script_to_create_tf_records', 'records')  # ERROR

        if os.path.exists(os.path.join(local_dir, 'images')):
            shutil.rmtree(os.path.join(local_dir, 'images'))
        if os.path.exists(os.path.join(local_dir, 'annotations')):
            shutil.rmtree(os.path.join(local_dir, 'annotations'))

        print(colored('\n Script finished', 'blue', attrs=['bold']))
        print(colored("File's train.record, val.record were created", 'blue', attrs=['bold']))
