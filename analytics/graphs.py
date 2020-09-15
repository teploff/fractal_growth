import matplotlib.pyplot as plt


def _plot_graph_line_len(self) -> None:
    """
    # TODO: docstring
    :return:
    """
    # TODO: to name this shirt
    x_train = [i for i in range(len(self.koch_curve.lines))]
    y_train = [sum(line.len() for line in lines) for i, lines in enumerate(self.koch_curve.lines)]
    y = [sum(line.len() for line in lines) for i, lines in enumerate(self.koch_curve.lines)
         if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
    x = [i for i in range(len(self.koch_curve.lines)) if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
    x = x[1:]
    y = y[1:]
    x = np.array(x)
    y = np.array(y)
    x_train = np.array(x_train)
    y_train = np.array(y_train)

    [a, b], res1 = curve_fit(lambda x1, a, b: a * np.exp(b * x1), x_train, y_train, p0=[0.01285, 0.0351])

    y1 = a * np.exp(b * x_train)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label='Original data', markersize=5)
    ax.plot(x_train, y1)
    ax.set(xlabel='Число циклов роста фрактала, ед.', ylabel='Длина фрактальной линии, ед.')
    ax.grid(True)
    plt.show()