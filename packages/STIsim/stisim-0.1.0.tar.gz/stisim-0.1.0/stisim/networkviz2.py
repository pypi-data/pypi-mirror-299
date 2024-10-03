import numpy as np
import sciris as sc
import pylab as pl
import starsim as ss
import stisim as sti


class networkviz(ss.Analyzer):
    def __init__(self, layout='parallel'):
        super().__init__()
        self.ti = []
        self.data = []
        self.layout = layout
        return
    
    def init_pre(self, sim):
        self.count = 0
        self.yearvec = sim.yearvec
        return
        
    def apply(self, sim):
        self.ti.append(sim.ti)
        self.data.append(sim.networks[0].to_df())
        self.count += 1
        self.fem = sim.people.female.raw
        self.age = sim.people.age.raw
        self.order = np.argsort(self.age)
        
        self.rorder = np.zeros(len(self.order))
        self.rorder[self.order] = np.arange(len(self.order))

        
        n = len(sim.people)
        self.a = np.arange(n)
        if self.layout == 'square':
            sqn = np.floor(np.sqrt(n))
            self.x = self.rorder // sqn
            self.y = self.rorder % sqn
        elif self.layout == 'circle':
            const = 2*np.pi/n
            self.x = np.cos(self.rorder*const)
            self.y = np.sin(self.rorder*const)
        elif self.layout == 'parallel':
            self.x = self.fem + np.random.randn(n)*0.1
            self.y = self.rorder/self.rorder.max()*self.age.max()
        return
        
    def plot(self):
        sc.options(dpi=200)
        pl.set_cmap('turbo')
        fig = pl.figure(figsize=(10,12))
        
        for i in range(self.count):
            pl.cla()
            pl.title(f't = {self.yearvec[i]} ({self.ti[i]})')
            pl.xticks([0,1], ['Male', 'Female'])
            pl.ylabel('Age')
            for tf,marker in enumerate(['s','o']):
                inds = sc.findinds(self.fem, tf)
                pl.scatter(self.x[inds], self.y[inds], color=sc.vectocolor(self.age[inds]), marker=marker)
            d = self.data[i]
            for p1,p2 in zip(d.p1, d.p2):
                x = [self.x[p1], self.x[p2]]
                y = [self.y[p1], self.y[p2]]
                pl.plot(x, y, lw=0.1, alpha=0.5, c='k')
            pl.pause(0.1)
        return fig


if __name__ == '__main__':
    
    nv = networkviz()
    nw = ['random', sti.StructuredSexual()][1]
    sim = ss.Sim(n_agents=500, networks=nw, analyzers=nv, copy_inputs=False, dt=1/12)
    sim.run()
    nv.plot()