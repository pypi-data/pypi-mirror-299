# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymatio', 'src']

package_data = \
{'': ['*']}

modules = \
['xmake']
setup_kwargs = {
    'name': 'pymatio',
    'version': '0.1.0',
    'description': '',
    'long_description': '[中文](./README.md) [English](./README_en.md)\n\n# 背景\n\nPython 中始终没有一个一站式读取 mat 文件的库，mat5 总是依赖 scipy.io, mat7.3 总是依赖 h5py，h5py 直接读取 mat 文件又需要很多手动转换，有一个 mat73 转换，但是核心逻辑是纯 Python 写的，又非常慢。\n\n恰巧 C 中有一个库 [matio](https://github.com/tbeu/matio)，我就想用 pybind11 做一个绑定。\n\n# 路线\n\n- [x] 完成基本函数的绑定\n- [x] 使用 xmake 在 Windows 和 Linux 上编译通过\n- [x] 打包为 whl 文件\n- [x] 添加关于构建成功的基本测试\n- [ ] 添加 cibuildwheel 和 Github Action\n- [ ] 吸取 https://github.com/pybind/scikit_build_example 中的优势\n- [x] 编译扩展时自动处理虚拟环境\n- [ ] 添加更 Pythonic 的调用接口\n- [ ] 添加 benchmark\n- [ ] 导入 scio 的测试和 mat73 的测试\n\n# 使用\n\n当前还没有打包到 whl，如需试用需安装 [xmake](https://github.com/xmake-io/xmake/)，这是一个基于 lua 的构建系统，非常轻量。\n\n```bash\ngit clone https://github.com/myuanz/pymatio\nxmake\n```\n\n之后即可在`build`目录下见对应平台的 Python 扩展，hdf5 和 matio 之依赖会自动处理。\n\n# 样例\n\n```python\nimport pymatio as pm\n\nprint(pm.get_library_version())\nprint(pm.log_init(\'pymatio\'))\nprint(pm.set_debug(1))\npm.critical("abcdefg%d,%d\\n" % (234, 456,))\nmat = pm.create_ver(\'test.mat\', None, pm.MatFt.MAT73)\n\nvar1 = pm.var_create(\'var1\', pm.MatioClasses.DOUBLE, pm.MatioTypes.DOUBLE, 2, (2, 3,), (1, 2, 3, 4, 5, 6,), 0)\npm.var_write(mat, var1, pm.MatioCompression.NONE)\npm.var_free(var1)\nprint(mat.filename, mat.version, mat.fp, mat.header, mat.byte_swap, mat.mode, mat.bof, mat.next_index, mat.num_datasets, mat.refs_id, mat.dir)\n```\n\n输出：\n\n```\n(1, 5, 26)\n0\nNone\n-E- abcdefg234,456\n: abcdefg234,456\n\ntest.mat 512 <capsule object NULL at 0x7f85197b3fc0> MATLAB 7.3 MAT-file, Platform: x86_64-pc-Linux, Created by: libmatio v1.5.26 on Tue Dec 26 15:49:00 2023\n HDF5 sche 0 MatAcc.RDWR 128 0 1 -1 []\n ```',
    'author': 'zhengmy',
    'author_email': 'zhengmy@ion.ac.cn',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'python_requires': '>=3.9,<3.13',
}
from build_arg import *
build(setup_kwargs)

setup(**setup_kwargs)
