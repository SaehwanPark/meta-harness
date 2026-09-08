#!/usr/bin/env bash
# Meta Harness Installer (macOS and Linux)
#
# Quick install:
#   curl -fsSL https://raw.githubusercontent.com/SaehwanPark/meta-harness/main/install.sh | bash
#
# Local install from cloned repository:
#   ./install.sh
#
set -euo pipefail

REPO_URL="https://github.com/SaehwanPark/meta-harness.git"
TARBALL_URL="https://github.com/SaehwanPark/meta-harness/archive/refs/heads/main.tar.gz"
DEFAULT_BIN_DIR="${HOME}/.local/bin"
DEFAULT_INSTALL_DIR="${HOME}/.meta-harness"

BIN_DIR="${META_HARNESS_BIN_DIR:-$DEFAULT_BIN_DIR}"
INSTALL_DIR="${META_HARNESS_INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
USE_SYMLINK=false
FORCE=false

print_help() {
  cat << EOF
Meta Harness Installer

Usage:
  install.sh [OPTIONS]

Options:
  --bin-dir <path>      Directory for the meta-harness executable (default: ~/.local/bin)
  --install-dir <path>  Target directory when cloning standalone (default: ~/.meta-harness)
  --symlink             Create a symlink instead of an executable wrapper script
  --force               Overwrite existing launcher if present
  -h, --help            Show this help message
EOF
}

# Parse command line options
while [[ $# -gt 0 ]]; do
  case "$1" in
    --bin-dir)
      BIN_DIR="$2"
      shift 2
      ;;
    --install-dir)
      INSTALL_DIR="$2"
      shift 2
      ;;
    --symlink)
      USE_SYMLINK=true
      shift
      ;;
    --force)
      FORCE=true
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      print_help >&2
      exit 1
      ;;
  esac
done

# Step 1: Detect Python 3.8+
find_python() {
  for candidate in python3 python; do
    if command -v "$candidate" >/dev/null 2>&1; then
      if "$candidate" -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)" >/dev/null 2>&1; then
        echo "$candidate"
        return 0
      fi
    fi
  done
  return 1
}

PYTHON="$(find_python || true)"
if [[ -z "$PYTHON" ]]; then
  echo "ERROR: Python 3.8 or newer is required to run Meta Harness, but none was found." >&2
  echo "Please install Python 3:" >&2
  echo "  - macOS: brew install python3" >&2
  echo "  - Ubuntu/Debian: sudo apt update && sudo apt install -y python3" >&2
  echo "  - Fedora/RHEL: sudo dnf install -y python3" >&2
  echo "  - Or download from https://www.python.org/downloads/" >&2
  exit 1
fi

# Step 2: Determine source repository location
# Check if running from within an existing meta-harness repository clone
LOCAL_REPO=""
SCRIPT_SOURCE=""

if [[ -n "${BASH_SOURCE[0]:-}" && "${BASH_SOURCE[0]}" != "sh" && "${BASH_SOURCE[0]}" != "bash" && -f "${BASH_SOURCE[0]}" ]]; then
  SCRIPT_SOURCE="${BASH_SOURCE[0]}"
elif [[ -n "${0:-}" && "$0" != "sh" && "$0" != "-sh" && "$0" != "bash" && -f "$0" ]]; then
  SCRIPT_SOURCE="$0"
fi

if [[ -n "$SCRIPT_SOURCE" ]]; then
  CANDIDATE="$(cd -P "$(dirname "$SCRIPT_SOURCE")" && pwd)"
  if [[ -f "$CANDIDATE/scripts/install_harness.py" && -d "$CANDIDATE/.agents/skills/harness" ]]; then
    LOCAL_REPO="$CANDIDATE"
  fi
fi

if [[ -z "$LOCAL_REPO" && -f "./scripts/install_harness.py" && -d "./.agents/skills/harness" ]]; then
  LOCAL_REPO="$(pwd -P)"
fi

if [[ -n "$LOCAL_REPO" ]]; then
  TARGET_REPO="$LOCAL_REPO"
  echo "==> Using local Meta Harness repository: $TARGET_REPO"
