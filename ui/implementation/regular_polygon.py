from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap

from analytics.graphs import plot_line_len
from analytics.graphs import plot_scale
from analytics.graphs import plot_angle
from fractals.koch.curve import Curve
from ui.generated.regular_polygon import Ui_MainWindow
from settings import STATIC_PATH


class RegularPolygonUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graph_type = None

        # make default settings
        # TODO: pictures
        self.lb_image.setPixmap(QPixmap(str(STATIC_PATH / 'several_phases_model.png')))

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculate)

    def _calculate(self) -> None:
        """

        :return:
        """
        settings = {
            'model': 'regular_polygon',
            'count_iterations': self.sb_count_iterations.value(),
            'count_angles': self.sb_regular_polygon_count_angle.value(),
            'building_way': "inside" if self.rb_regular_polygon_build_inside.isChecked() else "outside"
        }

        regular_polygon_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                      self.dsb_angle.value(), **settings)
        regular_polygon_model.build()

        if self.graph_type == 'len':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_line_len(regular_polygon_model.lines[self.sb_count_iterations.value():],
                          self.sb_count_iterations.value())
        elif self.graph_type == 'scale':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_scale(regular_polygon_model.lines[self.sb_count_iterations.value():],
                       self.sb_count_iterations.value())
        elif self.graph_type == 'angle':
            # escape line growth phases, so lines = lines[count_iter:]
            plot_angle(regular_polygon_model.lines[self.sb_count_iterations.value():],
                       self.sb_count_iterations.value(), self.dsb_angle.value())
        else:
            raise TypeError('unknown graph type')
