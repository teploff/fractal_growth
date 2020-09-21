from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap

from analytics.graphs import plot_line_len_single_several_phases
from fractals.koch.curve import Curve
from ui.generated.single_several import Ui_MainWindow
from settings import STATIC_PATH


class SingleSeveralPhasesUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graph_type = None

        # make default settings
        self.lb_image_single_phase.setPixmap(QPixmap(str(STATIC_PATH / 'single_phase_model.png')))
        self.lb_image_several_phases.setPixmap(QPixmap(str(STATIC_PATH / 'several_phases_model.png')))

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculate)

    def _calculate(self) -> None:
        """

        :return:
        """
        settings = dict()
        settings["model"] = "single"
        settings["count_iterations"] = self.sb_count_iterations.value()
        single_phase_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                   self.dsb_angle.value(), **settings)
        single_phase_model.build()

        settings["model"] = "several"
        settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
        settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
        settings["count_iterations"] = int(self.sb_count_iterations.value())
        several_phase_model_1 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                      self.dsb_angle.value(), **settings)
        several_phase_model_1.build()

        settings["count_iterations"] = int(self.sb_count_iterations.value() - 30)
        several_phase_model_2 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                      self.dsb_angle.value(), **settings)
        several_phase_model_2.build()

        if self.graph_type == 'line':
            # escape line growth phases, so lines = lines[count_iter:] and ect
            plot_line_len_single_several_phases(
                single_phase_model.lines[self.sb_count_iterations.value():],
                several_phase_model_1.lines[self.sb_count_iterations.value():],
                several_phase_model_2.lines[self.sb_count_iterations.value() - 30:],
                self.sb_count_iterations.value(),
                self.dsb_max_line_legth.value()
            )
        elif self.graph_type == 'span':
            pass
        else:
            raise TypeError('unknown graph type')
