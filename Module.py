import atexit
import pycuda.gpuarray as garray
import pycuda.driver as cuda
import tools.parray as parray
import Network as nn
import numpy as np

"""
Can you please construct an object-oriented PyCUDA implementation of a network
of ML neurons randomly connected by alpha function synapses (similar to the
IAF network you implemented for E9070) that we can use for testing the
architecture?
I imagine that a standard numerical ODE solver such as low-order Runge-Kutta
should be sufficient for simulating the network.
Also, I'm not sure what dynamics we should expect to observe for such a
network. You may need to talk to Yiyin or Nikul for further information about
both of these points.
"""
class Module:

    def __init__(self, manager, dt, num_in_non, num_in_spike, num_proj_non,
                 num_proj_spike, dev):
        """
        Interface between LPU and architecture.
            Parameters
            ----------
            in_non_list : list of numpy.ndarray of numpy.float64
                States (membrane voltages) of external non-spiking neurons
                presynaptic to the module at the current time.
            in_spike_list : list of numpy.ndarray of numpy.int32
                Indices of external spiking neurons presynaptic to the module
                that emitted a spike at the current time.
            pro_non : numpy.ndarray of numpy.float64
                States (membrane voltages) of non-spiking projec- tion neurons
                at current time.
            proj_spike : numpy.ndarray of numpy.int32
                Indices of spiking projection neurons that emitted a spike at
                the current time.
            param : list
                List of variables to configure the LPU.
            dev : int
                Indicates which GPU device will be used by this module.
        """

        ctx = cuda.Device(dev).make_context()
        atexit.register(ctx.pop)

        self.network = nn.Network(dt)
        self.manager = manager
        self.running = True
        self.dt = dt

        if num_in_non > 0:
            self.in_non_list = parray.to_gpu(np.ones([1, num_in_non]))
        else:
            self.in_non_list = None
        if num_in_spike > 0:
            self.in_spike_list = parray.to_gpu(np.ones([1, num_in_spike]))
        else:
            self.in_spike_list = None

        self.proj_non = []
        self.proj_spike = []

    def __run_step(self, in_non_list, in_spike_list, proj_non, proj_spike):

        self.network.run_step(in_non_list, in_spike_list, proj_non, proj_spike)

    def __sync(self):

        # receive input from outside
        I_ext = parray.to_gpu(np.ones([1, num_in_non]))
        self.in_non_list = int(I_ext.gpudata) + I_ext.dtype.itemsize
        self.in_spike_list = None

        # send output
        self.proj_non
        self.proj_spike

    def start(self):

#        proj_non = np.empty((1, len(self.proj_non)), np.double)
#        proj_spike = np.empty((1, len(self.proj_spike)), np.double)
        dt = self.dt

        I_ext = parray.to_gpu(np.ones([1 / dt, 4608]))
        out = np.empty((1 / dt, 4608), np.double)

        for i in range(int(1 / dt)):
            self.__run_step(int(I_ext.gpudata) + \
                                        I_ext.dtype.itemsize * \
                                        I_ext.ld * i, None, out[i, :], None)

#        while(self.running):
#            self.__run_step(self.in_non_list, self.in_spike_list, proj_non,
#                       proj_spike)
#            self.proj_non.append(proj_non)
#            self.proj_spike.append(proj_spike)
#            __sync()
