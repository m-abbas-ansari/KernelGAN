from PIL import Image
import numpy as np
import os.path as osp
import glob
import os
import argparse
import rasterio as rio
import numpy as np
# import yaml

parser = argparse.ArgumentParser(description='create a dataset')
parser.add_argument('--dataset', default='../Dataset/SDEM/', type=str, help='selecting different datasets')
parser.add_argument('--artifacts', default='', type=str, help='selecting different artifacts type')
parser.add_argument('--cleanup_factor', default=2, type=int, help='downscaling factor for image cleanup')
parser.add_argument('--upscale_factor', default=4, type=int, choices=[4], help='super resolution upscale factor')
opt = parser.parse_args()


def noise_patch(img, sp, max_var, min_mean):
    img = np.array(img)

    w, h = img.shape
    collect_patchs = []

    for i in range(0, w - sp, sp):
        for j in range(0, h - sp, sp):
            patch = img[i:i + sp, j:j + sp]
            var_global = np.var(patch)
            mean_global = np.mean(patch)
            print(var_global,mean_global)
            if var_global < max_var and mean_global > min_mean:
                collect_patchs.append(patch)

    return collect_patchs

if __name__ == '__main__':
    img_dir = '../Dataset/SDEM/'
    noise_dir = '../Noise_patch/'
    
    max_var = 200
    min_mean = 200

# assert not os.path.exists(noise_dir)
# os.mkdir(noise_dir)

img_paths = sorted(glob.glob(osp.join(img_dir, '*.asc')))
cnt = 0
for path in img_paths:
    img_name = osp.splitext(osp.basename(path))[0]
    print('**********', img_name, '**********')
    img = rio.open(path).read(1).astype('float64')
    sp = int(img.max()-img.min())
    print(f'Shape of image : {img.shape}')
    patchs = noise_patch(img, sp, max_var, min_mean)
    print(f'Shape of patch : {len(patchs)}')
    for idx, patch in enumerate(patchs):
        print(idx)
        save_path = "../Noise_patch/"
        cnt += 1
        print('collect:', cnt, save_path)
        # Image.fromarray(patch).save(save_path)
        np.save(save_path + str(idx),patch)
        print(f"Saved File {img_name} !")