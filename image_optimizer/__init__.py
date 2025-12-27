# Image Optimizer Tool
# Properly resizes images for various app uses with minimal quality loss

from pathlib import Path
from .optimizer import ImageOptimizer, OutputFormat, OptimizationResult
from .presets import SIZE_PRESETS, get_preset, list_presets
from .strategies import ResizeStrategy

__all__ = [
    'ImageOptimizer',
    'OutputFormat',
    'OptimizationResult',
    'SIZE_PRESETS',
    'get_preset',
    'list_presets',
    'ResizeStrategy',
]
__version__ = '1.0.0'


def launch_gui():
    """Launch the desktop graphical user interface."""
    from .gui import main
    return main()


def launch_webapp():
    """
    Launch the web app (accessible from phone).

    Run from command line instead:
        streamlit run image_optimizer/webapp.py

    Then access from phone at: http://YOUR_COMPUTER_IP:8501
    """
    import subprocess
    import sys
    webapp_path = Path(__file__).parent / "webapp.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", str(webapp_path)])
