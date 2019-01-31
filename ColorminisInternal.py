# AUTHOR Francis
# VERSION 1.24.512
# Render stuff for figuromo models

import lux
import os
import re
import time

TEST_RUNNING = True

FPS = 31

WIDTH = 817
HEIGHT = 900

# Regex pattern to match folder names of Models, ex. 22-001_Witch
model_id_regex = re.compile(r'^\d\d\-\d\d\d_.+')
rgx = re.compile(r'^\d+(.+)')

# lux.setEnvironmentImage('E:\\dev\\upwork\\forkeyshot\\Sample Files\\APP MODELS\\KeyShot_Lightscape1.hdz')


def read_config(models_folder):

    csv_location = os.path.join(models_folder, 'Real3d_V1.csv')
    print('Reading config file: {} '.format('Real3d_V1.csv'))

    if not os.path.exists(csv_location):
        print("Real3d_V1.csv was not found")
        raise FileNotFoundError()

    with open(csv_location, 'rt') as fp:
        row = 0
        isReady = 0
        model_names = []
        areReady = []

        lines = list(fp.readlines())

        headers = [c.strip() for c in lines[0].split(',')]
        try:
            isReady = headers.index('isReady')
        except Exception as e:
            print("'isReady' field was not found in the csv file")
            isReady = 0
            raise e

        for line in lines[1:]:
            split_line = line.split(',')
            model_names.append(split_line[0].strip())
            areReady.append((split_line[isReady]).replace(
                '\r', '').replace('\n', '').strip())

        if len(model_names) != len(areReady):
            raise Exception(
                "Sorry, i cannot properly parse the data on 'Real3d_V1.csv'.\nPlease check values.")

        return {k: v for k, v in zip(model_names, areReady)}


def setEnvironmentImage(envImage):
    lux.setEnvironmentImage(envImage)


def winpath(path):
    return os.path.abspath(path)


def ensure_folder(folder, with_file=False):
    try:
        if with_file:
            head, tail = os.path.split(folder)
            os.makedirs(head)
        else:
            os.makedirs(folder)
    except Exception as e:
        print(e)


def clean_up(model_folder):
    try:

        var_render_location = os.path.join(
            model_folder, 'Keyshot', 'Renders')

        for root, dirs, files in os.walk(var_render_location):
            for f in files:
                if f.endswith('.0.png'):
                    os.remove(os.path.join(root, f))
    except:
        pass



# def my_render_frames(path, frame_files, opts, dummy=False):

#     animationInfo = lux.getAnimationInfo()
#     frames = animationInfo['frames']

#     zero_reran = False
#     for current_frame_number in range(frames+1):

#         lux.setAnimationFrame(current_frame_number)

#         lux.renderImage(
#             path=os.path.join(path, frame_files % (current_frame_number,)),
#             width=WIDTH,
#             height=HEIGHT,
#             opts=opts
#         )

#         if not zero_reran and current_frame_number == 0:
#             lux.setAnimationFrame(current_frame_number)

#             lux.renderImage(
#                 path=os.path.join(path, frame_files % (current_frame_number,)),
#                 width=WIDTH,
#                 height=HEIGHT,
#                 opts=opts
#             )

#             zero_reran = True

#         if dummy:
#             break

def my_render_frames(path, frame_files, opts, dummy=False):

    if dummy:
        lux.setAnimationFrame(0)

        lux.renderImage(
            path=os.path.join(path, frame_files % (0,)),
            width=WIDTH,
            height=HEIGHT,
            opts=opts
        )
           
        return

    lux.renderFrames(
        folder = path,
        frameFiles = frame_files,
        width=WIDTH,
        height=HEIGHT,
        fps = FPS,
        opts=opts
    )

def exclude_number_prefix(mask_name):
    match = rgx.search(mask_name)
    if match:
        return match.group(1)
    return mask_name


def ensure_file_exist(filename):
    if not os.path.exists(filename):
        print('{} was not found'.format(filename))
        raise FileNotFoundError()


def get_folders_to_process(appmodels_folder):

    processing = []
    skipping = []

    config = read_config(appmodels_folder)

    files = os.listdir(appmodels_folder)
    for model_name in files:
        if not model_id_regex.match(model_name):
            continue

        try:
            isReady = int(config[model_name].strip())
            if isReady == 1:
                processing.append(model_name)
            else:
                skipping.append(model_name)
        except:
            skipping.append(model_name)

    return processing, skipping


