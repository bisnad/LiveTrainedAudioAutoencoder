# ALTA - Audio Live-Trained Autoencoder
## Installation Guide

> **Requirements:** 
>
> - Operating system requirements: The code has been tested on Windows computers running Windows 10 and 11, and Apple computers with  Apple silicon running macOS Ventura or newer. 
> - GPU requirements: The code required a graphics processing unit (Apple-designed GPU or Nvidia GPU) to run at acceptable speed for training and real-time inference.

---

## Contents

1. [Install a compilation environment](#2-install-a-compilation-environment)
2. [Install Git and Git LFS](#3-install-git-and-git-lfs)
3. [Install uv](#4-install-uv)
4. [Download this repository](#5-download-repository)
5. [Install python environment](#6-install-python-environment)
6. [Test installation](#7-test-installation)

---

## 1. Install a compilation environment

Some Python dependencies require compilation during installation. 

### macOS: install Xcode Command Line Tools (includes Git)

1. Open **Terminal**.
2. Run:

```bash
xcode-select --install
```

3. A macOS dialog appears. Choose **Install**.
4. Accept any licence or permission requests and wait until installation completes.
5. Close Terminal, then open a new Terminal window.

#### Verify the compiler and Git

Run these commands one at a time:

```bash
clang --version
make --version
git --version
```

**Success:** Each command displays version information rather than an error.

### Windows: install Visual Studio Build Tools

1. Open **PowerShell**.
2. Copy the complete command below into PowerShell and press Enter. This is one command; the backtick character (`` ` ``) continues it onto the next line.

```powershell
winget install --exact --id Microsoft.VisualStudio.2022.BuildTools `
  --override "--passive --wait --norestart --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended"
```

3. If Windows shows a UAC permission window, choose **Yes**.
4. Wait for the installation to finish. It may take some time.
5. Close every currently open PowerShell window.

#### Verify the compiler

1. Open the **Start** menu.
2. Search for and open:

```text
x64 Native Tools Command Prompt for VS 2022
```

3. Run:

```text
cl
```

**Success:** The output begins with text similar to:

```text
Microsoft (R) C/C++ Optimizing Compiler Version ...
```

---

## 2. Install Git and Git LFS

Git it useful to download small files such as source code whereas Git LFS (*Large File Storage*) can download large files, such as audio and model weights.

### macOS: install Git LFS

Git was installed in Section 1 with the Xcode Command Line Tools. This section installs Git LFS.

1. Open [git-lfs.com](https://git-lfs.com/) in a web browser.
2. Download the **Apple Silicon** version of Git LFS for macOS.
3. Open the downloaded ZIP file to unpack it.
4. Open **Terminal**.
5. Run:

```bash
cd ~/Downloads/git-lfs-*
sudo ./install.sh
```

6. Enter your Mac password if requested. 

#### Verify Git LFS

Open a new Terminal window and run:

```bash
git lfs version
```

**Success:** You should see a Git LFS version number.

### Windows: install Git

1. Open the **Start** menu.
2. Search for **PowerShell** and open it.
3. Paste this command and press Enter:

```powershell
winget install --exact --id Git.Git --source winget
```

4. If Windows displays a **User Account Control (UAC)** prompt, choose **Yes**.
5. When the installation is complete, close PowerShell.

#### Verify Git

Open a **new** PowerShell window and run:

```powershell
git --version
```

**Success:** You should see a version number, such as `git version 2.x.x`.

### Windows: install Git LFS

1. Open [git-lfs.com](https://git-lfs.com/) in a web browser.
2. Download and install the Windows version of Git LFS.
3. Open a new PowerShell window.
4. Run:

```powershell
git lfs install
```

#### Verify Git LFS

```powershell
git lfs version
```

**Success:** You should see a Git LFS version number.

---

## 3. Install uv

[`uv`](https://docs.astral.sh/uv/) manages the Python environment and packages used by the autoencoder.

### macOS: install uv

1. Open **Terminal**.
2. Run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. When the installation finishes, close Terminal.
4. Open a **new** Terminal window.

#### Verify uv

```bash
uv --version
```

**Success:** You should see a uv version number.

> If Terminal says `uv: command not found`, close Terminal completely, open it again, and retry.

### Windows: install uv

1. Open **PowerShell**.
2. Run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

3. When installation finishes, close PowerShell.
4. Open a **new** PowerShell window.

#### Verify uv

```powershell
uv --version
```

**Success:** You should see a uv version number.

---

## 4. Download the repository

1. Open **Terminal** on macOS or **PowerShell** on Windows.
2. Move into your folder you want the repository be downloaded into. 

```bash
cd <path-to-your-folde>
```

3. Download the repository:

```bash
git clone https://github.com/bisnad/LiveTrainedAudioAutoencoder
```

4. Wait for the command to complete. Do not close the window during the download.

#### Check your work

Your folder should now contain:

```text
LiveTrainedAudioAutoencoder
```

### macOS: open `.sh` files in Terminal

The repository provides bash shell scripts for convenience to automate certain installation steps and the starting of python scripts. For these scripts to be double-clickable, the Finder has to be configured to open the shell scripts in Terminal:

1. In Finder, open `LiveTrainedAudioAutoencoder`.
2. Navigate to `Installers/run_installation_macos.sh`.
3. Select the file and press **Command + I** to open **Get Info**.
4. Under **Open with**, select **Terminal**.
5. Click **Change All...** if you want every `.sh` file to open in Terminal.
6. Confirm the change if macOS asks.

---

## 5. Install the Python environment

The installation script copies the correct `uv` project file (`pyproject.toml`) to the Software folder.

### macOS: run the installation script

1. In Finder, open:

```text
LiveTrainedAudioAutoencoder/Installers
```

2. Double-click:

```text
run_installation_macos.sh
```

3. Terminal opens and runs the script.
4. Wait until the script completes.

### Windows: run the installation script

1. In File Explorer, open:

```text
LiveTrainedAudioAutoencoder/Installers
```

2. Double-click:

```text
run_installation_windows.bat
```

3. Command prompt opens and runs the script.
4. Wait until the script completes.

> If Windows displays a security warning, first confirm that the file is inside the `LiveTrainedAudioAutoencoder` folder downloaded from the official course link. Then choose to run it.

---

## 6. Run the audio autoencoder

When you run the autoencoder for the first time, `uv` automatically creates a Python environment and downloads the required packages. This can take a while. Later runs are much faster.

### macOS: run the application script

1. In Finder, open:

```text
LiveTrainedAudioAutoencoder/Software/AudioAutoencoder
```

2. Double-click:

```text
audio_autoencoder.sh
```

3. Terminal opens and runs the script.
4. If you run the script for the first time, the uv environment will be created and model weights will be downloaded.
5. If everything works fine, application window of the audio autoencoder opens.

### Windows: run the application script

1. In File Explorer, open:

```text
LiveTrainedAudioAutoencoder/Software/AudioAutoencoder
```

2. Double-click:

```text
audio_autoencoder.bat
```

3. Command prompt opens and runs the script.
4. If you run the script for the first time, the uv environment will be created and model weights will be downloaded.
5. If everything works fine, application window of the audio autoencoder opens.

---

