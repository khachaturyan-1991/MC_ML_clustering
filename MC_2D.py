from libraries import *;
import itertools
class MC2():
     
    def __init__(self,system_size=10, temperature=100, I1=1, I2=1):
        '''
        inputs:
        system_size: linear system size
        temperature: is ambient temperature
        I1, I2: exchange integrals of left/right and upper/down neighbors respectively
        '''
        self.N = system_size
        self.T = temperature
        self.config = self.generate_initialstate()
        self.I1, self.I2 = I1, I2
        self.cost = self.get_cost()

    def generate_initialstate(self):
        N = self.N
        config = 2*np.random.randint(2, size=(N,N))-1
        return config

    def get_cost(self):
        cost = {}
        for i, i11,i12,i21,i22 in product([-1,1], repeat=5):
            w = 2*i*((i11+i12)*self.I1 + (i21+i22)*self.I2)
            cost[f'{i}{i11}{i12}{i21}{i22}'] = np.exp(-w/self.T)
        return cost

    def get_energy(self, cfg):
        text = ''.join([str(c) for c in cfg])
        return self.cost[text]

    def make_switch(self, x):
        a,b = x
        N = self.N
        r=1
        if rand() < self.get_energy([self.config[a,b],\
                                    self.config[(a-1)%N,b],\
                                    self.config[(a+1)%N,b],\
                                        self.config[a,(b-1)%N],\
                                            self.config[a,(b+1)%N]]):
            r = -1
        return r

    def mcmove(self):
        N = self.N
        for i in range(N*N):
            a = np.random.randint(0, N)
            b = np.random.randint(0, N)
            ###
            x, y = a%N, b%N
            r = self.make_switch([x, y])
            self.config[x, y] = self.config[x, y]*r
            # n = N//6
            # X = [[(a+m*int(N/n))%N for m in range(n)], [(b+m*int(N/n))%N for m in range(n)]]
            # X = [x for x in itertools.product(*X)]
            # Y = list(map(self.make_switch, X))
            # for j,x in enumerate(X):
            #     self.config[x] = self.config[x]*Y[j]

    def plot_config(self):
        plt.figure()
        X, Y = np.meshgrid(range(self.N), range(self.N)) 
        plt.title(np.abs(np.mean(self.config)))
        plt.pcolormesh(X, Y, self.config, cmap=plt.cm.RdBu);