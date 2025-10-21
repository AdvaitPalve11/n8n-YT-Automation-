"""
FULLY DYNAMIC 60-second video generator:
- Qwen3 AI generates topics and scripts
- Fetches information from Wikipedia
- Edge TTS with British/American accents
- 720p 60fps high quality
"""

import subprocess
import json
from pathlib import Path
import time
import os
import wikipedia
import requests
import asyncio


def select_topic_from_wikipedia(topic_number, total_topics):
    """STEP 1: Dynamically select topic from Wikipedia - search for equations and interesting concepts"""
    print(f"\n📚 Searching Wikipedia for interesting topics {topic_number}/{total_topics}...")
    
    import random
    
    # Search categories in Wikipedia for interesting mathematical topics
    search_queries = [
        "mathematical theorem",
        "famous equation",
        "mathematical formula",
        "mathematics paradox",
        "mathematical constant",
        "mathematical proof",
        "number theory",
        "mathematical identity",
        "mathematical conjecture",
        "mathematical inequality"
    ]
    
    try:
        # Pick a random search query
        query = random.choice(search_queries)
        print(f"  Searching Wikipedia for: '{query}'...")
        
        # Search Wikipedia
        wikipedia.set_lang("en")
        search_results = wikipedia.search(query, results=20)
        
        if search_results:
            # Filter for interesting mathematical topics
            filtered = []
            for result in search_results:
                result_lower = result.lower()
                # Look for mathematical keywords
                if any(word in result_lower for word in [
                    "theorem", "equation", "formula", "paradox", "identity",
                    "conjecture", "proof", "constant", "sequence", "number",
                    "inequality", "law", "principle", "hypothesis"
                ]):
                    filtered.append(result)
            
            if filtered:
                topic = random.choice(filtered)
                print(f"✅ Selected from Wikipedia: {topic}")
                return topic
            else:
                # Use any result if no filtered match
                topic = random.choice(search_results[:10])
                print(f"✅ Selected from Wikipedia: {topic}")
                return topic
        else:
            raise Exception("No search results")
            
    except Exception as e:
        print(f"  ⚠️  Wikipedia search failed: {e}")
        print(f"  Trying random Wikipedia page in mathematics category...")
        
        try:
            # Try to get a random page from mathematics category
            from urllib.parse import quote
            import requests
            
            # Use Wikipedia API to get random mathematics article
            api_url = "https://en.wikipedia.org/w/api.php"
            params = {
                "action": "query",
                "format": "json",
                "list": "random",
                "rnnamespace": 0,
                "rnlimit": 10
            }
            
            response = requests.get(api_url, params=params, timeout=10)
            data = response.json()
            
            if "query" in data and "random" in data["query"]:
                pages = data["query"]["random"]
                topic = random.choice(pages)["title"]
                print(f"✅ Random Wikipedia topic: {topic}")
                return topic
            else:
                raise Exception("API failed")
                
        except Exception as e2:
            print(f"  ⚠️  Random page also failed: {e2}")
            print(f"  Using fallback search...")
            
            # Last resort: search for "mathematical" and pick first result
            try:
                results = wikipedia.search("mathematical", results=5)
                if results:
                    topic = results[0]
                    print(f"✅ Fallback topic: {topic}")
                    return topic
            except:
                pass
            
            # Ultimate fallback
            topic = "Mathematics"
            print(f"✅ Ultimate fallback: {topic}")
            return topic


def generate_animation_keyframes_with_qwen(topic, script, wiki_info):
    """Generate smart animation keyframes based on topic + script"""
    print(f"🎬 Generating animation keyframes from content...")
    
    try:
        # Extract key sentences from script - ensure they're clean
        sentences = [s.strip() for s in script.split('. ') if s.strip() and len(s.strip()) > 10]
        
        # Ensure we have enough content
        if len(sentences) < 3:
            print(f"⚠️  Script too short, using enhanced content...")
            sentences = [
                f"Let's explore {topic}",
                f"{topic} is a fascinating mathematical concept",
                "It has applications across science and engineering",
                "Understanding this opens new mathematical insights"
            ]
        
        keyframes = []
        
        # Build rich keyframes from actual script content
        for i, sentence in enumerate(sentences[:6]):
            # Clean sentence
            clean_sentence = sentence.strip()
            if not clean_sentence.endswith('.') and not clean_sentence.endswith('!') and not clean_sentence.endswith('?'):
                clean_sentence += '.'
            
            # Vary colors for visual interest
            colors = ["YELLOW", "BLUE", "WHITE", "GREEN", "GOLD", "RED"]
            
            keyframes.append({
                "type": "text",
                "content": clean_sentence,
                "duration": 3.5,
                "color": colors[i % len(colors)]
            })
        
        # Add formula visualization
        formula = extract_formula_from_wiki(topic, wiki_info)
        keyframes.insert(2, {
            "type": "formula",
            "content": formula,
            "duration": 4.0,
            "color": "BLUE"
        })
        
        print(f"✅ Generated {len(keyframes)} content-rich keyframes")
        return {"keyframes": keyframes}
        
    except Exception as e:
        print(f"⚠️  Keyframe generation failed: {e}")
        return {
            "keyframes": [
                {"type": "text", "content": topic, "duration": 5.0, "color": "YELLOW"},
                {"type": "formula", "content": "x^2 + y^2 = z^2", "duration": 5.0, "color": "BLUE"}
            ]
        }


