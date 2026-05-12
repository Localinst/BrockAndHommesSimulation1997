import numpy as np
import matplotlib.pyplot as plt

class BrockHommes:
    def __init__ ( self, B=0.5, b=1.35, C=1.0):
        self.B =B
        self.b= b 
        self.C = C
    def cobweb_next (self, p,m,beta):
        # p = price
        # m = difference fractions
        # beta = Intensity of choice
        # B = question slope
        # b = offer slope
        # C = Information cost
        # A = Intercept question
        denom= 2*self.B + self.b * (1+m)
        p_next = -self.b * (1-m)*p/denom
        ins= (self.b/2.0)* ((self.b*(1-m)/denom+1.0)*p**2-self.C)
        m_next = np.tanh((beta/2.0)*ins)
        return p_next, m_next

    def simulation(self, beta, n= 12000,block=3000, p0=0.1, m0=-0.8):
        trajectory = np.zeros((n,2))
        p,m = p0,m0
        for t in range(n):
            trajectory[t]= [p,m]
            p,m = self.cobweb_next(p,m,beta)
        return trajectory[block:]
    def plot_attractor(self,beta):
        trajectory = self.simulation(beta)
        plt.figure(figsize=(10,8))
        plt.plot(trajectory[:,0], trajectory[:,1], ',', alpha=0.6, ms=1)
        plt.title(f'Attractor - Beta = {beta} (Brock and hommes 1997)')
        plt.xlabel(r'\( p_t \)')
        plt.ylabel(r'\( m_t \)')
        plt.grid(True, alpha=0.3)
        plt.axhline(0,color='k', lw=0.5)
        plt.axvline(0,color='k',lw=0.5)
        plt.show()
        
    def plot_time_series(self, beta, n=12000):
        trajectory = self.simulation(beta, n=12000, block=3000)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        ax1.plot(trajectory[:n, 0]); ax1.set_title(f'prezzi p_t - beta={beta}'); ax1.grid(True)
        ax2.plot(trajectory[:n, 1]); ax2.set_title(f'm_t (razionali - naive)  - beta = {beta}'); ax2.grid(True)
        plt.tight_layout()
        plt.show()
if __name__ == "__main__":
    print("Simulazione in corso")
    sim = BrockHommes(B=0.5, b=1.35, C=1.0)
    betas = [2.0, 2.73, 2.8, 10.0]
    for beta in betas:
        print(f"Generando grafici per beta={beta}")
        sim.plot_attractor(beta)
        sim.plot_time_series(beta, n=12000)
        