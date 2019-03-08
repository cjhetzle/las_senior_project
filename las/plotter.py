#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from src.load_func import load_function
a = []

plt.style.use('dark_background')


def savefig(ax, name):
    ax.get_figure().savefig(name, bbox_inches="tight", dpi=300, transparent=True)


load_curve = np.load("schedule.npy")
load_curve /= max(load_curve)

# Load curve only
now = datetime.now().timestamp()
week = 60*60*24*7
load_function_data = np.vectorize(load_function)(np.arange(now, now + week))
load_function_data /= max(load_function_data)
fig, ax = plt.subplots()
ax.plot(load_function_data, color='orange')
savefig(ax, "load_curve_only.png")

fig, ax = plt.subplots()
ax.plot(load_curve/max(load_curve), color='white')
savefig(ax, "schedule-only.png")

ax.plot(load_function_data, color='orange')
savefig(ax, "both.png")