def fetch_wikipedia_info(topic):
    """Fetch information about the topic from Wikipedia"""
    print(f"📚 Fetching Wikipedia info for: {topic}...")
    
    try:
        # Search Wikipedia
        wikipedia.set_lang("en")
        page = wikipedia.page(topic, auto_suggest=True)
        
        # Get summary (first few paragraphs)
        summary = wikipedia.summary(topic, sentences=5)
        
        # Get the full content for more details
        content = page.content[:2000]  # First 2000 characters
        
        print(f"✅ Wikipedia info retrieved ({len(summary)} chars)")
        return {
            "summary": summary,
            "content": content,
            "url": page.url
        }
    except wikipedia.exceptions.DisambiguationError as e:
        # Multiple pages, pick the first one
        try:
            topic = e.options[0]
            page = wikipedia.page(topic)
            summary = wikipedia.summary(topic, sentences=5)
            return {
                "summary": summary,
                "content": page.content[:2000],
                "url": page.url
            }
        except:
            return None
    except:
        print(f"⚠️  Wikipedia fetch failed")
        return None


def generate_script_with_qwen(topic, wiki_info):
    """STEP 2: Use Wikipedia + Qwen3 AI to generate a detailed 60-second script"""
    print(f"🤖 Generating script using Wikipedia + Qwen3 AI...")
    
    # Get Wikipedia summary for context
    wiki_text = wiki_info["summary"] if wiki_info else f"Topic: {topic}"
    
    try:
        # Suppress warnings
        import os
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
        
        import torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        import warnings
        warnings.filterwarnings('ignore')
        
        # Check for GPU availability
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"  Loading Qwen3-4B model on {device.upper()}...")
        
        model_name = "Qwen/Qwen3-4B"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,  # Use FP16 on GPU for speed
            device_map="auto" if device == "cuda" else None,  # Auto GPU mapping
            low_cpu_mem_usage=True
        )
        
        # Move to GPU if not already there
        if device == "cuda" and not next(model.parameters()).is_cuda:
            model = model.to(device)
        
        # Create prompt with Wikipedia context
        prompt = f"""Write an engaging 60-second educational script about {topic}.

Wikipedia summary: {wiki_text[:500]}

Create a script that:
- Starts with a hook to grab attention
- Explains the key concept clearly
- Uses simple language
- Is exactly 140-150 words (60 seconds at speaking pace)

Script: """
        
        print("  Generating script with AI...")
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # Move inputs to GPU if available
        if device == "cuda":
            inputs = {k: v.to(device) for k, v in inputs.items()}
        
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.8,
            do_sample=True,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.2
        )
        
        generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
        script = generated.replace(prompt, "").strip()
        
        # Clean up
        script = " ".join(script.split())
        
        # Validate length (should be ~140 words for 60 seconds)
        words = script.split()
        if len(words) < 50:
            print("  ⚠️  Script too short, using Wikipedia-based fallback...")
            raise ValueError("Script too short")
        
        word_count = len(words)
        print(f"✅ AI script ready ({word_count} words, ~{word_count/2.5:.0f} seconds)")
        return script
        
    except Exception as e:
        print(f"  ⚠️  Qwen3 generation failed, using Wikipedia content...")
        
        # Fallback: Use Wikipedia content intelligently
        if wiki_info:
            intro = f"Let me tell you about {topic}."
            
            # Extract first few sentences from Wikipedia
            sentences = wiki_info['summary'].split('. ')
            main_content = '. '.join(sentences[:3]) + '.'
            
            # Add engaging conclusion
            conclusion = f" This concept is fundamental to mathematics and continues to fascinate researchers and enthusiasts worldwide. Understanding {topic} opens doors to deeper mathematical insights."
            
            script = f"{intro} {main_content} {conclusion}"
        else:
            script = f"""{topic} is one of the most fascinating concepts in mathematics. 
            It reveals deep truths about numbers, patterns, and the structure of mathematical reality. 
            This concept has applications across science, engineering, and technology.
            From theoretical foundations to practical implementations, {topic} continues to shape 
            our understanding of the mathematical universe and its countless applications."""
        
        # Clean and format
        clean_script = " ".join(script.split())
        word_count = len(clean_script.split())
        
        print(f"✅ Wikipedia-based script ready ({word_count} words, ~{word_count/2.5:.0f} seconds)")
        return clean_script
        
    except Exception as e:
        print(f"⚠️  Script generation error: {e}")
        return f"{topic} is a fascinating mathematical concept with important applications in science and technology."


