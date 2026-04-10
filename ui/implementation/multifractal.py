import math
import typing

import matplotlib.pyplot as plt
import numpy.linalg
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap

from analytics.graphs import plot_line_len
from analytics.graphs import plot_scale
from analytics.graphs import plot_angle
from fractals.koch.curve import Curve
from ui.generated.multifractal import Ui_MainWindow
from settings import STATIC_PATH
from geometry.entity_2d import Segment

CM = 1.0 / 2.54
A4_FIG_SIZE = (8.27, 11.69)

def bb(tau_q, pi: typing.List[float], li: typing.List[float], span: float, q: int):
    import numpy as np

    return np.sum([(pi[i] ** q) / ((li[i] / span) ** tau_q) for
                   i, _ in enumerate(pi)]) - 1


class MultifractalUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.graph_type = None

        # make default settings
        self.lb_image.setPixmap(QPixmap(str(STATIC_PATH / 'several_phases_model.png')))

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculate)
        self.pb_multifractal_graph_build.clicked.connect(self._build_graph)
        self.pb_several_multifractal_graph_build.clicked.connect(self._several_build_graph)

    def _calculate(self) -> None:
        """

        :return:
        """
        settings = {
            'model': 'several',
            'count_iterations': self.sb_count_iterations.value(),
            'coefficient_a': self.dsb_several_phase_coefficient_a.value(),
            'coefficient_h': self.dsb_several_phase_coefficient_h.value(),
            'max_val': self.dsb_max_line_legth.value(),
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

    @staticmethod
    def _calc_d(eps: float, pi: typing.List[float], q: int) -> float:
        sum_ = 0.0

        for i, _ in enumerate(pi):
            if q != 1:
                sum_ += pi[i] ** q
            else:
                sum_ += pi[i] * math.log(pi[i])

        if q != 1:
            return (math.log(sum_) / math.log(eps)) / (q - 1)
        else:
            return sum_ / math.log(eps)

    @staticmethod
    def _new_calc_d(pi: typing.List[float], li: typing.List[float], span: float, q: int) -> float:
        from scipy.optimize import fsolve
        import numpy as np

        a = fsolve(lambda tau_q: np.sum([(pi[i] ** q) / ((li[i] / span) ** tau_q) for i, _ in enumerate(pi)]) - 1, [20])
        # tau_q_list = []
        # sum_list = []
        # for tau_q in range(-10, 9):
        #     sum_list.append(bb(tau_q=tau_q, pi=pi, li=li, span=span, q=q))
        #     tau_q_list.append(tau_q)
        #
        # fig, ax = plt.subplots()
        #
        # ax.plot(tau_q_list, sum_list, 'o', c='black', linewidth=1)
        # # ax.plot(q_list, d_list_char, 'o', c='black', linewidth=1)
        #
        # ax.grid(True)
        #
        # ax.set_xlabel('tau(q), ед.', fontsize=20)
        # ax.set_ylabel('Сумма, ед.', fontsize=20)
        # ax.tick_params(axis='x', labelsize=15)
        # ax.tick_params(axis='y', labelsize=15)
        # plt.title(f'Сумма от q = {q}')
        #
        # plt.show()

        return a / (q-1)

    def _build_graph(self):
        model = 'several'
        # model = 'stochastic'
        settings = {
            'model': model,
            'max_val': self.dsb_max_line_legth.value(),
            'count_iterations': self.sb_count_iterations.value(),
            'coefficient_a': self.dsb_several_phase_coefficient_a.value(),
            'coefficient_h': self.dsb_several_phase_coefficient_h.value(),
            'max_char_val_from': self.dsb_rnd_max_characteristic_from.value(),
            'max_char_val_to': self.dsb_rnd_max_characteristic_to.value(),
        }

        several_phases_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                     self.dsb_angle.value(), **settings)
        several_phases_model.build()

        q_list = [q for q in range(self.sb_left_q.value(), self.sb_right_q.value() + 1)]

        iterations = [int(iteration) for iteration in self.te_iterations_growth.toPlainText().splitlines()]
        # Всегда добавляем половинную и последнюю итерации роста
        iterations.append((len(several_phases_model.lines) - 1)//2)
        iterations.append(len(several_phases_model.lines) - 1)

        d_lists, d_char_lists  = [], []
        for iteration in iterations:
            lines = several_phases_model.lines[iteration]

            total_sum = sum(line.len() for line in lines)
            # TODO: если мы хотим с массами
            total_sum_char = sum(line.weight for line in lines)

            l_i = [line.len() for line in lines]
            p_i = [line.len() / total_sum for line in lines]
            # TODO: если мы хотим с массами
            p_i_char = [line.weight / total_sum_char for line in lines]

            fractal_span = Segment(lines[0].start, lines[-1].finish).len()

            # TODO: Новый способ расчета D для многофазной модели
            d_list, d_list_char = [], []
            for q in q_list:
                value, value_ch = None, None
                if q != 1:
                    value = self._new_calc_d(p_i, l_i, fractal_span, q)
                    value_ch = self._new_calc_d(p_i_char, l_i, fractal_span, q)
                d_list.append(value)
                d_list_char.append(value_ch)

            # TODO: so ugly. Так как не нашли до сих пор способ посчиать для q = 1 D для массы и длины - аппроксимируем
            index = None
            for i, d in enumerate(d_list):
                if d is None:
                    index = i
                    break

            if index:
                d_list[index] = d_list[index - 1] + (d_list[index + 1] - d_list[index - 1]) / 2.0
                d_list_char[index] = d_list_char[index - 1] + (d_list_char[index + 1] - d_list_char[index - 1]) / 2.0
            # TODO: окончание аппроксимации

            # TODO: Старый способ расчета D для многофазной модели
            # d_list = [round(self._calc_d(self.dsb_max_line_legth.value()/fractal_span, p_i, q), 3) for q in q_list]
            # d_list_char = [self._calc_d(self.dsb_max_line_legth.value(), p_i_char, q) for q in q_list]
            d_lists.append(d_list)
            d_char_lists.append(d_list_char)

        fig, axs = plt.subplots(2, figsize=A4_FIG_SIZE, dpi=100)
        fig.subplots_adjust(top=0.975,bottom=0.05,left=0.1,right=0.995,hspace=0.215,wspace=0.2)

        axs[0].set_title(f'Итерация роста - {iterations[0]}')
        axs[0].plot(q_list, d_lists[0], 'o', c='black', markersize=10, label='Спектр длины')
        axs[0].plot(q_list, d_char_lists[0], 's', c='black', markersize=10, label='Спектр массы')
        axs[0].set_xlabel('$q$, ед.', fontsize=18)
        axs[0].set_ylabel('$D_q$, ед.', fontsize=18)
        axs[0].xaxis.set_tick_params(labelsize=14)
        axs[0].yaxis.set_tick_params(labelsize=14)
        axs[0].grid(True)
        axs[0].legend(loc="upper right")

        axs[1].set_title(f'Итерация роста - {iterations[1]}')
        axs[1].plot(q_list, d_lists[1], 'o', c='black', markersize=10, label='Спектр длины')
        axs[1].plot(q_list, d_char_lists[1], 's', c='black', markersize=10, label='Спектр массы')
        axs[1].set_xlabel('$q$, ед.', fontsize=18)
        axs[1].set_ylabel('$D_q$, ед.', fontsize=18)
        axs[1].xaxis.set_tick_params(labelsize=14)
        axs[1].yaxis.set_tick_params(labelsize=14)
        axs[1].grid(True)
        axs[1].legend(loc="upper right")

        plt.show()

        # Отрисуем гистограммы масс
        fig, ax = plt.subplots(figsize=(35.0 * CM, 12.0 * CM), dpi=100)
        fig.subplots_adjust(top=0.959, bottom=0.181, left=0.053, right=0.998, hspace=0.2, wspace=0.2)
        ax.bar([i for i, _ in enumerate(several_phases_model.lines[-1])], [line.weight for line in several_phases_model.lines[-1]])
        ax.grid(True)
        # TODO
        # ax.set_title(f'from = {settings["max_char_val_from"]}, to = {settings["max_char_val_to"]}')
        ax.set_xlabel('Номер отрезка фрактала, №', fontsize=20)
        ax.set_ylabel('Масса фрактала, ед.', fontsize=20)
        ax.xaxis.set_tick_params(labelsize=20)
        ax.yaxis.set_tick_params(labelsize=20)
        ax.set_xlim([-1.0, 258])
        # ax.set(xlabel='Порядковый номер отрезка фрактала, №', ylabel='Величина параметра фрактала, ед.')
        plt.show()

        iterations_list = [i for i in range(len(several_phases_model.lines))]
        length_list = [sum(line.len() for line in lines) for i, lines in enumerate(several_phases_model.lines)]
        weight_list = [sum(line.weight for line in lines) for i, lines in enumerate(several_phases_model.lines)]

        # TODO: legacy представление длины и массы фрактала на двух независимых графиках от итерации роста
        fig, axs = plt.subplots(2, figsize=A4_FIG_SIZE, dpi=100)
        fig.subplots_adjust(top=0.99,bottom=0.055,left=0.110,right=0.995,hspace=0.215,wspace=0.2)
        # fig.suptitle(f'Порядок фрактала: {self.sb_fractal_depth.value()}; Кол-во итерация роста: {settings["count_iterations"]}')

        axs[0].plot(iterations_list, length_list, 'o', c='black', linewidth=1)
        # axs[0].set_title(f'max_a = {settings["max_val"]}')
        axs[0].set_xlabel('Итерация роста фрактала, ед.', fontsize=18)
        axs[0].set_ylabel('Длина фрактальной линии, ед.', fontsize=18)
        axs[0].xaxis.set_tick_params(labelsize=14)
        axs[0].yaxis.set_tick_params(labelsize=14)
        axs[0].grid(True)

        axs[1].plot(iterations_list, weight_list, 'o', c='black', linewidth=1)
        # axs[1].set_title(f'from = {settings["max_char_val_from"]}, to = {settings["max_char_val_to"]}')
        axs[1].set_xlabel('Итерация роста фрактала, ед.', fontsize=18)
        axs[1].set_ylabel('Масса фрактала, ед.', fontsize=18)
        axs[1].xaxis.set_tick_params(labelsize=14)
        axs[1].yaxis.set_tick_params(labelsize=14)
        axs[1].grid(True)
        plt.show()
        # TODO: legacy представление длины и массы фрактала на двух независимых графиках от итерации роста

        # # TODO: Третий график статьи. НАЧНАЛО
        # # TODO: Внимание!!! Вторая часть графика принадлежит множественному мультифрактальному
        # # TODO: графику, но так как их надо поместить вместе в статье делаем их и тут.
        # # Нормированное представление длинны и массы фрактала в зависимости от итерации роста на одном графике
        # fig, axs = plt.subplots(1, 2, figsize=(17.0 * CM, 17.0 * CM), dpi=100)
        # fig.subplots_adjust(top=0.998, bottom=0.096, left=0.096, right=0.993, hspace=0.215, wspace=0.2)
        #
        # max_length = sum(line.len() for line in several_phases_model.lines[-1])
        # max_weight = sum(line.weight for line in several_phases_model.lines[-1])
        # axs[0].plot(iterations_list, [l / max_length for l in length_list], c='lightsalmon', markersize=10, linewidth=4, label='Длина фрактальной линии')
        # axs[0].plot(iterations_list, [w / max_weight for w in weight_list], c='darkolivegreen', markersize=10, linewidth=4, label='Масса фрактала')
        # axs[0].set_xlabel('Итерация роста фрактала, ед.', fontsize=20)
        # axs[0].set_ylabel('Нормированная величина, ед.', fontsize=20)
        # axs[0].xaxis.set_tick_params(labelsize=14)
        # axs[0].yaxis.set_tick_params(labelsize=14)
        # axs[0].grid(True)
        # axs[0].legend(loc="upper left", fontsize=20)
        #
        # #TODO: Тот самый график по множественному мультифракталу
        # models = []
        #
        # settings_ = {
        #     'model': 'several',
        #     'max_val': self.dsb_max_line_legth.value(),
        #     'count_iterations': self.sb_count_iterations.value(),
        #     'coefficient_a': self.dsb_several_phase_coefficient_a.value(),
        #     'coefficient_h': self.dsb_several_phase_coefficient_h.value(),
        #     'max_char_val_from': self.dsb_rnd_max_characteristic_from.value(),
        #     'max_char_val_to': self.dsb_rnd_max_characteristic_to.value(),
        #     'count_beginner_from': self.sb_count_items_from_1.value(),
        #     'count_beginner_to': self.sb_count_items_to_1.value(),
        # }
        #
        # model_1 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
        #                 self.dsb_angle.value(), **settings_)
        # model_1.build()
        # models.append(model_1)
        #
        # settings_['count_beginner_from'] = self.sb_count_items_from_2.value()
        # settings_['count_beginner_to'] = self.sb_count_items_to_2.value()
        # model_2 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
        #                 self.dsb_angle.value(), **settings_)
        # model_2.build()
        # models.append(model_2)
        #
        # settings_['count_beginner_from'] = self.sb_count_items_from_3.value()
        # settings_['count_beginner_to'] = self.sb_count_items_to_3.value()
        # model_3 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
        #                 self.dsb_angle.value(), **settings_)
        # model_3.build()
        # models.append(model_3)
        #
        # settings_['count_beginner_from'] = self.sb_count_items_from_4.value()
        # settings_['count_beginner_to'] = self.sb_count_items_to_4.value()
        # model_4 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
        #                 self.dsb_angle.value(), **settings_)
        # model_4.build()
        # models.append(model_4)
        #
        # iterations_list = [i for i in range(len(model_1.lines))]
        # max_ = [sum(line.weight for line in models[0].lines[-1]), sum(line.weight for line in models[1].lines[-1]),
        #         sum(line.weight for line in models[2].lines[-1]), sum(line.weight for line in models[3].lines[-1])]
        # weight_lists = [[sum(line.weight for line in lines) / max_[i_] for i, lines in enumerate(model.lines)] for
        #                 i_, model in enumerate(models)]
        #
        # colors = ['lightsalmon', 'orangered', 'darkolivegreen', 'darkkhaki']
        #
        # for i, weight_list in enumerate(weight_lists):
        #     axs[1].plot(iterations_list, weight_list, markersize=10, linewidth=4, c=f'{colors[i]}', label=f'Спектр {i + 1}')
        #
        # axs[1].set_xlabel('Итерация роста фрактала, ед.', fontsize=20)
        # axs[1].set_ylabel('Масса фрактала, ед.', fontsize=20)
        # axs[1].xaxis.set_tick_params(labelsize=14)
        # axs[1].yaxis.set_tick_params(labelsize=14)
        # axs[1].legend(loc="upper left", fontsize=20)
        # axs[1].grid(True)
        # plt.show()
        # # TODO: Третий график статьи. ОКОНЧАНИЕ

        # TODO: НАЧАЛО Место для второго изображения для статьи по мультифракталам
        # Сделаем вычисление для нескольких max_char_val_to 1,10, 100 при константе max_char_val_from = 0
        d_lists, d_char_lists = [], []
        for max_char_val in [1, 10, 100]:
            settings['max_char_val_from'] = 0.1
            settings['max_char_val_to'] = max_char_val

            several_phases_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                         self.dsb_angle.value(), **settings)
            several_phases_model.build()

            q_list = [q for q in range(self.sb_left_q.value(), self.sb_right_q.value() + 1)]

            lines = several_phases_model.lines[-1]

            total_sum = sum(line.len() for line in lines)
            total_sum_char = sum(line.weight for line in lines)

            l_i = [line.len() for line in lines]
            p_i = [line.len() / total_sum for line in lines]
            # TODO: если мы хотим с массами
            p_i_char = [line.weight / total_sum_char for line in lines]

            fractal_span = Segment(lines[0].start, lines[-1].finish).len()

            # TODO: Новый способ расчета D для многофазной модели
            d_list, d_list_char = [], []
            for q in q_list:
                value, value_ch = None, None
                if q != 1:
                    value = self._new_calc_d(p_i, l_i, fractal_span, q)
                    value_ch = self._new_calc_d(p_i_char, l_i, fractal_span, q)
                d_list.append(value)
                d_list_char.append(value_ch)

            # TODO: so ugly. Так как не нашли до сих пор способ посчиать для q = 1 D для массы и длины - аппроксимируем
            index = None
            for i, d in enumerate(d_list):
                if d is None:
                    index = i
                    break

            if index:
                d_list[index] = d_list[index - 1] + (d_list[index + 1] - d_list[index - 1]) / 2.0
                d_list_char[index] = d_list_char[index - 1] + (d_list_char[index + 1] - d_list_char[index - 1]) / 2.0
            # TODO: окончание аппроксимации

            # TODO: Старый способ расчета D для многофазной модели
            # d_list = [round(self._calc_d(self.dsb_max_line_legth.value()/fractal_span, p_i, q), 3) for q in q_list]
            # d_list_char = [self._calc_d(self.dsb_max_line_legth.value(), p_i_char, q) for q in q_list]
            d_lists.append(d_list)
            d_char_lists.append(d_list_char)
        fig, axs = plt.subplots(1, 2, figsize=(17.0 * CM, 17.0 * CM), dpi=100)
        fig.subplots_adjust(top=0.998, bottom=0.096, left=0.096, right=0.993, hspace=0.215, wspace=0.2)
        axs[0].plot(q_list, d_lists[0], c='black', markersize=10, linewidth=4, label='Спектр монофрактала')
        axs[0].plot(q_list, d_char_lists[0], c='lightsalmon', markersize=10, linewidth=4, label=r'Спектр при $\Delta m_i \leq 1$')
        axs[0].plot(q_list, d_char_lists[1], c='orangered', markersize=10, linewidth=4, label=r'Спектр при $\Delta m_i \leq 10$')
        axs[0].plot(q_list, d_char_lists[2], c='darkolivegreen', markersize=10, linewidth=4, label=r'Спектр при $\Delta m_i \leq 100$')
        axs[0].set_xlabel('$q$, ед.', fontsize=20)
        axs[0].set_ylabel('$D_q$, ед.', fontsize=20)
        axs[0].xaxis.set_tick_params(labelsize=14)
        axs[0].yaxis.set_tick_params(labelsize=14)
        axs[0].set_xticks([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])
        axs[0].grid(True)
        axs[0].legend(loc="upper right", fontsize=20)

        # Сделаем вычисление для нескольких spectr_variant, а именно: ordinary_numerator, ordinary_denominator, quadratic_numerator, quadratic_denominator и выведем все на один график
        d_lists, d_char_lists = [], []
        for spectr_variant in ['ordinary_numerator', 'ordinary_denominator', 'quadratic_numerator', 'quadratic_denominator']:
            settings['spectr_variant'] = spectr_variant

            several_phases_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                         self.dsb_angle.value(), **settings)
            several_phases_model.build()

            q_list = [q for q in range(self.sb_left_q.value(), self.sb_right_q.value() + 1)]

            lines = several_phases_model.lines[-1]

            total_sum = sum(line.len() for line in lines)
            total_sum_char = sum(line.weight for line in lines)

            l_i = [line.len() for line in lines]
            p_i = [line.len() / total_sum for line in lines]
            # TODO: если мы хотим с массами
            p_i_char = [line.weight / total_sum_char for line in lines]

            fractal_span = Segment(lines[0].start, lines[-1].finish).len()

            # TODO: Новый способ расчета D для многофазной модели
            d_list, d_list_char = [], []
            for q in q_list:
                value, value_ch = None, None
                if q != 1:
                    value = self._new_calc_d(p_i, l_i, fractal_span, q)
                    value_ch = self._new_calc_d(p_i_char, l_i, fractal_span, q)
                d_list.append(value)
                d_list_char.append(value_ch)

            # TODO: so ugly. Так как не нашли до сих пор способ посчиать для q = 1 D для массы и длины - аппроксимируем
            index = None
            for i, d in enumerate(d_list):
                if d is None:
                    index = i
                    break

            if index:
                d_list[index] = d_list[index - 1] + (d_list[index + 1] - d_list[index - 1]) / 2.0
                d_list_char[index] = d_list_char[index - 1] + (d_list_char[index + 1] - d_list_char[index - 1]) / 2.0
            # TODO: окончание аппроксимации

            # TODO: Старый способ расчета D для многофазной модели
            # d_list = [round(self._calc_d(self.dsb_max_line_legth.value()/fractal_span, p_i, q), 3) for q in q_list]
            # d_list_char = [self._calc_d(self.dsb_max_line_legth.value(), p_i_char, q) for q in q_list]
            d_lists.append(d_list)
            d_char_lists.append(d_list_char)
        axs[1].plot(q_list, d_lists[0], c='black', markersize=10, linewidth=4, label='Спектр монофрактала')
        axs[1].plot(q_list, d_char_lists[0], c='lightsalmon', markersize=10, linewidth=4, label=r'Спектр для $k$')
        axs[1].plot(q_list, d_char_lists[1], c='orangered', markersize=10, linewidth=4, label=r'Спектр для $\frac{1}{k}$')
        axs[1].plot(q_list, d_char_lists[2], c='darkolivegreen', markersize=10, linewidth=4, label=r'Спектр для $k^2$')
        axs[1].plot(q_list, d_char_lists[3], c='darkkhaki', markersize=10, linewidth=4, label=r'Спектр для $\frac{1}{k^2}$')
        axs[1].set_xlabel('$q$, ед.', fontsize=20)
        axs[1].set_ylabel('$D_q$, ед.', fontsize=20)
        axs[1].xaxis.set_tick_params(labelsize=14)
        axs[1].yaxis.set_tick_params(labelsize=14)
        axs[1].set_xticks([-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10])
        axs[1].grid(True)
        axs[1].legend(loc="upper right", fontsize=20)
        plt.show()
        # TODO: ОКОНЧАНИЕ. Место для второго изображения для статьи по мультифракталам

    def _several_build_graph(self):
        models = []

        settings = {
            'model': 'several',
            'max_val': self.dsb_max_line_legth.value(),
            'count_iterations': self.sb_count_iterations.value(),
            'coefficient_a': self.dsb_several_phase_coefficient_a.value(),
            'coefficient_h': self.dsb_several_phase_coefficient_h.value(),
            'max_char_val_from': self.dsb_rnd_max_characteristic_from.value(),
            'max_char_val_to': self.dsb_rnd_max_characteristic_to.value(),
            'count_beginner_from': self.sb_count_items_from_1.value(),
            'count_beginner_to': self.sb_count_items_to_1.value(),
        }

        model_1 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                     self.dsb_angle.value(), **settings)
        model_1.build()
        models.append(model_1)

        settings['count_beginner_from'] = self.sb_count_items_from_2.value()
        settings['count_beginner_to'] = self.sb_count_items_to_2.value()
        model_2 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                     self.dsb_angle.value(), **settings)
        model_2.build()
        models.append(model_2)

        settings['count_beginner_from'] = self.sb_count_items_from_3.value()
        settings['count_beginner_to'] = self.sb_count_items_to_3.value()
        model_3 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                       self.dsb_angle.value(), **settings)
        model_3.build()
        models.append(model_3)

        settings['count_beginner_from'] = self.sb_count_items_from_4.value()
        settings['count_beginner_to'] = self.sb_count_items_to_4.value()
        model_4 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                       self.dsb_angle.value(), **settings)
        model_4.build()
        models.append(model_4)

        iterations_list = [i for i in range(len(model_1.lines))]
        max_ = [sum(line.weight for line in models[0].lines[-1]), sum(line.weight for line in models[1].lines[-1]), sum(line.weight for line in models[2].lines[-1]), sum(line.weight for line in models[3].lines[-1])]
        weight_lists = [[sum(line.weight for line in lines)/max_[i_] for i, lines in enumerate(model.lines)] for i_, model in enumerate(models)]

        fig, ax = plt.subplots(figsize=A4_FIG_SIZE, dpi=100)
        fig.subplots_adjust(top=0.985, bottom=0.055, left=0.09, right=0.99, hspace=0.2, wspace=0.2)

        colors = ['green', 'blue', 'red', 'black']

        for i, weight_list in enumerate(weight_lists):
            ax.plot(iterations_list, weight_list, 'o', c=f'{colors[i]}', markersize=5, label=f'Спектр {i + 1}')

        ax.set_xlabel('Итерация роста фрактала, ед.', fontsize=18)
        ax.set_ylabel('Масса фрактала, ед.', fontsize=18)
        ax.xaxis.set_tick_params(labelsize=14)
        ax.yaxis.set_tick_params(labelsize=14)
        ax.legend(loc="upper left")
        ax.grid(True)

        plt.show()