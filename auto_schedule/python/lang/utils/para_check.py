#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright 2019-2020 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""
common function for check ops parameter
"""
import re
import math
import warnings

from enum import Enum
from functools import reduce as _reduce
from functools import wraps
from te.utils import error_manager

STACKLEVEL_FOR_PARA_CHECK = 2
SHAPE_SIZE_LIMIT = 2 ** 31 - 1
SHAPE_SIZE_ZERO = 0
DIM_LIMIT = SHAPE_SIZE_LIMIT
MIN_UNKNOWN_SHAPE_RANK = 0
MAX_UNKNOWN_SHAPE_NUM = 2 ** 31 - 1
DEFAULT_MIN_SHAPE_DIM = 1
DEFAULT_MAX_SHAPE_DIM = 8
DEFAULT_MAX_SHAPE_NUM = 200000000

RANK_ZERO = 0
RANK_LIMIT = 8
ZERO_DIM = 0
NONE_TYPE = type(None)

# the max len of kernel_name
MAX_KERNEL_NAME_LEN = 200
KERNEL_NAME = "kernel_name"

CONST = "const"
SPECIAL = "special"
ORIGINAL = "original"
SPECIAL_SCALAR = "special_scalar"
COMMON = "common"
BROADCAST = "broadcast"

REQUIRED_INPUT = "required_input"
OPTION_INPUT = "option_input"
DYNAMIC_INPUT = "dynamic_input"

REQUIRED_OUTPUT = "required_output"
OPTION_OUTPUT = "option_output"
DYNAMIC_OUTPUT = "dynamic_output"

# in proto attr can be a Tensor/BYTES/LIST_TYPE Type, but not te fusion don't support this type
REQUIRED_ATTR_INT = "REQUIRED_ATTR_INT"
REQUIRED_ATTR_FLOAT = "REQUIRED_ATTR_FLOAT"
REQUIRED_ATTR_STR = "REQUIRED_ATTR_STR"
REQUIRED_ATTR_BOOL = "REQUIRED_ATTR_BOOL"
REQUIRED_ATTR_TYPE = "REQUIRED_ATTR_TYPE"
REQUIRED_ATTR_LIST_INT = "REQUIRED_ATTR_LIST_INT"
REQUIRED_ATTR_LIST_FLOAT = "REQUIRED_ATTR_LIST_FLOAT"
REQUIRED_ATTR_LIST_BOOL = "REQUIRED_ATTR_LIST_BOOL"
REQUIRED_ATTR_LIST_LIST_INT = "REQUIRED_ATTR_LIST_LIST_INT"

OPTION_ATTR_INT = "OPTION_ATTR_INT"
OPTION_ATTR_FLOAT = "OPTION_ATTR_FLOAT"
OPTION_ATTR_STR = "OPTION_ATTR_STR"
OPTION_ATTR_BOOL = "OPTION_ATTR_BOOL"
OPTION_ATTR_TYPE = "OPTION_ATTR_TYPE"
OPTION_ATTR_LIST_INT = "OPTION_ATTR_LIST_INT"
OPTION_ATTR_LIST_FLOAT = "OPTION_ATTR_LIST_FLOAT"
OPTION_ATTR_LIST_BOOL = "OPTION_ATTR_LIST_BOOL"
OPTION_ATTR_LIST_LIST_INT = "OPTION_ATTR_LIST_LIST_INT"

OP_ERROR_CODE_000 = 'E80000'
OP_ERROR_CODE_001 = 'E80001'
OP_ERROR_CODE_002 = 'E80002'
OP_ERROR_CODE_003 = 'E80003'
OP_ERROR_CODE_004 = 'E80004'
OP_ERROR_CODE_005 = 'E80005'
OP_ERROR_CODE_006 = 'E80006'
OP_ERROR_CODE_007 = 'E80007'
OP_ERROR_CODE_008 = 'E80008'
OP_ERROR_CODE_009 = 'E80009'
OP_ERROR_CODE_010 = 'E80010'
OP_ERROR_CODE_011 = 'E80011'
OP_ERROR_CODE_012 = 'E80012'
OP_ERROR_CODE_013 = 'E80013'
OP_ERROR_CODE_014 = 'E80014'
OP_ERROR_CODE_015 = 'E80015'
OP_ERROR_CODE_016 = 'E80016'
OP_ERROR_CODE_017 = 'E80017'
OP_ERROR_CODE_018 = 'E80018'
OP_ERROR_CODE_019 = 'E80019'
OP_ERROR_CODE_020 = 'E80020'
OP_ERROR_CODE_021 = 'E80021'
OP_ERROR_CODE_022 = 'E80022'
OP_ERROR_CODE_023 = 'E80023'
OP_ERROR_CODE_024 = 'E80024'
OP_ERROR_CODE_025 = 'E80025'
OP_ERROR_CODE_026 = 'E80026'
OP_ERROR_CODE_027 = 'E80027'


# OpParamInfoKey && TensorFormat :Internal Use Only
class OpParamInfoKey(Enum):
    """
    Op Parameter Info enum
    """
    SHAPE = "shape"
    FORMAT = "format"
    ORI_SHAPE = "ori_shape"
    ORI_FORMAT = "ori_format"
    D_TYPE = "dtype"
    RANGE = "range"


class TensorFormat(Enum):
    """
    Tensor Format enum
    """
    ND = "ND"
    NCHW = "NCHW"
    NHWC = "NHWC"
    NDHWC = "NDHWC"
    NCDHW = "NCDHW"
    CHWN = "CHWN"
    NC1HWC0 = "NC1HWC0"
    NC1HWC0_C04 = "NC1HWC0_C04"
    NDC1HWC0 = "NDC1HWC0"
    FRACTAL_NZ = "FRACTAL_NZ"
    HWCN = "HWCN"
    DHWCN = "DHWCN"
    FRACTAL_Z = "FRACTAL_Z"
    FRACTAL_Z_C04 = "FRACTAL_Z_C04"
    C1HWNCoC0 = "C1HWNCoC0"
    FRACTAL_Z_3D = "FRACTAL_Z_3D"
    FRACTAL_ZN_LSTM = "FRACTAL_ZN_LSTM"


ALL_FORMAT_LIST = [entry.value for entry in TensorFormat]
ALL_DTYPE_LIST = ("int8", "uint8", "int16", "uint16", "int32", "uint32", "bfloat16",
                  "int64", "uint64", "float16", "float32", "float64", "bool", "uint1")
OP_NAME = ""
PARAM_NAME = ""


def check_op_params(*type_args, **type_kwargs):
    """
    check op params
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_op_params
    return check_op_params(*type_args, **type_kwargs)


