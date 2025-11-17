# Docker Quick Start Guide

Get Project Forge running in 5 minutes on Windows, macOS, or Linux.

## Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop/))
- OpenAI API key OR Anthropic API key

## 3-Step Setup

### Step 1: Configure API Key

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
# Windows: notepad .env
# Mac/Linux: nano .env
```

Add your key to the `.env` file:
```env
OPENAI_API_KEY=sk-your-key-here
# OR
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

### Step 2: Build the Image

**Windows:**
```cmd
docker-build.bat
```

**Mac/Linux:**
```bash
docker-compose build
```

### Step 3: Start the Web UI

**Windows:**
```cmd
docker-start-ui.bat
```

**Mac/Linux:**
```bash
docker-compose up -d streamlit
```

### Step 4: Open Your Browser

Navigate to: **http://localhost:8501**

## Usage Examples

### Web UI (Recommended)

1. Start the UI (see Step 3 above)
2. Open http://localhost:8501
3. Enter your project idea
4. Select skill level and project type
5. Click "Generate README"
6. Download your generated README from the `output/` folder

### Command Line Interface

**Windows:**
```cmd
docker-run-cli.bat "Build a todo app with React and Firebase"
```

**Mac/Linux:**
```bash
docker-compose run --rm cli "Build a todo app with React and Firebase"
```

Output will be saved to `output/` folder.

## Stopping the Application

**Windows:**
```cmd
docker-stop.bat
```

**Mac/Linux:**
```bash
docker-compose down
```

## Viewing Logs

**Windows:**
```cmd
docker-logs.bat
```

**Mac/Linux:**
```bash
docker logs -f project-forge-streamlit
```

## Common Issues

### "Docker daemon not running"
- Start Docker Desktop and wait for it to fully start

### "Port 8501 already in use"
- Stop other Streamlit apps or change the port in `docker-compose.yml`

### "API key error"
- Verify your API key in the `.env` file
- Make sure there are no extra spaces or quotes

## File Locations

| Location | Purpose |
|----------|---------|
| `output/` | Generated READMEs and PRDs |
| `input/` | Input files for batch processing (optional) |
| `.env` | Your API keys (do not commit!) |
| `project_forge/src/config/` | Configuration files |

## More Help

- **Windows Users:** See [DOCKER_WINDOWS_GUIDE.md](DOCKER_WINDOWS_GUIDE.md) for detailed Windows-specific instructions
- **Project Details:** See [README.md](README.md) for full project documentation
- **Issues:** Create an issue on GitHub

---

**That's it! You're ready to generate comprehensive project READMEs with AI.**
