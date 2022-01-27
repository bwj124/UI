import serial
import time
from light import LightController
from camera.BasicDemo.CamOperation_class import *


def take_photo(camera_id=0, light_id=1, value=255):
    contr = LightController()

    cam = MvCamera()
    deviceList = MV_CC_DEVICE_INFO_LIST()

    fp = './images/input.bmp'
    for i in range(1, 7):
        if light_id == i:
            contr.send(contr.CMD_SET, light_id, value)
        else:
            contr.send(contr.CMD_SET, i, 0)

    ret = MvCamera.MV_CC_EnumDevices(MV_USB_DEVICE, deviceList)
    print("Find %d devices!" % deviceList.nDeviceNum)

    cam_opt = CameraOperation(cam, deviceList, camera_id)
    cam_opt.Open_device()

    cam_opt.obj_cam.MV_CC_StartGrabbing()
    if ret != 0:
        print('start grabbing fail!')
        exit(0)
    cam_opt.b_start_grabbing = True
    print("start grabbing successfully!")

    cam_opt.exposure_time = 30000.
    cam_opt.gain = 30.

    print(cam_opt.exposure_time)
    print(cam_opt.gain)

    def worker():
        buf_cache = None
        stOutFrame = MV_FRAME_OUT()
        cam_opt.obj_cam.MV_CC_ClearImageBuffer()
        ret = cam_opt.obj_cam.MV_CC_GetImageBuffer(stOutFrame, 1000)
        if 0 == ret:
            if buf_cache is None:
                buf_cache = (c_ubyte * stOutFrame.stFrameInfo.nFrameLen)()
            # 获取到图像的时间开始节点获取到图像的时间开始节点
            cam_opt.st_frame_info = stOutFrame.stFrameInfo
            cdll.msvcrt.memcpy(byref(buf_cache), stOutFrame.pBufAddr, cam_opt.st_frame_info.nFrameLen)
            print("get one frame: Width[%d], Height[%d], nFrameNum[%d]" % (
                cam_opt.st_frame_info.nWidth, cam_opt.st_frame_info.nHeight, cam_opt.st_frame_info.nFrameNum))
            cam_opt.n_save_image_size = cam_opt.st_frame_info.nWidth * cam_opt.st_frame_info.nHeight * 3 + 2048
            cam_opt.Save_Bmp(buf_cache, fp)
            print(f'{fp} saved!')
            contr.send(contr.CMD_CLOSE, light_id)
            cam_opt.Close_device()
            cam_opt.Stop_grabbing()

    cam_opt.n_win_gui_id = random.randint(1, 10000)
    cam_opt.h_thread_handle = threading.Thread(target=worker)
    cam_opt.h_thread_handle.start()
    cam_opt.b_thread_closed = True


if __name__ == '__main__':
    take_photo()
