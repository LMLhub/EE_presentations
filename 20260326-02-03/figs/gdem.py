import matplotlib.pyplot as plt
import numpy as np

# Generate the data
# Set seed for reproducibility
np.random.seed(1)

# Set parameters
mu=.05
sigma=np.sqrt(0.2)
N=20
Tmax = 100
dt=1
t=np.arange(0,Tmax+dt,dt)
T=len(t)
sdt=np.sqrt(dt)

#generate Brownian motion
noise = np.random.normal(loc=(mu-0.5*sigma*sigma)*dt, scale=sigma*sdt, size=(T,N))
noise[0,:] = 0.0
Y = np.cumsum(noise, axis=0) # log wealth
X = np.exp(Y) # wealth
max_X = np.max(X, axis=1)/N
finite_ensemble_average = np.mean(X, axis=1)
ensemble_average = np.exp(mu*t)
time_average = np.exp((mu-0.5*sigma*sigma)*t)
tc = 2.0*np.log(N)/(sigma*sigma)
 
# GDP and DDP
GDP = finite_ensemble_average
DDP = np.exp(np.mean(Y, axis=1))

# Plot trajectories
fig, ax = plt.subplots(1,1)
#ax.semilogy(t, finite_ensemble_average, label=r'$\langle x(t) \rangle_N$', linewidth=3, color='C0')
#ax.semilogy(t, max_X, label=r'$\frac{1}{N}\max\left\{x_i(t)\right\}$', linewidth=1, color='orange')
ax.semilogy(t, X[:,0], color='lightgrey', linewidth=0.75, label="$x_i(t)$")
ax.semilogy(t, X[:,1:], linewidth=0.75, color='lightgrey') # no label
#ax.semilogy([tc,tc], [1E-15,1E15], color='black', linestyle=':',label="$t=t_c$")
ax.semilogy(t, ensemble_average, label=r'$\exp(\mu t)$', color='C2')
ax.semilogy(t, time_average, label=r'$\exp((\mu-\sigma^2/2) t)$', color='C1')
#ax.semilogy(t[1:], np.exp((mu-sigma**2/2-np.log(N)/t[1:]+(np.sqrt(2*np.log(N))*sigma)/np.sqrt(t[1:]))*t[1:]), label=r'$x(0)\exp\left(\left(\mu-\frac{\sigma^2}{2}-\frac{\ln(N)}{t}+\frac{\sqrt{2\ln N}\sigma}{t^{1/2}}\right) t\right)$', color='C3')

# add GDP
ax.semilogy(t, DDP, color='blue', label=r'$\exp(g_\text{dem}(t)t)$')

# Labels, legends, etc.
ax.set_xlabel('time $t$')
ax.set_ylabel('wealth $X(t)$')
ax.set_title(rf"GBM: $x(0)=1$, $\mu={mu:.2f}$, $\sigma={sigma:.2f}$")
ax.legend(loc='lower left', ncol=1, facecolor='white', framealpha=1, fontsize=7)
tlim = [0, Tmax]
ax.set_xlim(tlim)
Xlim = [1E-7, 1E3]
ax.set_ylim(Xlim)

# Apply final tweaks and save figure as pdf
ratio = 0.7
size = fig.get_size_inches()[0]
fig.set_size_inches(size, size*ratio)
plt.savefig('gdem.pdf', bbox_inches='tight', pad_inches=0)