from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap

from analytics.graphs import plot_line_len
from analytics.graphs import plot_scale
from analytics.graphs import plot_angle
from fractals.koch.curve import Curve
from ui.generated.several_phases import Ui_MainWindow
from settings import STATIC_PATH


class SeveralPhasesUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graph_type = None

        # make default settings
        self.lb_image.setPixmap(QPixmap(str(STATIC_PATH / 'several_phases_model.png')))

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculate)

    def _calculate(self) -> None:
        """

        :return:
        """
        settings = {
            'model': 'several',
            'count_iterations': self.sb_count_iterations.value(),
            'coefficient_a': self.dsb_several_phase_coefficient_a.value(),
            'coefficient_h': self.dsb_several_phase_coefficient_h.value()
        }

        several_phases_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                     self.dsb_angle.value(), **settings)
        several_phases_model.build()

        if self.graph_type == 'len':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_line_len(several_phases_model.lines[self.sb_count_iterations.value():],
                          self.sb_count_iterations.value())
        elif self.graph_type == 'span':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_scale(several_phases_model.lines[self.sb_count_iterations.value():],
                       self.sb_count_iterations.value())
        elif self.graph_type == 'angle':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_angle(several_phases_model.lines[self.sb_count_iterations.value():],
                       self.sb_count_iterations.value(), self.dsb_angle.value())
        else:
            raise TypeError('unknown graph type')
