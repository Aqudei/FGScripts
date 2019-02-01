import subprocess
import os
import tempfile
import re
import csv

KEYSHOT_EXECUTABLE = 'C:/Program Files/KeyShot7/bin/keyshot.exe'

KEYSHOT_MATERIALS_FOLDER = 'C:/Users/Administrator/Documents/KeyShot 7/Materials'

INPUT_APP_MODELS_FOLDER = 'C:/Users/Dell/Downloads/Compressed/MACRO AUTOMATION JOB Files/Sample Files/APP MODELS/'

# CONFIG_CSV = os.path.join(INPUT_APP_MODELS_FOLDER, 'Real3d_V1.csv')

MODEL_NAME_PATTERN = re.compile(r'^\d+\-\d+_[a-z0-9]+', re.I)

# def read_config():
#     if not os.path.exists(CONFIG_CSV):
#         print('Real3d_V1.csv was not found')
#         raise FileNotFoundError()

#     with open(CONFIG_CSV, 'rt', newline='') as fp:
#         reader = csv.DictReader(fp)
#         return {row['model']: row for row in reader}


# def read_mtl(file):
#     with open(file, 'rt') as f:
#         return f.read()


# def replace_value(mtl, key, value):
#     rgx = re.compile(r'\"{}\" .+'.format(key))
#     match = rgx.search(mtl)
#     return mtl.replace(match.group(0), '\"{}\" \"{}\",'.format(key, value))


# def change_name(mtl, newname):
#     return mtl.replace("Flat Black", newname)


# def get_model_folders():
#     for file in os.listdir(INPUT_APP_MODELS_FOLDER):
#         modelname = model_name_pattern.search(file)
#         if modelname:
#             yield (modelname.group(0), os.path.join(INPUT_APP_MODELS_FOLDER, file))


# def ensure_directory(folder):
#     try:
#         os.makedirs(folder)
#     except:
#         pass


# def check_settings():
#     good = os.path.exists(KEYSHOT_EXECUTABLE) and os.path.exists(
#         KEYSHOT_MATERIALS_FOLDER) and os.path.exists(INPUT_APP_MODELS_FOLDER) and os.path.exists(
#             FLAT_BLACK_LOCATION) and os.path.exists(CONFIG_CSV)
#     if not good:
#         print('Please check your settings variable.\n Some files/folders were not found.')
#         raise FileNotFoundError()


# def main():

#     check_settings()

#     config = read_config()

#     print('Running with the following setting:\n{} := {}\n{} := {}\n{} := {}\n'.format(
#         'KEYSHOT_EXECUTABLE', KEYSHOT_EXECUTABLE, 'KEYSHOT_MATERIALS_FOLDER', KEYSHOT_MATERIALS_FOLDER, 'INPUT_APP_MODELS_FOLDER', INPUT_APP_MODELS_FOLDER))

#     if not os.path.exists(FLAT_BLACK_LOCATION):
#         print('"Flat Black.mtl" was not found.\nPlease put it inside the same folder with this script')
#         raise FileNotFoundError()

#     print('Reading "Flat Black.mtl"')
#     flat_black_template = read_mtl(FLAT_BLACK_LOCATION)

#     for modelname, model_folder in get_model_folders():

#         isReady = 0

#         try:
#             isReady = int(config[modelname]['isReady'])
#         except:
#             isReady = 0

#         if isReady == 0:
#             print('Skipping model: {}'.format(modelname))
#             continue

#         print('Processing model folder: {}'.format(model_folder))

#         input_masks_folder = os.path.join(model_folder, 'Masks')
#         temp_masks_folder = os.path.join(
#             tempfile.gettempdir(), 'Figuromo', modelname, 'Masks')
#         ensure_directory(temp_masks_folder)

#         for file in os.listdir(input_masks_folder):
#             print('Generating texture for mask {}'.format(file))
#             mask_file = os.path.join(input_masks_folder, file)
#             mask_mat = replace_value(flat_black_template, 'texture', mask_file)

#             fname, ext = os.path.splitext(file)

#             output_mask_material_name = os.path.join(
#                 temp_masks_folder, modelname + '~' + fname + '.mtl')

#             mask_mat = change_name(mask_mat, modelname + '~' + fname)

#             # with open(output_mask_mat, 'wt') as f:
#             #     f.write(mask_mat)

#             with open(os.path.join(KEYSHOT_MATERIALS_FOLDER, os.path.basename(output_mask_material_name)), 'wt') as f:
#                 f.write(mask_mat)

#     print('Opening Keyshot...')
#     pid = subprocess.Popen([KEYSHOT_EXECUTABLE, ]).pid
#     print('Done.')


