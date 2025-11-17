# Docker Setup Guide for Windows

This guide will help you run Project Forge seamlessly on Windows using Docker.

## Prerequisites

### 1. Install Docker Desktop for Windows

Download and install Docker Desktop from: https://www.docker.com/products/docker-desktop/

**System Requirements:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- OR Windows 11 64-bit: Home, Pro, Enterprise, or Education
- WSL 2 feature enabled (Docker Desktop will help you set this up)
- At least 4GB RAM (8GB recommended)
- Virtualization enabled in BIOS

**Installation Steps:**
1. Download Docker Desktop installer
2. Run the installer
3. Follow the prompts to enable WSL 2
4. Restart your computer when prompted
5. Launch Docker Desktop and wait for it to start

**Verify Installation:**
```cmd
docker --version
docker-compose --version
```

You should see version numbers for both commands.

### 2. Configure API Keys

1. Copy the example environment file:
   ```cmd
   copy .env.example .env
   ```

2. Edit `.env` file with your favorite text editor (Notepad, VS Code, etc.)

3. Add your API key(s):
   ```
   # Use OpenAI
   OPENAI_API_KEY=sk-your-actual-openai-key-here

   # OR use Anthropic
   ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
   ```

**Note:** You need at least ONE API key (OpenAI or Anthropic).

## Quick Start (Windows)

### Option 1: Streamlit Web UI (Recommended)

**Step 1: Build the Docker Image**
```cmd
docker-build.bat
```
Wait for the build to complete (first time takes 2-5 minutes).

**Step 2: Start the Web UI**
```cmd
docker-start-ui.bat
```

**Step 3: Open Your Browser**
Navigate to: http://localhost:8501

You should see the Project Forge Streamlit interface!

**Step 4: Stop the UI When Done**
```cmd
docker-stop.bat
```

### Option 2: Command Line Interface (CLI)

**Run the CLI with your project idea:**
```cmd
docker-run-cli.bat "Build a habit tracker app with daily reminders and streak tracking"
```

The generated README/PRD will be saved in the `output/` folder.

## Detailed Usage

### Windows Batch Scripts

We've provided convenient batch scripts for Windows users:

| Script | Purpose |
|--------|---------|
| `docker-build.bat` | Build the Docker image |
| `docker-start-ui.bat` | Start the Streamlit web interface |
| `docker-run-cli.bat` | Run the CLI to generate a README |
| `docker-stop.bat` | Stop all running containers |
| `docker-logs.bat` | View logs from the Streamlit container |

### Manual Docker Commands

If you prefer to use Docker commands directly:

**Build the image:**
```cmd
docker-compose build
```

**Start Streamlit UI:**
```cmd
docker-compose up -d streamlit
```

**Run CLI:**
```cmd
docker-compose run --rm cli "Your project idea here"
```

**Stop containers:**
```cmd
docker-compose down
```

**View logs:**
```cmd
docker logs -f project-forge-streamlit
```

## File Locations

### Output Directory

Generated READMEs and PRDs are saved to:
```
Readme-Builder/output/
```

This folder is automatically created and mounted to the Docker container.

### Input Directory (CLI only)

For batch processing, you can place text files with project ideas in:
```
Readme-Builder/input/
```

### Configuration Files

Default configurations are in:
```
Readme-Builder/project_forge/src/config/defaults.yaml
```

You can modify these settings - changes will be reflected in the container.

## Troubleshooting

### "Docker daemon is not running"

**Solution:** Start Docker Desktop from the Windows Start menu and wait for it to fully start.

### "Permission denied" or "Access denied" errors

**Solution:**
1. Make sure Docker Desktop is running
2. Ensure your Windows user has admin privileges
3. Try running Command Prompt as Administrator

### "Port 8501 is already in use"