else
  TARGET_REPO="$INSTALL_DIR"
  echo "==> Installing Meta Harness to: $TARGET_REPO"
  mkdir -p "$(dirname "$TARGET_REPO")"
  if [[ -d "$TARGET_REPO/.git" ]]; then
    echo "Updating existing installation in $TARGET_REPO..."
    git -C "$TARGET_REPO" pull --ff-only || true
  elif [[ -d "$TARGET_REPO" && -f "$TARGET_REPO/scripts/install_harness.py" ]]; then
    echo "Found existing installation at $TARGET_REPO."
  else
    if command -v git >/dev/null 2>&1; then
      echo "Cloning repository..."
      git clone --depth 1 "$REPO_URL" "$TARGET_REPO"
    elif command -v curl >/dev/null 2>&1 && command -v tar >/dev/null 2>&1; then
      echo "Downloading archive..."
      mkdir -p "$TARGET_REPO"
      curl -fsSL "$TARBALL_URL" | tar -xz -C "$TARGET_REPO" --strip-components=1
    else
      echo "ERROR: Neither 'git' nor 'curl' + 'tar' was found. Please install git or curl." >&2
      exit 1
    fi
  fi
fi

# Step 3: Set up executable launcher in $BIN_DIR
mkdir -p "$BIN_DIR"
LAUNCHER="$BIN_DIR/meta-harness"

if [[ -e "$LAUNCHER" && "$FORCE" != "true" ]]; then
  echo "Existing executable found at $LAUNCHER (updating launcher)..."
fi

if [[ "$USE_SYMLINK" == "true" ]]; then
  ln -sf "$TARGET_REPO/meta-harness" "$LAUNCHER"
else
  cat << EOF > "$LAUNCHER"
#!/usr/bin/env bash
# Meta Harness CLI Launcher
set -euo pipefail

# Discover Python 3
PYTHON=""
if command -v python3 >/dev/null 2>&1; then
  PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON="python"
else
  echo "Error: Python 3 was not found on PATH." >&2
  exit 1
fi

exec "\$PYTHON" "$TARGET_REPO/scripts/install_harness.py" "\$@"
EOF
  chmod +x "$LAUNCHER"
fi

# Step 4: Validate installation
VERSION_OUTPUT="$("$LAUNCHER" --version 2>&1 || true)"

# Step 5: Check PATH status
PATH_CONFIGURED=false
case ":$PATH:" in
  *":$BIN_DIR:"*)
    PATH_CONFIGURED=true
    ;;
esac

echo ""
echo "========================================================"
echo "  Meta Harness $VERSION_OUTPUT installed successfully!"
echo "========================================================"
echo ""
echo "Executable installed at:"
echo "  $LAUNCHER"
echo ""

if [[ "$PATH_CONFIGURED" == "true" ]]; then
  echo "'meta-harness' is in your PATH and immediately executable!"
  echo ""
  echo "Try running:"
  echo "  meta-harness --help"
  echo "  meta-harness install --scope project --target /path/to/repo --agent generic"
else
  echo "NOTICE: '$BIN_DIR' is not currently in your system PATH."
  echo ""
  echo "To make 'meta-harness' executable from any directory, add this line to your shell profile:"

  USER_SHELL="$(basename "${SHELL:-bash}")"
  case "$USER_SHELL" in
    zsh)
      PROFILE_FILE="~/.zshrc"
      echo "  echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.zshrc"
      echo "  source ~/.zshrc"
      ;;
    bash)
      if [[ "$(uname -s)" == "Darwin" ]]; then
        PROFILE_FILE="~/.bash_profile"
        echo "  echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.bash_profile"
        echo "  source ~/.bash_profile"
      else
        PROFILE_FILE="~/.bashrc"
        echo "  echo 'export PATH=\"$BIN_DIR:\$PATH\"' >> ~/.bashrc"
        echo "  source ~/.bashrc"
      fi
      ;;
    fish)
      echo "  fish_add_path $BIN_DIR"
      ;;
    *)
      echo "  export PATH=\"$BIN_DIR:\$PATH\""
      ;;
  esac

  echo ""
  echo "In the meantime, you can run meta-harness directly using:"
  echo "  $LAUNCHER --help"
fi
echo ""