class MatGenerator(object):

    def __init__(self, *args, **kwargs):
        self.root = kwargs.get('root', INPUT_APP_MODELS_FOLDER)
        self.parent = kwargs.get('parent')
        self.csv_config_location = os.path.join(self.root, 'Real3d_V1.csv')
        # self.mask_location = os.path.join(self.root,'Real3d_V1.csv')

        head, tail = os.path.split(__file__)
        self.flat_black = os.path.join(head, 'Flat Black.mtl')

    def __read_config(self):
        if not os.path.exists(self.csv_config_location):
            print('Real3d_V1.csv was not found')
            raise FileNotFoundError()

        with open(self.csv_config_location, 'rt', newline='') as fp:
            reader = csv.DictReader(fp)
            return {row['model']: row for row in reader}

    def __read_mtl(self, file):
        with open(file, 'rt') as f:
            return f.read()

    def __mtl_replace_value(self, mtl, key, value):
        rgx = re.compile(r'\"{}\" .+'.format(key))
        match = rgx.search(mtl)
        return mtl.replace(match.group(0), '\"{}\" \"{}\",'.format(key, value))

    def __mtl_change_name(self, mtl, newname):
        return mtl.replace("Flat Black", newname)

    def __get_model_folders(self):
        for file in os.listdir(self.root):
            modelname = MODEL_NAME_PATTERN.search(file)
            if modelname:
                yield (modelname.group(0), os.path.join(self.root, file))

    def __ensure_directory_exists(self, folder):
        try:
            os.makedirs(folder)
        except:
            pass

    def __check_settings(self):
        if not os.path.exists(KEYSHOT_EXECUTABLE):
            print('KeyShot exeutable not found: {}'.format(KEYSHOT_EXECUTABLE))
            raise FileNotFoundError(KEYSHOT_EXECUTABLE)

        if not os.path.exists(KEYSHOT_MATERIALS_FOLDER):
            print('KeyShot materials folder not found: {}'.format(
                KEYSHOT_MATERIALS_FOLDER))
            raise FileNotFoundError(KEYSHOT_MATERIALS_FOLDER)

        if not os.path.exists(self.flat_black):
            print('"Flat Black.mtl" was not found. Expected location: {}'.format(
                self.flat_black))
            raise FileNotFoundError(self.flat_black)

        if not os.path.exists(self.csv_config_location):
            print('Csv Read3d_V1.csv file was not found: {}'.format(
                os.path.abspath(self.csv_config_location)))
            raise FileNotFoundError(self.csv_config_location)

    def __say(self, message, color = 'green'):
        print(message)

        if self.parent:
            self.parent.set_script2_message(message, color)

    def start(self):
        self.__check_settings()

        config = self.__read_config()

        print('Running with the following setting:\n{} := {}\n{} := {}\n{} := {}\n'.format(
            'KEYSHOT_EXECUTABLE', KEYSHOT_EXECUTABLE, 'KEYSHOT_MATERIALS_FOLDER', KEYSHOT_MATERIALS_FOLDER, 'APP_MODELS_FOLDER', self.root))

        self.__say('Reading "Flat Black.mtl"')
        flat_black_template = self.__read_mtl(self.flat_black)

        for modelname, model_folder in self.__get_model_folders():
            try:
                isReady = 0

                try:
                    isReady = int(config[modelname]['isReady'])
                except:
                    isReady = 0

                if isReady == 0:
                    self.__say('Skipping model: {}'.format(modelname))
                    continue

                self.__say('Processing model folder: {}'.format(model_folder))

                input_masks_folder = os.path.join(model_folder, 'Masks')
                temp_masks_folder = os.path.join(
                    tempfile.gettempdir(), 'Figuromo', modelname, 'Masks')
                self.__ensure_directory_exists(temp_masks_folder)

                for file in os.listdir(input_masks_folder):
                    self.__say('Generating texture for mask {}'.format(file))
                    mask_file = os.path.join(input_masks_folder, file)
                    mask_mat = self.__mtl_replace_value(
                        flat_black_template, 'texture', mask_file)

                    fname, ext = os.path.splitext(file)

                    output_mask_material_name = os.path.join(
                        temp_masks_folder, modelname + '~' + fname + '.mtl')

                    mask_mat = self.__mtl_change_name(
                        mask_mat, modelname + '~' + fname)

                    # with open(output_mask_mat, 'wt') as f:
                    #     f.write(mask_mat)

                    with open(os.path.join(KEYSHOT_MATERIALS_FOLDER, os.path.basename(output_mask_material_name)), 'wt') as f:
                        f.write(mask_mat)

            except Exception as e:
                self.__say('Something went wrong while processing {}.\Moving on to next model'.format(
                    modelname),color='red')

                print(e)

        self.__say('Opening Keyshot...')
        pid = subprocess.Popen([KEYSHOT_EXECUTABLE, ]).pid
        self.__say('Generate Mat/texture for keyshot done.')


if __name__ == "__main__":
    mat_gen = MatGenerator()
    mat_gen.start()