def _check_range(shape, shape_range, min_dim=0, max_dim=RANK_LIMIT,
                 max_shape_num=MAX_UNKNOWN_SHAPE_NUM, param_name=PARAM_NAME):
    """
    check rule for tensor shape
    """
    if not isinstance(shape_range, (tuple, list)):
        error_info = {
            'errCode': OP_ERROR_CODE_003, 'op_name': OP_NAME,
            'param_name': param_name, 'param_type': "list tuple",
            'actual_type': shape_range.__class__.__name__}
        raise RuntimeError(
            error_info,
            "In op, the parameter[%s]'s type should be [%s],"
            "but actually is [%s]."
            % (error_info['param_name'], error_info['param_type'],
               error_info['actual_type']))
    if len(shape) != len(shape_range):
        error_info = {
            'errCode': OP_ERROR_CODE_021, 'op_name': OP_NAME,
            'param_name': param_name, 'shape_len': len(shape),
            'range_len': len(shape_range)}
        raise RuntimeError(
            error_info,
            "In op, the length of shape[%s] and the length of range[%s] "
            "must be the same."
            % (error_info['shape_len'], error_info['range_len']))

    for range_i in shape_range:
        if len(range_i) == 2 and (range_i[1] is None) \
                and isinstance(range_i[0], int) \
                and 0 < range_i[0] <= max_shape_num:
            continue
        if not isinstance(range_i[0], int):
            error_info = {
                'errCode': OP_ERROR_CODE_003, 'op_name': OP_NAME,
                'param_name': param_name, 'param_type': 'int',
                'actual_type': range_i[0].__class__.__name__}
            raise RuntimeError(
                error_info,
                "In op, the parameter[%s]'s type should be [%s], "
                "but actually is [%s]."
                % (error_info['param_name'], error_info['param_type'],
                   error_info['actual_type']))
        if not isinstance(range_i[1], int):
            error_info = {
                'errCode': OP_ERROR_CODE_003, 'op_name': OP_NAME,
                'param_name': param_name, 'param_type': 'int',
                'actual_type': range_i[1].__class__.__name__}
            raise RuntimeError(
                error_info,
                "In op, the parameter[%s]'s type should be [%s],"
                "but actually is [%s]."
                % (error_info['param_name'], error_info['param_type'],
                   error_info['actual_type']))
        valid_type = isinstance(range_i[0], int) and isinstance(range_i[1], int)
        if len(range_i) != 2:
            error_info = {'errCode': OP_ERROR_CODE_023, 'op_name': OP_NAME,
                          'param_name': param_name}
            raise RuntimeError(
                error_info,
                "In op[%s],the length of each element in the range must be two"
                % (error_info['op_name']))
        valid_range = \
            len(range_i) == 2 and 0 <= range_i[0] <= range_i[1] <= max_shape_num
        if valid_type and valid_range:
            continue
        else:
            error_info = {
                'errCode': OP_ERROR_CODE_022, 'op_name': OP_NAME,
                'param_name': param_name, 'first_real_value': range_i[0],
                'second_real_value': range_i[1], 'min_range_value': 0,
                'max_range_value': max_shape_num}
            raise RuntimeError(
                error_info,
                "In op, the n-dim of first range input[%s] is less than "
                "that of the second range input[%s], and the n-dim of range "
                "should be in the range of [%s, %s]."
                % (error_info['first_real_value'],
                   error_info['second_real_value'], 0, max_shape_num))


