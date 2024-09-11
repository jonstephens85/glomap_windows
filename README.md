# GLOMAP: Global Structure-from-Motion Revisited

[Project page](https://lpanaf.github.io/eccv24_glomap/) | [Paper](https://arxiv.org/pdf/2407.20219)
---

## About

GLOMAP is a general purpose global structure-from-motion pipeline for
image-based reconstruction. GLOMAP requires a COLMAP database as input and
outputs a COLMAP sparse reconstruction. As compared to COLMAP, this project
provides a much more efficient and scalable reconstruction process, typically
1-2 orders of magnitude faster, with on-par or superior reconstruction quality.

If you use this project for your research, please cite
```
@inproceedings{pan2024glomap,
    author={Pan, Linfei and Barath, Daniel and Pollefeys, Marc and Sch\"{o}nberger, Johannes Lutz},
    title={{Global Structure-from-Motion Revisited}},
    booktitle={European Conference on Computer Vision (ECCV)},
    year={2024},
}
```

## Getting Started

**[Watch this video to learn how to Install and Use GLOMAP](https://youtu.be/QIxXuilEEVw)**

### Install COLMAP
_If you have COLMAP already installed and added to path, skip this step._

I recommend downloading the COLMAP pre-built binaries [Here](https://github.com/colmap/colmap/releases)

### Install GLOMAP
Pre-compiled Windows binaries can be downloaded from the official
[release page](https://github.com/colmap/glomap/releases).

### Standalone Use
After installation, one can run GLOMAP by (starting from a database)
```shell
glomap mapper --database_path DATABASE_PATH --output_path OUTPUT_PATH --image_path IMAGE_PATH
```
For more details on the command line interface, one can type `glomap -h` or `glomap mapper -h` for help.

We also provide a guide on improving the obtained reconstruction, which can be found [here](docs/getting_started.md)
<br>
<br>


## Automated Python Scripting
In this section I walk you through how to the `run_glomap.py` which automates the manual step for running GLOWMAP. Specifically, I added modifiers to output file structure and format to use with 3DGS and Nerfstudio.

### Accessing run_glowmap.py
You can either clone this database or manually download the file. **Note: only the python script is maintained on this repository. Clone the original project for the most up to date information**

### Usage
Use run_glowmap.py by passing this command:
`python run_glowmap.py --image_path path\to\images`

**note: if the image folder is named "images" or "input" you may have some issues with the script. This will be addressed in future updates**

This will run colmap feature_extractor, colmap sequential_matcher, and glowmap mapper sequentially. The data will output in a structure and format immediately usable for the original 3DGS project.

### Modifiers
<details>
<summary><span style="font-weight: bold;">Command Line Arguments for run_glowmap.py</span></summary>

  ####  --image_path
  Path to the source directory of images.
  #### --matcher_type {sequential_matcher,exhaustive_matcher}
  Type of matcher to used by COLMAP (default: sequential_matcher).
  #### --interval {int}
  Interval of images to use in source image directory. Increase the number to use less images. For example: 2 uses every other image, 6 uses every 6th image. (default: 1)
  ####  --model_type {3dgs,nerfstudio}
  Model type to run. '3dgs' includes undistortion, 'nerfstudio' skips undistortion.

</details>
<br>
<br>

## Manual GLOWMAP Usage (from original repo)
In this section, we will use datasets from [this link](https://demuc.de/colmap/datasets) as examples.
Download the datasets and put them under `data` folder.

### From database

If a COLMAP database already exists, GLOMAP can directly use it to perform mapping:
```shell
glomap mapper \
    --database_path ./data/gerrard-hall/database.db \
    --image_path    ./data/gerrard-hall/images \
    --output_path   ./output/gerrard-hall/sparse
```

### From images

To obtain a reconstruction from images, the database needs to be established
first. Here, we utilize the functions from COLMAP:
```shell
colmap feature_extractor \
    --image_path    ./data/gerrard-hall/images \
    --database_path ./data/gerrard-hall/database.db \
colmap exhaustive_matcher \
    --database_path ./data/gerrard-hall/database.db \
glomap mapper \
    --database_path ./data/gerrard-hall/database.db \
    --image_path    ./data/gerrard-hall/images \
    --output_path   ./output/gerrard-hall/sparse
```

### Visualize and use the results

The results are written out in the COLMAP sparse reconstruction format. Please
refer to [COLMAP](https://colmap.github.io/format.html#sparse-reconstruction)
for more details.

The reconstruction can be visualized using the COLMAP GUI, for example:
```shell
colmap gui --import_path ./output/south-building/sparse/0 \
--image_path ./data/gerrard-hall/images \
--database_path ./data/gerrard-hall/database.db 
```
Alternatives like [rerun.io](https://rerun.io/examples/3d-reconstruction/glomap)
also enable visualization of COLMAP and GLOMAP outputs.

If you want to inspect the reconstruction programmatically, you can use
`pycolmap` in Python or link against COLMAP's C++ library interface.

### Notes From Original Project Page

- For larger scale datasets, it is recommended to use `sequential_matcher` or
  `vocab_tree_matcher` from `COLMAP`.
```shell
colmap sequential_matcher --database_path DATABASE_PATH
colmap vocab_tree_matcher --database_path DATABASE_PATH --VocabTreeMatching.vocab_tree_path VOCAB_TREE_PATH
```
- Alternatively, one can use
  [hloc](https://github.com/cvg/Hierarchical-Localization/) for image retrieval
  and matching with learning-based descriptors.



## Acknowledgement

We are highly inspired by COLMAP, PoseLib, Theia. Please consider also citing
them, if using GLOMAP in your work.

## Support

Please, use GitHub Discussions at https://github.com/colmap/glomap/discussions
for questions and the GitHub issue tracker at https://github.com/colmap/glomap
for bug reports, feature requests/additions, etc.

## Contribution

Contributions (bug reports, bug fixes, improvements, etc.) are very welcome and
should be submitted in the form of new issues and/or pull requests on GitHub.

## License

```
Copyright (c) 2024, ETH Zurich.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

    * Neither the name of ETH Zurich nor the names of its contributors may
      be used to endorse or promote products derived from this software
      without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
```
