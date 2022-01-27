# YOLOv5 PyTorch utils

from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime
from math import ceil, exp
from os import environ
from pathlib import Path
from subprocess import check_output, CalledProcessError, STDOUT
from time import time

from torch.distributed import barrier
from torch.nn.functional import pad, interpolate
from torch import mm, cuda, Tensor, diag, zeros, no_grad, float16, sqrt, manual_seed, __version__
from torch.nn import Conv2d, parallel, Hardswish, LeakyReLU, ReLU6, Parameter, ReLU, Module, BatchNorm2d
from torchvision import models


@contextmanager
def torch_distributed_zero_first(local_rank: int):
    """
    Decorator to make all processes in distributed training wait for each local_master to do something.
    """
    if local_rank not in [-1, 0]:
        barrier()
    yield
    if local_rank == 0:
        barrier()


def init_torch_seeds(seed=0):
    # Speed-reproducibility tradeoff https://pytorch.org/docs/stable/notes/randomness.html
    manual_seed(seed)


def date_modified(path=__file__):
    # return human-readable file modification date, i.e. '2021-3-26'
    t = datetime.fromtimestamp(Path(path).stat().st_mtime)
    return f'{t.year}-{t.month}-{t.day}'


def git_describe(path=Path(__file__).parent):  # path must be a directory
    # return human-readable git description, i.e. v5.0-5-g3e25f1e https://git-scm.com/docs/git-describe
    s = f'git -C {path} describe --tags --long --always'
    try:
        return check_output(s, shell=True, stderr=STDOUT).decode()[:-1]
    except CalledProcessError as e:
        return ''  # not a git repository


def select_device(device='', batch_size=None):
    # device = 'cpu' or '0' or '0,1,2,3'
    s = f'YOLOv5 🚀 {git_describe() or date_modified()} torch {__version__} '  # string
    device = str(device).strip().lower().replace('cuda:', '')  # to string, 'cuda:0' to '0'
    environ['CUDA_VISIBLE_DEVICES'] = '-1'  # force torch.cuda.is_available() = False
    s += 'CPU\n'

    return 'cpu'


def time_sync():
    # pytorch-accurate time
    if cuda.is_available():
        cuda.synchronize()
    return time()


def profile(x, ops, n=100, device=None):
    # profile a pytorch module or list of modules. Example usage:
    #     x = torch.randn(16, 3, 640, 640)  # input
    #     m1 = lambda x: x * torch.sigmoid(x)
    #     m2 = nn.SiLU()
    #     profile(x, [m1, m2], n=100)  # profile speed over 100 iterations

    device = device or device('cuda:0' if cuda.is_available() else 'cpu')
    x = x.to(device)
    x.requires_grad = True
    print(__version__, device.type, cuda.get_device_properties(0) if device.type == 'cuda' else '')
    print(f"\n{'Params':>12s}{'GFLOPs':>12s}{'forward (ms)':>16s}{'backward (ms)':>16s}{'input':>24s}{'output':>24s}")
    for m in ops if isinstance(ops, list) else [ops]:
        m = m.to(device) if hasattr(m, 'to') else m  # device
        m = m.half() if hasattr(m, 'half') and isinstance(x, Tensor) and x.dtype is float16 else m  # type
        dtf, dtb, t = 0., 0., [0., 0., 0.]  # dt forward, backward
        flops = 0

        for _ in range(n):
            t[0] = time_sync()
            y = m(x)
            t[1] = time_sync()
            try:
                _ = y.sum().backward()
                t[2] = time_sync()
            except:  # no backward method
                t[2] = float('nan')
            dtf += (t[1] - t[0]) * 1000 / n  # ms per op forward
            dtb += (t[2] - t[1]) * 1000 / n  # ms per op backward

        s_in = tuple(x.shape) if isinstance(x, Tensor) else 'list'
        s_out = tuple(y.shape) if isinstance(y, Tensor) else 'list'
        p = sum(list(x.numel() for x in m.parameters())) if isinstance(m, Module) else 0  # parameters
        print(f'{p:12}{flops:12.4g}{dtf:16.4g}{dtb:16.4g}{str(s_in):>24s}{str(s_out):>24s}')


def is_parallel(model):
    # Returns True if line_detection is of type DP or DDP
    return type(model) in (parallel.DataParallel, parallel.DistributedDataParallel)


def de_parallel(model):
    # De-parallelize a line_detection: returns single-GPU line_detection if line_detection is of type DP or DDP
    return model.module if is_parallel(model) else model


def intersect_dicts(da, db, exclude=()):
    # Dictionary intersection of matching keys and shapes, omitting 'exclude' keys, using da values
    return {k: v for k, v in da.items() if k in db and not any(x in k for x in exclude) and v.shape == db[k].shape}


def initialize_weights(model):
    for m in model.modules():
        t = type(m)
        if t is Conv2d:
            pass  # nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
        elif t is BatchNorm2d:
            m.eps = 1e-3
            m.momentum = 0.03
        elif t in [Hardswish, LeakyReLU, ReLU, ReLU6]:
            m.inplace = True


def find_modules(model, mclass=Conv2d):
    # Finds layer indices matching module class 'mclass'
    return [i for i, m in enumerate(model.module_list) if isinstance(m, mclass)]


def sparsity(model):
    # Return global line_detection sparsity
    a, b = 0., 0.
    for p in model.parameters():
        a += p.numel()
        b += (p == 0).sum()
    return b / a


