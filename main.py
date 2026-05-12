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
        ins= (self.b/2.0)* ((self.b*(1-m)/denom+1.0)**2 *p**2-self.C)
        m_next = np.tanh((beta/2.0)*ins)
        return p_next, m_next

    def simulation(self, beta, n= 12000,block=3000, p0=0.1, m0=-0.8):
        trajectory = np.zeros((n,2))
        p,m = p0,m0
        for t in range(n):
            trajectory[t]= [p,m]
            p,m = self.cobweb_next(p,m,beta)
        return trajectory[block:]
    def plot_attractor(self, beta, output_dir='output', n_points=None):
       
        trajectory = self.simulation(beta, n=12000, block=3000)
        if n_points is not None:
            trajectory = trajectory[:n_points]
        plt.figure(figsize=(12, 10))
      
        scatter = plt.scatter(trajectory[:, 0], trajectory[:, 1], s=20, alpha=0.7, c=range(len(trajectory)), cmap='viridis', edgecolors='none')
        plt.title(f'Attractor - Beta = {beta} (Brock and Hommes 1997)', fontsize=14, fontweight='bold')
        plt.xlabel(r'$p_t$ (Price)', fontsize=12)
        plt.ylabel(r'$m_t$ (Rational fraction)', fontsize=12)
      
        x_min, x_max = trajectory[:, 0].min(), trajectory[:, 0].max()
        y_min, y_max = trajectory[:, 1].min(), trajectory[:, 1].max()
        
        x_margin = (x_max - x_min) * 0.15 if (x_max - x_min) > 0 else 0.1
        y_margin = (y_max - y_min) * 0.15 if (y_max - y_min) > 0 else 0.1
        plt.xlim(x_min - x_margin, x_max + x_margin)
        plt.ylim(y_min - y_margin, y_max + y_margin)
        
        plt.grid(True, alpha=0.3, linestyle='--')
        plt.axhline(0, color='red', lw=1.5, alpha=0.5, label='Neutral')
        plt.axvline(0, color='red', lw=1.5, alpha=0.5)
        plt.colorbar(scatter, label='Time progression')
        plt.tight_layout()
       
        filename = os.path.join(output_dir, f'attractor_beta_{beta:.2f}.png')
        plt.savefig(filename, dpi=200, bbox_inches='tight')
        print(f"Salvato: {filename} - Range: p_t=[{x_min:.4f}, {x_max:.4f}], m_t=[{y_min:.4f}, {y_max:.4f}]")
        plt.close()
        
    def plot_time_series(self, beta, output_dir='output', n=200):
        trajectory = self.simulation(beta, n=12000, block=3000)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))
        ax1.plot(trajectory[:n, 0], linewidth=1.5)
        ax1.set_title(f'Prezzi $p_t$ - Beta={beta}')
        ax1.grid(True, alpha=0.3)
        ax2.plot(trajectory[:n, 1], linewidth=1.5, color='orange')
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
    betas = [ 4.0,4.3,5.0 ,6.0, 10.0]
    for beta in betas:
        print(f"Generando grafici per beta={beta}")
        sim.plot_attractor(beta, output_dir=output_dir)
        sim.plot_time_series(beta, output_dir=output_dir, n=200)
        
