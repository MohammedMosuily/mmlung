
import xlrd
from openpyxl.utils.cell import coordinate_to_tuple
import numpy as np
import pandas as pd
from glob import glob
from os.path import splitext, basename, exists
from sklearn.preprocessing import minmax_scale


def extract_file_paths(ground_truth_folder, tasks_folder, tasks_dict, selected_tasks):

    count = 0

    dataset_df = pd.DataFrame(columns=['Spirometry_file'] + [f'{task_name}_file' for task_name in selected_tasks] )

    skipped = 0

    for spiro_file in glob(f'{ground_truth_folder}/*.xls'):
        #Getting the file name to get the groundtruth. Eg. getting '1' from 'folder/1.wav'
        recording_index = (splitext(basename(spiro_file))[0]).split('_')[0]
        
        task_files = []

        for task_name in selected_tasks:
          task = tasks_dict[task_name]
          task_folder = task['folder']
          task_suffix = task['suffix']
          task_file = f'{tasks_folder}/{task_folder}/{recording_index}_{task_suffix}.wav'

          if not (exists(task_file)):
            skipped = skipped + 1
            task_file = None
          task_files.append(task_file)

        dataset_df.loc[len(dataset_df.index)] = [spiro_file] + task_files
        count = count + 1

    print(f'{count} spirometry readings found and {skipped} recordings missing')

    return dataset_df

def read_cells_from_excel(filepath = None, cell_coordinates = None):

    wb = xlrd.open_workbook(filename = filepath)
    sheet = wb.sheet_by_index(0)
    values = []
    for coordinates in cell_coordinates:
        x, y = coordinate_to_tuple(coordinates)
        values.append(np.float64(str(sheet.cell_value(rowx=x-1, colx=y-1)).replace('*','')))
    return tuple(values)

def get_target_columns(row, cell_coordinates):

    file_path = row['Spirometry_file']
    return read_cells_from_excel(file_path, cell_coordinates)


def get_normalized_channels(data):

  #Extracting channel data
  ch_data = np.empty(data.shape)
  ch_data[:,0] = np.copy(data[:,0])
  ch_data[:,1] = np.copy(data[:,1])

  
  #Normalizing channel data using min max normalization (Same formula in paper)
  ch_data[:,0] = minmax_scale(ch_data[:,0])
  ch_data[:,1] = minmax_scale(ch_data[:,1])

  return ch_data


def get_rms(foo):

  return np.sqrt(np.mean(foo**2))


def get_best_channel(ch_data):

  #Getting RMS value
  ch0_rms = get_rms(ch_data[:,0])
  ch1_rms = get_rms(ch_data[:,1])

  if (ch0_rms > ch1_rms):
    return ch0_rms, ch1_rms, 0
  else:
    return ch0_rms, ch1_rms, 1


def window(a, w = 4, o = 2, copy = False):

    sh = (a.size - w + 1, w)
    print(a.strides)
    st = a.strides * 2
    view = np.lib.stride_tricks.as_strided(a, strides = st, shape = sh)[0::o]
    if copy:
        return view.copy()
    else:
        return view


def extract_tasks_dict_from_folder(folder_path):
  '''
  Return a dictionary containing the task names and the recording prefixes from the folder containing all tasks
  '''
  tasks_dict = {}
  for task_folder in glob(f'{folder_path}/*'):
    foldername = basename(task_folder)
    suffix = basename(glob(f'{task_folder}/*.wav')[0]).split('_')[1].replace('.wav','')

    tasks_dict[foldername] = {
        'folder': foldername,
        'suffix': suffix
    }
    
  return tasks_dict