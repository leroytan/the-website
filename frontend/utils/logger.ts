/**
 * Centralized logging utility that respects the NEXT_PUBLIC_DEBUG environment variable
 */

const isDebugEnabled = (): boolean => {
  return process.env.NEXT_PUBLIC_DEBUG === 'true';
};

export const logger = {
  /**
   * Debug logging - only outputs when NEXT_PUBLIC_DEBUG=true
   * Automatically adds debug prefix
   */
  debug: (...args: any[]) => {
    if (isDebugEnabled()) {
      console.log("🔍 [DEBUG]", ...args);
    }
  },

  /**
   * Info logging - only outputs when NEXT_PUBLIC_DEBUG=true
   */
  info: (...args: any[]) => {
    if (isDebugEnabled()) {
      console.info("ℹ️ [INFO]", ...args);
    }
  },

  /**
   * Warning logging - only outputs when NEXT_PUBLIC_DEBUG=true
   */
  warn: (...args: any[]) => {
    if (isDebugEnabled()) {
      console.warn("⚠️ [WARN]", ...args);
    }
  },

  /**
   * Error logging - always outputs regardless of debug setting
   * This ensures production errors are still visible for debugging
   */
  error: (...args: any[]) => {
    console.error("❌ [ERROR]", ...args);
  },

  /**
   * Log function - only outputs when NEXT_PUBLIC_DEBUG=true
   * Alias for debug method
   */
  log: (...args: any[]) => {
    if (isDebugEnabled()) {
      console.log("🔍 [DEBUG]", ...args);
    }
  }
};

export default logger;