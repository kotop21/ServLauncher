<div align="center">

# Astra Launcher

**A fast and modern Minecraft server manager.**

<br>

<img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/GUI-CustomTkinter-1f5c87?style=for-the-badge" alt="CustomTkinter">
<img src="https://img.shields.io/badge/Package_Manager-uv-232F3E?style=for-the-badge" alt="uv">
<img src="https://img.shields.io/badge/CI/CD-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions">
<img src="https://img.shields.io/badge/License-AGPLv3-blue?style=for-the-badge" alt="License">

<br><br>

![preview](public/preview.png)

</div>


## Installation & Downloads

All downloads and setup instructions are available on the [website](https://kotop21.github.io/AstraLauncher/).

Development builds and CI status can be found in [GitHub Actions](https://github.com/kotop21/AstraLauncher/actions).

## Building from Source

Astra Launcher uses a modern monorepo architecture powered by `uv`.

### 1. Clone the repository

```bash
git clone https://github.com/kotop21/AstraLauncher.git
cd AstraLauncher
```

### 2. Install dependencies

```bash
uv sync --all-packages --no-dev
```

### 3. Run in development mode

```bash
uv run desktop
```

### 4. Build locally

```bash
uv run build_local.py
```

## Community & Support

Feel free to open an issue if you find a bug, want to suggest a feature, or need help.

## License

Licensed under the GNU AGPLv3 License.