def prune(model, amount=0.3):
    # Prune line_detection to requested global sparsity
    import torch.nn.utils.prune as prune
    print('Pruning line_detection... ', end='')
    for name, m in model.named_modules():
        if isinstance(m, Conv2d):
            prune.l1_unstructured(m, name='weight', amount=amount)  # prune
            prune.remove(m, 'weight')  # make permanent
    print(' %.3g global sparsity' % sparsity(model))


def fuse_conv_and_bn(conv, bn):
    # Fuse convolution and batchnorm layers https://tehnokv.com/posts/fusing-batchnorm-and-conv/
    fusedconv = Conv2d(conv.in_channels,
                       conv.out_channels,
                       kernel_size=conv.kernel_size,
                       stride=conv.stride,
                       padding=conv.padding,
                       groups=conv.groups,
                       bias=True).requires_grad_(False).to(conv.weight.device)

    # prepare filters
    w_conv = conv.weight.clone().view(conv.out_channels, -1)
    w_bn = diag(bn.weight.div(sqrt(bn.eps + bn.running_var)))
    fusedconv.weight.copy_(mm(w_bn, w_conv).view(fusedconv.weight.shape))

    # prepare spatial bias
    b_conv = zeros(conv.weight.size(0), device=conv.weight.device) if conv.bias is None else conv.bias
    b_bn = bn.bias - bn.weight.mul(bn.running_mean).div(sqrt(bn.running_var + bn.eps))
    fusedconv.bias.copy_(mm(w_bn, b_conv.reshape(-1, 1)).reshape(-1) + b_bn)

    return fusedconv


def model_info(model, verbose=False, img_size=640):
    # Model information. img_size may be int or list, i.e. img_size=640 or img_size=[640, 320]
    n_p = sum(x.numel() for x in model.parameters())  # number parameters
    n_g = sum(x.numel() for x in model.parameters() if x.requires_grad)  # number gradients
    if verbose:
        print('%5s %40s %9s %12s %20s %10s %10s' % ('layer', 'name', 'gradient', 'parameters', 'shape', 'mu', 'sigma'))
        for i, (name, p) in enumerate(model.named_parameters()):
            name = name.replace('module_list.', '')
            print('%5g %40s %9s %12g %20s %10.3g %10.3g' %
                  (i, name, p.requires_grad, p.numel(), list(p.shape), p.mean(), p.std()))


def load_classifier(name='resnet101', n=2):
    # Loads a pretrained line_detection reshaped to n-class output
    model = models.__dict__[name](pretrained=True)

    # ResNet line_detection properties
    # input_size = [3, 224, 224]
    # input_space = 'RGB'
    # input_range = [0, 1]
    # mean = [0.485, 0.456, 0.406]
    # std = [0.229, 0.224, 0.225]

    # Reshape output to n classes
    filters = model.fc.weight.shape[1]
    model.fc.bias = Parameter(zeros(n), requires_grad=True)
    model.fc.weight = Parameter(zeros(n, filters), requires_grad=True)
    model.fc.out_features = n
    return model


def scale_img(img, ratio=1.0, same_shape=False, gs=32):  # img(16,3,256,416)
    # scales img(bs,3,y,x) by ratio constrained to gs-multiple
    if ratio == 1.0:
        return img
    else:
        h, w = img.shape[2:]
        s = (int(h * ratio), int(w * ratio))  # new size
        img = interpolate(img, size=s, mode='bilinear', align_corners=False)  # resize
        if not same_shape:  # pad/crop img
            h, w = [ceil(x * ratio / gs) * gs for x in (h, w)]
        return pad(img, [0, w - s[1], 0, h - s[0]], value=0.447)  # value = imagenet mean


def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)


class ModelEMA:
    """ Model Exponential Moving Average from https://github.com/rwightman/pytorch-image-models
    Keep a moving average of everything in the line_detection state_dict (parameters and buffers).
    This is intended to allow functionality like
    https://www.tensorflow.org/api_docs/python/tf/train/ExponentialMovingAverage
    A smoothed version of the weights is necessary for some training schemes to perform well.
    This class is sensitive where it is initialized in the sequence of line_detection init,
    GPU assignment and distributed training wrappers.
    """

    def __init__(self, model, decay=0.9999, updates=0):
        # Create EMA
        self.ema = deepcopy(model.module if is_parallel(model) else model).eval()  # FP32 EMA
        # if next(line_detection.parameters()).device.type != 'cpu':
        #     self.ema.half()  # FP16 EMA
        self.updates = updates  # number of EMA updates
        self.decay = lambda x: decay * (1 - exp(-x / 2000))  # decay exponential ramp (to help early epochs)
        for p in self.ema.parameters():
            p.requires_grad_(False)

    def update(self, model):
        # Update EMA parameters
        with no_grad():
            self.updates += 1
            d = self.decay(self.updates)

            msd = model.module.state_dict() if is_parallel(model) else model.state_dict()  # line_detection state_dict
            for k, v in self.ema.state_dict().items():
                if v.dtype.is_floating_point:
                    v *= d
                    v += (1. - d) * msd[k].detach()

    def update_attr(self, model, include=(), exclude=('process_group', 'reducer')):
        # Update EMA attributes
        copy_attr(self.ema, model, include, exclude)
