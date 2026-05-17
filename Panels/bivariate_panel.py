from Distributions.Multivariate_normal import binorm


def draw_bivariate(input_frame, fig, canvas):
    fig.clear()
    ax = fig.add_subplot(111, projection='3d')
    binorm(ax)
    canvas.draw()
