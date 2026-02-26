# Gazeful

<!--toc:start-->
- [Gazeful](#gazeful)
  - [Hardware Support](#hardware-support)
  - [Supported Platforms](#supported-platforms)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
    - [3. Activate the Virtual Environment](#3-activate-the-virtual-environment)
      - [Linux / macOS (BASH or Zsh)](#linux-macos-bash-or-zsh)
      - [Windows (PowerShell)](#windows-powershell)
      - [Windows (Command Prompt)](#windows-command-prompt)
    - [4. Install Dependencies](#4-install-dependencies)
  - [Usage](#usage)
  - [Data Format](#data-format)
<!--toc:end-->

Gazeful is an open-source desktop graphical environment, acting as an end-to-end
workflow for integrated eye-tracking data acquisition and interactive gaze
visualization.

A screenshot of the analysis view:
![Gazeful editor view](./assets/images/editor-w-window-decorations.png)

A figure presenting the Gazeful workflow:
![Gazeful workflow](./assets/images/workflow.svg)

## Hardware Support

| Hardware | Status | Notes |
| --- | --- | --- |
| Tobii Pro Spark | Working | Used throughout development |
| Other Tobii SDK trackers | Untested | Expected to work |
| Other screen-mounted trackers | Currently unsupported | |
| Head-mounted trackers | Unsupported | |

## Supported Platforms

Gazeful is written with Python and aims to be cross-platform, but testing
coverage varies.

| Platform | Status | Notes |
| --- | --- | --- |
| Linux (X11) | Supported | Expected to work with full functionality |
| Linux (Wayland) | Partial | Gaze visualizer overlay and taking screenshots not supported |
| Windows | Fully functional | |
| macOS | Untested | |

## Features

- Data Acquisition:
    Gazeful supports direct recording of screen-based eye tracker data from a
    single participant at a time.
    Recordings are saved to `.csv` files,
    [examples of which you can find here](./tests/samples/).

- Mouse Emulation:
    Mouse movements may be used to simulate eye tracker data acquisition, where
    the position of the cursor represents human gaze.
    The feature allows for development, demonstration, and exploration of the
    tool without an eye tracker.

- Gaze Visualizer:
    When an eye tracker is connected to Gazeful, a visualizer may be enabled,
    displaying the participant's current eye position as an overlay on the
    screen.

- Automatic Processing:
    After recording has been finished, or a `.csv` file is manually loaded,
    Gazeful automatically processes the raw data into fixations using an
    implementation of dispersion-threshold identification.

- Editor:
    Once the data has been processed, it may be interactively explored in the
    Editor view.
    The Editor features:

  - A choice between absolute fixation duration heatmaps, fixation count
    heatmaps, and gaze plots.
    The visualization may be changed at any time.

  - Parameters necessary for identification by dispersion-threshold.
    Changing these will automatically reprocess the data.

  - Visualization parameters, such as the heatmap color scale, opacity,
    blur strength, gaze plot connection and spot colors.

  - Interactive analysis.
    Heatmap color scales can be moved to emphasize or suppress fixation regions.
    Both heatmaps and gaze plots utilize hover-based interaction, where hovering
    over fixations will display quantitative information, such as duration and
    location.
    Hovering over fixations in the gaze plot will additionally highlight
    adjacent fixations.

## Getting Started

The following section outlines how to set up Gazeful.

- Python 3.10 is required.
- Dependencies are listed in [requirements.txt](./requirements.txt).
- Using a virtual environment is recommended.

### 1. Clone the Repository

```bash
git clone git@github.com:krznck/gazeful.git
cd gazeful
```

### 2. Create a Virtual Environment

All platforms:

```bash
python -m venv .venv
```

### 3. Activate the Virtual Environment

#### Linux / macOS (BASH or Zsh)

```bash
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
.venv\Scripts\Activate.ps1
```

> If PowerShell blocks activation, you may need to run:
>
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

#### Windows (Command Prompt)

```cmd
.venv\Scripts\activate.bat
```

### 4. Install Dependencies

All platforms:

```bash
pip install --requirement requirements.txt
```

## Usage

Run the application:

```bash
python main.py
```

## Data Format

Gazeful produces and reads eye-tracked data via `.csv` files in the following
format.
Note that samples of recorded gaze
[can be found here](./tests/samples/).

```csv
#1920x1200
x,y,timestamp
0.2854602783918381,0.15251591056585312,0.0
0.2863858789205551,0.1512339562177658,0.030999999999039574
0.2857642024755478,0.15045832842588425,0.046999999998661224
0.28722967207431793,0.14983608573675156,0.06199999999989814
NA,NA,0.07799999999951979
NA,NA,0.09399999999914144
NA,NA,0.10899999999855936
NA,NA,0.125
0.2894028425216675,0.1486806944012642,0.13999999999941792
0.288333460688591,0.150211863219738,0.15599999999903957
0.28788837790489197,0.1548076942563057,0.17199999999866122
0.28981468081474304,0.15458183735609055,0.18699999999989814
```

The first line should be the resolution of the target screen.
The second line should be the column declaration, `x,y,timestamp`.
Values should be written in floating point format.
When eyes are closed or undetected, the `x` and `y` values should be marked as
`NA`.
