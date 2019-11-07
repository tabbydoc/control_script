import sys
import os
import shutil


def transform(input_folder, output_folder, folder_ann, folder_img, display_mode):
    count_files = 0
    if display_mode == 2:
        print("\nParams:\n-" + sys.argv[1] + "\n-" + sys.argv[2] + "\n-" + sys.argv[3] + "\nLength=" + str(
            len(sys.argv)) + "\n")

    try:
        os.mkdir(output_folder + '\\annotations')
        os.mkdir(output_folder + '\\annotations\\xmls')
        os.mkdir(output_folder + '\\images')
    except OSError:
        print("Create directory %s failed. Maybe it already exists." % output_folder)
    else:
        if display_mode != 0:
            print("Directory successfully created %s" % output_folder)

    files = os.listdir(input_folder + '\\' + folder_ann)

    xml_folder = os.path.join(output_folder, "annotations\\xmls")
    trainval_path = os.path.join(output_folder, "annotations")
    img_folder = os.path.join(output_folder, "images")

    f = open(trainval_path + '\\' + 'trainval.txt', 'w')

    for xml_file in files:
        if xml_file.endswith('.xml'):
            count_files += 1
            ann_path_in = os.path.join(input_folder, folder_ann + '\\' + xml_file)
            if display_mode == 2:
                print("Xml file - " + ann_path_in)
            ann_path_out = os.path.join(xml_folder, xml_file)
            if display_mode == 2:
                print("Xml file copied - " + ann_path_out)
            file_name = xml_file[:-4]
            if display_mode == 2:
                print("File name - " + str(file_name))
            f.write(str(file_name) + '\n')

            img_path_in = os.path.join(input_folder, folder_img + '\\' + file_name + '.jpeg')
            if display_mode == 2:
                print("Jpeg file - " + img_path_in)
            img_path_out = os.path.join(img_folder, file_name + '.jpeg')
            if display_mode == 2:
                print("Jpeg file copied - " + img_path_out)
            shutil.copyfile(ann_path_in, ann_path_out)
            shutil.copyfile(img_path_in, img_path_out)
            if display_mode == 2 or display_mode == 1:
                print("%s file (xml and jpeg) copied!" % file_name)

            if display_mode == 2:
                print("==================")

    print("Copying completed! \n Number of files:" + str(count_files))
    f.close()