def main():

    app_folder = lux.getInputFolder(
        title='Select "APP MODELS" Folder Location')

    processing, skipping = get_folders_to_process(app_folder)

    print('The following models will be PROCESSED')
    print('\n'.join(processing))

    print('The following models will be SKIPPED')
    print('\n'.join(skipping))

    var_env_image = winpath(os.path.join(
        app_folder, 'KeyShot_Lightscape1.hdz'))

    var_env_image_gloss = winpath(os.path.join(
        app_folder, 'KeyShot_Lightscape_Gloss.hdz'))

    ensure_file_exist(var_env_image)

    ensure_file_exist(var_env_image_gloss)

    for model_name in processing:
        try:
            print('Processing model {}'.format(model_name))

            model_folder = winpath(os.path.join(app_folder, model_name))

            var_clay_bip = os.path.join(model_folder, 'KeyShot', 'Scenes')
            var_clay_bip = winpath(os.path.join(
                var_clay_bip, os.listdir(var_clay_bip)[0]))

            lux.openFile(var_clay_bip)
            setEnvironmentImage(var_env_image)
            var_clay_render_location = os.path.join(
                model_folder, 'Keyshot', 'Renders', 'Z_SOURCE')
            ensure_folder(var_clay_render_location)

            var_mask_render_location = os.path.join(
                model_folder, 'Keyshot', 'Renders', 'Z_MATTE')
            ensure_folder(var_mask_render_location)

            var_shadow_render_location = os.path.join(
                model_folder, 'Keyshot', 'Renders', 'Z_SHADOW')
            ensure_folder(var_shadow_render_location)

            opts = lux.getRenderOptions()
            opts.setOutputAlphaChannel(enable=False)
            opts.setAddToQueue(add=False)

            my_render_frames(var_clay_render_location,
                             'Clay1.%d.png', opts, dummy=True)
            my_render_frames(var_clay_render_location, 'Clay1.%d.png', opts)

            root = lux.getSceneTree()
            for node in root.find(name='Final'):
                final = node
                break

            lux.setBackgroundColor((0, 0, 0))
            final.setMaterial('Hard Rough Plastic Black')
            setEnvironmentImage(var_env_image_gloss)

            my_render_frames(var_clay_render_location,
                             'Gloss1.%d.png', opts, dummy=True)
            my_render_frames(var_clay_render_location, 'Gloss1.%d.png', opts)

            final.setMaterial('Hard Shiny Plastic Black')
            setEnvironmentImage(var_env_image_gloss)
            lux.setBackgroundColor(color=(0, 0, 0))

            my_render_frames(var_clay_render_location,
                             'Gloss2.%d.png', opts, dummy=True)
            my_render_frames(var_clay_render_location, 'Gloss2.%d.png', opts)

            input_masks_directory = os.path.join(model_folder, 'Masks')

            # masks render
            for node in root.find(name='Final'):
                for file in os.listdir(input_masks_directory):
                    input_mask_file = os.path.join(input_masks_directory, file)
                    input_fname_only, ext = os.path.splitext(
                        os.path.basename(input_mask_file))
                    material_name = model_name + '~' + input_fname_only
                    node.setMaterial(material_name)

                    lux.setLightingPreset('Performance Mode')

                    frameFiles = input_fname_only

                    my_render_frames(var_mask_render_location,
                                     '{}.%d.png'.format(frameFiles), opts, dummy=True)

                    my_render_frames(var_mask_render_location,
                                     '{}.%d.png'.format(frameFiles), opts)

            final.setMaterial('Flat White')
            lux.setBackgroundColor(color=(255, 255, 255))

            my_render_frames(var_shadow_render_location,
                             'SM_Shadow_01.%d.png', opts, dummy=True)
            my_render_frames(var_shadow_render_location,
                             'SM_Shadow_01.%d.png', opts)

            clean_up(model_folder)

            print('Processing model {} done.'.format(model_name))

        except:
            print('Something went wrong while processesing model {}. Moving on to next model'.format(
                model_name))


try:
    main()
    print('Render operation done.')
    # app_folder = 'D:\\Downloads\Compressed\\MACRO AUTOMATION JOB Files\\Sample Files\\APP MODELS\\'
    # processing, skipping = get_folders_to_process(app_folder)
    # print('The following models will be PROCESSED')
    # print('\n'.join(processing))

    # print('The following models will be SKIPPED')
    # print('\n'.join(skipping))
except Exception as e:
    print(e)
