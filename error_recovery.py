"""
Error Recovery and Self-Healing System
Provides automatic error detection, recovery, and system health monitoring
"""

import os
import sys
import logging
import traceback
import json
from typing import Dict, Any, Optional, Callable, List
from datetime import datetime
from pathlib import Path
import subprocess
import threading
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ErrorRecoverySystem:
    """
    Autonomous error recovery and self-healing system
    
    Features:
    - Automatic error detection and classification
    - Self-healing mechanisms for common issues
    - System health monitoring
    - Automatic restart on critical failures
    - Error pattern learning
    - Rollback capabilities
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.error_log = []
        self.recovery_actions = {}
        self.health_checks = []
        self.monitoring_active = False
        self.recovery_history = []
        
        self._register_default_recovery_actions()
        self._start_health_monitoring()
        
        logger.info("Error Recovery System initialized")
    
    def _register_default_recovery_actions(self):
        """Register default recovery actions for common errors"""
        
        self.recovery_actions = {
            "ImportError": self._recover_import_error,
            "ModuleNotFoundError": self._recover_module_not_found,
            "FileNotFoundError": self._recover_file_not_found,
            "PermissionError": self._recover_permission_error,
            "ConnectionError": self._recover_connection_error,
            "TimeoutError": self._recover_timeout_error,
            "MemoryError": self._recover_memory_error,
            "SyntaxError": self._recover_syntax_error,
            "AttributeError": self._recover_attribute_error,
            "KeyError": self._recover_key_error,
        }
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Handle an error with automatic recovery attempts
        
        Args:
            error: The exception that occurred
            context: Additional context about the error
            
        Returns:
            Recovery result with success status and actions taken
        """
        error_type = type(error).__name__
        error_msg = str(error)
        
        logger.error(f"Error detected: {error_type} - {error_msg}")
        
        # Log the error
        error_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_msg,
            "traceback": traceback.format_exc(),
            "context": context or {}
        }
        self.error_log.append(error_entry)
        
        # Attempt recovery
        recovery_result = self._attempt_recovery(error_type, error, context)
        
        # Log recovery attempt
        self.recovery_history.append({
            "timestamp": datetime.now().isoformat(),
            "error": error_entry,
            "recovery": recovery_result
        })
        
        return recovery_result
    
    def _attempt_recovery(self, error_type: str, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Attempt to recover from an error"""
        
        if error_type in self.recovery_actions:
            logger.info(f"Attempting recovery for {error_type}")
            try:
                recovery_func = self.recovery_actions[error_type]
                result = recovery_func(error, context)
                
                if result.get("success"):
                    logger.info(f"Successfully recovered from {error_type}")
                else:
                    logger.warning(f"Recovery attempt failed for {error_type}")
                
                return result
            except Exception as recovery_error:
                logger.error(f"Recovery function failed: {recovery_error}")
                return {
                    "success": False,
                    "error": "Recovery function failed",
                    "details": str(recovery_error)
                }
        else:
            logger.warning(f"No recovery action registered for {error_type}")
            return {
                "success": False,
                "error": "No recovery action available",
                "suggestion": self._suggest_recovery(error_type, error)
            }
    
    # ==================== RECOVERY ACTIONS ====================
    
    def _recover_import_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from import errors by installing missing packages"""
        error_msg = str(error)
        
        # Extract module name
        if "No module named" in error_msg:
            module_name = error_msg.split("'")[1] if "'" in error_msg else None
            
            if module_name:
                logger.info(f"Attempting to install missing module: {module_name}")
                try:
                    result = subprocess.run(
                        [sys.executable, "-m", "pip", "install", module_name],
                        capture_output=True,
                        text=True,
                        timeout=120
                    )
                    
                    if result.returncode == 0:
                        return {
                            "success": True,
                            "action": "installed_package",
                            "package": module_name,
                            "message": f"Successfully installed {module_name}"
                        }
                    else:
                        return {
                            "success": False,
                            "action": "install_failed",
                            "error": result.stderr
                        }
                except Exception as e:
                    return {"success": False, "error": str(e)}
        
        return {"success": False, "error": "Could not extract module name"}
    
    def _recover_module_not_found(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from module not found errors"""
        return self._recover_import_error(error, context)
    
    def _recover_file_not_found(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from file not found errors"""
        error_msg = str(error)
        
        # Try to create the file if it's expected to exist
        if context and "expected_file" in context:
            file_path = Path(context["expected_file"])
            try:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()
                
                return {
                    "success": True,
                    "action": "created_file",
                    "file": str(file_path),
                    "message": f"Created missing file: {file_path}"
                }
            except Exception as e:
                return {"success": False, "error": str(e)}
        
        return {
            "success": False,
            "error": "Cannot auto-create file without context",
            "suggestion": "Verify file path and permissions"
        }
    
    def _recover_permission_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from permission errors"""
        return {
            "success": False,
            "error": "Permission denied",
            "suggestion": "Check file/directory permissions or run with appropriate privileges"
        }
    
    def _recover_connection_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from connection errors with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        if context and "retry_function" in context:
            retry_func = context["retry_function"]
            
            for attempt in range(max_retries):
                logger.info(f"Retry attempt {attempt + 1}/{max_retries}")
                time.sleep(retry_delay)
                
                try:
                    result = retry_func()
                    return {
                        "success": True,
                        "action": "retry_succeeded",
                        "attempts": attempt + 1,
                        "result": result
                    }
                except Exception:
                    continue
            
            return {
                "success": False,
                "action": "retry_failed",
                "attempts": max_retries,
                "error": "All retry attempts failed"
            }
        
        return {
            "success": False,
            "error": "No retry function provided",
            "suggestion": "Check network connection and retry manually"
        }
    
    def _recover_timeout_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from timeout errors"""
        return {
            "success": False,
            "error": "Operation timed out",
            "suggestion": "Increase timeout duration or optimize the operation"
        }
    
    def _recover_memory_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from memory errors"""
        import gc
        gc.collect()
        
        return {
            "success": True,
            "action": "garbage_collection",
            "message": "Performed garbage collection to free memory",
            "suggestion": "Consider processing data in smaller chunks"
        }
    
    def _recover_syntax_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from syntax errors"""
        return {
            "success": False,
            "error": "Syntax error detected",
            "suggestion": "Review and fix syntax in the affected file",
            "details": str(error)
        }
    
    def _recover_attribute_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from attribute errors"""
        return {
            "success": False,
            "error": "Attribute not found",
            "suggestion": "Verify object has the expected attribute or update code",
            "details": str(error)
        }
    
    def _recover_key_error(self, error: Exception, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Recover from key errors"""
        return {
            "success": False,
            "error": "Key not found in dictionary",
            "suggestion": "Use .get() method or verify key exists",
            "details": str(error)
        }
    
    def _suggest_recovery(self, error_type: str, error: Exception) -> str:
        """Suggest recovery actions for unknown error types"""
        suggestions = {
            "ValueError": "Validate input data and ensure correct data types",
            "TypeError": "Check data types and function signatures",
            "IndexError": "Verify list/array indices are within bounds",
            "ZeroDivisionError": "Add check for zero before division",
            "RuntimeError": "Review runtime conditions and state",
        }
        
        return suggestions.get(error_type, "Review error details and consult documentation")
    
    # ==================== HEALTH MONITORING ====================
    
    def _start_health_monitoring(self):
        """Start background health monitoring"""
        self.monitoring_active = True
        
        def monitor():
            while self.monitoring_active:
                self._perform_health_checks()
                time.sleep(60)  # Check every minute
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        
        logger.info("Health monitoring started")
    
    def _perform_health_checks(self):
        """Perform system health checks"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "checks": []
        }
        
        # Check disk space
        disk_check = self._check_disk_space()
        health_status["checks"].append(disk_check)
        
        # Check memory usage
        memory_check = self._check_memory_usage()
        health_status["checks"].append(memory_check)
        
        # Check critical files
        files_check = self._check_critical_files()
        health_status["checks"].append(files_check)
        
        # Log health status
        if any(check.get("status") == "critical" for check in health_status["checks"]):
            logger.warning(f"Health check critical: {health_status}")
        
        return health_status
    
    def _check_disk_space(self) -> Dict[str, Any]:
        """Check available disk space"""
        try:
            import shutil
            total, used, free = shutil.disk_usage(self.project_root)
            free_percent = (free / total) * 100
            
            status = "healthy" if free_percent > 10 else "critical"
            
            return {
                "name": "disk_space",
                "status": status,
                "free_percent": round(free_percent, 2),
                "free_gb": round(free / (1024**3), 2)
            }
        except Exception as e:
            return {"name": "disk_space", "status": "error", "error": str(e)}
    
    def _check_memory_usage(self) -> Dict[str, Any]:
        """Check memory usage"""
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            status = "healthy" if memory.percent < 90 else "critical"
            
            return {
                "name": "memory_usage",
                "status": status,
                "percent": memory.percent,
                "available_gb": round(memory.available / (1024**3), 2)
            }
        except ImportError:
            return {"name": "memory_usage", "status": "unavailable", "error": "psutil not installed"}
        except Exception as e:
            return {"name": "memory_usage", "status": "error", "error": str(e)}
    
    def _check_critical_files(self) -> Dict[str, Any]:
        """Check if critical files exist"""
        critical_files = ["main.py", "requirements.txt", "agent_brain.py"]
        missing_files = []
        
        for file in critical_files:
            if not (self.project_root / file).exists():
                missing_files.append(file)
        
        status = "healthy" if not missing_files else "critical"
        
        return {
            "name": "critical_files",
            "status": status,
            "missing": missing_files
        }
    
    def stop_monitoring(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        logger.info("Health monitoring stopped")
    
    # ==================== ROLLBACK ====================
    
    def create_checkpoint(self, name: str, files: List[str]) -> Dict[str, Any]:
        """Create a checkpoint for rollback"""
        checkpoint_dir = self.project_root / ".checkpoints"
        checkpoint_dir.mkdir(exist_ok=True)
        
        checkpoint_path = checkpoint_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        checkpoint_path.mkdir(exist_ok=True)
        
        backed_up = []
        for file in files:
            src = self.project_root / file
            if src.exists():
                dst = checkpoint_path / file
                dst.parent.mkdir(parents=True, exist_ok=True)
                
                import shutil
                shutil.copy2(src, dst)
                backed_up.append(file)
        
        return {
            "success": True,
            "checkpoint": str(checkpoint_path),
            "files": backed_up
        }
    
    def rollback_to_checkpoint(self, checkpoint_path: str) -> Dict[str, Any]:
        """Rollback to a previous checkpoint"""
        checkpoint = Path(checkpoint_path)
        
        if not checkpoint.exists():
            return {"success": False, "error": "Checkpoint not found"}
        
        restored = []
        import shutil
        
        for file in checkpoint.rglob("*"):
            if file.is_file():
                relative = file.relative_to(checkpoint)
                dst = self.project_root / relative
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file, dst)
                restored.append(str(relative))
        
        return {
            "success": True,
            "restored": restored,
            "count": len(restored)
        }
    
    # ==================== REPORTING ====================
    
    def get_error_report(self, limit: int = 10) -> Dict[str, Any]:
        """Get error report"""
        return {
            "total_errors": len(self.error_log),
            "recent_errors": self.error_log[-limit:],
            "recovery_success_rate": self._calculate_recovery_rate()
        }
    
    def _calculate_recovery_rate(self) -> float:
        """Calculate recovery success rate"""
        if not self.recovery_history:
            return 0.0
        
        successful = sum(1 for r in self.recovery_history if r["recovery"].get("success"))
        return (successful / len(self.recovery_history)) * 100
    
    def export_logs(self, output_file: str = "error_recovery_log.json"):
        """Export error and recovery logs"""
        log_data = {
            "error_log": self.error_log,
            "recovery_history": self.recovery_history,
            "recovery_rate": self._calculate_recovery_rate()
        }
        
        output_path = self.project_root / output_file
        with open(output_path, 'w') as f:
            json.dump(log_data, f, indent=2)
        
        return {"success": True, "file": str(output_path)}
