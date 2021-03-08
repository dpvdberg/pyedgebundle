from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class EBCanvas(FigureCanvas):
    def __init__(self):
        fig = Figure()
        self.axes = fig.add_subplot(111)
        super(EBCanvas, self).__init__(fig)