def _check_dynamic_shape(shape, max_dim=DIM_LIMIT, max_rank=RANK_LIMIT,
                         param_name=PARAM_NAME):

    _check_shape_range(max_rank, MIN_UNKNOWN_SHAPE_RANK, param_name, shape)
    for _, dim in enumerate(shape):
        valid_dim = -1 <= dim <= max_dim
        if not valid_dim:
            error_info = {
                'errCode': OP_ERROR_CODE_002, 'op_name': OP_NAME,
                'param_name': param_name, 'min_value': "-1",
                'max_value': max_dim, 'real_value': dim}
            raise RuntimeError(
                error_info,
                "In op, the parameter[%s] should be in "
                "the range of [%s, %s], "
                "but actually is [%s]."
                % (error_info['param_name'], -1, max_dim, dim))


def check_shape(shape, min_dim=0, max_dim=DIM_LIMIT, min_rank=0,
                max_rank=RANK_LIMIT, min_size=0,
                max_size=SHAPE_SIZE_LIMIT, param_name=PARAM_NAME):
    """
    check shape size
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_shape
    return check_shape(shape, min_dim, max_dim, min_rank, max_rank, min_size, max_size, param_name)


def _check_shape_range(max_rank, min_rank, param_name, shape):
    if len(shape) < min_rank or len(shape) > max_rank:
        error_info = {
            'errCode': OP_ERROR_CODE_012, 'op_name': OP_NAME,
            'param_name': param_name, 'min_value': min_rank,
            'max_value': max_rank, 'real_value': len(shape)}
        raise RuntimeError(
            error_info,
            "In op, the num of dimensions of input[%s] should be in"
            "the range of [%s, %s], but actually is [%s]."
            % (error_info['param_name'], min_rank, max_rank, len(shape)))


def check_dtype(dtype, check_list=ALL_DTYPE_LIST, param_name=PARAM_NAME):
    """
    The common check rule for tensor dtype
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_dtype
    return check_dtype(dtype, check_list, param_name)


def check_format(data_format, check_list=None, param_name=PARAM_NAME):
    """
    The common check rule for tensor dtype
    """

    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_format
    return check_format(data_format, check_list, param_name)


