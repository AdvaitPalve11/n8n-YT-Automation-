"""
Script: render_manim.py
Purpose: Creates an animated video using Manim based on the STEM topic
Input: Reads output/topic.json
Output: Creates media/videos/render_manim/720p30/STEMScene.mp4
"""

from manim import *
import json
import logging
from pathlib import Path
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class STEMScene(Scene):
    """
    High-quality Manim scene for detailed, engaging 30-second STEM animations.
    1080p 60fps with professional visual effects.
    """
    def construct(self):
        try:
            # Load topic data
            topic_file = Path("output/topic.json")
            logger.info(f"Loading topic from {topic_file}")
            
            if not topic_file.exists():
                raise FileNotFoundError(f"Topic file not found: {topic_file}")
            
            with open(topic_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            topic_text = data.get("topic", "STEM Topic")
            category = data.get("category", "Science")
            explanation = data.get("explanation", "")
            
            logger.info(f"Animating topic: {topic_text}")
            
            # === INTRO SEQUENCE (0-5 seconds) ===
            # Create animated title with gradient effect
            title = Text(topic_text, font_size=52, color=BLUE, weight=BOLD)
            title.to_edge(UP, buff=0.5)
            
            # Create subtitle with category
            subtitle = Text(
                f"{category} Explained", 
                font_size=32, 
                color=YELLOW
            )
            subtitle.next_to(title, DOWN, buff=0.4)
            
            # Opening animation with zoom effect
            self.play(
                Write(title, run_time=2),
                FadeIn(subtitle, shift=UP, run_time=1.5)
            )
            
            # Create decorative elements
            underline = Line(
                start=LEFT * 6,
                end=RIGHT * 6,
                color=BLUE,
                stroke_width=3
            )
            underline.next_to(subtitle, DOWN, buff=0.3)
            
            self.play(Create(underline), run_time=1)
            self.wait(0.5)
            
            # === MAIN CONTENT (5-25 seconds) ===
            
            # Mathematics visualizations only
            # Advanced Math symbols and formulas
            symbols = VGroup(
    # Fundamental constants
    MathTex(r"\pi = 3.14159...", font_size=48, color=BLUE),
    MathTex(r"e = 2.71828...", font_size=48, color=ORANGE),
    MathTex(r"i = \sqrt{-1}", font_size=48, color=PURPLE),

    # Summation, Product, Integrals
    MathTex(r"\sum_{i=1}^{n} i = \frac{n(n+1)}{2}", font_size=42, color=GREEN),
    MathTex(r"\prod_{i=1}^{n} i = n!", font_size=42, color=GREEN),
    MathTex(r"\int_{a}^{b} f(x) dx", font_size=48, color=ORANGE),
    MathTex(r"\iint_{D} f(x,y) dx dy", font_size=44, color=ORANGE),
    MathTex(r"\oint_C \mathbf{F} \cdot d\mathbf{r}", font_size=44, color=ORANGE),

    # Algebra & Geometry
    MathTex(r"x^2 + y^2 = r^2", font_size=44, color=TEAL),
    MathTex(r"a^2 + b^2 = c^2", font_size=44, color=TEAL),
    MathTex(r"x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}", font_size=44, color=TEAL),

    # Euler & Exponentials
    MathTex(r"e^{i\pi} + 1 = 0", font_size=48, color=PURPLE),
    MathTex(r"a^b", font_size=44, color=PURPLE),

    # Limits & Infinity
    MathTex(r"\lim_{x \to \infty} f(x)", font_size=44, color=RED),
    MathTex(r"\infty", font_size=60, color=RED),

    # Derivatives
    MathTex(r"\frac{dy}{dx}", font_size=44, color=GREEN),
    MathTex(r"\frac{\partial f}{\partial x}", font_size=44, color=GREEN),

    # Physics symbols
    MathTex(r"F = ma", font_size=48, color=YELLOW),
    MathTex(r"E = mc^2", font_size=48, color=YELLOW),
    MathTex(r"\vec{v}", font_size=44, color=BLUE),
    MathTex(r"\vec{F} = q (\vec{E} + \vec{v} \times \vec{B})", font_size=40, color=YELLOW),

   
    # Greek letters
    MathTex(r"\alpha, \beta, \gamma, \delta, \epsilon, \zeta, \eta, \theta, \lambda, \mu, \nu, \xi, \pi, \rho, \sigma, \tau, \phi, \chi, \psi, \omega",
            font_size=36, color=PURPLE),

    # Miscellaneous symbols
    MathTex(r"\forall x \in X, \exists y \leq \epsilon", font_size=42, color=BLUE),
    MathTex(r"\nabla \cdot \vec{F} = 0", font_size=44, color=GREEN),
    MathTex(r"\approx, \neq, \leq, \geq, \subset, \supset, \in", font_size=40, color=RED),
    MathTex(r"\Delta x, \Delta y, \Delta t", font_size=42, color=TEAL)
)
            
            # Arrange in a circular pattern for visual interest
            symbols.arrange_in_grid(rows=2, cols=3, buff=1.2)
            symbols.move_to(ORIGIN)
            
            # Transition: Fade out header, bring in main content
            self.play(
                FadeOut(title),
                FadeOut(subtitle),
                FadeOut(underline),
                run_time=1
            )
            
            # Animate symbols appearing one by one with rotation
            for i, symbol in enumerate(symbols):
                self.play(
                    FadeIn(symbol, scale=0.5),
                    Rotate(symbol, angle=PI/4),
                    run_time=0.6
                )
                if i < len(symbols) - 1:
                    self.wait(0.1)
            
            self.wait(1.5)
            
            # Create circular arrangement animation
            circle_positions = [
                np.array([2*np.cos(i*2*PI/len(symbols)), 2*np.sin(i*2*PI/len(symbols)), 0])
                for i in range(len(symbols))
            ]
            
            animations = []
            for symbol, pos in zip(symbols, circle_positions):
                animations.append(symbol.animate.move_to(pos))
            
            self.play(*animations, run_time=2)
            self.wait(0.5)
            
            # Rotate the entire arrangement
            self.play(
                Rotate(symbols, angle=2*PI, run_time=3),
                rate_func=smooth
            )
            
            # === OUTRO (25-30 seconds) ===
            # Create key facts display
            key_fact_box = Rectangle(
                width=10,
                height=2,
                fill_color=BLUE,
                fill_opacity=0.3,
                stroke_color=BLUE,
                stroke_width=4
            )
            
            key_fact_text = Text(
                f"Explore {topic_text}!",
                font_size=38,
                color=WHITE,
                weight=BOLD
            )
            key_fact_text.move_to(key_fact_box.get_center())
            
            key_fact_group = VGroup(key_fact_box, key_fact_text)
            
            # Final transition
            self.play(
                FadeOut(symbols),
                FadeIn(key_fact_group, scale=0.8),
                run_time=2
            )
            
            # Pulse effect for emphasis
            self.play(
                key_fact_group.animate.scale(1.15),
                run_time=0.5
            )
            self.play(
                key_fact_group.animate.scale(1/1.15),
                run_time=0.5
            )
            
            # Add sparkle effect
            stars = VGroup(*[
                Star(color=YELLOW, fill_opacity=0.8).scale(0.3).move_to(
                    key_fact_box.get_corner(corner) + np.array([0.3, 0.3, 0])
                )
                for corner in [UL, UR, DL, DR]
            ])
            
            self.play(
                LaggedStart(*[GrowFromCenter(star) for star in stars], lag_ratio=0.2),
                run_time=1
            )
            
            self.wait(1.5)
            
            logger.info("Animation sequence completed successfully")
            
        except Exception as e:
            logger.error(f"Error in Manim scene construction: {str(e)}")
            raise

def render_manim_video():
    """
    Programmatically renders the Manim scene for YouTube Shorts.
    1080x1920 (9:16 vertical) 60fps for mobile-optimized videos.
    Returns: Path to the rendered video file
    """
    try:
        # Configure Manim settings for YouTube Shorts
        config.pixel_height = 1920  # Vertical
        config.pixel_width = 1080   # Vertical
        config.frame_rate = 60
        config.output_file = "STEMScene"
        
        logger.info("Starting YouTube Shorts video rendering...")
        logger.info(f"Resolution: {config.pixel_width}x{config.pixel_height} (Vertical 9:16)")
        logger.info(f"Frame rate: {config.frame_rate} fps")
        
        # The video will be rendered when this script is called via manim CLI
        # Output location: media/videos/render_manim/1080p60/STEMScene.mp4
        
        return "media/videos/render_manim/1080p60/STEMScene.mp4"
        
    except Exception as e:
        logger.error(f"Error rendering Manim video: {str(e)}")
        raise

if __name__ == "__main__":
    # This is called when running: manim render_manim.py STEMScene
    from manim import config
    # YOUTUBE SHORTS VERTICAL FORMAT: 1080x1920 (9:16)  60fps
    config.pixel_height = 1920  # VERTICAL
    config.pixel_width = 1080   # VERTICAL
    config.frame_rate = 60
