import sys
import select
import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt


def main():
    plt.ion()
    fig, ax = plt.subplots()
    ax.set_xlabel("step")
    ax.set_ylabel("loss")
    ax.set_yscale("log")
    ax.set_title("Real-time loss (log-scale, waiting for data…)")

    plt.show(block=False)
    fig.canvas.start_event_loop(0.1)

    xs, ys = [], []
    step = 0
    fd = sys.stdin.fileno()

    while True:
        # wait up to 0.1s for stdin
        rlist, _, _ = select.select([fd], [], [], 0.1)

        if rlist:
            line = sys.stdin.readline()
            if not line:
                break
            try:
                y = float(line.strip())
            except ValueError:
                continue

            # skip non-positive values (log axis can’t handle <= 0)
            if y <= 0:
                continue

            step += 1
            xs.append(step)
            ys.append(y)

            ax.clear()
            ax.set_xlabel("step")
            ax.set_ylabel("loss")
            ax.set_yscale("log")
            ax.plot(xs, ys, "-o", markersize=4, color="tab:blue")

            # annotate each point
            for x_pt, y_pt in zip(xs, ys):
                ax.annotate(
                    f"{y_pt:.4g}",
                    xy=(x_pt, y_pt),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    fontsize=8,
                    color="black",
                )

            ax.set_title(f"Last loss = {y:.4g}")

            fig.canvas.draw()

        # always process GUI events
        fig.canvas.start_event_loop(0.01)

    plt.ioff()
    plt.show()


if __name__ == "__main__":
    main()
