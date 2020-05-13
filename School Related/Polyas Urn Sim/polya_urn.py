# Polya urn simulation
# Oliver Tsang, May 2020

# This is a quick simulation of the Polya Urn martingale
# discussed in my class on stochastic processes (Math 23500).
# I run the simulation several times and plot the output to help
# visualize the behavior of Polya's Urn.
#
# Polya's Urn:
#     Start with a green ball and a red ball in an urn.
#     At each step, pull a ball at random and replace it
#     -- but add to the urn another ball of the same color.
#
# Somewhat surprisingly, the distribution of red/green balls does
# not always tend towards 0/1 or 1/0, or even towards an even split
# (despite the mathetmatically expected fraction of 1/2).
# As the simulations show, the stable distribution is more evenly
# distributed than may be expected.

import numpy as np
import matplotlib.pyplot as plt

class Urn():
    def __init__(self, red=1, green=1):
        """Initialize balls and history array"""
        self.reds   = red
        self.greens = green
        self.red_hist   = np.array([red], dtype=np.int)
        self.green_hist = np.array([green], dtype=np.int)

        # Save the initialization details
        self.init_cnt = red+green
        self.init_red = red
        self.init_green = green

    def reset(self):
        """Reset the system to the initial conditions"""
        self.reds   = self.init_red
        self.greens = self.init_green
        self.red_hist   = np.array([self.init_red], dtype=np.int)
        self.green_hist = np.array([self.init_green], dtype=np.int)

    def pull_ball(self):
        """Pull a ball at random and return one with the same color"""
        rn = np.random.random()
        is_red = rn*(self.reds + self.greens) < self.reds
        if is_red:
            self.reds += 1
        else:
            self.greens += 1
        self.red_hist = np.append(self.red_hist, self.reds)
        self.green_hist = np.append(self.green_hist, self.greens)

    def run_sim(self, steps):
        """Pull a ball from the urn <steps> times"""
        for n in range(steps):
            self.pull_ball()

    def plot_frac(self, existing_fig=None):
        """Create a pretty pic but don't plot yet so we can add to the figure"""
        n = self.reds+self.greens-self.init_cnt+1
        ns = np.arange(n)
        if existing_fig is None:
            fig = plt.figure()
            axes = fig.add_axes([0.1,0.1, 0.8, 0.8])
            axes.set_ylim([0, 1])
        else:
            fig = existing_fig
            axes = fig.axes[0]
        axes.plot(ns, self.red_hist/(ns+self.init_cnt), label = "Reds", color='r')
        axes.plot(ns, self.green_hist/(ns+self.init_cnt), label = "Greens", color='g')
        return fig

    def run_plot(self, steps):
        """Just run once and plot the output"""
        self.run_sim(steps)
        self.plot_frac()
        plt.show()

    def run_n_plot(self, iters, steps):
        fig = None
        terminal_green = []
        terminal_red   = []
        # Run and add results to the figure
        for i in range(iters):
            self.run_sim(steps)
            tot = self.reds + self.greens
            terminal_red.append(self.reds / tot)
            terminal_green.append(self.greens / tot)
            fig = self.plot_frac(fig)
            self.reset()
        plt.ylabel("Fraction of green and red")
        plt.xlabel("Steps")
        plt.title("Simulations of the Polya urn")

        # Plot the distribution of the final red/green breakdown
        fig2 = plt.figure()
        axes2 = fig2.add_axes([0.1, 0.1, 0.8, 0.8])
        size = 0.05
        plt.hist(np.array(terminal_red), bins = np.arange(0, 1+size, size))
        plt.title("Distribution of terminal fractions of red balls")
        plt.xlabel("Fraction of red balls")
        plt.ylabel("Count")

        plt.show()

if __name__=="__main__":
    urn = Urn(1,1) # interesting to see Urn(10, 1)
    urn.run_n_plot(20, 1000)
