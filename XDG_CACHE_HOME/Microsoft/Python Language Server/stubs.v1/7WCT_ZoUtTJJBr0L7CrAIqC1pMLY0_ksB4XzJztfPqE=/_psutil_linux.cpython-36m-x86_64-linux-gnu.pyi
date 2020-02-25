DUPLEX_FULL = 1
DUPLEX_HALF = 0
DUPLEX_UNKNOWN = 255
RLIMIT_AS = 9
RLIMIT_CORE = 4
RLIMIT_CPU = 0
RLIMIT_DATA = 2
RLIMIT_FSIZE = 1
RLIMIT_LOCKS = 10
RLIMIT_MEMLOCK = 8
RLIMIT_MSGQUEUE = 12
RLIMIT_NICE = 13
RLIMIT_NOFILE = 7
RLIMIT_NPROC = 6
RLIMIT_RSS = 5
RLIMIT_RTPRIO = 14
RLIMIT_RTTIME = 15
RLIMIT_SIGPENDING = 11
RLIMIT_STACK = 3
RLIM_INFINITY = -1
__doc__ = None
__file__ = '/home/olutobi/.local/lib/python3.6/site-packages/psutil/_psutil_linux.cpython-36m-x86_64-linux-gnu.so'
__name__ = 'psutil_linux'
__package__ = 'psutil'
def disk_partitions():
    'Return disk mounted partitions as a list of tuples including device, mount point and filesystem type'
    pass

def linux_prlimit():
    'Get or set process resource limits.'
    pass

def linux_sysinfo():
    'A wrapper around sysinfo(), return system memory usage statistics'
    pass

def net_if_duplex_speed():
    'Return duplex and speed info about a NIC'
    pass

def proc_cpu_affinity_get():
    'Return process CPU affinity as a Python long (the bitmask).'
    pass

def proc_cpu_affinity_set():
    'Set process CPU affinity; expects a bitmask.'
    pass

def proc_ioprio_get():
    'Get process I/O priority'
    pass

def proc_ioprio_set():
    'Set process I/O priority'
    pass

def set_testing():
    'Set psutil in testing mode'
    pass

def users():
    'Return currently connected users as a list of tuples'
    pass

version = 547