**Solution:**
1. Stop any other Streamlit apps running on your system
2. OR change the port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8502:8501"  # Change 8501 to 8502 or any free port
   ```

### "Cannot connect to Docker daemon"

**Solution:**
1. Restart Docker Desktop
2. Check if WSL 2 is properly installed:
   ```cmd
   wsl --status
   ```
3. Update WSL if needed:
   ```cmd
   wsl --update
   ```

### ".env file not found" error

**Solution:**
1. Make sure you've copied `.env.example` to `.env`
2. Place the `.env` file in the root `Readme-Builder/` directory
3. Check that the file is named exactly `.env` (not `.env.txt`)

### API key errors

**Solution:**
1. Verify your API key is correct in the `.env` file
2. Make sure there are no extra spaces or quotes around the key
3. Test your API key independently before using with Docker

### Slow performance on Windows

**Solution:**
1. Ensure WSL 2 is being used (not WSL 1)
2. Allocate more resources to Docker Desktop:
   - Open Docker Desktop
   - Go to Settings → Resources
   - Increase CPUs and Memory
   - Click "Apply & Restart"

### Container won't start

**Solution:**
1. Check the logs:
   ```cmd
   docker-logs.bat
   ```
2. Rebuild the image:
   ```cmd
   docker-compose down
   docker-build.bat
   ```
3. Clear Docker cache and rebuild:
   ```cmd
   docker system prune -a
   docker-build.bat
   ```

## Advanced Usage

### Using Different LLM Models

Edit your `.env` file to specify a different model:

```env
# For OpenAI
OPENAI_MODEL=gpt-4-turbo

# For Anthropic
ANTHROPIC_MODEL=claude-3-sonnet-20240229
```

### Customizing Configurations

Edit `project_forge/src/config/defaults.yaml` to customize:
- Skill level presets (beginner, intermediate, advanced)
- Framework templates
- Project type settings
- Agent behavior parameters

Changes take effect immediately (no rebuild needed).

### Running on Different Network

To access the UI from other devices on your network:

1. Find your Windows IP address:
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" under your active network adapter.

2. Access from other devices:
   ```
   http://YOUR_IP_ADDRESS:8501
   ```

3. Make sure Windows Firewall allows incoming connections on port 8501.

### Batch Processing Multiple Ideas

Create a text file `input/ideas.txt` with one idea per line:
```
Build a habit tracker app
Create a recipe API with search
Develop a code review agent system
```

Then process each idea:
```cmd
for /f "delims=" %i in (input/ideas.txt) do docker-run-cli.bat "%i"
```

## Performance Tips

1. **First Run is Slow:** The first build downloads ~1GB of dependencies. Subsequent builds use cache and are much faster.

2. **Keep Docker Desktop Running:** Leave Docker Desktop running in the background for faster container starts.

3. **Allocate Sufficient Resources:**
   - Minimum: 2 CPUs, 4GB RAM
   - Recommended: 4 CPUs, 8GB RAM
   - Configure in Docker Desktop → Settings → Resources

4. **Use SSD:** Store the project on an SSD for better I/O performance.

5. **WSL 2 Backend:** Always use WSL 2 backend (not Hyper-V) for better performance.

## Security Best Practices

1. **Never commit your `.env` file** - It's in `.gitignore` by default
2. **Use environment-specific API keys** - Don't use production keys for testing
3. **Keep Docker Desktop updated** - Regular updates include security patches
4. **Limit API key permissions** - Use keys with minimal required permissions

## Getting Help

### Check Logs
```cmd
docker-logs.bat
```

### Check Container Status
```cmd
docker ps -a
```

### Access Container Shell (for debugging)
```cmd
docker exec -it project-forge-streamlit /bin/bash
```

### Reset Everything
```cmd
docker-compose down
docker system prune -a
docker-build.bat
docker-start-ui.bat
```

## Next Steps

1. **Explore the Web UI:** Try different project ideas and skill levels
2. **Read the Main README:** See `README.md` for project details
3. **Check Examples:** Look in `project_forge/examples/` for sample outputs
4. **Customize Configs:** Modify `defaults.yaml` for your preferences

## Additional Resources

- [Docker Desktop for Windows Documentation](https://docs.docker.com/desktop/windows/)
- [WSL 2 Setup Guide](https://docs.microsoft.com/en-us/windows/wsl/install)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Project Forge GitHub Issues](https://github.com/mshears713/Readme-Builder/issues)

---

**Happy Building! 🚀**

For questions or issues, please create an issue on GitHub or consult the main README.md file.
