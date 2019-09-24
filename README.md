# control_script

Script to optimize data preparation for training ANN models

------------

### Whats new
+ Correction of errors when running a script without conversion and tuning scripts.
+ Added algorithm for removing unnecessary (excess) data from the dataset.
+ Replaced and removed some parameters.
+ Multi Platforming (path)
+ [TEST] Local training process.

------------

The script uses a special file *config.ini*. This file contains the script start-up parameters. This is necessary to simplify the launch of the script. *Config.ini* file is divided into sections. The first section is ‘‘Datasets’’. 
```ini
    [datasets]
    output_path = 
    local_path = 
    amount_of_datasets = N
```
The *output_path* parameter stores the path where the converted data will be saved. The *local_path* parameter is the path to the directory where the temporary script files will be stored. This parameter is needed if there are several datasets and a script that converts one dataset into another re-creates the directories, thereby deleting the files that were in the *output_path* folder. The converted dataset will be copied to the temporary folder, files that have the same name will be renamed. The *amount_of_datasets* parameter shows how many datasets need to be converted.

------------
The following N sections store parameters for specific datasets.
```ini
    [dataN]
    name = 
    path_to_dataset = 
    script_to_convert =
```
[dataN] are sections of [data1], [data2], ... [dataN], where N is the number of datasets (parameter *amount_of_datasets*).
Example: 
```ini
    [datasets]
    output_path = 
    local_path = 
    amount_of_datasets = 3
    
    [data1]
    name = 
    path_to_dataset = 
    script_to_convert =
    
    [data2]
    name = 
    path_to_dataset = 
    script_to_convert =
    
    [data3]
    name = 
    path_to_dataset = 
    script_to_convert =
```
Inside the *dataN* section there are three parameters: *name*, *path_to_datasets*, *script_to_convert*. The *name* parameter is needed in order to display a message on the console exactly which data is converted (this parameter is necessary for the convenience of reading logs). The *path_to_datasets* parameter stores the path to dataset. The *script_to_convert* contains the path to the script that converts datasets

------------
   **Note:** There may be changes!

------------
The next section is *image-transform*. This section contains options for image conversion.
```ini
    [image-transform]
    script_to_transform =   
    amount_of_parameters = K
    parameter1 = 
    parameter2 = 
    ...
    parameterK = 
```
The path to the script that converts the image is written to the *script_to_transform* parameter. The *amount_of_parameters* is the number of script start-up options. At the moment, the maximum number of launch parameters is 9 (0 < K ≤ 9). The *parameter1* contains the first launch parameter, the *parameter2* contains the second launch parameter, ... the *parameterK* contains the K-th launch parameter.
Example: 
```ini
    [image-transform]
    script_to_transform = script.py
    amount_of_parameters = 2
    parameter1 = -i Data/In
    parameter2 = -o Data/OUT
```
------------
The *tuning-transform* section contains parameters for running a script that will perform data augmentation.
**Tip:** It is better to specify a local folder in the *-o*/*--output* parameter.
```ini
    [tuning-transform]
    script_to_tuning =   
    amount_of_parameters = K
    parameter1 = 
    parameter2 = 
    ...
    parameterK = 
```
In the parameter *script_to_tuning* the script is specified that will make the data augmentation. The *amount_of_parameters* contains the number of script startup parameters. The parameters *parameter1*, *parameter2*, ... and *parameterK* are the launch parameters.

------------
The last section is *records*. This section contains the parameters for running the script that creates input files of the record type.
```ini
    [records]
    script_to_create_tf_records = 
    amount_of_parameters = K
    parameter1 = 
    parameter2 = 
    ...
    parameterK = 
```
The parameter *path_to_output* stores the path to the folder where to save the record type files. The *amount_of_parameters* contains the number of script startup parameters. The parameters *parameter1*, *parameter2*, ... and *parameterK* are the launch parameters.

------------
It is also possible to use links to parameters *output_path*, *local_path*. To do this, write the parameters in curly braces. 
For example:
```ini
    [datasets]
    output_path = Data/Out
    local_path = Local/Temp
    amount_of_datasets = 1
    
    ...
    
    [image-transform]
    script_to_transform = script.py
    amount_of_parameters = 2
    parameter1 = -i {output_path}
    parameter2 = -o {local_path}
```
The script will automatically replace the references to the path specified in the specified parameters.
