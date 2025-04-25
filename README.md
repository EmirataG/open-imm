# IMM Issues Browser - README

## Overview
`open_issue.py` is a Python application that provides a simple GUI to browse and open PDF issues from the IMM collection. It allows you to specify year, month, and page number to quickly access specific documents.

## Important Limitations

⚠️ **Critical Notes Before Use:**

1. **Safari Requirement**:  
   Currently, this application only works properly if **Safari is set as your default PDF viewer** on macOS. Other browsers may not handle the PDF page anchoring correctly.

2. **Page Functionality Not Working**:  
   The page number parameter in the application **does not currently work** due to browser/PDF viewer limitations. This feature may be implemented in future versions.

3. **File Location Requirement**:  
   Due to macOS security restrictions, the `IMM_issues` folder **must be located in your Documents directory** (`~/Documents/IMM_issues/`). The application cannot access files on the Desktop or other locations because of macOS sandboxing rules.

## Requirements
- Python 3.x
- tkinter (usually included with Python)
- macOS, Windows, or Linux

## Installation & Usage

1. Place your PDF files in:  
   `~/Documents/IMM_issues/`  
   (Example path: `/Users/yourusername/Documents/IMM_issues/1869_01.pdf`)

2. Run the application:
   ```bash
   python3 open_issue.py
   ```

3. Enter the year (e.g., 1869), month (e.g., 01), and (optionally) page number, then click "Open PDF"

## Platform Support

- **macOS**: Uses Safari for PDF viewing (must be default PDF handler)
- **Windows**: Uses default browser with PDF handling capability
- **Linux**: Uses xdg-open with fallback to browser

## Troubleshooting

Common issues and solutions:

1. **File not found errors**:
   - Verify the PDF files exist in: `~/Documents/IMM_issues/`
   - Check filename format: `YYYY_MM.pdf` (e.g., `1869_01.pdf`)

2. **Permission errors**:
   ```bash
   chmod +r ~/Documents/IMM_issues/*.pdf
   ```

3. **macOS specific issues**:
   - Grant Full Disk Access to your terminal/IDE:
     - System Settings → Privacy & Security → Full Disk Access
   - Set Safari as default PDF viewer

## Known Issues
- Page number parameter not functional
- Limited to Documents directory on macOS
- Requires Safari on macOS for best results

## Future Improvements
- Add support for more PDF viewers
- Implement working page navigation
- Allow configuration of PDF directory location
- Add support for additional file formats

## License
This project is provided as-is without warranty. Feel free to modify for your needs.
