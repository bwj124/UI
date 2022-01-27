import time
from argparse import ArgumentParser
import serial

from cv2 import imwrite

import chandou
import year
import zuo
from yolo_detection import judge_xpc_direction, detect_aqs_ptx_kkx
from light_controller import take_photo


def parse_opt():
    parser = ArgumentParser()
    parser.add_argument('--position', default='P130', type=str)
    parser.add_argument('--camera_id', default=0, type=int)
    parser.add_argument('--light_id', default=1, type=int)
    parser.add_argument('--value', default=255, type=int)
    parser.add_argument('--input', type=str, default='./images/input.bmp', help='input file path')
    parser.add_argument('--output', type=str, default='./outputs/output.jpg', help='output file path')
    parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints')
    return parser.parse_args()


def main(opt):
    take_photo(camera_id=opt.camera_id, light_id=opt.light_id, value=opt.value)

    handler = {
        "kkx": lambda tmp: detect_aqs_ptx_kkx.run(detect_type='kkx', source=tmp.input, conf_thres=0.10,
                                                  # output=tmp.output,
                                                  weights=tmp.checkpoints_dir.rstrip('/').rstrip('\\') + '/kkx.onnx'),
        "xpc": lambda tmp: judge_xpc_direction.judge(input_path=tmp.input,  # output_path=tmp.output,
                                                     weight=tmp.checkpoints_dir.rstrip('/').rstrip(
                                                         '\\') + '/xpc.onnx'),
        "aqs": lambda tmp: detect_aqs_ptx_kkx.run(detect_type='aqs', source=tmp.input, conf_thres=0.10,
                                                  # output=tmp.output,
                                                  weights=tmp.checkpoints_dir.rstrip('/').rstrip(
                                                      '\\') + '/aqs.onnx'),
        "ptx": lambda tmp: detect_aqs_ptx_kkx.run(detect_type='ptx', source=tmp.input, conf_thres=0.19,
                                                  # output=tmp.output,
                                                  weights=tmp.checkpoints_dir.rstrip('/').rstrip('\\') + '/ptx.onnx'),
        "year": lambda tmp: year.run(weights=tmp.checkpoints_dir.rstrip('/').rstrip('\\'), input_path=tmp.input),
        "chandou": lambda tmp: chandou.run(
            weights=tmp.checkpoints_dir.rstrip('/').rstrip('\\') + '/segment_net_200.pth',
            input_path=tmp.input, output_path=tmp.output),
        "zuo": lambda tmp: zuo.run(source=tmp.input,
                                   weights=tmp.checkpoints_dir.rstrip('/').rstrip('\\') + "/calib.onnx")
    }

    def dual_handler(key0, key1, tmp):
        ret0, bool0 = handler[key0](tmp)
        ret1, bool1 = handler[key1](tmp)
        ret0, ret1 = ret0.astype("float"), ret1.astype("float")
        ret = (ret0 + ret1) / 2
        return ret.astype('int'), bool1 and bool0

    time.sleep(1.5)
    pos = opt.position
    ret, bool_ret = {
        'P130': lambda tmp: handler['zuo'](tmp),  # “左”字识别
        'P140': lambda tmp: handler['chandou'](tmp),  # 铲斗识别
        'P200': lambda tmp: handler['kkx'](tmp),  # 开口销识别
        'P150': lambda tmp: handler['xpc'](tmp),  # 滚子防反识别
        'P160': lambda tmp: handler['ptx'](tmp),  # 扁口销识别
        'P170': lambda tmp: handler['aqs'](tmp),  # 安全锁识别
        'P180': lambda tmp: dual_handler("kkx", "aqs", tmp),  # 开口销，安全锁识别
        'P190': lambda tmp: handler['ptx'](tmp),  # 扁口销识别
        'P210': lambda tmp: handler['zuo'](tmp),  # “左”字识别
        'P230': lambda tmp: dual_handler("kkx", "aqs", tmp),  # 开口销，安全锁识别
        'P260': lambda tmp: handler['year'](tmp),  # 年限识别
        'P340': lambda tmp: handler['zuo'](tmp),  # “左”字识别
        'P350': lambda tmp: dual_handler("kkx", "aqs", tmp),  # 开口销识别、安全锁识别
        'P360': lambda tmp: handler['xpc'](tmp),  # 滚子防反
        'P370': lambda tmp: handler['aqs'](tmp),  # 安全锁识别
        'P380': lambda tmp: handler['kkx'](tmp),  # 开口销识别
        'P400': lambda tmp: handler['chandou'](tmp)  # 铲斗识别
    }[pos](opt)

    imwrite(opt.output, ret)

    return bool_ret


if __name__ == "__main__":
    main(parse_opt())
