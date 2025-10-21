"""Quick script to generate ONE test video"""

import subprocess
import json
from pathlib import Path

# Create a simple prompt
prompt = {
    "topic": "Pythagorean Theorem",
    "script": "The Pythagorean theorem states that in a right triangle, the square of the hypotenuse equals the sum of squares of the other two sides. Written as: a² + b² = c². This fundamental relationship has been known for thousands of years and forms the basis of trigonometry and geometry.",
    "entities": [
        {"text": "a² + b² = c²", "type": "formula"}
    ]
}

# Save to output folder
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

with open(output_dir / "topic.json", "w") as f:
    json.dump({"topic": prompt["topic"]}, f)

with open(output_dir / "script.json", "w") as f:
    json.dump({"script": prompt["script"]}, f, indent=2)

with open(output_dir / "entities.json", "w") as f:
    json.dump({"entities": prompt["entities"]}, f, indent=2)

print("✅ Created input files")
print(f"📝 Topic: {prompt['topic']}")
print(f"📄 Script length: {len(prompt['script'])} characters")

# Run Manim renderer
print("\n🎬 Rendering video with Manim...")
cmd = ["python", "scripts/render_manim_shorts.py"]

try:
    result = subprocess.run(cmd, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(result.stdout)
    print("\n✅ Video generated successfully!")
    print("📁 Check: media/videos/render_manim_shorts/")
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    print(f"Output: {e.stdout}")
    print(f"Error: {e.stderr}")
