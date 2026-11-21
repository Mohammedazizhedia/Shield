// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.core

import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.Looper
import android.util.Log
import java.io.File
import java.io.PrintWriter
import java.io.StringWriter
import java.text.SimpleDateFormat
import java.util.*

object CrashReporter {
    private const val TAG = "CrashReporter"
    private const val PREFS = "shield_crash_prefs"
    private const val KEY_ENABLED = "error_reporting_enabled"
    private const val REPORTS_DIR = "crash_reports"

    fun install(context: Context) {
        val defaultHandler = Thread.getDefaultUncaughtExceptionHandler()
        Thread.setDefaultUncaughtExceptionHandler { thread, throwable ->
            try {
                if (isEnabled(context)) {
                    saveReport(context, thread, throwable)
                }
            } catch (e: Exception) {
                Log.e(TAG, "Failed to save crash report", e)
            } finally {
                defaultHandler?.uncaughtException(thread, throwable)
            }
        }
    }

    fun isEnabled(context: Context): Boolean =
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE).getBoolean(KEY_ENABLED, true)

    fun setEnabled(context: Context, enabled: Boolean) {
        context.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
            .edit().putBoolean(KEY_ENABLED, enabled).apply()
    }

    fun getReportsDir(context: Context): File {
        val dir = File(context.filesDir, REPORTS_DIR)
        if (!dir.exists()) dir.mkdirs()
        return dir
    }

    fun clearReports(context: Context) {
        getReportsDir(context).deleteRecursively()
    }

    private fun saveReport(context: Context, thread: Thread, throwable: Throwable) {
        val timestamp = SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.US).format(Date())
        val file = File(getReportsDir(context), "crash_$timestamp.txt")
        val sw = StringWriter()
        throwable.printStackTrace(PrintWriter(sw))

        val report = buildString {
            appendLine("=== Shield Crash Report ===")
            appendLine("Timestamp: $timestamp")
            appendLine("App Version: ${getAppVersion(context)}")
            appendLine("Android: ${Build.VERSION.RELEASE} (API ${Build.VERSION.SDK_INT})")
            appendLine("Device: ${Build.MANUFACTURER} ${Build.MODEL}")
            appendLine("Thread: ${thread.name}")
            appendLine()
            appendLine("--- Stack Trace ---")
            appendLine(sw.toString())
        }
        file.writeText(report)
        Log.e(TAG, "Crash report saved: ${file.absolutePath}")
    }

    private fun getAppVersion(context: Context): String = try {
        val pi = context.packageManager.getPackageInfo(context.packageName, 0)
        "${pi.versionName} (${pi.versionCode})"
    } catch (e: Exception) { "unknown" }
}
