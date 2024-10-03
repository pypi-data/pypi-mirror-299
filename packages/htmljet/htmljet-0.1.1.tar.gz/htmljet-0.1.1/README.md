# HTMLJet

HTMLJet is a powerful command-line tool for capturing screenshots of HTML elements on web pages. It provides advanced features for analyzing HTML structure, taking screenshots at different levels, and cleaning up similar images.

## Features

- 📸 Capture screenshots of HTML elements on web pages
- 🔍 Analyze HTML structure to determine the most likely component level
- 🌐 Support for capturing screenshots at all levels of the HTML structure
- 🧹 Clean up similar images to reduce redundancy
- 🎭 User-friendly command-line interface with rich output

## Installation

To install HTMLJet, you need Python 3.7 or higher. You can install it using pip:

```bash
pip install htmljet
```

## Usage

HTMLJet provides two main commands: `snap` and `cleanup`.

### Snap Command

The `snap` command captures screenshots of HTML elements on a webpage.

```bash
htmljet snap <URL> [OPTIONS]
```

Options:
- `--output-dir`: Directory to save screenshots (default: "htmljet")
- `--all-levels`: Capture screenshots for all levels

Example:
```bash
htmljet snap https://example.com --output-dir my_screenshots
```

### Cleanup Command

The `cleanup` command cleans up similar images in a directory, keeping the larger ones.

```bash
htmljet cleanup <DIRECTORY> [OPTIONS]
```

Options:
- `--similarity-threshold`: Threshold for considering images as similar (0.0 to 1.0, default: 0.9)

Example:
```bash
htmljet cleanup my_screenshots --similarity-threshold 0.8
```

## Development

TBA