def check_elewise_shape_range(inputs: list, support_broadcast=False):
    """
    :param support_broadcast:True or False
    :param inputs: list, all inputs of operator
    :return:
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_elewise_shape_range
    return check_elewise_shape_range(inputs, support_broadcast)


def _check_input_type_dict(input_dict, input_key, input_name):
    """
    check input parameter type for new type: dict
    rule1: key of input_dict should be in the input_key
    rule2: type of input_dict[shape] should be in (list, tuple), if have shape
    rule3: type of input_dict[dtype] should be in (str), if have dtype

    Parameters
    ----------
    input_dict: dict
        input_dict
    input_key: list or tuple
        all input key list, the key of input must in input_key
    input_name: str
        input param name, only used for error print

    Returns
    -------
    None
    """

    def _check_input_type(input_key, input_type):
        if not isinstance(input_dict[input_key], input_type):
            args_dict = {
                "errCode": "E60037",
                "param_name": "{}".format(input_key),
                "type_list": "{}".format(input_type),
                "type": "{}".format(type(input_dict[input_key]))
            }
            raise RuntimeError(
                args_dict,
                error_manager.get_error_message(args_dict)
            )

    for key in input_dict.keys():
        if key not in input_key:
            args_dict = {
                "errCode": "E60038",
                "desc": "input parameter value must have property {}".format(key)
            }
            raise RuntimeError(
                args_dict,
                error_manager.get_error_message(args_dict)
            )
        # check shape's type of input_dict, if have shape
        if key == "shape":
            _check_input_type(key, (list, tuple))

        # check dtype's type of input_dict, if have dtype
        if key == "dtype":
            _check_input_type(key, (str,))


def check_input_type(*type_args, **type_kwargs):
    """
    check input parameter type
    """

    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_input_type
    return check_input_type(*type_args, **type_kwargs)


def check_dtype_rule(dtype, check_list, param_name="default"):
    """
    The common check rule for tensor dtype
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_dtype_rule
    return check_dtype_rule(dtype, check_list, param_name)


def check_shape_rule(shape, min_dim=None, max_dim=None, max_shape_num=None):
    """
    The common check rule for tensor shape
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_shape_rule
    return check_shape_rule(shape, min_dim, max_dim, max_shape_num)


def check_kernel_name(kernel_name):
    """
    check kernel_name
    ----------
    kernel_name: str or None

    Returns
    -------
    None
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_kernel_name
    return check_kernel_name(kernel_name)


def check_and_init_5hdc_reduce_support(input_tensor, axis):
    """5HD Special param for 5hd schedule"""
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_and_init_5hdc_reduce_support
    return check_and_init_5hdc_reduce_support(input_tensor, axis)


def is_scalar(shape):
    """
    verify that tensor is scalar
    ----------
    shape: shape of data

    Returns
    -------
    True or False
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import is_scalar
    return is_scalar(shape)


def check_shape_size(shape, limit=SHAPE_SIZE_LIMIT+1):
    """
    if get all shape size, use get_shape_size function.
    ----------
    shape: shape of data

    limit: limit of the product of all dimension

    Returns
    -------
    None
    """
    warnings.warn("te.utils.para_check is expired, please replace it with tbe.common.utils.para_check",
                  DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from tbe.common.utils import check_shape_size
    return check_shape_size(shape, limit)


def check_tensor_shape_size(shape):
    """
    The function is deprecated.
    if check shape size, use check_shape_size function.
    if get all shape size,use get_shape_size function.
    """
    warnings.warn("check_tensor_shape_size is deprecated", DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from functools import reduce
    product = reduce(lambda x, y: x * y, shape[:])  # product of all dimension

    return product


def check_reduce_shape_rule(shape):
    """
    check the shape of reduce axis must be less than MAX_REDUCE_SHAPE_NUM
    :param shape: inout shape
    """
    # the shape of reduce axis must be less than MAX_REDUCE_SHAPE_NUM
    warnings.warn("check_reduce_shape_rule is deprecated", DeprecationWarning, stacklevel=STACKLEVEL_FOR_PARA_CHECK)
    from functools import reduce
    product = reduce(lambda x, y: x * y, shape[:])  # product of all dimension
