import numpy as np
import matplotlib.pyplot as plt

## Implementing Qubit

class Qubit:
    @property
    def theta(self):
        return 2*np.arccos(self.a)

    @property
    def phi(self):   
        return np.arctan2(self.b.imag, self.b.real)

    @property
    def x(self):
        return np.sin(self.theta)*np.cos(self.phi)

    @property
    def y(self):
        return np.sin(self.theta)*np.sin(self.phi)

    @property
    def z(self):
        return np.cos(self.theta)

    def __init__(self):
        # theta e phi from Bloch Sphere
        # a e b from wave function
        # Default: |0⟩ - ket 0
        self.a = 1.0
        self.b = 0.0+0.0j
        # self.theta = 0.0
        # self.phi = 0.0
        # self.x = 0
        # self.y = 0
        # self.z = 1

    def wf(self):
        # return of vector from wave function 
        return np.array([[self.a],[self.b]])

    def __repr__(self):
        return str(self.wf())

    def set_bs(self, theta, phi):
        # assign values to a, b from theta, phi
        # ensure theta & phi are consistent with the spherical representation and calculate a e b 
        if not(0.0 <= theta <= np.pi):
            theta = np.pi = theta%np.pi
        if not(-np.pi <= phi <= np.pi):
            phi = phi%(2*np.pi) - 2*np.pi
        self.a = np.cos(theta/2) #já está com a fase zerada
        self.b = np.sin(theta/2)*np.exp(1j*phi)

    def set_pa(self, a, b):
        # assign values to a, b
        aux = np.abs(a)**2 + np.abs(b)**2
        self.a = np.sqrt(np.abs(a)**2/aux)
        self.b = np.sqrt(np.abs(b)**2/aux)*(b/np.abs(b))*(np.abs(a)/a)

    def set_wf(self, colvec):
        # from column vector, assign values to a, b
        a = colvec[0,0]
        b = colvec[1,0]
        self.set_pa(a, b)

    @staticmethod
    def plot(*args, **kwargs):
        def repel_from_center(x, y, z, m=0.1):
            return x + (-m if x < 0 else m), \
                    y + (-m if y < 0 else m), \
                    z + (-m if z < 0 else m)
        def bloch_sphere():
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            u = np.linspace(0, 2*np.pi, 30)
            v = np.linspace(0, np.pi, 20)
            x = 1 * np.outer(np.cos(u), np.sin(v))
            y = 1 * np.outer(np.sin(u), np.sin(v))
            z = 1 * np.outer(np.ones(np.size(u)), np.cos(v))
            ax.plot_wireframe(x, y, z, color='gray', linestyle=':')
            ax.plot3D([-1, 1], [0, 0], [0, 0], color='k', linestyle='--')
            ax.text(-1.1, 0, 0, '$|-\\rangle$', 'x', horizontalalignment='right', \
                fontweight='bold', fontsize=11)
            ax.text(1.1, 0, 0, '$|+\\rangle$', 'x', horizontalalignment='left', \
                fontweight='bold', fontsize=11)
            ax.plot3D([0, 0], [-1, 1], [0, 0], color='k', linestyle='--')
            ax.text(0, -1.1, 0, '$|-i\\rangle$', 'y', horizontalalignment='right', \
                fontweight='bold', fontsize=11)
            ax.text(0, 1.1, 0, '$|i\\rangle$', 'y', horizontalalignment='left', \
                fontweight='bold', fontsize=11)
            ax.plot3D([0, 0], [0, 0], [-1, 1], color='k', linestyle='--')
            ax.text(0, 0, -1.1, '$|1\\rangle$', 'x', horizontalalignment='center', \
                fontweight='bold', fontsize=11)
            ax.text(0, 0, 1.1, '$|0\\rangle$', 'x', horizontalalignment='center', \
                fontweight='bold', fontsize=11)
            limits = np.array([getattr(ax, f'get_{axis}lim')() \
                for axis in 'xyz'])
            ax.set_box_aspect(np.ptp(limits, axis = 1))
            ax._axis3don = False
            return ax
        if kwargs.get('title', False):
            title = kwargs['title']
        else:
            title = ''
        ax = bloch_sphere()
        for arg in args:
            label, color = '| ', 'r'
            if type(arg) == tuple:
                if len(arg) == 3: color = arg[2]
                label = '$|' + arg[1] + '\\rangle$'
                arg = arg[0]
            ax.quiver(0, 0, 0, arg.x, arg.y, arg.z, color=color)
            ax.text(*repel_from_center(arg.x, arg.y, arg.z), label, 'x', \
                horizontalalignment='center', fontweight='bold', fontsize=11, \
                color=color)
        plt.title(title)
        plt.show()

# lines to run just when this script is running, if there's another script importing a qubit from the original script, this snippet won't run
if __name__ == "__main__":
    q = Qubit()
    print(q)
    # q.set_bs(50*2*np.pi+3/2*np.pi, 50*2*np.pi+3/2*np.pi)
    # q.set_pa(-1j*np.sqrt(2)/2, (np.sqrt(2)/2))
    q.set_pa(np.sqrt(25), np.sqrt(75))
    # print(q.a, q.b)
    # print(np.sqrt(2)/2, 1j*np.sqrt(2)/2)
    Qubit.plot((q, 'ψ', 'b'), title='My first qubit')