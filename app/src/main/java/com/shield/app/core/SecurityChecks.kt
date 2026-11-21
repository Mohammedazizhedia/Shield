// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.core

import java.io.File

object SecurityChecks {
    private const val TAG = "SecurityChecks"
    data class SecurityReport(val isRooted: Boolean, val isDebugger: Boolean, val recommendations: List<String>)

    fun runChecks(): SecurityReport {
        val rooted = checkRoot()
        val debugger = android.os.Debug.isDebuggerConnected()
        val recs = mutableListOf<String>()
        if (rooted) recs.add("Device appears rooted — overlay may be bypassed by other apps")
        if (debugger) recs.add("Debugger attached — disable for production use")
        if (recs.isEmpty()) recs.add("All security checks passed ✓")
        return SecurityReport(rooted, debugger, recs)
    }

    private fun checkRoot(): Boolean {
        val paths = listOf("/system/app/Superuser.apk", "/sbin/su", "/system/bin/su", "/system/xbin/su", "/data/local/xbin/su", "/data/local/bin/su", "/system/sd/xbin/su", "/system/bin/failsafe/su", "/data/local/su")
        return paths.any { File(it).exists() }
    }
}
