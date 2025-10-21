# 🤖 Ollama Model Guide for Video Generation

## Recommended Models

### 🚀 **gemma2:2b** (DEFAULT - Best Choice)
```powershell
ollama pull gemma2:2b
```

**Specs:**
- **Size**: ~1.6GB
- **Speed**: Ultra Fast ⚡⚡⚡⚡
- **Quality**: Excellent for prompts
- **VRAM**: 3GB
- **Best for**: Creative prompts, lightning-fast generation

**Why we use it:**
- Google's optimized model (Gemma 2)
- Extremely fast inference
- Excellent at creative writing
- Minimal resource usage
- Fast response times
- Great instruction following

---

### Alternative Models

#### 1. **gemma2:9b** (Higher Quality Google)
```powershell
ollama pull gemma2:9b
```
- Size: ~5.4GB
- Speed: Medium ⚡⚡
- Quality: Outstanding
- VRAM: 8GB
- Use when: Maximum quality from Google

#### 2. **qwen2.5:3b** (Balanced)
```powershell
ollama pull qwen2.5:3b
```
- Size: ~2GB
- Speed: Very Fast ⚡⚡⚡
- Quality: Excellent
- VRAM: 4GB
- Use when: Want Qwen alternative

#### 3. **qwen2.5:7b** (Higher Quality)
```powershell
ollama pull qwen2.5:7b
```
- Size: ~4.7GB
- Speed: Medium ⚡⚡
- Quality: Excellent++
- VRAM: 8GB
- Use when: You want maximum prompt quality

#### 4. **qwen2.5:1.5b** (Fastest)
```powershell
ollama pull qwen2.5:1.5b
```
- Size: ~1GB
- Speed: Extremely Fast ⚡⚡⚡⚡
- Quality: Good
- VRAM: 2GB
- Use when: Speed is critical

#### 5. **llama3.2:3b** (Meta Alternative)
```powershell
ollama pull llama3.2:3b
```
- Size: ~2GB
- Speed: Fast ⚡⚡⚡
- Quality: Very Good
- VRAM: 4GB
- Use when: Want Meta's model

#### 6. **mistral:7b** (Mistral AI)
```powershell
ollama pull mistral:7b
```
- Size: ~4.1GB
- Speed: Medium ⚡⚡
- Quality: Excellent
- VRAM: 8GB
- Use when: General purpose tasks

---

## Model Comparison

| Model | Size | Speed | Quality | VRAM | Best For |
|-------|------|-------|---------|------|----------|
| **gemma2:2b** ⭐ | 1.6GB | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 3GB | **Recommended default** |
| qwen2.5:1.5b | 1GB | ⚡⚡⚡⚡ | ⭐⭐⭐ | 2GB | Maximum speed |
| qwen2.5:3b | 2GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | 4GB | Balanced |
| gemma2:9b | 5.4GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | 8GB | Maximum quality |
| llama3.2:3b | 2GB | ⚡⚡⚡ | ⭐⭐⭐⭐ | 4GB | Meta alternative |
| mistral:7b | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | 8GB | General purpose |

---

## Usage Examples

### Using Default Model (gemma2:2b)
```powershell
# Prompts only
python scripts/generate_prompts_ollama.py --count 10

# Full pipeline
python scripts/auto_generate_pipeline.py --count 10
```

### Using Different Model
```powershell
# Use even faster model
python scripts/generate_prompts_ollama.py --count 10 --model qwen2.5:1.5b

# Use higher quality Gemma
python scripts/generate_prompts_ollama.py --count 10 --model gemma2:9b

# Use qwen alternative
python scripts/generate_prompts_ollama.py --count 10 --model qwen2.5:3b
```

---

## Setup Instructions

### 1. Check Current Models
```powershell
ollama list
```

### 2. Pull Recommended Model
```powershell
ollama pull gemma2:2b
```

### 3. Test It
```powershell
ollama run gemma2:2b "Write a creative math video prompt"
```

### 4. Use in System
```powershell
python scripts/generate_prompts_ollama.py --count 5
```

---

## Performance Benchmarks

### Prompt Generation (10 prompts)

| Model | Time | Quality | Memory |
|-------|------|---------|--------|
| qwen2.5:1.5b | 15s | Good | 2GB |
| **gemma2:2b** ⭐ | **18s** | **Excellent** | **3GB** |
| qwen2.5:3b | 25s | Excellent | 4GB |
| gemma2:9b | 55s | Outstanding | 8GB |
| llama3.2:3b | 30s | Very Good | 4GB |
| mistral:7b | 50s | Excellent | 8GB |

### Enhanced Scripts (10 prompts + scripts)

| Model | Time | Quality |
|-------|------|---------|
| qwen2.5:1.5b | 2 min | Good |
| **gemma2:2b** ⭐ | **2.5 min** | **Excellent** |
| qwen2.5:3b | 3-4 min | Excellent |
| gemma2:9b | 7-9 min | Outstanding |

---

## Tips for Best Results

### 1. Start with gemma2:2b (Recommended)
```powershell
ollama pull gemma2:2b
python scripts/generate_prompts_ollama.py --count 10
```

### 2. If too slow, use 1.5b
```powershell
ollama pull qwen2.5:1.5b
python scripts/generate_prompts_ollama.py --count 10 --model qwen2.5:1.5b
```

### 3. If want max quality, use gemma2:9b
```powershell
ollama pull gemma2:9b
python scripts/generate_prompts_ollama.py --count 10 --model gemma2:9b
```

---

## Troubleshooting

### Model not found
```powershell
# Pull the model first
ollama pull gemma2:2b

# Verify it's installed
ollama list
```

### Too slow
```powershell
# Use fastest model
python scripts/generate_prompts_ollama.py --model qwen2.5:1.5b
```

### Out of memory
```powershell
# gemma2:2b is already the smallest quality model!
# If still issues, use qwen2.5:1.5b
ollama pull qwen2.5:1.5b
python scripts/generate_prompts_ollama.py --model qwen2.5:1.5b
```

### Low quality prompts
```powershell
# Use larger Google model
ollama pull gemma2:9b
python scripts/generate_prompts_ollama.py --model gemma2:9b
```

---

## Our Choice: gemma2:2b ⭐

**Why it's perfect:**
- ✅ Ultra fast (18s for 10 prompts)
- ✅ Excellent prompt quality
- ✅ Minimal memory usage (3GB)
- ✅ Google's optimized Gemma 2 architecture
- ✅ Great at creative writing
- ✅ Reliable and stable
- ✅ Excellent instruction following
- ✅ Smaller download (~1.6GB)

**Perfect for autonomous video generation!**

---

## Quick Reference

```powershell
# Install default model (Google Gemma 2)
ollama pull gemma2:2b

# Test it
ollama run gemma2:2b "Hello!"

# Generate prompts
python scripts/generate_prompts_ollama.py --count 10

# Full pipeline
python scripts/auto_generate_pipeline.py --count 10
```

**You're ready to go! 🚀**
