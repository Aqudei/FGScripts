import csv
import os
import re


class PostMacro(object):

    def __init__(self, *args, **kwargs):
        self.model_folder = kwargs['model_folder']
        self.parts_path = os.path.join(self.model_folder, 'KeyShot', 'Renders', self.__model_name(), '{}_Parts.csv'.format(self.__model_name()))
        self.features_path = os.path.join(self.model_folder, 'KeyShot', 'Renders', self.__model_name(), '{}_Features.csv'.format(self.__model_name()))
        #self.parts_path = './20-009_SpellRider_Parts.csv'
        #self.features_path = './20-009_SpellRider_Features.csv'

    def __model_name(self):
        selected_dir = self.model_folder
        rgx = re.compile(r'\d+\-\d+_[a-z]+',re.I)
        rslt = rgx.search(selected_dir)
        if not rslt:
            raise Exception('Invalid model folder name')
        
        return rslt.group(0).strip()

    def __get_indexes(self, iterable, item):
        indexs = []
        for idx, _item in enumerate(iterable):
            if item == _item:
                indexs.append(idx)
        return indexs

    def remove_prefix(self, name):
        rgx = re.compile(r'^\d+(.+)')
        rslt = rgx.search(name)
        if rslt:
            return rslt.group(1).strip()
        return name.strip()

    def __get_prefix(self, name):
        rgx = re.compile(r'^(\d+).+')
        rslt = rgx.search(name)
        if rslt:
            return rslt.group(1).strip()
        return ''

    def __get_eyegloss_prefix(self):
        with open(self.parts_path, mode='rt', newline='') as fp:
            reader = csv.reader(fp)
            for idx, row in enumerate(reader):
                if 'EyesGLOSS' in row[0]:
                    return self.__get_prefix(row[0])

    def __process_parts(self):
        buffer = []
        tab3_col = 0
        
        eyegloss_prefix = self.__get_eyegloss_prefix()

        with open(self.parts_path, mode='rt', newline='') as fp:
            reader = csv.reader(fp)
            for idx, row in enumerate(reader):
                print('Processing row {}'.format(row[0]))
                if idx == 0:
                    header = [cell.strip() for cell in row]

                if idx == 1:
                    try:
                        tab3_col = row.index('TAB3')
                    except Exception as e:
                        print("TAB 3 data not found.\nPossible already removed.")

                if idx > 1 and 'Background' != row[0].strip():

                    row[header.index('Tab3 Image')] = ''
                    row[header.index('Tab4 Image')] = ''

                    if self.remove_prefix(row[header.index('Model Part')]) == 'Eyes':
                        row[header.index('#ofTabs')] = 1
                        row[header.index('Tab2 Image')] = ''

                        eye_gloss_indexes = self.__get_indexes(header, 'Part Gloss Image')[0:2]
                        
                        for eye_gloss_indexe in eye_gloss_indexes:
                            if eyegloss_prefix:
                                row[eye_gloss_index] = '{}EyesGLOSS_Clay1.'.format(eyegloss_prefix)
                            else:
                                row[eye_gloss_index] = 'EyesGLOSS_Clay1.'

                    else:
                        row[header.index('#ofTabs')] = 2

                    indexes = self.__get_indexes(header, 'Part Base Image')
                    for part_base_idx in indexes:
                        try:
                            row[part_base_idx] = row[part_base_idx].replace(
                                '_Clay2.', '_Clay1.')
                        except:
                            pass

                if 'EyesPRINT' in self.remove_prefix(row[0].strip()) or 'EyesGLOSS' in self.remove_prefix(row[0].strip()):
                    continue

                if 'Background' == row[0].strip():
                    row[header.index('SortOrder')], row[header.index(
                        'TmenuOrder')] = row[header.index('TmenuOrder')], row[header.index('SortOrder')]

                buffer.append(row)

        with open(self.parts_path, mode='wt', newline='') as fp:
            writer = csv.writer(fp)
            for idx, row in enumerate(buffer):
                if idx == 0:
                    header_row = row
                    writer.writerow(header_row)
                elif idx == 1:
                    pad_length = len(header_row) - len(row)
                    row.extend(['' for i in range(pad_length)])
                    writer.writerow(row)
                else:
                    if row[0].strip() == 'Background':
                        writer.writerow(row)
                        continue

                    with_data = row[0:tab3_col]
                    print('with data length := {}'.format(len(with_data)))
                    pad_length = len(header) - len(with_data)
                    print('pad data length := {}'.format(pad_length))

                    with_data.extend(
                        ['' for i in range(pad_length)])

                    writer.writerow(with_data)

        print('Done processing Parts.csv.')

    def __write_buffer_to_csv(self, buffer, csvfile):
        with open(csvfile, mode='wt', newline='') as fp:
            writer = csv.writer(fp)
            for row in buffer:
                writer.writerow(row)

    def __process_features(self):
        buffer = []
        with open(self.features_path, mode='rt', newline='') as fp:
            reader = csv.reader(fp)

            for idx, row in enumerate(reader):
                if idx == 0:
                    header = [cell.strip() for cell in row]
                    buffer.append(row)
                    continue
                if self.remove_prefix(row[header.index('Model Part')].strip()) in ['EyesPRINT', 'EyesGLOSS']:
                    continue
                else:
                    buffer.append(row)

        self.__write_buffer_to_csv(buffer, self.features_path)
        print('Done processing Feautures.csv.')

    def start(self):
        print('Starting post macro script inside {}'.format(self.model_folder))
        self.__process_parts()
        self.__process_features()


if __name__ == "__main__":
    post_script = PostMacro(model_folder = 'C:\\Users\\Dell\\Downloads\\Compressed\\APP MODELS\\23-001_Castle')
    post_script.start()