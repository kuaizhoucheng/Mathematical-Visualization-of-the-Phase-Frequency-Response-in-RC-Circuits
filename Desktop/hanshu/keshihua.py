from manim import *
import numpy as np

class ACCircuitPhaseAnalysis(Scene):
    def construct(self):
        # 定义输入电压函数 u = 5e^(j*w*t) = 5cos(wt) + 5jsin(wt)
        # 电容两端电压为 u_c = (1/C)∫i dt，其中 i = C du/dt
        # 所以 u_c 的导数与电流成正比，即 du_c/dt = (1/C)i = du/dt
        # 因此我们需要绘制 du/dt 随时间 t 的变化
        # du/dt = 5jw e^(jwt) = -5w sin(wt) + 5w j cos(wt)
        # 我们将绘制实部和虚部

        # 场景1: w=5
        self.setup_scene(5, "w=5")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # 场景2: w=10
        self.setup_scene(10, "w=10")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # 场景3: w=100
        self.setup_scene(100, "w=100")
        self.wait(2)
        self.play(FadeOut(*self.mobjects))

        # 场景4: 比较三个频率
        self.compare_scenes()
        self.wait(3)

    def setup_scene(self, w, title):
        # 创建坐标系
        axes = Axes(
            x_range=[0, 2*np.pi/w*3, np.pi/w],
            y_range=[-5*w*1.2, 5*w*1.2, 5*w],
            x_length=10,
            y_length=6,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(0, 2*np.pi/w*3+0.1, np.pi/w),
                "numbers_with_elongated_ticks": np.arange(0, 2*np.pi/w*3+0.1, np.pi/w),
                "label_direction": DOWN
            },
            tips=True,
        )

        # 设置x轴标签为时间t
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("du/dt")
        axes_labels = VGroup(x_label, y_label)

        # 绘制实部和虚部
        real_part = axes.plot(lambda t: -5*w*np.sin(w*t), color=BLUE)
        imag_part = axes.plot(lambda t: 5*w*np.cos(w*t), color=RED)

        # 添加图例
        real_label = axes.get_graph_label(real_part, "\text{Re}(du/dt)", x_val=2*np.pi/w, direction=UP)
        imag_label = axes.get_graph_label(imag_part, "\text{Im}(du/dt)", x_val=2*np.pi/w + np.pi/(2*w), direction=DOWN)

        # 添加标题
        scene_title = Tex(f"du/dt vs t: {title}", font_size=24)
        scene_title.to_corner(UP + LEFT)

        # 组合所有元素
        plot = VGroup(axes, real_part, imag_part)
        labels = VGroup(axes_labels, real_label, imag_label, scene_title)

        # 添加到场景
        self.play(Create(axes), run_time=2)
        self.play(Create(real_part), Create(imag_part), run_time=2)
        self.play(FadeIn(labels))

    def compare_scenes(self):
        # 创建坐标系，适应最大频率的范围
        max_w = 100
        axes = Axes(
            x_range=[0, 2*np.pi/max_w*3, np.pi/max_w],
            y_range=[-5*max_w*1.2, 5*max_w*1.2, 5*max_w],
            x_length=10,
            y_length=6,
            axis_config={"color": GREEN},
            tips=True,
        )

        # 设置轴标签
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("du/dt")
        axes_labels = VGroup(x_label, y_label)

        # 绘制三个频率的实部和虚部
        # w=5 (蓝色)
        real_part_5 = axes.plot(lambda t: -5*5*np.sin(5*t), color=BLUE)
        imag_part_5 = axes.plot(lambda t: 5*5*np.cos(5*t), color=BLUE_D)

        # w=10 (红色)
        real_part_10 = axes.plot(lambda t: -5*10*np.sin(10*t), color=RED)
        imag_part_10 = axes.plot(lambda t: 5*10*np.cos(10*t), color=RED_D)

        # w=100 (绿色)
        real_part_100 = axes.plot(lambda t: -5*100*np.sin(100*t), color=GREEN)
        imag_part_100 = axes.plot(lambda t: 5*100*np.cos(100*t), color=GREEN_D)

        # 添加图例
        legend = VGroup(
            Text("w=5 实部").set_color(BLUE).next_to(axes, UP + RIGHT),
            Text("w=5 虚部").set_color(BLUE_D).next_to(axes, UP + RIGHT).shift(DOWN*0.5),
            Text("w=10 实部").set_color(RED).next_to(axes, UP + RIGHT).shift(DOWN*1),
            Text("w=10 虚部").set_color(RED_D).next_to(axes, UP + RIGHT).shift(DOWN*1.5),
            Text("w=100 实部").set_color(GREEN).next_to(axes, UP + RIGHT).shift(DOWN*2),
            Text("w=100 虚部").set_color(GREEN_D).next_to(axes, UP + RIGHT).shift(DOWN*2.5),
        )

        # 添加标题
        scene_title = Text("不同频率下导数随时间变化比较", font_size=24)
        scene_title.to_corner(UP + LEFT)

        # 组合所有元素
        plot = VGroup(axes, real_part_5, imag_part_5, real_part_10, imag_part_10, real_part_100, imag_part_100)
        labels = VGroup(axes_labels, legend, scene_title)

        # 添加到场景
        self.play(Create(axes), run_time=2)
        self.play(
            Create(real_part_5), Create(imag_part_5),
            Create(real_part_10), Create(imag_part_10),
            Create(real_part_100), Create(imag_part_100),
            run_time=10
        )
        self.play(FadeIn(labels))