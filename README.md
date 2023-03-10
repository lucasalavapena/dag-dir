# dag-dir

Like tree but draws it in the form of a DAG. My idea was that symbolic links essentially make a file system a DAG. Although after reading more it does seem like symbolic link loops are allowed at least on Unix system. I will deal with that case later.
I still need to make it more robust, I need to add a lot more tests.

## Example Usage

For the following tree output:

```python3
[X@X tmp7sojntl_]$ tree
.
├── a.txt
└── subdir
    ├── ptr.txt -> /tmp/tmp7sojntl_/a.txt
    └── b.text
```

With `dag_dir.py` this results in:

```
[X@X tmp7sojntl_]$ (dag-show) [lap@lap-arch show-dag]$ python dag_dir.py /tmp/tmp7sojntl_ --canvas-size 20 50
          subdir/ptr.txt
                *^
               *  *
               *   *
              *     *
             *      *
            *        *
           *          *
           *          *
          *         subdir
         *             *  ^
        *              *      *
        *             *          *
       *              *             *
      *               *                 *
     *                *                    *
    *                 *                       *
    *                *                           *
   ∨                 ∨                               *
a.txt <********subdir/b.txt*********************/tmp/tmp7sojntl_

```

## Installation

It is writing in python (I in particular during development was using 3.10.9), just create a virtual env in your prefered way and install `netgraph` in your virtual environment. Either via:

- via pip 0: `pip install netgraph`
- via pip 1: `pip install -u netgraph`
- if you are using a conda env and wanted to use [the conda package](https://anaconda.org/conda-forge/netgraph): ` conda install -c conda-forge netgraph`

## Usage Set Up 

So far I have only tested it on Linux, will test it on Windows. 
This would work best on a horizontal screen setup, as the height is most important, since right now I am only writing text from left to right not top to bottom or similar.


