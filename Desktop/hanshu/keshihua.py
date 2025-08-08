from manim import *
import numpy as np

class ACCircuitPhaseAnalysis(Scene):
    def construct(self):
        # 依次动态展示w=5, w=10, w=20，场景间淡出淡入
        # 让快慢对比更明显：w=5用6秒，w=10用3秒，w=20用1.5秒
        run_times = {5: 6, 10: 3, 20: 1.5}
        last_group = last_u_curve = last_du_curve = last_tracker = None
        for w, title in zip([5, 10, 20], ["w=5", "w=10", "w=20"]):
            group, u_curve, du_curve, tracker = self.setup_complex_split_scene(w, title, return_group=True)
            self.wait(0.3)
            self.play(tracker.animate.set_value(2 * np.pi / w), run_time=run_times[w], rate_func=linear)
            self.wait(1.2)
            if w != 20:
                self.play(FadeOut(group, u_curve, du_curve), run_time=1)
            else:
                last_group, last_u_curve, last_du_curve, last_tracker = group, u_curve, du_curve, tracker

        # 先淡出最后一个分屏场景
        self.play(FadeOut(last_group, last_u_curve, last_du_curve), run_time=1)
        # ====== 新增对比场景：三频率原函数/导函数复平面轨迹对比（最后一个场景） ======
        self.compare_complex_plane_multi()  # <--- 最后一个场景主函数调用
        self.wait(3)

    def compare_complex_plane_multi(self):
        # ====== 最后一个场景：三频率原函数/导函数复平面轨迹对比 ======
        # 颜色定义（w=5红，w=10青，w=20黄）
        color_map = {5: RED, 10: TEAL, 20: YELLOW}
        ws = [5, 10, 20]

        # ---------- 左侧：原函数多频率对比（同一坐标系） ----------
        plane1 = ComplexPlane(
            x_range=[-7, 7, 1],
            y_range=[-7, 7, 1],
            x_length=4.2,
            y_length=4.2,
            axis_config={"color": GREEN},
        )
        x_label1 = Text("Re", font_size=20).next_to(plane1, RIGHT, buff=0.2)
        y_label1 = Text("Im", font_size=20).next_to(plane1, UP, buff=0.2)
        trackers1 = [ValueTracker(0.01) for _ in ws]  # 每条曲线独立的ValueTracker
        curves1 = VGroup()  # 三条原函数曲线
        # 每条原函数曲线的最大t值不同，分别为2π/w
        max_t_list = [2 * np.pi / w for w in ws]
        def make_curve1(tracker, w, max_t):
            u_func = lambda t: np.array([5 * np.cos(w * t), 5 * np.sin(w * t)])
            return always_redraw(lambda: ParametricFunction(
                lambda t: plane1.coords_to_point(*u_func(t)),
                t_range=[0, min(tracker.get_value(), max_t)],
                color=color_map[w],
                stroke_width=4,
                use_smoothing=False,
                fill_opacity=0
            ))
        legend_labels1 = [Text(f"w={w}", font_size=16, color=color_map[w]) for w in ws]
        legends1 = VGroup(*legend_labels1).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        legends1.next_to(plane1, UP + RIGHT, buff=1.1, aligned_edge=LEFT)
        for i, w in reversed(list(enumerate(ws))):
            max_t = max_t_list[i]
            curve = make_curve1(trackers1[i], w, max_t)
            curves1.add(curve)
        title1 = Text("原函数多频率复平面对比", font_size=18).next_to(plane1, UP, buff=0.5)
        # left_group只包含静态元素，不包含曲线
        left_group = VGroup(plane1, x_label1, y_label1, legends1, title1)

        # ---------- 右侧：导函数多频率对比（同一坐标系） ----------
        # 缩小右侧复平面尺寸，扩大显示范围，保障大半径曲线完整
        plane2 = ComplexPlane(
            x_range=[-110, 110, 20],
            y_range=[-110, 110, 20],
            x_length=2.8,  # 缩小尺寸
            y_length=2.8,
            axis_config={"color": GREEN},
        )
        x_label2 = Text("Re", font_size=16).next_to(plane2, RIGHT, buff=0.15)
        y_label2 = Text("Im", font_size=16).next_to(plane2, UP, buff=0.15)
        trackers2 = [ValueTracker(0.01) for _ in ws]  # 每条曲线独立的ValueTracker
        curves2 = VGroup()  # 三条导函数曲线
        legend_labels2 = [Text(f"w={w}", font_size=13, color=color_map[w]) for w in ws]
        legends2 = VGroup(*legend_labels2).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        legends2.next_to(plane2, UP + RIGHT, buff=0.8, aligned_edge=LEFT)
        def make_curve2(tracker, w, color):
            du_func = lambda t: np.array([-5 * w * np.sin(w * t), 5 * w * np.cos(w * t)])
            return always_redraw(lambda: ParametricFunction(
                lambda t: plane2.coords_to_point(*du_func(t)),
                t_range=[0, tracker.get_value()],
                color=color,
                stroke_width=4,
                use_smoothing=False,
                fill_opacity=0
            ))
        for i, (w, color) in enumerate(zip(ws, color_map.values())):
            curve = make_curve2(trackers2[i], w, color)
            curves2.add(curve)
        title2 = Text("导函数多频率复平面对比", font_size=15).next_to(plane2, UP, buff=0.35)
        # right_group只包含静态元素，不包含曲线
        right_group = VGroup(plane2, x_label2, y_label2, legends2, title2)

        # ---------- 左右排列，整体组合 ----------
        all_group = VGroup(left_group, right_group).arrange(RIGHT, buff=1.2)
        # 先只add一次网格和静态元素
        self.add(all_group)
        # 曲线直接add即可，已自动对齐plane原点
        for curve in curves1:
            self.add(curve)
        for curve in curves2:
            self.add(curve)
        self.wait(0.3)
        # 左侧：三频率原函数圆，半径相同，速度不同
        run_times = {5: 6, 10: 3, 20: 1.5}
        # 左侧三条圆同时开始生长，但各自以不同速度结束
        run_times = {5: 6, 10: 3, 20: 1.5}
        max_run_time = max(run_times.values())
        from manim import UpdateFromAlphaFunc, AnimationGroup
        anims_left = []
        def make_updater(tracker, max_t):
            return lambda mobj, alpha: tracker.set_value(alpha * max_t)
        for i in range(3):
            tracker = trackers1[i]
            max_t = max_t_list[i]
            anim = UpdateFromAlphaFunc(tracker, make_updater(tracker, max_t), run_time=run_times[ws[i]], rate_func=linear)
            anims_left.append(anim)
        # 右侧三频率导函数圆，半径不同，速度与左侧同色一致（用UpdateFromAlphaFunc实现独立时长）
        from manim import UpdateFromAlphaFunc
        anims_right = []
        # 右侧动画t_range与左侧一致，确保角速度一致
        def make_updater_right(tracker, max_t):
            return lambda mobj, alpha: tracker.set_value(alpha * max_t)
        for i in range(3):
            tracker = trackers2[i]
            max_t = max_t_list[i]  # 与左侧一致
            anim = UpdateFromAlphaFunc(tracker, make_updater_right(tracker, max_t), run_time=run_times[ws[i]], rate_func=linear)
            anims_right.append(anim)
        # 左右两组动画合并，同时播放
        self.play(AnimationGroup(*anims_left, *anims_right, lag_ratio=0))
        self.wait(1.2)


    def setup_complex_split_scene(self, w, title, return_group=False):
        tracker = ValueTracker(0.01)

        # 左：原函数 u(t) 复平面轨迹
        plane1 = ComplexPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=4.2,
            y_length=4.2,
            axis_config={"color": GREEN},
        )
        plane1_group = VGroup(plane1)
        x_label1 = Text("Re", font_size=20).next_to(plane1, RIGHT, buff=0.2)
        y_label1 = Text("Im", font_size=20).next_to(plane1, UP, buff=0.2)
        u_func = lambda t: (5 * np.cos(w * t), 5 * np.sin(w * t))
        u_curve = always_redraw(lambda: plane1.plot_parametric_curve(
            u_func,
            t_range=[0, tracker.get_value()],
            color=BLUE,
        ))
        legend1 = Text("原函数 u(t)", font_size=16, color=BLUE).next_to(plane1, UP + RIGHT)
        title1 = Text(f"原函数复平面轨迹: {title}", font_size=18).next_to(plane1, UP, buff=0.5)
        plane1_group.add(x_label1, y_label1, u_curve, legend1, title1)

        # 右：导函数 du/dt 复平面轨迹
        plane2 = ComplexPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=4.2,
            y_length=4.2,
            axis_config={"color": GREEN},
        )
        plane2_group = VGroup(plane2)
        x_label2 = Text("Re", font_size=20).next_to(plane2, RIGHT, buff=0.2)
        y_label2 = Text("Im", font_size=20).next_to(plane2, UP, buff=0.2)
        du_func = lambda t: (-5 * np.sin(w * t), 5 * np.cos(w * t))
        du_curve = always_redraw(lambda: plane2.plot_parametric_curve(
            du_func,
            t_range=[0, tracker.get_value()],
            color=RED,
        ))
        legend2 = Text("导函数 du/dt", font_size=16, color=RED).next_to(plane2, UP + RIGHT)
        title2 = Text(f"导函数复平面轨迹: {title}", font_size=18).next_to(plane2, UP, buff=0.5)
        plane2_group.add(x_label2, y_label2, du_curve, legend2, title2)

        # 左右完全分开排列
        all_group = VGroup(plane1_group, plane2_group).arrange(RIGHT, buff=1.2)
        self.add(all_group)
        self.add(u_curve, du_curve)

        if return_group:
            return all_group, u_curve, du_curve, tracker

    def setup_complex_scene(self, w, title):
        # 创建复平面
        plane = ComplexPlane(
            x_range=[-6, 6, 1],
            y_range=[-6, 6, 1],
            x_length=7,
            y_length=7,
            axis_config={"color": GREEN},
        )
        # 添加横纵坐标标签
        x_label = Text("Re", font_size=24).next_to(plane, RIGHT, buff=0.3)
        y_label = Text("Im", font_size=24).next_to(plane, UP, buff=0.3)

        # 原函数 u(t) = 5e^{jwt} = 5cos(wt) + 5j sin(wt)
        u_func = lambda t: (5 * np.cos(w * t), 5 * np.sin(w * t))
        # 导函数 du/dt = 5jw e^{jwt}，缩放模长为5，便于对比
        du_func = lambda t: (-5 * np.sin(w * t), 5 * np.cos(w * t))
        # 绘制参数曲线（t从0到2π/w）
        u_curve = plane.plot_parametric_curve(
            u_func,
            t_range=[0, 2 * np.pi / w],
            color=BLUE,
        )
        du_curve = plane.plot_parametric_curve(
            du_func,
            t_range=[0, 2 * np.pi / w],
            color=RED,
        )
        # 图例
        legend = VGroup(
            Text("原函数 u(t)", font_size=18, color=BLUE).next_to(plane, UP + RIGHT),
            Text("导函数 du/dt", font_size=18, color=RED).next_to(plane, UP + RIGHT).shift(DOWN*0.6),
        )
        # 标题
        scene_title = Text(f"复平面轨迹: {title}", font_size=22).to_corner(UP + LEFT)
        # 组合
        self.play(Create(plane), run_time=2)
        self.play(FadeIn(x_label), FadeIn(y_label))
        self.play(Create(u_curve), Create(du_curve), run_time=3)
        self.play(FadeIn(legend), FadeIn(scene_title))

    def setup_scene(self, w, title):
        # 创建坐标系
        axes = Axes(
            x_range=[0, 2*np.pi/w*3, np.pi/w],
            y_range=[-5*w*1.2, 5*w*1.2, 5*w],
            x_length=10,
            y_length=6,
            axis_config={"color": GREEN},
            x_axis_config={
                "label_direction": DOWN,
                "font_size": 20,
            },
            y_axis_config={
                "numbers_to_include": [],  # 不显示y轴数字
            },
            tips=True,
        )
        # 替换x轴标签为π的形式
        x_labels = {0: "0", np.pi/w: "\\pi", 2*np.pi/w: "2\\pi", 3*np.pi/w: "3\\pi"}
        for x, label in x_labels.items():
            axes.x_axis.add_labels({x: MathTex(label, font_size=20)})

        # 设置x轴标签为时间t
        x_label = axes.get_x_axis_label("t")
        y_label = axes.get_y_axis_label("du/dt")
        axes_labels = VGroup(x_label, y_label)

        # 绘制实部和虚部
        real_part = axes.plot(lambda t: -5*w*np.sin(w*t), color=BLUE)
        imag_part = axes.plot(lambda t: 5*w*np.cos(w*t), color=RED)

        # 添加图例
        real_label = axes.get_graph_label(real_part, "\\text{Re}(du/dt)", x_val=2*np.pi/w, direction=UP).scale(0.5).shift(UP*0.3)
        imag_label = axes.get_graph_label(imag_part, "\\text{Im}(du/dt)", x_val=2*np.pi/w + np.pi/(2*w), direction=DOWN).scale(0.5).shift(DOWN*0.3)

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