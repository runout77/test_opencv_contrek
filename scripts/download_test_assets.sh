#!/usr/bin/env bash
set -euo pipefail

mkdir -p images

download_if_missing() {
  local file="$1"
  local url="$2"

  if [ -f "images/$file" ]; then
    echo "[OK] images/$file already present"
    return
  fi

  echo "[DOWNLOAD] $file"
  curl -L --fail "$url" -o "images/$file"
}

download_if_missing \
  test_81920x81920.png \
  "https://github.com/runout77/test_opencv_contrek/releases/download/test-assets-v1/test_81920x81920.png"