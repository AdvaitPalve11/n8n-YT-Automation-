"""
AI PROMPT GENERATOR - Using Qwen3-4B
Generates creative video prompts using Hugging Face Transformers

Usage:
    python scripts/generate_prompts_hf.py --count 10
    python scripts/generate_prompts_hf.py --count 20 --topic science
"""

import json
import csv
import time
from pathlib import Path
from typing import List, Dict

# Check for transformers
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    HF_AVAILABLE = True
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
except ImportError:
    HF_AVAILABLE = False
    DEVICE = "cpu"
    print("⚠️  Hugging Face Transformers not installed")
    print("💡 Install with: pip install transformers torch accelerate")
    import sys
    sys.exit(1)

MODEL_NAME = "Qwen/Qwen3-4B"


class HuggingFaceGenerator:
    """Generate prompts using Gemma 2 from Hugging Face"""
    
    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self.device = DEVICE
        
        print(f"🤖 Loading {model_name}...")
        print(f"📍 Device: {self.device}")
        
        if not HF_AVAILABLE:
            raise ImportError("Hugging Face Transformers not installed")
        
        # Load tokenizer and model
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.device == "cpu":
                self.model = self.model.to(self.device)
            
            print(f"✅ Model loaded successfully!")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            print("\n💡 First time? Download the model:")
            print(f"   huggingface-cli login")
            print(f"   huggingface-cli download {model_name}")
            raise
    
    def generate_text(self, prompt: str, max_length: int = 512) -> str:
        """Generate text using Gemma 2"""
        
        # Format prompt for instruction-tuned model
        formatted_prompt = f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"
        
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt").to(self.device)
        
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=0.8,
                top_p=0.9,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract model response (after the prompt)
        if "<start_of_turn>model" in response:
            response = response.split("<start_of_turn>model")[-1].strip()
        
        return response
    
    def generate_prompts(self, topic: str, count: int) -> List[Dict]:
        """Generate video prompts"""
        
        system_prompt = f"""Generate {count} creative video prompt ideas for {topic} educational content.

Each prompt should:
- Be 10-20 words describing a specific visual scene/animation
- Focus on one clear mathematical concept
- Be suitable for 5-10 second videos
- Be engaging for YouTube Shorts audience

Format as JSON array:
[
  {{"prompt": "Visual description", "name": "short-slug", "variations": 2}}
]

Generate creative, varied prompts covering:
- Geometric animations
- Formula visualizations
- Mathematical patterns
- Problem-solving visuals
- Abstract math art"""

        print(f"\n🎨 Generating {count} prompts with Gemma 2...")
        
        try:
            response = self.generate_text(system_prompt, max_length=2048)
            
            # Try to extract JSON
            try:
                start_idx = response.find('[')
                end_idx = response.rfind(']') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = response[start_idx:end_idx]
                    prompts = json.loads(json_str)
                    print(f"✅ Generated {len(prompts)} prompts!")
                    return prompts
                else:
                    print("⚠️  No JSON found, parsing text...")
                    return self.parse_text_prompts(response, count)
                    
            except json.JSONDecodeError:
                print("⚠️  JSON parse error, parsing text...")
                return self.parse_text_prompts(response, count)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return []
    
    def parse_text_prompts(self, text: str, count: int) -> List[Dict]:
        """Fallback text parser"""
        prompts = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            
            if any(kw in line.lower() for kw in ['animation', 'visual', 'spiral', 'wave', 'formula', 'geometric']):
                if 20 < len(line) < 200:
                    name = line[:30].lower()
                    name = ''.join(c if c.isalnum() or c == ' ' else '' for c in name)
                    name = '-'.join(name.split())[:50]
                    
                    prompts.append({
                        'prompt': line,
                        'name': name,
                        'variations': 2
                    })
            
            if len(prompts) >= count:
                break
        
        return prompts[:count]
    
    def generate_script(self, prompt: str) -> Dict:
        """Generate detailed script for a prompt"""
        
        script_prompt = f"""Create a 30-second YouTube Shorts script for:

Visual: {prompt}

Generate JSON with:
{{
  "hook": "Attention-grabbing opener (5 sec)",
  "main_content": "Educational explanation (20 sec)",
  "cta": "Call-to-action (5 sec)",
  "visual_notes": "Key visual elements"
}}"""

        try:
            response = self.generate_text(script_prompt, max_length=1024)
            
            # Try JSON extraction
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
            else:
                return {
                    'hook': prompt[:50],
                    'main_content': prompt,
                    'cta': 'Like and subscribe!',
                    'visual_notes': 'Show animation'
                }
        except:
            return {
                'hook': prompt[:50],
                'main_content': prompt,
                'cta': 'Like and subscribe!',
                'visual_notes': 'Show animation'
            }


def save_to_csv(prompts: List[Dict], output_path: str = "prompts.csv"):
    """Save prompts to CSV"""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Prompt', 'Name', 'Variations'])
        writer.writeheader()
        
        for p in prompts:
            writer.writerow({
                'Prompt': p['prompt'],
                'Name': p['name'],
                'Variations': p.get('variations', 2)
            })
    
    print(f"✅ Saved to {output_path}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate AI video prompts using Qwen3-4B")
    parser.add_argument('--count', type=int, default=10, help='Number of prompts to generate')
    parser.add_argument('--topic', default='mathematics', help='Topic area (mathematics, science, physics, etc.)')
    parser.add_argument('--model', default=MODEL_NAME, help='HuggingFace model (default: Qwen3-4B)')
    parser.add_argument('--output', default='prompts.csv', help='Output CSV file')
    parser.add_argument('--enhance', action='store_true', help='Generate detailed scripts (takes longer)')
    
    args = parser.parse_args()
    
    print("="*60)
    print("🤖 AI PROMPT GENERATOR")
    print("="*60)
    print(f"Model: {args.model}")
    print(f"Topic: {args.topic}")
    print(f"Count: {args.count}")
    print("="*60 + "\n")
    
    # Initialize generator
    generator = HuggingFaceGenerator(args.model)
    
    # Generate prompts
    prompts = generator.generate_prompts(args.topic, args.count)
    
    if not prompts:
        print("❌ No prompts generated")
        return
    
    # Enhance with scripts if requested
    if args.enhance:
        print("\n📝 Generating scripts...")
        for i, p in enumerate(prompts, 1):
            print(f"  [{i}/{len(prompts)}] {p['name']}")
            p['script'] = generator.generate_script(p['prompt'])
            time.sleep(0.5)
    
    # Save
    save_to_csv(prompts, args.output)
    
    print("\n" + "="*60)
    print(f"✅ Generated {len(prompts)} prompts")
    print(f"📁 Saved to: {args.output}")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