def extract_formula_from_wiki(topic, wiki_info):
    """Extract the main formula/equation from Wikipedia text"""
    
    # Common math formulas for known topics
    formula_map = {
        "pythagorean": "a² + b² = c²",
        "fibonacci": "F(n) = F(n-1) + F(n-2)",
        "euler": "e^(iπ) + 1 = 0",
        "quadratic": "x = (-b ± √(b²-4ac)) / 2a",
        "circle": "A = πr²",
        "golden ratio": "φ = (1 + √5) / 2",
        "prime": "p is prime if p > 1 and only divisible by 1 and p",
        "derivative": "f'(x) = lim(h→0) [f(x+h) - f(x)] / h",
        "complex": "z = a + bi where i² = -1",
    }
    
    # Try to find matching formula
    topic_lower = topic.lower()
    for key, formula in formula_map.items():
        if key in topic_lower:
            return formula
    
    # Default formula
    return f"{topic}"


def generate_audio(script, output_path, accent="british"):
    """Generate audio using Edge TTS with British or American accent"""
    print(f"🎤 Generating audio ({accent} accent)...")
    
    try:
        import edge_tts
        import asyncio
        
        # Choose voice based on accent
        voice = "en-GB-RyanNeural" if accent == "british" else "en-US-GuyNeural"
        
        # Edge TTS requires async
        async def _generate():
            communicate = edge_tts.Communicate(script, voice)
            await communicate.save(str(output_path))
        
        # Run async function
        asyncio.run(_generate())
        print(f"✅ Audio generated with {accent} accent")
        return True
        
    except Exception as e:
        print(f"⚠️  Edge TTS failed: {e}")
        print(f"💡 Install with: pip install edge-tts")
        
        # Try fallback to gTTS
        try:
            from gtts import gTTS
            print("  Trying gTTS fallback...")
            
            tts = gTTS(text=script[:500], lang='en', slow=False)
            tts.save(str(output_path))
            print(f"✅ Audio generated with gTTS")
            return True
        except Exception as e2:
            print(f"⚠️  gTTS also failed: {e2}")
            return False


