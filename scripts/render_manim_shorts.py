"""
Script: render_manim_shorts.py  
Purpose: Creates DYNAMIC animated YouTube Shorts with topic-specific animations + AUDIO SYNC
Input: Reads output/topic.json, output/audio.mp3, output/script.json, output/animation_data.json
Output: Creates engaging, animated vertical videos (1080x1920, 60fps) WITH AUDIO
"""

from manim import *
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class STEMScene(Scene):
    """
    YouTube Shorts with DYNAMIC topic-specific animations + AUDIO SYNC
    """
    def construct(self):
        try:
            # Load ALL data
            topic_file = Path("output/topic.json")
            audio_file = Path("output/audio.mp3")
            script_file = Path("output/script.json")
            animation_file = Path("output/animation_data.json")
            
            logger.info(f"Loading topic from {topic_file}")
            
            if not topic_file.exists():
                raise FileNotFoundError(f"Topic file not found: {topic_file}")
            
            with open(topic_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            topic_text = data.get("topic", "Math Topic")
            
            # Load animation data if available
            animation_data = {}
            if animation_file.exists():
                with open(animation_file, "r", encoding="utf-8") as f:
                    animation_data = json.load(f)
                logger.info(f"Loaded animation data with {len(animation_data.get('keyframes', []))} keyframes")
            
            # ADD AUDIO if it exists
            if audio_file.exists():
                logger.info("Adding audio track to video!")
                self.add_sound(str(audio_file))
            else:
                logger.warning("No audio file found - video will be silent")
            
            logger.info(f"Creating DYNAMIC animation for: {topic_text}")
            
            # === PHASE 1: INTRO (0-3 seconds) ===
            self.create_intro(topic_text)
            
            # === PHASE 2: DYNAMIC ANIMATION (3-50 seconds) ===
            # Use animation data if available, otherwise pattern match
            if animation_data:
                self.animate_with_data(topic_text, animation_data)
            else:
                self.animate_topic(topic_text)
            
            # === PHASE 3: OUTRO (50-60 seconds) ===
            self.create_outro()
            
            logger.info("YouTube Shorts animation completed successfully!")
            
        except Exception as e:
            logger.error(f"Error in animation: {str(e)}")
            raise
    
    def create_intro(self, topic_text):
        """Create intro with topic title"""
        title = Text(
            topic_text,
            font_size=64,
            weight=BOLD,
            color=WHITE,
            line_spacing=1.2
        ).to_edge(UP, buff=1.2)
        
        if title.width > config.frame_width - 1:
            title.scale_to_fit_width(config.frame_width - 1)
        
        subtitle = Text(
            "🔢 Mathematics",
            font_size=48,
            color=BLUE_A
        ).next_to(title, DOWN, buff=0.5)
        
        underline = Line(
            start=subtitle.get_left() + LEFT * 0.3,
            end=subtitle.get_right() + RIGHT * 0.3,
            color=BLUE,
            stroke_width=4
        ).next_to(subtitle, DOWN, buff=0.3)
        
        self.play(
            Write(title, run_time=1.5),
            FadeIn(subtitle, shift=UP, run_time=1),
        )
        self.play(Create(underline), run_time=0.5)
        self.wait(1)
        
        # Transition out
        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(underline),
            run_time=0.5
        )
    
    def animate_with_data(self, topic, animation_data):
        """Animate using AI-generated keyframes and timing"""
        logger.info("Animating with AI-generated keyframes...")
        
        keyframes = animation_data.get("keyframes", [])
        
        for i, keyframe in enumerate(keyframes):
            kf_type = keyframe.get("type", "text")
            content = keyframe.get("content", "")
            duration = keyframe.get("duration", 2.0)
            color = keyframe.get("color", "WHITE")
            
            if kf_type == "text":
                text = Text(content, font_size=44, color=eval(color))
                if text.width > config.frame_width - 1.5:
                    text.scale_to_fit_width(config.frame_width - 1.5)
                self.play(Write(text), run_time=duration * 0.6)
                self.wait(duration * 0.4)
                self.play(FadeOut(text), run_time=0.5)
            
            elif kf_type == "formula":
                formula = MathTex(content, font_size=48, color=eval(color))
                self.play(Write(formula), run_time=duration * 0.7)
                self.wait(duration * 0.3)
                self.play(FadeOut(formula), run_time=0.5)
            
            elif kf_type == "shape":
                if "circle" in content.lower():
                    shape = Circle(radius=1.5, color=eval(color), stroke_width=5)
                elif "square" in content.lower():
                    shape = Square(side_length=2, color=eval(color), stroke_width=5)
                else:
                    shape = RegularPolygon(n=6, color=eval(color), stroke_width=5)
                
                self.play(Create(shape), run_time=duration * 0.6)
                self.wait(duration * 0.4)
                self.play(FadeOut(shape), run_time=0.5)
    
    def animate_topic(self, topic):
        """Create dynamic animation based on the topic"""
        topic_lower = topic.lower()
        
        # Pattern matching for topic types
        if "pascal" in topic_lower and "triangle" in topic_lower:
            self.animate_pascals_triangle()
        elif "fibonacci" in topic_lower:
            self.animate_fibonacci()
        elif "pythagoras" in topic_lower or "pythagorean" in topic_lower:
            self.animate_pythagorean_theorem()
        elif "pi" == topic_lower or "π" in topic_lower or topic_lower == "pi":
            self.animate_pi()
        elif "euler" in topic_lower and ("identity" in topic_lower or "formula" in topic_lower):
            self.animate_euler_identity()
        elif "golden ratio" in topic_lower or "phi" in topic_lower:
            self.animate_golden_ratio()
        elif "prime" in topic_lower:
            self.animate_primes()
        elif "fractal" in topic_lower or "mandelbrot" in topic_lower:
            self.animate_fractals()
        elif "circle" in topic_lower or "sphere" in topic_lower:
            self.animate_circle()
        elif "quadratic" in topic_lower:
            self.animate_quadratic()
        else:
            # Default: Show topic with dynamic effects
            self.animate_default(topic)
    
    def animate_pascals_triangle(self):
        """Animate Pascal's Triangle being built row by row"""
        logger.info("Animating Pascal's Triangle...")
        
        title = Text("Pascal's Triangle", font_size=48, color=YELLOW).to_edge(UP, buff=0.8)
        self.play(Write(title))
        self.wait(0.5)
        
        # Build triangle row by row
        rows = [
            [1],
            [1, 1],
            [1, 2, 1],
            [1, 3, 3, 1],
            [1, 4, 6, 4, 1],
            [1, 5, 10, 10, 5, 1],
        ]
        
        triangle_group = VGroup()
        y_start = 1.5
        
        for row_idx, row in enumerate(rows):
            row_group = VGroup()
            for col_idx, num in enumerate(row):
                # Calculate position
                x_offset = (col_idx - len(row)/2 + 0.5) * 0.9
                y_offset = y_start - row_idx * 0.7
                
                # Create number
                number = Text(str(num), font_size=36, color=WHITE)
                number.move_to([x_offset, y_offset, 0])
                
                # Highlight special patterns
                if num == 1:
                    number.set_color(BLUE)
                elif num % 2 == 0:
                    number.set_color(GREEN)
                else:
                    number.set_color(YELLOW)
                
                row_group.add(number)
            
            triangle_group.add(row_group)
            
            # Animate row appearing
            self.play(*[FadeIn(num, scale=0.5) for num in row_group], run_time=0.6)
            self.wait(0.2)
        
        self.wait(1)
        
        # Highlight patterns - flash certain numbers
        if len(rows) > 1:
            self.play(*[Indicate(triangle_group[i][1], color=RED) for i in range(1, len(rows))], run_time=1.5)
        self.wait(0.5)
        
        self.play(FadeOut(title), FadeOut(triangle_group))
    
    def animate_fibonacci(self):
        """Animate Fibonacci sequence and spiral"""
        logger.info("Animating Fibonacci sequence...")
        
        title = Text("Fibonacci Sequence", font_size=48, color=GOLD).to_edge(UP, buff=0.8)
        self.play(Write(title))
        
        # Show sequence building
        fib_numbers = [0, 1, 1, 2, 3, 5, 8, 13]
        sequence = VGroup()
        
        for i, num in enumerate(fib_numbers):
            number = Text(str(num), font_size=44, color=YELLOW if i < 2 else WHITE)
            if i == 0:
                number.move_to(LEFT * 3 + UP * 1)
            else:
                number.next_to(sequence[-1], RIGHT, buff=0.4)
            
            sequence.add(number)
            self.play(FadeIn(number, scale=0.7), run_time=0.4)
            
            # Show addition for new numbers
            if i >= 2:
                plus = Text("+", font_size=32, color=BLUE).move_to(
                    (sequence[i-2].get_center() + sequence[i-1].get_center()) / 2 + DOWN * 0.8
                )
                self.play(FadeIn(plus, shift=UP*0.3), run_time=0.2)
                self.play(
                    sequence[i-2].animate.set_color(GREEN),
                    sequence[i-1].animate.set_color(GREEN),
                    run_time=0.3
                )
                self.play(FadeOut(plus), run_time=0.2)
        
        self.wait(1)
        
        # Create golden spiral
        spiral = ParametricFunction(
            lambda t: np.array([
                0.3 * np.exp(0.15 * t) * np.cos(t),
                0.3 * np.exp(0.15 * t) * np.sin(t),
                0
            ]),
            t_range=[0, 3*PI],
            color=GOLD,
            stroke_width=4
        ).shift(DOWN * 0.5)
        
        self.play(
            FadeOut(sequence),
            Create(spiral, run_time=3),
        )
        self.wait(0.5)
        
        self.play(FadeOut(title), FadeOut(spiral))
    
    def animate_pythagorean_theorem(self):
        """Animate Pythagorean theorem with visual proof"""
        logger.info("Animating Pythagorean theorem...")
        
        title = Text("Pythagorean Theorem", font_size=44, color=BLUE).to_edge(UP, buff=0.8)
        self.play(Write(title))
        
        # Create right triangle
        triangle = Polygon(
            LEFT * 1.5 + DOWN * 1,
            LEFT * 1.5 + UP * 1,
            RIGHT * 0.5 + DOWN * 1,
            color=WHITE,
            stroke_width=3
        )
        
        # Label sides
        a_label = MathTex("a", font_size=40, color=YELLOW).next_to(triangle, LEFT, buff=0.2)
        b_label = MathTex("b", font_size=40, color=GREEN).next_to(triangle, UP, buff=0.2)
        c_label = MathTex("c", font_size=40, color=RED).move_to(triangle.get_center() + RIGHT * 0.6 + DOWN * 0.2)
        
        self.play(Create(triangle), run_time=1)
        self.play(Write(a_label), Write(b_label), Write(c_label), run_time=0.8)
        self.wait(0.5)
        
        # Show squares on each side
        square_a = Square(side_length=1.2, color=YELLOW, fill_opacity=0.3).next_to(triangle, LEFT, buff=0)
        square_b = Square(side_length=1.2, color=GREEN, fill_opacity=0.3).next_to(triangle, UP, buff=0)
        
        self.play(FadeIn(square_a), FadeIn(square_b), run_time=1)
        self.wait(0.5)
        
        # Show formula
        formula = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=56)
        formula[0].set_color(YELLOW)
        formula[2].set_color(GREEN)
        formula[4].set_color(RED)
        formula.move_to(DOWN * 2.5)
        
        self.play(Write(formula), run_time=1.5)
        self.wait(1)
        
        self.play(FadeOut(VGroup(title, triangle, a_label, b_label, c_label, square_a, square_b, formula)))
    
    def animate_pi(self):
        """Animate Pi and circle circumference"""
        logger.info("Animating Pi...")
        
        title = Text("π = 3.14159...", font_size=52, color=BLUE).to_edge(UP, buff=0.8)
        self.play(Write(title))
        
        # Create circle
        circle = Circle(radius=1.5, color=YELLOW, stroke_width=4)
        self.play(Create(circle), run_time=1.5)
        
        # Show diameter
        diameter = Line(LEFT * 1.5, RIGHT * 1.5, color=RED, stroke_width=4)
        d_label = MathTex("d", font_size=44, color=RED).next_to(diameter, DOWN, buff=0.2)
        
        self.play(Create(diameter), Write(d_label), run_time=1)
        self.wait(0.5)
        
        # Show circumference formula
        circum = MathTex(r"C = \pi d", font_size=48, color=GREEN).move_to(DOWN * 2.5)
        self.play(Write(circum), run_time=1)
        self.wait(1)
        
        # Animate circle rotating
        self.play(Rotate(circle, angle=2*PI, run_time=2), rate_func=linear)
        self.wait(0.5)
        
        self.play(FadeOut(VGroup(title, circle, diameter, d_label, circum)))
    
    def animate_euler_identity(self):
        """Animate Euler's identity"""
        logger.info("Animating Euler's identity...")
        
        formula = MathTex(r"e^{i\pi} + 1 = 0", font_size=64, color=GOLD)
        
        self.play(Write(formula), run_time=2)
        self.wait(1)
        
        # Highlight each part
        self.play(Indicate(formula[0], color=BLUE, scale_factor=1.2), run_time=1)
        self.wait(1)
        
        # Show "Most beautiful equation"
        subtitle = Text("Most Beautiful Equation", font_size=40, color=YELLOW).to_edge(DOWN, buff=1)
        self.play(Write(subtitle), run_time=1)
        self.wait(1)
        
        self.play(FadeOut(formula), FadeOut(subtitle))
    
    def animate_golden_ratio(self):
        """Animate golden ratio and spiral"""
        logger.info("Animating golden ratio...")
        
        title = Text("Golden Ratio", font_size=52, color=GOLD).to_edge(UP, buff=0.8)
        phi = MathTex(r"\phi = 1.618...", font_size=56, color=YELLOW)
        
        self.play(Write(title), Write(phi), run_time=1.5)
        self.wait(0.5)
        
        # Create golden spiral
        spiral = ParametricFunction(
            lambda t: np.array([
                0.4 * (1.618 ** (t/3)) * np.cos(t),
                0.4 * (1.618 ** (t/3)) * np.sin(t),
                0
            ]),
            t_range=[0, 2.5*PI],
            color=GOLD,
            stroke_width=5
        ).shift(DOWN * 0.8)
        
        self.play(FadeOut(phi), Create(spiral, run_time=4))
        self.wait(1)
        
        self.play(FadeOut(title), FadeOut(spiral))
    
    def animate_primes(self):
        """Animate prime numbers"""
        logger.info("Animating prime numbers...")
        
        title = Text("Prime Numbers", font_size=48, color=RED).to_edge(UP, buff=0.8)
        self.play(Write(title))
        
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
        prime_group = VGroup()
        
        for i, p in enumerate(primes):
            num = Text(str(p), font_size=42, color=YELLOW)
            if i == 0:
                num.move_to(LEFT * 3 + UP * 1)
            elif i % 4 == 0:
                num.move_to(LEFT * 3 + UP * (1 - (i//4) * 0.8))
            else:
                num.next_to(prime_group[-1], RIGHT, buff=0.5)
            
            prime_group.add(num)
            self.play(FadeIn(num, scale=0.7), run_time=0.3)
        
        self.wait(1)
        self.play(FadeOut(title), FadeOut(prime_group))
    
    def animate_circle(self):
        """Animate circle/sphere"""
        logger.info("Animating circle...")
        
        circle = Circle(radius=2, color=BLUE, stroke_width=5)
        self.play(Create(circle), run_time=2)
        
        # Show formula
        formula = MathTex(r"x^2 + y^2 = r^2", font_size=56, color=YELLOW).move_to(DOWN * 2.5)
        self.play(Write(formula), run_time=1.5)
        self.wait(1)
        
        # Pulse animation
        self.play(circle.animate.scale(1.2).set_color(GREEN), run_time=0.8)
        self.play(circle.animate.scale(1/1.2).set_color(BLUE), run_time=0.8)
        self.wait(0.5)
        
        self.play(FadeOut(circle), FadeOut(formula))
    
    def animate_quadratic(self):
        """Animate quadratic formula"""
        logger.info("Animating quadratic formula...")
        
        formula = MathTex(
            r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}",
            font_size=48,
            color=YELLOW
        )
        
        self.play(Write(formula), run_time=3)
        self.wait(1.5)
        self.play(FadeOut(formula))
    
    def animate_fractals(self):
        """Animate fractal pattern"""
        logger.info("Animating fractals...")
        
        # Create simple fractal tree
        def create_branch(start, angle, length, depth):
            if depth == 0 or length < 0.1:
                return VGroup()
            
            end = start + length * np.array([np.cos(angle), np.sin(angle), 0])
            branch = Line(start, end, color=GREEN, stroke_width=2)
            
            left = create_branch(end, angle + PI/6, length * 0.7, depth - 1)
            right = create_branch(end, angle - PI/6, length * 0.7, depth - 1)
            
            return VGroup(branch, left, right)
        
        tree = create_branch(DOWN * 2, PI/2, 1.5, 5)
        self.play(Create(tree), run_time=4)
        self.wait(1)
        self.play(FadeOut(tree))
    
    def animate_default(self, topic):
        """Default animation for unknown topics"""
        logger.info(f"Creating default animation for: {topic}")
        
        # Show topic name with effects
        main_text = Text(topic, font_size=60, weight=BOLD, color=YELLOW)
        if main_text.width > config.frame_width - 1.5:
            main_text.scale_to_fit_width(config.frame_width - 1.5)
        
        self.play(Write(main_text, run_time=2))
        self.wait(1)
        
        # Pulse effect
        self.play(main_text.animate.scale(1.15).set_color(WHITE), run_time=0.7)
        self.play(main_text.animate.scale(1/1.15).set_color(YELLOW), run_time=0.7)
        self.wait(1)
        
        # Show some mathematical symbols around it
        symbols = VGroup(
            MathTex(r"\sum", font_size=48, color=BLUE),
            MathTex(r"\int", font_size=48, color=GREEN),
            MathTex(r"\pi", font_size=48, color=RED),
            MathTex(r"\infty", font_size=52, color=ORANGE),
        )
        
        symbols[0].to_corner(UL, buff=1)
        symbols[1].to_corner(UR, buff=1)
        symbols[2].to_corner(DL, buff=1)
        symbols[3].to_corner(DR, buff=1)
        
        self.play(*[FadeIn(s, scale=0.7) for s in symbols], run_time=1)
        self.wait(1.5)
        
        self.play(FadeOut(main_text), FadeOut(symbols))
    
    def create_outro(self):
        """Create engaging outro with CTA"""
        # CTA Box
        cta_box = Rectangle(
            width=config.frame_width - 1,
            height=2.5,
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_color=GOLD,
            stroke_width=6
        )
        
        cta_text = Text(
            "❤️ LIKE & SUBSCRIBE!",
            font_size=52,
            weight=BOLD,
            color=WHITE
        )
        
        cta_group = VGroup(cta_box, cta_text).move_to(ORIGIN)
        
        # Sparkles around CTA
        sparkles = VGroup(*[
            Star(n=5, outer_radius=0.15, color=YELLOW, fill_opacity=0.8)
            .move_to([
                np.random.uniform(-2, 2),
                np.random.uniform(-1, 1),
                0
            ])
            for _ in range(8)
        ])
        
        self.play(
            FadeIn(cta_box, scale=0.8),
            Write(cta_text),
            run_time=1
        )
        
        self.play(*[FadeIn(s, scale=0.5) for s in sparkles], run_time=0.8)
        
        # Pulse CTA
        self.play(
            cta_group.animate.scale(1.1),
            run_time=0.5
        )
        self.play(
            cta_group.animate.scale(1/1.1),
            run_time=0.5
        )
        
        self.wait(1)

# Configure for YouTube Shorts (vertical format)
if __name__ == "__main__":
    from manim import config
    config.pixel_height = 1920
    config.pixel_width = 1080
    config.frame_height = 16.0
    config.frame_width = 9.0
