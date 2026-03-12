import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from shared.plotting import set_style, apply_tweaks, tplot

# First define the transformations that can be applied to each axis

def tlin(x):
    return x

def tlog(x):
    return np.log10(x)

def g_individual(g,r):
   return np.sqrt(g**2 - r**2)

def g_cooperative(g,r):
   return np.sqrt(g*np.sqrt(g**2 - r**2))


def plot_farmers_fable(g: float, r: float, n_paths: int, n_steps: int) -> plt.Figure:
  # Plot some trajectories of the farmer's fable
  X1 = np.zeros((n_paths, n_steps))
  X2 = np.zeros((n_paths, n_steps))

  steps =np.linspace(1.0, n_steps+1, n_steps)
  gbar2 = g_cooperative(g,r)
  MLtrajectory = [100*gbar2**(n-1) for n in steps]
  for n in range(n_paths):
    outcomes1 = np.random.choice([g+r, g-r], size=n_steps, p=[0.5, 0.5])
    outcomes2 = np.random.choice([g+r, g-r], size=n_steps, p=[0.5, 0.5])
    X1[n, 0] = 100
    X2[n, 0] = 100
    for t in range(1, n_steps):
      X1[n, t] = X1[n, t-1] * 0.5*(outcomes1[t-1] + outcomes2[t-1])
      X2[n, t] = X1[n, t]

  fig, ax = plt.subplots(figsize=(9, 4))
  for n in range(n_paths):
    if n == 1:
       L = "A/B trajectories"
    else:
       L=None
    ax = tplot(steps, X1[n,:], tlin, tlog, ax, xticks='linear',
               yticks='log', label = L, color="green", alpha=0.5)

  ax = tplot(steps, MLtrajectory, tlin, tlog, ax, xticks='linear',
             yticks='log', label = r"$\bar{g}_\text{coop}^t$", color="red", lw=2)

  # Turn on legend
  ax.legend(loc="upper left")
  # Label axes
  ax.set_xlabel('steps, t')
  ax.set_ylabel(r"wealth, $X_t$")
  # Set x axis range
  ax.set_xlim([0,n_steps])
  ax.set_ylim([-7,50])
  ax.set_title("With pooling and sharing")
  return fig, ax

def plot_farmers_fable_individual(g: float, r: float, n_paths: int, n_steps: int) -> plt.Figure:
  # Plot some trajectories of the farmer's fable
  X1 = np.zeros((n_paths, n_steps))
  X2 = np.zeros((n_paths, n_steps))

  steps =np.linspace(1.0, n_steps+1, n_steps)
  gbar1 = g_individual(g,r)
  MLtrajectory = [100*gbar1**(n-1) for n in steps]
  for n in range(n_paths):
    outcomes1 = np.random.choice([g+r, g-r], size=n_steps, p=[0.5, 0.5])
    outcomes2 = np.random.choice([g+r, g-r], size=n_steps, p=[0.5, 0.5])
    X1[n, 0] = 100
    X2[n, 0] = 100
    for t in range(1, n_steps):
      X1[n, t] = X1[n, t-1] * outcomes1[t-1]
      X2[n, t] = X2[n, t-1] * outcomes2[t-1]

  fig, ax = plt.subplots(figsize=(9, 4))
  for n in range(n_paths):
    if n == 1:
       L1 = "A trajectories"
       L2 = "B trajectories"
    else:
       L1=None
       L2=None
    ax = tplot(steps, X1[n,:], tlin, tlog, ax, xticks='linear',
               yticks='log', label = L1, color="green", alpha=0.5)
    ax = tplot(steps, X2[n,:], tlin, tlog, ax, xticks='linear',
               yticks='log', label = L2, color="blue", alpha=0.5)

  ax = tplot(steps, MLtrajectory, tlin, tlog, ax, xticks='linear',
             yticks='log', label = r"$\bar{g}_\text{indiv}^t$", color="red", lw=2)

  # Turn on legend
  ax.legend(loc="lower left")
  # Label axes
  ax.set_xlabel('steps, t')
  ax.set_ylabel(r"wealth, $X_t$")
  # Set x axis range
  ax.set_xlim([0,n_steps])
  ax.set_ylim([-100,10])
  ax.set_title("Without pooling and sharing")
  return fig, ax