def create_dynamic_video(video_num, total):
    """STEP 3: Generate one video dynamically - Wikipedia topic → Script (Wiki + Qwen3) → Video"""
    
    print(f"\n{'='*70}")
    print(f"🎬 DYNAMIC VIDEO {video_num}/{total}")
    print(f"{'='*70}")
    
    # STEP 1: Select topic from Wikipedia
    topic = select_topic_from_wikipedia(video_num, total)
    
    # STEP 2: Fetch Wikipedia info about the topic
    wiki_info = fetch_wikipedia_info(topic)
    
    # STEP 3: Generate script using Wikipedia + Qwen3
    script = generate_script_with_qwen(topic, wiki_info)
    
    # STEP 4: Extract formula from Wikipedia
    formula = extract_formula_from_wiki(topic, wiki_info)
    
    # STEP 5: Generate animation keyframes based on script
    animation_data = generate_animation_keyframes_with_qwen(topic, script, wiki_info)
    
    # Create output files
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "topic.json", "w") as f:
        json.dump({"topic": topic}, f)
    
    with open(output_dir / "script.json", "w") as f:
        json.dump({"script": script}, f, indent=2)
    
    with open(output_dir / "entities.json", "w") as f:
        json.dump({"entities": [{"text": formula, "type": "formula"}]}, f, indent=2)
    
    # Save animation data
    with open(output_dir / "animation_data.json", "w") as f:
        json.dump(animation_data, f, indent=2)
    
    print(f"📝 Topic: {topic}")
    print(f"📐 Formula: {formula}")
    print(f"📄 Script: {len(script)} characters")
    print(f"🎬 Animation: {len(animation_data.get('keyframes', []))} keyframes")
    
    # Generate audio with British accent
    audio_path = output_dir / "audio.mp3"
    audio_generated = generate_audio(script, audio_path, accent="british")
    
    # Calculate audio duration for proper sync
    audio_duration = 60.0  # Default
    if audio_generated and audio_path.exists():
        try:
            from mutagen.mp3 import MP3
            audio = MP3(str(audio_path))
            audio_duration = audio.info.length
            print(f"🎵 Audio duration: {audio_duration:.1f} seconds")
        except:
            # Fallback: estimate from word count
            word_count = len(script.split())
            audio_duration = word_count / 2.5  # Average speaking rate
            print(f"🎵 Estimated audio duration: {audio_duration:.1f} seconds (from word count)")
    
    # STEP 6: DYNAMICALLY GENERATE MANIM CODE
    print(f"🎨 Generating custom Manim animation code...")
    from scripts.generate_manim_code import generate_manim_code, save_manim_script
    
    manim_code = generate_manim_code(topic, script, wiki_info, formula, audio_duration)
    manim_script_path = save_manim_script(manim_code, "scripts/render_manim_dynamic.py")
    
    if not audio_generated:
        print("⚠️  Continuing without audio...")
    
    # Render video with Manim
    print(f"🎬 Rendering video with DYNAMIC animation + audio (720p 60fps)...")
    
    # Create final output directory
    final_output_dir = Path("output/videos")
    final_output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Use the dynamically generated script
        cmd = ["manim", "-qh", "--fps", "60", "scripts/render_manim_dynamic.py", "DynamicScene"]
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True,
            encoding='utf-8',
            errors='ignore'
        )
        
        # Find generated video
        video_files = list(Path("media/videos/render_manim_dynamic/1080p60").glob("DynamicScene.mp4"))
        if video_files:
            temp_video = video_files[0]
            safe_name = topic.replace(" ", "_").replace("'", "").replace("/", "_")
            final_name = f"{video_num:02d}_{safe_name}_60sec_720p60fps.mp4"
            
            # Use FFmpeg to merge audio if Manim didn't embed it properly
            if audio_generated and audio_path.exists():
                print(f"🔊 Merging audio with FFmpeg...")
                
                # Output directly to final folder
                final_path = final_output_dir / final_name
                
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-i", str(temp_video),
                    "-i", str(audio_path),
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "192k",
                    "-shortest",
                    "-y",
                    str(final_path)
                ]
                
                try:
                    subprocess.run(
                        ffmpeg_cmd,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    print(f"✅ Audio merged successfully with FFmpeg!")
                        
                except subprocess.CalledProcessError as e:
                    print(f"⚠️  FFmpeg failed: {e}")
                    # Fallback: copy original to final location
                    final_path = final_output_dir / final_name
                    if final_path.exists():
                        final_path.unlink()
                    import shutil
                    shutil.copy2(temp_video, final_path)
            else:
                # No audio to merge - copy to final location
                final_path = final_output_dir / final_name
                if final_path.exists():
                    final_path.unlink()
                import shutil
                shutil.copy2(temp_video, final_path)
            
            # Clean up intermediate files
            print(f"🧹 Cleaning up intermediate files...")
            try:
                # Remove the entire media directory tree
                import shutil
                media_dir = Path("media")
                if media_dir.exists():
                    shutil.rmtree(media_dir)
                    print(f"  ✓ Removed media/ directory")
            except Exception as e:
                print(f"  ⚠️  Could not clean media/: {e}")
            
            # If audio was generated separately, merge it (Manim should handle this)
            # Manim's add_sound() should embed the audio automatically
            
            file_size = final_path.stat().st_size / (1024 * 1024)
            print(f"✅ Video saved: {final_path} ({file_size:.1f} MB)")
            
            if audio_generated:
                print(f"🔊 Audio included in video!")
            
            return str(final_path)
        else:
            print("⚠️  Video file not found")
            return None
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error rendering video: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr[:500]}")
        return None


def main():
    """Generate all videos DYNAMICALLY - Wikipedia → Script (Wiki + Qwen3) → Video"""
    
    # Number of videos to generate (can be changed via command line)
    import sys
    num_videos = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    
    print("\n" + "="*70)
    print("🎬 DYNAMIC AI VIDEO GENERATOR")
    print("="*70)
    print(f"📹 Generating {num_videos} videos with:")
    print("  📚 Wikipedia for topic selection")
    print("  🤖 Qwen3-4B AI + Wikipedia for script generation")
    print("  🎤 Edge TTS for professional audio")
    print("  🎨 Manim for 720p 60fps animations")
    print("\n🔄 Pipeline: Wikipedia Topic → Script (Wiki + Qwen3) → Video")
    print("="*70 + "\n")
    
    import time
    start_time = time.time()
    successful = 0
    generated = []
    
    for i in range(1, num_videos + 1):
        video_path = create_dynamic_video(i, num_videos)
        if video_path:
            successful += 1
            generated.append(video_path)
        
        # Brief pause between videos
        time.sleep(2)
    
    total_time = time.time() - start_time
    
    print("\n" + "="*70)
    print(f"✅ COMPLETED: {successful}/{num_videos} videos generated successfully")
    print(f"⏱️  Total time: {total_time/60:.1f} minutes")
    print(f"📁 Location: output/videos/")
    print("="*70)
    
    if generated:
        print("\n📹 Generated videos:")
        for video in generated:
            print(f"  • {Path(video).name}")
    
    print()


if __name__ == "__main__":
    main()
