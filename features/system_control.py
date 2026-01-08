"""System automation and control features."""

import logging
import subprocess
import os
from typing import Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    logging.warning("psutil not available - some features disabled")

logger = logging.getLogger(__name__)


class SystemController:
    """Control system functions."""
    
    def __init__(self):
        """Initialize system controller."""
        self.platform = os.name  # 'nt' for Windows, 'posix' for Linux/Mac
    
    def open_application(self, app_name: str) -> bool:
        """Open an application.
        
        Args:
            app_name: Application name or path
            
        Returns:
            Success status
        """
        try:
            logger.info(f"Opening application: {app_name}")
            
            if self.platform == 'nt':  # Windows
                # Common Windows apps
                apps_map = {
                    'notepad': 'notepad.exe',
                    'calculator': 'calc.exe',
                    'browser': 'start chrome',
                    'explorer': 'explorer.exe',
                    'spotify': 'spotify.exe'
                }
                
                command = apps_map.get(app_name.lower(), app_name)
                subprocess.Popen(command, shell=True)
                
            else:  # Linux/Mac
                subprocess.Popen([app_name])
            
            logger.info(f"Opened: {app_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to open {app_name}: {e}")
            return False
    
    def set_volume(self, level: int) -> bool:
        """Set system volume.
        
        Args:
            level: Volume level (0-100)
            
        Returns:
            Success status
        """
        try:
            level = max(0, min(100, level))  # Clamp to 0-100
            logger.info(f"Setting volume to {level}%")
            
            if self.platform == 'nt':  # Windows
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
                
                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level / 100, None)
                
            else:  # Linux/Mac
                subprocess.run(['amixer', 'set', 'Master', f'{level}%'])
            
            logger.info(f"Volume set to {level}%")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set volume: {e}")
            return False
    
    def get_system_info(self) -> dict:
        """Get system information.
        
        Returns:
            System info dictionary
        """
        if not PSUTIL_AVAILABLE:
            return {'status': 'psutil not installed'}
            
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                'cpu_usage': f"{cpu_percent}%",
                'memory_usage': f"{memory.percent}%",
                'disk_usage': f"{disk.percent}%",
                'memory_available': f"{memory.available / (1024**3):.1f} GB"
            }
        except Exception as e:
            logger.error(f"Failed to get system info: {e}")
            return {}
    
    def shutdown(self, delay_seconds: int = 0) -> bool:
        """Shutdown system.
        
        Args:
            delay_seconds: Delay before shutdown
            
        Returns:
            Success status
        """
        try:
            logger.warning(f"Shutdown requested (delay: {delay_seconds}s)")
            
            if self.platform == 'nt':  # Windows
                subprocess.run(['shutdown', '/s', '/t', str(delay_seconds)])
            else:  # Linux/Mac
                subprocess.run(['shutdown', '-h', f'+{delay_seconds//60}'])
            
            return True
        except Exception as e:
            logger.error(f"Failed to shutdown: {e}")
            return False
    
    def lock_screen(self) -> bool:
        """Lock the screen.
        
        Returns:
            Success status
        """
        try:
            logger.info("Locking screen")
            
            if self.platform == 'nt':  # Windows
                subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
            else:  # Linux/Mac
                subprocess.run(['gnome-screensaver-command', '-l'])
            
            return True
        except Exception as e:
            logger.error(f"Failed to lock screen: {e}")
            return False


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("\nTesting System Controller...")
    
    controller = SystemController()
    
    # Test system info
    print("\nSystem Info:")
    info = controller.get_system_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    # Test volume (commented out to avoid disruption)
    # controller.set_volume(50)
    
    print("\n✅ System controller ready!")
