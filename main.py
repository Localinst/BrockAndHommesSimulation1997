import numpy as np
import matplotlib.pyplot as plt
import os

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
        # 3.8 formula
        
        noise = np.random.uniform(-0.02, 0.02)
        p_realized = p_next + noise
        # noise citato nel paper uniforme tra -0.02 e 0.02
        
        profit_rational = (self.b  / 2.0)*(p_realized**2)-self.C
        profit_naive = (self.b / 2.0)* p * (2*p_next - p)
        # formula 3.4 
        
        ins= profit_rational - profit_naive
        m_next = np.tanh((beta/2.0)*ins)
        #3.9 formula
        return p_next, m_next

    def simulation(self, beta, n= 12000,block=100, p0=0.1, m0=-0.8):
        trajectory = np.zeros((n,2))
        p,m = p0,m0
        for t in range(n):
            trajectory[t]= [p,m]
            p,m = self.cobweb_next(p,m,beta)
        return trajectory[block:]
    def plot_attractor(self, beta, output_dir='output', n_points=None):
       
        trajectory = self.simulation(beta, n=12000, block=100)
        if n_points is not None:
            trajectory = trajectory[:n_points]
        
        print(f"Beta {beta}: {len(trajectory)} punti nel trajectory")
        
        plt.figure(figsize=(12, 10))
        plt.scatter(trajectory[:, 0], trajectory[:, 1], s=8, color='black', alpha=0.6, rasterized=True)
        plt.title(f'Attractor - Beta = {beta} (Brock and Hommes 1997)', fontsize=14, fontweight='bold')
        plt.xlabel(r'$p$ (Price)', fontsize=12)
        plt.ylabel(r'$m$ (Rational fraction)', fontsize=12)
        plt.xlim(-2, 2)
        plt.ylim(-1.1, 1.1)
        
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.axhline(0, color='black', lw=0.6, alpha=0.3)
        plt.axvline(0, color='black', lw=0.6, alpha=0.3)
        plt.tight_layout()
        
        filename = os.path.join(output_dir, f'attractor_beta_{beta:.2f}.png')
        plt.savefig(filename, dpi=200, bbox_inches='tight')
        print(f"Salvato: {filename} - Attractor con {len(trajectory)} punti")
        plt.close()
        
    def plot_time_series(self, beta, output_dir='output', n=200):
        trajectory = self.simulation(beta, n=12000, block=100)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        ax1.plot(trajectory[:n, 0], linewidth=1.5)
        ax1.set_ylim(-2, 2)
        ax1.set_title(f'Prezzi $p_t$ - Beta={beta}')
        ax1.grid(True, alpha=0.3)
        ax2.plot(trajectory[:n, 1], linewidth=1.5, color='orange')
        ax2.set_ylim(-1.1, 1.1)
        ax2.set_title(f'Frazione razionali vs naive $m_t$ - Beta={beta}')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
       
        filename = os.path.join(output_dir, f'timeseries_beta_{beta:.2f}.png')
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        print(f"Salvato: {filename}")
        plt.close()
if __name__ == "__main__":
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    print("Simulazione in corso")
    sim = BrockHommes(B=0.5, b=1.35, C=1.0)
    betas = [0.5, 0.77, 1.0, 2.0, 3.0, 4.0, 4.77 ,5.0 , 10.0,20.0]
    for beta in betas:
        print(f"Generando grafici per beta={beta}")
        sim.plot_attractor(beta, output_dir=output_dir)
        sim.plot_time_series(beta, output_dir=output_dir, n=200)
        
        
# β₁ ≈ 0.7777
# β₂ ≈ 4.76