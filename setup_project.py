#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shield Project Auto-Generator — BFB.AI Edition
Built with BFB.AI — Built For Benefits, by AI
ينشئ مشروع Shield كاملاً بمعيار BFB.AI v4.3
"""
import os, sys

BFB_HEADER = "// Built with BFB.AI — Built For Benefits, by AI\n"

FILES = {
    # ============ جذر المشروع ============
    "build.gradle.kts": """plugins {
    id("com.android.application") version "8.5.2" apply false
    id("org.jetbrains.kotlin.android") version "1.9.24" apply false
}
""",

    "settings.gradle.kts": """pluginManagement {
    repositories { google(); mavenCentral(); gradlePluginPortal() }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories { google(); mavenCentral() }
}
rootProject.name = "Shield"
include(":app")
""",

    "gradle.properties": """org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
kotlin.code.style=official
android.nonTransitiveRClass=true
""",

    "gradle/wrapper/gradle-wrapper.properties": """distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""",

    ".gitignore": """*.iml
.gradle
/local.properties
/.idea/
.DS_Store
/build
/captures
.externalNativeBuild
.cxx
local.properties
*.jks
*.keystore
!gradle/wrapper/gradle-wrapper.jar
""",

    # ============ app module ============
    "app/build.gradle.kts": """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.shield.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.shield.app"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
        vectorDrawables.useSupportLibrary = true
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
        debug {
            isMinifyEnabled = false
            applicationIdSuffix = ".debug"
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions { jvmTarget = "17" }

    buildFeatures { viewBinding = true }
}

dependencies {
    implementation("androidx.core:core-ktx:1.13.1")
    implementation("androidx.core:core-splashscreen:1.0.1")
    implementation("androidx.appcompat:appcompat:1.7.0")
    implementation("com.google.android.material:material:1.12.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.8.4")
    implementation("androidx.datastore:datastore-preferences:1.1.1")
    implementation("androidx.activity:activity-ktx:1.9.1")
    implementation("androidx.fragment:fragment-ktx:1.8.2")
    testImplementation("junit:junit:4.13.2")
}
""",

    "app/proguard-rules.pro": """# BFB.AI Shield - ProGuard Rules
-keepclassmembers class * extends android.service.quicksettings.TileService { public <methods>; }
-keep class com.shield.app.data.theme.** { *; }
-keep class com.shield.app.data.theme.ThemeDto { *; }
-dontwarn org.bouncycastle.**
""",

    # ============ AndroidManifest ============
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:name=".ShieldApp"
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.Shield"
        tools:targetApi="34">

        <activity
            android:name=".ui.MainActivity"
            android:exported="true"
            android:theme="@style/Theme.Shield.Splash">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.PrivacyTileService"
            android:exported="true"
            android:icon="@drawable/ic_shield_tile"
            android:label="@string/tile_label"
            android:permission="android.permission.BIND_QUICK_SETTINGS_TILE">
            <intent-filter>
                <action android:name="android.service.quicksettings.action.QS_TILE" />
            </intent-filter>
            <meta-data android:name="android.service.quicksettings.ACTIVE_TILE" android:value="true" />
        </service>

        <service
            android:name=".service.PrivacyOverlayService"
            android:exported="false"
            android:foregroundServiceType="specialUse" />

    </application>
</manifest>
""",

    # ============ Application class (Crash Reporter) ============
    "app/src/main/java/com/shield/app/ShieldApp.kt": BFB_HEADER + """package com.shield.app

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.shield.app.core.CrashReporter
import com.shield.app.data.theme.ThemeRepository

class ShieldApp : Application() {
    lateinit var themeRepo: ThemeRepository
        private set

    override fun onCreate() {
        super.onCreate()
        instance = this
        CrashReporter.install(this)
        themeRepo = ThemeRepository(this)
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(
                NotificationChannel(
                    "shield_overlay",
                    getString(R.string.notif_channel_overlay),
                    NotificationManager.IMPORTANCE_LOW
                ).apply { description = getString(R.string.notif_channel_overlay_desc); setShowBadge(false) }
            )
            manager.createNotificationChannel(
                NotificationChannel(
                    "shield_crash",
                    getString(R.string.notif_channel_crash),
                    NotificationManager.IMPORTANCE_DEFAULT
                )
            )
        }
    }

    companion object {
        lateinit var instance: ShieldApp
            private set
    }
}
""",

    # ============ Crash Reporter (القسم 10) ============
    "app/src/main/java/com/shield/app/core/CrashReporter.kt": BFB_HEADER + """package com.shield.app.core

import android.content.Context
import android.os.Build
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
""",

    # ============ Theme System (4.9) ============
    "app/src/main/java/com/shield/app/data/theme/ThemeMode.kt": BFB_HEADER + """package com.shield.app.data.theme
enum class ThemeMode { LIGHT, DARK, AMOLED, SYSTEM }
""",

    "app/src/main/java/com/shield/app/data/theme/ThemeColors.kt": BFB_HEADER + """package com.shield.app.data.theme

data class ThemeColors(
    val primary: Long = 0xFF00A6A6,
    val secondary: Long = 0xFF0B1B3A,
    val accent: Long = 0xFF00D4AA,
    val background: Long = 0xFFF5F7FA,
    val surface: Long = 0xFFFFFFFF,
    val onPrimary: Long = 0xFFFFFFFF,
    val onBackground: Long = 0xFF0B1B3A,
    val onSurface: Long = 0xFF0B1B3A,
    val error: Long = 0xFFFF5A5F,
    val success: Long = 0xFF2ECC71,
    val warning: Long = 0xFFF5A623
)
""",

    "app/src/main/java/com/shield/app/data/theme/ThemeConfig.kt": BFB_HEADER + """package com.shield.app.data.theme

data class ThemeConfig(
    val schema: Int = 1,
    val name: String = "Shield Default",
    val mode: ThemeMode = ThemeMode.SYSTEM,
    val colors: ThemeColors = ThemeColors(),
    val cornerRadius: CornerRadius = CornerRadius.MEDIUM,
    val motionLevel: MotionLevel = MotionLevel.FULL,
    val fontScale: Float = 1.0f
)

enum class CornerRadius { SHARP, MEDIUM, LARGE }
enum class MotionLevel { FULL, REDUCED, NONE }
""",

    "app/src/main/java/com/shield/app/data/theme/BuiltInThemes.kt": BFB_HEADER + """package com.shield.app.data.theme

object BuiltInThemes {
    val DEFAULT = ThemeConfig(
        name = "Shield Default", mode = ThemeMode.SYSTEM,
        colors = ThemeColors(primary = 0xFF00A6A6, secondary = 0xFF0B1B3A, accent = 0xFF00D4AA, background = 0xFFF5F7FA, surface = 0xFFFFFFFF, onBackground = 0xFF0B1B3A, onSurface = 0xFF0B1B3A)
    )
    val LIGHT = ThemeConfig(
        name = "Light", mode = ThemeMode.LIGHT,
        colors = ThemeColors(primary = 0xFF00A6A6, secondary = 0xFF1E3A5F, accent = 0xFF00D4AA, background = 0xFFF5F7FA, surface = 0xFFFFFFFF, onBackground = 0xFF0B1B3A, onSurface = 0xFF0B1B3A)
    )
    val DARK = ThemeConfig(
        name = "Dark", mode = ThemeMode.DARK,
        colors = ThemeColors(primary = 0xFF4DE1E1, secondary = 0xFF1E3A5F, accent = 0xFF00FFCC, background = 0xFF0B1B3A, surface = 0xFF13264D, onBackground = 0xFFFFFFFF, onSurface = 0xFFFFFFFF)
    )
    val AMOLED = ThemeConfig(
        name = "AMOLED", mode = ThemeMode.AMOLED,
        colors = ThemeColors(primary = 0xFF4DE1E1, secondary = 0xFF000000, accent = 0xFF00FFCC, background = 0xFF000000, surface = 0xFF0A0A0A, onBackground = 0xFFFFFFFF, onSurface = 0xFFFFFFFF)
    )
    val HIGH_CONTRAST = ThemeConfig(
        name = "High Contrast", mode = ThemeMode.DARK,
        colors = ThemeColors(primary = 0xFFFFD700, secondary = 0xFF000000, accent = 0xFF00FF00, background = 0xFF000000, surface = 0xFF000000, onBackground = 0xFFFFFFFF, onSurface = 0xFFFFFFFF, error = 0xFFFF4444, success = 0xFF00FF00, warning = 0xFFFFFF00)
    )
    val MIDNIGHT_GOLD = ThemeConfig(
        name = "Midnight Gold", mode = ThemeMode.DARK,
        colors = ThemeColors(primary = 0xFFD4AF37, secondary = 0xFF3A4A6B, accent = 0xFF4DE1E1, background = 0xFF0B1B3A, surface = 0xFF13264D, onBackground = 0xFFFFF8DC, onSurface = 0xFFFFF8DC)
    )
    val all: List<ThemeConfig> = listOf(DEFAULT, LIGHT, DARK, AMOLED, HIGH_CONTRAST, MIDNIGHT_GOLD)
}
""",

    "app/src/main/java/com/shield/app/data/theme/ThemeImporter.kt": BFB_HEADER + """package com.shield.app.data.theme

import android.util.Log
import org.json.JSONObject
import java.security.MessageDigest

object ThemeImporter {
    private const val MAX_SIZE = 64 * 1024
    private const val TAG = "ThemeImporter"

    data class ValidationResult(val success: Boolean, val theme: ThemeConfig? = null, val error: String? = null)

    fun validateAndParse(json: String): ValidationResult {
        if (json.length > MAX_SIZE) return ValidationResult(false, error = "File exceeds 64KB limit")
        if (!json.trimStart().startsWith("{")) return ValidationResult(false, error = "Invalid JSON")

        return try {
            val root = JSONObject(json)
            val schema = root.optInt("schema", 0)
            if (schema != 1) return ValidationResult(false, error = "Unsupported schema version: $schema")

            val colorsObj = root.optJSONObject("colors") ?: return ValidationResult(false, error = "Missing colors")
            val colors = ThemeColors(
                primary = parseHex(colorsObj.optString("primary")),
                secondary = parseHex(colorsObj.optString("secondary")),
                accent = parseHex(colorsObj.optString("accent")),
                background = parseHex(colorsObj.optString("background")),
                surface = parseHex(colorsObj.optString("surface")),
                onPrimary = parseHex(colorsObj.optString("onPrimary", "#FFFFFF")),
                onBackground = parseHex(colorsObj.optString("onBackground")),
                onSurface = parseHex(colorsObj.optString("onSurface")),
                error = parseHex(colorsObj.optString("error", "#FF5A5F")),
                success = parseHex(colorsObj.optString("success", "#2ECC71")),
                warning = parseHex(colorsObj.optString("warning", "#F5A623"))
            )

            val modeStr = root.optString("mode", "SYSTEM")
            val mode = try { ThemeMode.valueOf(modeStr) } catch (e: Exception) { ThemeMode.SYSTEM }

            val theme = ThemeConfig(schema = schema, name = root.optString("name", "Imported"), mode = mode, colors = colors)
            ValidationResult(true, theme)
        } catch (e: Exception) {
            Log.e(TAG, "Parse error", e)
            ValidationResult(false, error = "Parse error: ${e.message}")
        }
    }

    fun exportToJson(theme: ThemeConfig): String = JSONObject().apply {
        put("schema", theme.schema)
        put("name", theme.name)
        put("mode", theme.mode.name)
        put("colors", JSONObject().apply {
            put("primary", longToHex(theme.colors.primary))
            put("secondary", longToHex(theme.colors.secondary))
            put("accent", longToHex(theme.colors.accent))
            put("background", longToHex(theme.colors.background))
            put("surface", longToHex(theme.colors.surface))
            put("onPrimary", longToHex(theme.colors.onPrimary))
            put("onBackground", longToHex(theme.colors.onBackground))
            put("onSurface", longToHex(theme.colors.onSurface))
            put("error", longToHex(theme.colors.error))
            put("success", longToHex(theme.colors.success))
            put("warning", longToHex(theme.colors.warning))
        })
    }.toString(2)

    fun sha256(data: String): String {
        val digest = MessageDigest.getInstance("SHA-256")
        return digest.digest(data.toByteArray()).joinToString("") { "%02x".format(it) }
    }

    private fun parseHex(hex: String): Long {
        val clean = hex.trimStart('#')
        return if (clean.length == 6) "FF$clean".toLong(16) else clean.toLong(16)
    }

    private fun longToHex(color: Long): String = "#%06X".format(0xFFFFFF and color.toInt())
}
""",

    "app/src/main/java/com/shield/app/data/theme/ThemeRepository.kt": BFB_HEADER + """package com.shield.app.data.theme

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.*
import androidx.datastore.preferences.preferencesDataStore
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "shield_theme")

class ThemeRepository(private val context: Context) {
    private val KEY_MODE = stringPreferencesKey("theme_mode")
    private val KEY_NAME = stringPreferencesKey("theme_name")
    private val KEY_PRIMARY = longPreferencesKey("theme_primary")
    private val KEY_SECONDARY = longPreferencesKey("theme_secondary")
    private val KEY_ACCENT = longPreferencesKey("theme_accent")
    private val KEY_BACKGROUND = longPreferencesKey("theme_background")
    private val KEY_SURFACE = longPreferencesKey("theme_surface")
    private val KEY_ON_BG = longPreferencesKey("theme_on_bg")
    private val KEY_ON_SURFACE = longPreferencesKey("theme_on_surface")
    private val KEY_CORNER = stringPreferencesKey("theme_corner")
    private val KEY_MOTION = stringPreferencesKey("theme_motion")
    private val KEY_SCALE = floatPreferencesKey("theme_scale")

    val configFlow: Flow<ThemeConfig> = context.dataStore.data.map { prefs ->
        ThemeConfig(
            name = prefs[KEY_NAME] ?: "Shield Default",
            mode = try { ThemeMode.valueOf(prefs[KEY_MODE] ?: "SYSTEM") } catch (e: Exception) { ThemeMode.SYSTEM },
            colors = ThemeColors(
                primary = prefs[KEY_PRIMARY] ?: 0xFF00A6A6,
                secondary = prefs[KEY_SECONDARY] ?: 0xFF0B1B3A,
                accent = prefs[KEY_ACCENT] ?: 0xFF00D4AA,
                background = prefs[KEY_BACKGROUND] ?: 0xFFF5F7FA,
                surface = prefs[KEY_SURFACE] ?: 0xFFFFFFFF,
                onBackground = prefs[KEY_ON_BG] ?: 0xFF0B1B3A,
                onSurface = prefs[KEY_ON_SURFACE] ?: 0xFF0B1B3A
            ),
            cornerRadius = try { CornerRadius.valueOf(prefs[KEY_CORNER] ?: "MEDIUM") } catch (e: Exception) { CornerRadius.MEDIUM },
            motionLevel = try { MotionLevel.valueOf(prefs[KEY_MOTION] ?: "FULL") } catch (e: Exception) { MotionLevel.FULL },
            fontScale = prefs[KEY_SCALE] ?: 1.0f
        )
    }

    suspend fun saveConfig(config: ThemeConfig) {
        context.dataStore.edit { prefs ->
            prefs[KEY_NAME] = config.name
            prefs[KEY_MODE] = config.mode.name
            prefs[KEY_PRIMARY] = config.colors.primary
            prefs[KEY_SECONDARY] = config.colors.secondary
            prefs[KEY_ACCENT] = config.colors.accent
            prefs[KEY_BACKGROUND] = config.colors.background
            prefs[KEY_SURFACE] = config.colors.surface
            prefs[KEY_ON_BG] = config.colors.onBackground
            prefs[KEY_ON_SURFACE] = config.colors.onSurface
            prefs[KEY_CORNER] = config.cornerRadius.name
            prefs[KEY_MOTION] = config.motionLevel.name
            prefs[KEY_SCALE] = config.fontScale
        }
    }

    suspend fun applyImported(config: ThemeConfig) = saveConfig(config)
}
""",

    # ============ Security ============
    "app/src/main/java/com/shield/app/core/SecurityChecks.kt": BFB_HEADER + """package com.shield.app.core

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
""",

    # ============ Settings Manager ============
    "app/src/main/java/com/shield/app/data/SettingsManager.kt": BFB_HEADER + """package com.shield.app.data

import android.content.Context
import android.content.SharedPreferences
import android.graphics.Color

class SettingsManager(context: Context) {
    companion object {
        const val PREFS = "shield_prefs"
        const val KEY_ENABLED = "enabled"
        const val KEY_PATTERN = "pattern"
        const val KEY_OPACITY = "opacity"
        const val KEY_DENSITY = "density"
        const val KEY_OVERLAY_COLOR = "overlay_color"
        const val PATTERN_SOLID = "solid"
        const val PATTERN_GRID = "grid"
        const val PATTERN_DOTS = "dots"
        const val PATTERN_FOCUS = "focus"
    }
    private val prefs: SharedPreferences = context.applicationContext.getSharedPreferences(PREFS, Context.MODE_PRIVATE)
    fun isEnabled(): Boolean = prefs.getBoolean(KEY_ENABLED, false)
    fun setEnabled(v: Boolean) = prefs.edit().putBoolean(KEY_ENABLED, v).apply()
    fun getPattern(): String = prefs.getString(KEY_PATTERN, PATTERN_SOLID) ?: PATTERN_SOLID
    fun setPattern(v: String) = prefs.edit().putString(KEY_PATTERN, v).apply()
    fun getOpacity(): Int = prefs.getInt(KEY_OPACITY, 40)
    fun setOpacity(v: Int) = prefs.edit().putInt(KEY_OPACITY, v).apply()
    fun getDensity(): Int = prefs.getInt(KEY_DENSITY, 40)
    fun setDensity(v: Int) = prefs.edit().putInt(KEY_DENSITY, v).apply()
    fun getOverlayColor(): Int = prefs.getInt(KEY_OVERLAY_COLOR, Color.parseColor("#1A1A1A"))
    fun setOverlayColor(v: Int) = prefs.edit().putInt(KEY_OVERLAY_COLOR, v).apply()
}
""",

    # ============ Overlay View ============
    "app/src/main/java/com/shield/app/service/PrivacyOverlayView.kt": BFB_HEADER + """package com.shield.app.service

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.PorterDuff
import android.graphics.PorterDuffXfermode
import android.view.View
import com.shield.app.data.SettingsManager

class PrivacyOverlayView(context: Context) : View(context) {
    private val settings = SettingsManager(context)
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val clearPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply { xfermode = PorterDuffXfermode(PorterDuff.Mode.CLEAR) }
    init { setLayerType(LAYER_TYPE_SOFTWARE, null) }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)
        val pattern = settings.getPattern()
        val opacity = settings.getOpacity().coerceIn(0, 100) / 100f
        val density = settings.getDensity().coerceIn(5, 100)
        val color = settings.getOverlayColor()
        val alpha = (opacity * 255).toInt()
        canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR)
        when (pattern) {
            SettingsManager.PATTERN_SOLID -> drawSolid(canvas, color, alpha)
            SettingsManager.PATTERN_GRID -> drawGrid(canvas, color, alpha, density)
            SettingsManager.PATTERN_DOTS -> drawDots(canvas, color, alpha, density)
            SettingsManager.PATTERN_FOCUS -> drawFocus(canvas, color, alpha, density)
        }
    }
    private fun drawSolid(c: Canvas, color: Int, alpha: Int) {
        paint.style = Paint.Style.FILL; paint.color = color; paint.alpha = alpha
        c.drawRect(0f, 0f, width.toFloat(), height.toFloat(), paint)
    }
    private fun drawGrid(c: Canvas, color: Int, alpha: Int, density: Int) {
        paint.color = color; paint.alpha = alpha; paint.style = Paint.Style.STROKE; paint.strokeWidth = 2f
        val s = (120 - density).coerceAtLeast(8).toFloat()
        var x = 0f; while (x < width) { c.drawLine(x, 0f, x, height.toFloat(), paint); x += s }
        var y = 0f; while (y < height) { c.drawLine(0f, y, width.toFloat(), y, paint); y += s }
    }
    private fun drawDots(c: Canvas, color: Int, alpha: Int, density: Int) {
        paint.color = color; paint.alpha = alpha; paint.style = Paint.Style.FILL
        val s = (120 - density).coerceAtLeast(8).toFloat(); val r = s / 4f
        var y = s / 2; while (y < height) { var x = s / 2; while (x < width) { c.drawCircle(x.toFloat(), y.toFloat(), r, paint); x += s }; y += s }
    }
    private fun drawFocus(c: Canvas, color: Int, alpha: Int, density: Int) {
        paint.style = Paint.Style.FILL; paint.color = color; paint.alpha = alpha
        c.drawRect(0f, 0f, width.toFloat(), height.toFloat(), paint)
        val ratio = 1f - (density / 150f); val w = width * ratio; val h = height * ratio
        val l = (width - w) / 2f; val t = (height - h) / 2f
        c.drawRect(l, t, l + w, t + h, clearPaint)
        paint.style = Paint.Style.STROKE; paint.strokeWidth = 3f; paint.alpha = (alpha * 0.5f).toInt()
        c.drawRect(l, t, l + w, t + h, paint)
    }
}
""",

    "app/src/main/java/com/shield/app/service/PrivacyOverlayService.kt": BFB_HEADER + """package com.shield.app.service

import android.app.Service
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.WindowManager
import androidx.core.app.NotificationCompat
import com.shield.app.R

class PrivacyOverlayService : Service() {
    companion object { const val CHANNEL_ID = "shield_overlay"; const val NOTIF_ID = 1001 }
    private lateinit var wm: WindowManager
    private var view: PrivacyOverlayView? = null

    override fun onBind(i: Intent?): IBinder? = null
    override fun onCreate() {
        super.onCreate(); wm = getSystemService(WINDOW_SERVICE) as WindowManager
        startForeground(NOTIF_ID, NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(getString(R.string.app_name)).setContentText(getString(R.string.notif_active))
            .setSmallIcon(R.drawable.ic_shield).setPriority(NotificationCompat.PRIORITY_LOW).setOngoing(true).build())
        addOverlay()
    }
    override fun onStartCommand(i: Intent?, f: Int, s: Int): Int { view?.invalidate(); return START_STICKY }
    override fun onDestroy() { removeOverlay(); super.onDestroy() }

    private fun addOverlay() {
        if (view != null) return
        view = PrivacyOverlayView(this)
        val lp = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT, WindowManager.LayoutParams.MATCH_PARENT,
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
            else @Suppress("DEPRECATION") WindowManager.LayoutParams.TYPE_SYSTEM_OVERLAY,
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE or
            WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
            PixelFormat.TRANSLUCENT
        ).apply { gravity = Gravity.CENTER }
        try { wm.addView(view, lp) } catch (e: Exception) { e.printStackTrace(); stopSelf() }
    }
    private fun removeOverlay() {
        view?.let { try { wm.removeView(it) } catch (_: Exception) {} }
        view = null
    }
}
""",

    "app/src/main/java/com/shield/app/service/PrivacyTileService.kt": BFB_HEADER + """package com.shield.app.service

import android.content.Intent
import android.graphics.drawable.Icon
import android.os.Build
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService
import androidx.annotation.RequiresApi
import com.shield.app.R
import com.shield.app.data.SettingsManager
import com.shield.app.ui.MainActivity

@RequiresApi(Build.VERSION_CODES.N)
class PrivacyTileService : TileService() {
    private lateinit var settings: SettingsManager
    override fun onCreate() { super.onCreate(); settings = SettingsManager(this) }
    override fun onStartListening() { super.onStartListening(); updateTile() }
    override fun onClick() {
        super.onClick()
        val newState = !settings.isEnabled()
        settings.setEnabled(newState)
        if (newState) {
            if (!android.provider.Settings.canDrawOverlays(this)) {
                settings.setEnabled(false)
                startActivityAndCollapse(Intent(this, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                return
            }
            val i = Intent(this, PrivacyOverlayService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(i) else startService(i)
        } else {
            stopService(Intent(this, PrivacyOverlayService::class.java))
        }
        updateTile()
    }
    private fun updateTile() {
        val tile = qsTile ?: return
        val on = settings.isEnabled()
        tile.state = if (on) Tile.STATE_ACTIVE else Tile.STATE_INACTIVE
        tile.label = getString(if (on) R.string.tile_on else R.string.tile_off)
        tile.icon = Icon.createWithResource(this, R.drawable.ic_shield_tile)
        tile.updateTile()
    }
}
""",

    # ============ UI - MainActivity ============
    "app/src/main/java/com/shield/app/ui/MainActivity.kt": BFB_HEADER + """package com.shield.app.ui

import android.app.StatusBarManager
import android.content.ComponentName
import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.graphics.drawable.Icon
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import android.view.View
import android.widget.RadioButton
import android.widget.SeekBar
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton
import androidx.appcompat.widget.SwitchCompat
import androidx.lifecycle.lifecycleScope
import com.shield.app.R
import com.shield.app.ShieldApp
import com.shield.app.data.SettingsManager
import com.shield.app.data.theme.ThemeRepository
import com.shield.app.service.PrivacyOverlayService
import com.shield.app.service.PrivacyTileService
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {
    private lateinit var settings: SettingsManager
    private lateinit var themeRepo: ThemeRepository
    private lateinit var switchEnable: SwitchCompat
    private lateinit var statusText: TextView
    private lateinit var btnPermission: AppCompatButton
    private lateinit var btnAddTile: AppCompatButton
    private lateinit var radioSolid: RadioButton
    private lateinit var radioGrid: RadioButton
    private lateinit var radioDots: RadioButton
    private lateinit var radioFocus: RadioButton
    private lateinit var seekOpacity: SeekBar
    private lateinit var txtOpacity: TextView
    private lateinit var seekDensity: SeekBar
    private lateinit var txtDensity: TextView
    private lateinit var viewOverlayColor: View
    private lateinit var btnPickOverlay: AppCompatButton
    private lateinit var btnAppearance: AppCompatButton
    private lateinit var btnAbout: AppCompatButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        settings = SettingsManager(this)
        themeRepo = (application as ShieldApp).themeRepo
        bindViews(); setupToolbar(); setupPermission(); setupTile(); setupPattern()
        setupSliders(); setupColor(); setupSwitch(); setupNavButtons()
        observeTheme(); refreshUI()
    }

    override fun onResume() { super.onResume(); refreshUI() }

    private fun bindViews() {
        switchEnable = findViewById(R.id.switchEnable); statusText = findViewById(R.id.statusText)
        btnPermission = findViewById(R.id.btnPermission); btnAddTile = findViewById(R.id.btnAddTile)
        radioSolid = findViewById(R.id.radioSolid); radioGrid = findViewById(R.id.radioGrid)
        radioDots = findViewById(R.id.radioDots); radioFocus = findViewById(R.id.radioFocus)
        seekOpacity = findViewById(R.id.seekOpacity); txtOpacity = findViewById(R.id.txtOpacity)
        seekDensity = findViewById(R.id.seekDensity); txtDensity = findViewById(R.id.txtDensity)
        viewOverlayColor = findViewById(R.id.viewOverlayColor)
        btnPickOverlay = findViewById(R.id.btnPickOverlay)
        btnAppearance = findViewById(R.id.btnAppearance); btnAbout = findViewById(R.id.btnAbout)
    }

    private fun setupToolbar() { setSupportActionBar(findViewById(R.id.toolbar)) }
    private fun setupPermission() {
        btnPermission.setOnClickListener { startActivity(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName"))) }
    }
    private fun setupTile() {
        btnAddTile.setOnClickListener {
            try {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                    val statusBarManager = getSystemService(StatusBarManager::class.java)
                    val componentName = ComponentName(this, PrivacyTileService::class.java)
                    statusBarManager?.requestAddTileService(
                        componentName,
                        getString(R.string.tile_label),
                        Icon.createWithResource(this, R.drawable.ic_shield_tile),
                        { command -> command.run() },
                        {}
                    )
                } else {
                    startActivity(
                        Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS).apply {
                            data = Uri.parse("package:$packageName")
                        }
                    )
                }
            } catch (_: Exception) {}
        }
    }
    private fun setupPattern() {
        findViewById<android.widget.RadioGroup>(R.id.radioGroupPattern).setOnCheckedChangeListener { _, id ->
            val p = when (id) {
                R.id.radioSolid -> SettingsManager.PATTERN_SOLID
                R.id.radioGrid -> SettingsManager.PATTERN_GRID
                R.id.radioDots -> SettingsManager.PATTERN_DOTS
                R.id.radioFocus -> SettingsManager.PATTERN_FOCUS
                else -> SettingsManager.PATTERN_SOLID
            }
            settings.setPattern(p); refreshOverlay()
        }
    }
    private fun setupSliders() {
        seekOpacity.max = 100; seekDensity.max = 100
        seekOpacity.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(s: SeekBar?, p: Int, u: Boolean) {
                txtOpacity.text = getString(R.string.opacity_fmt, p)
                if (u) { settings.setOpacity(p); refreshOverlay() }
            }
            override fun onStartTrackingTouch(s: SeekBar?) {}
            override fun onStopTrackingTouch(s: SeekBar?) {}
        })
        seekDensity.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(s: SeekBar?, p: Int, u: Boolean) {
                txtDensity.text = getString(R.string.density_fmt, p)
                if (u) { settings.setDensity(p); refreshOverlay() }
            }
            override fun onStartTrackingTouch(s: SeekBar?) {}
            override fun onStopTrackingTouch(s: SeekBar?) {}
        })
    }
    private fun setupColor() {
        btnPickOverlay.setOnClickListener {
            val i = Intent(Intent.ACTION_PICK).setType("image/*")
            try { startActivity(i) } catch (_: Exception) {}
        }
    }
    private fun setupSwitch() {
        switchEnable.setOnCheckedChangeListener { _, on ->
            if (on && !Settings.canDrawOverlays(this)) {
                switchEnable.isChecked = false
                startActivity(Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION, Uri.parse("package:$packageName")))
                return@setOnCheckedChangeListener
            }
            settings.setEnabled(on)
            if (on) startOverlay() else stopOverlay()
            updateStatus()
        }
    }
    private fun setupNavButtons() {
        btnAppearance.setOnClickListener { startActivity(Intent(this, AppearanceActivity::class.java)) }
        btnAbout.setOnClickListener { startActivity(Intent(this, AboutActivity::class.java)) }
    }
    private fun observeTheme() {
        lifecycleScope.launch { themeRepo.configFlow.collect { /* Theme applied via ThemeManager */ } }
    }
    private fun refreshUI() {
        when (settings.getPattern()) {
            SettingsManager.PATTERN_SOLID -> radioSolid.isChecked = true
            SettingsManager.PATTERN_GRID -> radioGrid.isChecked = true
            SettingsManager.PATTERN_DOTS -> radioDots.isChecked = true
            SettingsManager.PATTERN_FOCUS -> radioFocus.isChecked = true
        }
        seekOpacity.progress = settings.getOpacity()
        txtOpacity.text = getString(R.string.opacity_fmt, settings.getOpacity())
        seekDensity.progress = settings.getDensity()
        txtDensity.text = getString(R.string.density_fmt, settings.getDensity())
        applyColorPreview(viewOverlayColor, settings.getOverlayColor())
        val hasPerm = Settings.canDrawOverlays(this)
        btnPermission.isEnabled = !hasPerm
        btnPermission.text = getString(if (hasPerm) R.string.perm_granted else R.string.perm_grant)
        switchEnable.isChecked = settings.isEnabled()
        updateStatus()
    }
    private fun updateStatus() {
        statusText.text = getString(if (settings.isEnabled()) R.string.status_on else R.string.status_off)
        statusText.setTextColor(if (settings.isEnabled()) Color.parseColor("#2ECC71") else Color.parseColor("#FF5A5F"))
    }
    private fun applyColorPreview(v: View, color: Int) {
        v.background = GradientDrawable().apply { shape = GradientDrawable.RECTANGLE; setColor(color); setStroke(2, Color.GRAY); cornerRadius = 16f }
    }
    private fun startOverlay() {
        val i = Intent(this, PrivacyOverlayService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(i) else startService(i)
    }
    private fun stopOverlay() { stopService(Intent(this, PrivacyOverlayService::class.java)) }
    private fun refreshOverlay() { if (settings.isEnabled()) try { startOverlay() } catch (_: Exception) {} }
}
""",

    "app/src/main/java/com/shield/app/ui/AppearanceActivity.kt": BFB_HEADER + """package com.shield.app.ui

import android.os.Bundle
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton
import androidx.lifecycle.lifecycleScope
import com.shield.app.R
import com.shield.app.ShieldApp
import com.shield.app.data.theme.BuiltInThemes
import com.shield.app.data.theme.ThemeConfig
import com.shield.app.data.theme.ThemeImporter
import com.shield.app.data.theme.ThemeMode
import com.shield.app.data.theme.ThemeRepository
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch

class AppearanceActivity : AppCompatActivity() {
    private lateinit var themeRepo: ThemeRepository
    private lateinit var radioGroup: RadioGroup
    private lateinit var radioLight: RadioButton
    private lateinit var radioDark: RadioButton
    private lateinit var radioAmoled: RadioButton
    private lateinit var radioSystem: RadioButton
    private lateinit var btnReset: AppCompatButton
    private lateinit var btnExport: AppCompatButton
    private lateinit var btnImport: AppCompatButton
    private lateinit var previewText: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_appearance)
        themeRepo = (application as ShieldApp).themeRepo
        setSupportActionBar(findViewById(R.id.toolbar))
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.appearance)

        radioGroup = findViewById(R.id.radioThemeMode)
        radioLight = findViewById(R.id.radioLight)
        radioDark = findViewById(R.id.radioDark)
        radioAmoled = findViewById(R.id.radioAmoled)
        radioSystem = findViewById(R.id.radioSystem)
        btnReset = findViewById(R.id.btnReset)
        btnExport = findViewById(R.id.btnExport)
        btnImport = findViewById(R.id.btnImport)
        previewText = findViewById(R.id.previewText)

        lifecycleScope.launch { themeRepo.configFlow.collect { config -> applyConfig(config) } }

        radioGroup.setOnCheckedChangeListener { _, id ->
            val mode = when (id) {
                R.id.radioLight -> ThemeMode.LIGHT
                R.id.radioDark -> ThemeMode.DARK
                R.id.radioAmoled -> ThemeMode.AMOLED
                else -> ThemeMode.SYSTEM
            }
            lifecycleScope.launch {
                val current = themeRepo.configFlow.first()
                themeRepo.saveConfig(current.copy(mode = mode))
            }
        }

        btnReset.setOnClickListener { lifecycleScope.launch { themeRepo.saveConfig(BuiltInThemes.DEFAULT) } }

        btnExport.setOnClickListener {
            lifecycleScope.launch {
                val config = themeRepo.configFlow.first()
                val json = ThemeImporter.exportToJson(config)
                val file = java.io.File(filesDir, "current_theme.bfbtheme")
                file.writeText(json)
                android.widget.Toast.makeText(this@AppearanceActivity, getString(R.string.theme_exported_to, file.absolutePath), android.widget.Toast.LENGTH_LONG).show()
            }
        }

        btnImport.setOnClickListener {
            android.widget.Toast.makeText(this, R.string.import_coming_soon, android.widget.Toast.LENGTH_SHORT).show()
        }
    }

    private fun applyConfig(config: ThemeConfig) {
        when (config.mode) {
            ThemeMode.LIGHT -> radioLight.isChecked = true
            ThemeMode.DARK -> radioDark.isChecked = true
            ThemeMode.AMOLED -> radioAmoled.isChecked = true
            ThemeMode.SYSTEM -> radioSystem.isChecked = true
        }
        previewText.text = getString(R.string.preview_theme_name, config.name)
    }

    override fun onSupportNavigateUp(): Boolean { finish(); return true }
}
""",

    "app/src/main/java/com/shield/app/ui/AboutActivity.kt": BFB_HEADER + """package com.shield.app.ui

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.shield.app.R

class AboutActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)
        setSupportActionBar(findViewById(R.id.toolbar))
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.about)

        findViewById<TextView>(R.id.txtVersion).text = getString(R.string.version_fmt, "1.0.0", "001")
        findViewById<TextView>(R.id.txtBfbSignature).text = getString(R.string.built_with_bfb)
        findViewById<TextView>(R.id.txtBfbMeaning).text = getString(R.string.bfb_meaning)
    }
    override fun onSupportNavigateUp(): Boolean { finish(); return true }
}
""",

    # ============ Layouts ============
    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto" xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent" android:layout_height="match_parent" android:fitsSystemWindows="true">
    <com.google.android.material.appbar.AppBarLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:fitsSystemWindows="true">
        <com.google.android.material.appbar.MaterialToolbar android:id="@+id/toolbar" android:layout_width="match_parent" android:layout_height="?attr/actionBarSize" android:title="@string/app_name" app:titleCentered="true" />
    </com.google.android.material.appbar.AppBarLayout>
    <androidx.core.widget.NestedScrollView android:layout_width="match_parent" android:layout_height="match_parent" app:layout_behavior="@string/appbar_scrolling_view_behavior">
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/section_status" android:textStyle="bold" android:textSize="16sp" />
                    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:gravity="center_vertical" android:orientation="horizontal">
                        <TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="@string/enable_shield" android:textSize="15sp" />
                        <androidx.appcompat.widget.SwitchCompat android:id="@+id/switchEnable" android:layout_width="wrap_content" android:layout_height="wrap_content" />
                    </LinearLayout>
                    <TextView android:id="@+id/statusText" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="4dp" android:textSize="13sp" tools:text="@string/status_off" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/section_permissions" android:textStyle="bold" android:textSize="16sp" />
                    <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnPermission" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="@string/perm_grant" />
                    <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnAddTile" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/add_tile" style="@style/Widget.Material3.Button.TonalButton" />
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="4dp" android:text="@string/tile_hint" android:textSize="12sp" android:alpha="0.7" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/section_pattern" android:textStyle="bold" android:textSize="16sp" />
                    <RadioGroup android:id="@+id/radioGroupPattern" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp">
                        <RadioButton android:id="@+id/radioSolid" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_solid" />
                        <RadioButton android:id="@+id/radioGrid" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_grid" />
                        <RadioButton android:id="@+id/radioDots" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_dots" />
                        <RadioButton android:id="@+id/radioFocus" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_focus" />
                    </RadioGroup>
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/section_adjust" android:textStyle="bold" android:textSize="16sp" />
                    <TextView android:id="@+id/txtOpacity" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:textSize="14sp" tools:text="Opacity: 40%" />
                    <SeekBar android:id="@+id/seekOpacity" android:layout_width="match_parent" android:layout_height="wrap_content" />
                    <TextView android:id="@+id/txtDensity" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:textSize="14sp" tools:text="Density: 40" />
                    <SeekBar android:id="@+id/seekDensity" android:layout_width="match_parent" android:layout_height="wrap_content" />
                    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:gravity="center_vertical" android:orientation="horizontal">
                        <View android:id="@+id/viewOverlayColor" android:layout_width="40dp" android:layout_height="40dp" />
                        <TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="12dp" android:layout_weight="1" android:text="@string/overlay_color" android:textSize="14sp" />
                        <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnPickOverlay" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/pick" style="@style/Widget.Material3.Button.TextButton" />
                    </LinearLayout>
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="horizontal" android:layout_marginBottom="12dp">
                <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnAppearance" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="@string/appearance" android:layout_marginEnd="4dp" />
                <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnAbout" android:layout_width="0dp" android:layout_height="wrap_content" android:layout_weight="1" android:text="@string/about" android:layout_marginStart="4dp" />
            </LinearLayout>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:layout_marginBottom="24dp" android:gravity="center" android:text="@string/footer_bfb" android:textSize="11sp" android:alpha="0.6" />
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
</androidx.coordinatorlayout.widget.CoordinatorLayout>
""",

    "app/src/main/res/layout/activity_appearance.xml": """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto" android:layout_width="match_parent" android:layout_height="match_parent" android:fitsSystemWindows="true">
    <com.google.android.material.appbar.AppBarLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:fitsSystemWindows="true">
        <com.google.android.material.appbar.MaterialToolbar android:id="@+id/toolbar" android:layout_width="match_parent" android:layout_height="?attr/actionBarSize" app:titleCentered="true" />
    </com.google.android.material.appbar.AppBarLayout>
    <androidx.core.widget.NestedScrollView android:layout_width="match_parent" android:layout_height="match_parent" app:layout_behavior="@string/appbar_scrolling_view_behavior">
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:id="@+id/previewText" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/preview_theme_name" android:textSize="14sp" android:gravity="center" android:padding="16dp" android:background="?attr/colorSurface" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/theme_mode" android:textStyle="bold" android:textSize="16sp" />
                    <RadioGroup android:id="@+id/radioThemeMode" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp">
                        <RadioButton android:id="@+id/radioLight" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/mode_light" />
                        <RadioButton android:id="@+id/radioDark" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/mode_dark" />
                        <RadioButton android:id="@+id/radioAmoled" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/mode_amoled" />
                        <RadioButton android:id="@+id/radioSystem" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/mode_system" />
                    </RadioGroup>
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="12dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp">
                    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/theme_actions" android:textStyle="bold" android:textSize="16sp" />
                    <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnReset" android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="@string/reset_default" />
                    <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnExport" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/export_theme" />
                    <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnImport" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/import_theme" style="@style/Widget.Material3.Button.TonalButton" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
</androidx.coordinatorlayout.widget.CoordinatorLayout>
""",

    "app/src/main/res/layout/activity_about.xml": """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto" android:layout_width="match_parent" android:layout_height="match_parent" android:fitsSystemWindows="true">
    <com.google.android.material.appbar.AppBarLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:fitsSystemWindows="true">
        <com.google.android.material.appbar.MaterialToolbar android:id="@+id/toolbar" android:layout_width="match_parent" android:layout_height="?attr/actionBarSize" app:titleCentered="true" />
    </com.google.android.material.appbar.AppBarLayout>
    <androidx.core.widget.NestedScrollView android:layout_width="match_parent" android:layout_height="match_parent" app:layout_behavior="@string/appbar_scrolling_view_behavior">
        <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="24dp" android:gravity="center_horizontal">
            <ImageView android:layout_width="96dp" android:layout_height="96dp" android:src="@drawable/ic_shield" android:layout_marginBottom="16dp" android:contentDescription="@string/app_name" />
            <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/app_name" android:textSize="24sp" android:textStyle="bold" android:layout_marginBottom="8dp" />
            <TextView android:id="@+id/txtVersion" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textSize="14sp" android:alpha="0.7" android:layout_marginBottom="32dp" />
            <com.google.android.material.card.MaterialCardView android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginBottom="16dp" app:cardCornerRadius="16dp" app:cardElevation="2dp">
                <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:orientation="vertical" android:padding="16dp" android:gravity="center_horizontal">
                    <TextView android:id="@+id/txtBfbSignature" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textSize="18sp" android:textStyle="bold" android:textColor="?attr/colorPrimary" android:layout_marginBottom="4dp" />
                    <TextView android:id="@+id/txtBfbMeaning" android:layout_width="wrap_content" android:layout_height="wrap_content" android:textSize="13sp" android:alpha="0.7" android:gravity="center" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/about_desc" android:textSize="14sp" android:lineSpacingMultiplier="1.4" android:layout_marginBottom="16dp" />
            <TextView android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/no_gms" android:textSize="13sp" android:alpha="0.7" android:gravity="center" />
        </LinearLayout>
    </androidx.core.widget.NestedScrollView>
</androidx.coordinatorlayout.widget.CoordinatorLayout>
""",

    # ============ Strings ============
    "app/src/main/res/values/strings.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Shield</string>
    <string name="tile_label">Privacy Shield</string>
    <string name="tile_on">Shield ON</string>
    <string name="tile_off">Shield OFF</string>
    <string name="notif_channel_overlay">Shield Service</string>
    <string name="notif_channel_overlay_desc">Keeps privacy overlay active</string>
    <string name="notif_channel_crash">Error Reports</string>
    <string name="notif_active">Privacy shield is active</string>
    <string name="section_status">Status</string>
    <string name="enable_shield">Enable Privacy Shield</string>
    <string name="status_on">Shield is active</string>
    <string name="status_off">Shield is inactive</string>
    <string name="section_permissions">Permissions</string>
    <string name="perm_grant">Grant Display Over Apps</string>
    <string name="perm_granted">Permission granted ✓</string>
    <string name="add_tile">Open Quick Settings</string>
    <string name="tile_hint">Add "Privacy Shield" tile from Quick Settings edit menu.</string>
    <string name="section_pattern">Pattern</string>
    <string name="pattern_solid">Solid veil</string>
    <string name="pattern_grid">Linear grid</string>
    <string name="pattern_dots">Dot grid</string>
    <string name="pattern_focus">Focus area</string>
    <string name="section_adjust">Adjustments</string>
    <string name="opacity_fmt">Opacity: %1$d%%</string>
    <string name="density_fmt">Density: %1$d</string>
    <string name="overlay_color">Overlay color</string>
    <string name="pick">Pick</string>
    <string name="appearance">Appearance</string>
    <string name="about">About</string>
    <string name="theme_mode">Theme Mode</string>
    <string name="mode_light">Light</string>
    <string name="mode_dark">Dark</string>
    <string name="mode_amoled">AMOLED</string>
    <string name="mode_system">System Default</string>
    <string name="theme_actions">Theme Actions</string>
    <string name="reset_default">Reset to Default</string>
    <string name="export_theme">Export .bfbtheme</string>
    <string name="import_theme">Import .bfbtheme</string>
    <string name="preview_theme_name">Preview: %1$s</string>
    <string name="theme_exported_to">Theme exported to: %1$s</string>
    <string name="import_coming_soon">Import feature coming in next update</string>
    <string name="version_fmt">Version %1$s (build #%2$s)</string>
    <string name="built_with_bfb">Built with BFB.AI</string>
    <string name="bfb_meaning">Built For Benefits, by AI</string>
    <string name="about_desc">Shield is a privacy screen protector inspired by modern Galaxy features. It works fully offline with no Google services required.</string>
    <string name="no_gms">No Google Play Services required</string>
    <string name="footer_bfb">Shield v1.0.0 · Built with BFB.AI</string>
</resources>
""",

    "app/src/main/res/values-ar/strings.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Shield</string>
    <string name="tile_label">درع الخصوصية</string>
    <string name="tile_on">الدرع مُفعّل</string>
    <string name="tile_off">الدرع مُعطّل</string>
    <string name="notif_channel_overlay">خدمة Shield</string>
    <string name="notif_channel_overlay_desc">تبقي طبقة الخصوصية نشطة</string>
    <string name="notif_channel_crash">تقارير الأخطاء</string>
    <string name="notif_active">درع الخصوصية نشط</string>
    <string name="section_status">الحالة</string>
    <string name="enable_shield">تفعيل درع الخصوصية</string>
    <string name="status_on">الدرع مُفعّل</string>
    <string name="status_off">الدرع مُعطّل</string>
    <string name="section_permissions">الصلاحيات</string>
    <string name="perm_grant">منح صلاحية الظهور فوق التطبيقات</string>
    <string name="perm_granted">تم منح الصلاحية ✓</string>
    <string name="add_tile">فتح الإعدادات السريعة</string>
    <string name="tile_hint">أضف بلاطة \"درع الخصوصية\" من قائمة التعديل في الإعدادات السريعة.</string>
    <string name="section_pattern">النمط</string>
    <string name="pattern_solid">ستارة كاملة</string>
    <string name="pattern_grid">شبكة خطية</string>
    <string name="pattern_dots">شبكة نقطية</string>
    <string name="pattern_focus">منطقة تركيز</string>
    <string name="section_adjust">الضبط</string>
    <string name="opacity_fmt">الشفافية: %1$d%%</string>
    <string name="density_fmt">الكثافة: %1$d</string>
    <string name="overlay_color">لون الطبقة</string>
    <string name="pick">اختيار</string>
    <string name="appearance">المظهر</string>
    <string name="about">حول</string>
    <string name="theme_mode">وضع الثيم</string>
    <string name="mode_light">فاتح</string>
    <string name="mode_dark">داكن</string>
    <string name="mode_amoled">AMOLED</string>
    <string name="mode_system">اتبع النظام</string>
    <string name="theme_actions">إجراءات الثيم</string>
    <string name="reset_default">إعادة للافتراضي</string>
    <string name="export_theme">تصدير .bfbtheme</string>
    <string name="import_theme">استيراد .bfbtheme</string>
    <string name="preview_theme_name">معاينة: %1$s</string>
    <string name="theme_exported_to">تم تصدير الثيم إلى: %1$s</string>
    <string name="import_coming_soon">ميزة الاستيراد قادمة في التحديث القادم</string>
    <string name="version_fmt">الإصدار %1$s (بناء #%2$s)</string>
    <string name="built_with_bfb">Built with BFB.AI</string>
    <string name="bfb_meaning">صُنع لأجل المنفعة، بواسطة الذكاء الاصطناعي</string>
    <string name="about_desc">Shield هو حامي شاشة الخصوصية مستوحى من ميزات Galaxy الحديثة. يعمل بدون إنترنت وبدون أي خدمات جوجل.</string>
    <string name="no_gms">لا يحتاج إلى خدمات Google Play</string>
    <string name="footer_bfb">Shield v1.0.0 · Built with BFB.AI</string>
</resources>
""",

    "app/src/main/res/values/colors.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="primary">#00A6A6</color>
    <color name="primary_dark">#008888</color>
    <color name="accent">#00D4AA</color>
    <color name="background_light">#F5F7FA</color>
    <color name="background_dark">#0B1B3A</color>
    <color name="surface_light">#FFFFFF</color>
    <color name="surface_dark">#13264D</color>
    <color name="on_primary">#FFFFFF</color>
    <color name="on_background_light">#0B1B3A</color>
    <color name="on_background_dark">#FFFFFF</color>
</resources>
""",

    "app/src/main/res/values/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.Shield" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
        <item name="android:colorBackground">@color/background_light</item>
        <item name="colorSurface">@color/surface_light</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        <item name="colorOnBackground">@color/on_background_light</item>
        <item name="colorOnSurface">@color/on_background_light</item>
    </style>
    <style name="Theme.Shield.Splash" parent="Theme.Shield">
        <item name="android:windowBackground">@color/primary</item>
    </style>
</resources>
""",

    "app/src/main/res/values-night/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.Shield" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">@color/primary</item>
        <item name="colorPrimaryDark">@color/primary_dark</item>
        <item name="colorAccent">@color/accent</item>
        <item name="android:colorBackground">@color/background_dark</item>
        <item name="colorSurface">@color/surface_dark</item>
        <item name="colorOnPrimary">@color/on_primary</item>
        <item name="colorOnBackground">@color/on_background_dark</item>
        <item name="colorOnSurface">@color/on_background_dark</item>
    </style>
    <style name="Theme.Shield.Splash" parent="Theme.Shield">
        <item name="android:windowBackground">@color/background_dark</item>
    </style>
</resources>
""",

    # ============ Drawables ============
    "app/src/main/res/drawable/ic_shield.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24"
    android:tint="?attr/colorControlNormal">
    <path android:fillColor="@android:color/white"
        android:pathData="M12,1L3,5v6c0,5.55 3.84,10.74 9,12 5.16,-1.26 9,-6.45 9,-12V5l-9,-4zM12,11.99h7c-0.53,4.12 -3.28,7.79 -7,8.94V12H5V6.3l7,-3.11v8.8z"/>
</vector>
""",

    "app/src/main/res/drawable/ic_shield_tile.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#FFFFFF"
        android:pathData="M12,1L3,5v6c0,5.55 3.84,10.74 9,12 5.16,-1.26 9,-6.45 9,-12V5l-9,-4zM12,11.99h7c-0.53,4.12 -3.28,7.79 -7,8.94V12H5V6.3l7,-3.11v8.8z"/>
</vector>
""",

    "app/src/main/res/drawable/ic_shield_foreground.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#4DE1E1"
        android:pathData="M54,20 L80,30 L80,54 C80,74 67,86 54,92 C41,86 28,74 28,54 L28,30 Z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M54,50 m-6,0 a6,6 0 1,0 12,0 a6,6 0 1,0 -12,0"/>
</vector>
""",

    "app/src/main/res/drawable/ic_shield_monochrome.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp" android:height="24dp" android:viewportWidth="24" android:viewportHeight="24">
    <path android:fillColor="#000000"
        android:pathData="M12,1L3,5v6c0,5.55 3.84,10.74 9,12 5.16,-1.26 9,-6.45 9,-12V5l-9,-4zM12,11.99h7c-0.53,4.12 -3.28,7.79 -7,8.94V12H5V6.3l7,-3.11v8.8z"/>
</vector>
""",

    "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/primary"/>
    <foreground android:drawable="@drawable/ic_shield_foreground"/>
    <monochrome android:drawable="@drawable/ic_shield_monochrome"/>
</adaptive-icon>
""",

    "app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/primary"/>
    <foreground android:drawable="@drawable/ic_shield_foreground"/>
    <monochrome android:drawable="@drawable/ic_shield_monochrome"/>
</adaptive-icon>
""",

    # ============ Brand Assets (BFB.AI section 16) ============
    "assets/brand/BFB_light.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 160" width="480" height="160" role="img" aria-label="BFB.AI">
<title>BFB.AI - Built For Benefits, by AI</title>
<text x="240" y="88" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="68" font-weight="800" letter-spacing="2" fill="#0B1B3A">BFB<tspan fill="#00A6A6">.AI</tspan></text>
<rect x="150" y="104" width="180" height="3" rx="1.5" fill="#00A6A6"/>
<text x="240" y="134" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="17" font-weight="500" letter-spacing="1.5" fill="#4A5A78">Built For Benefits, by AI</text>
</svg>
""",

    "assets/brand/BFB_dark.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 160" width="480" height="160" role="img" aria-label="BFB.AI">
<title>BFB.AI - Built For Benefits, by AI</title>
<rect width="480" height="160" rx="24" fill="#0B1B3A"/>
<text x="240" y="88" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="68" font-weight="800" letter-spacing="2" fill="#FFFFFF">BFB<tspan fill="#4DE1E1">.AI</tspan></text>
<rect x="150" y="104" width="180" height="3" rx="1.5" fill="#4DE1E1"/>
<text x="240" y="134" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="17" font-weight="500" letter-spacing="1.5" fill="#A9B8D4">Built For Benefits, by AI</text>
</svg>
""",

    "assets/brand/BFB_mono.svg": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 160" width="480" height="160" role="img" aria-label="BFB.AI">
<title>BFB.AI</title>
<text x="240" y="88" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="68" font-weight="800" letter-spacing="2" fill="currentColor">BFB<tspan fill="currentColor">.AI</tspan></text>
<rect x="150" y="104" width="180" height="3" rx="1.5" fill="currentColor"/>
<text x="240" y="134" text-anchor="middle" font-family="Inter, 'IBM Plex Sans', Cairo, sans-serif" font-size="17" font-weight="500" letter-spacing="1.5" fill="currentColor">Built For Benefits, by AI</text>
</svg>
""",

    # ============ Theme Schema + Sample Themes ============
    "themes/bfbtheme.schema.json": """{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BFB Theme",
  "type": "object",
  "required": ["schema", "name", "mode", "colors"],
  "properties": {
    "schema": { "type": "integer", "const": 1 },
    "name": { "type": "string", "maxLength": 64 },
    "mode": { "type": "string", "enum": ["LIGHT", "DARK", "AMOLED", "SYSTEM"] },
    "colors": {
      "type": "object",
      "required": ["primary", "secondary", "accent", "background", "surface"],
      "properties": {
        "primary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "secondary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "accent": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "background": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "surface": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "onPrimary": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "onBackground": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "onSurface": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "error": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "success": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" },
        "warning": { "type": "string", "pattern": "^#[0-9A-Fa-f]{6}$" }
      },
      "additionalProperties": false
    }
  },
  "additionalProperties": false
}
""",

    "themes/shield_default.bfbtheme": """{
  "schema": 1,
  "name": "Shield Default",
  "mode": "SYSTEM",
  "colors": {
    "primary": "#00A6A6",
    "secondary": "#0B1B3A",
    "accent": "#00D4AA",
    "background": "#F5F7FA",
    "surface": "#FFFFFF",
    "onPrimary": "#FFFFFF",
    "onBackground": "#0B1B3A",
    "onSurface": "#0B1B3A",
    "error": "#FF5A5F",
    "success": "#2ECC71",
    "warning": "#F5A623"
  }
}
""",

    "themes/midnight_gold.bfbtheme": """{
  "schema": 1,
  "name": "Midnight Gold",
  "mode": "DARK",
  "colors": {
    "primary": "#D4AF37",
    "secondary": "#3A4A6B",
    "accent": "#4DE1E1",
    "background": "#0B1B3A",
    "surface": "#13264D",
    "onPrimary": "#FFFFFF",
    "onBackground": "#FFF8DC",
    "onSurface": "#FFF8DC",
    "error": "#FF5A5F",
    "success": "#2ECC71",
    "warning": "#F5A623"
  }
}
""",

    # ============ Documentation ============
    "README.md": """# 🛡️ Shield — Privacy Screen Protector

> BFB.AI · Built For Benefits, by AI

تطبيق أندرويد خفيف يوفّر طبقة خصوصية فوق الشاشة (Privacy Overlay) تُفعَّل بضغطة واحدة من **الإعدادات السريعة** (Quick Settings Tile).

## ✨ المميزات
- ⚡ **تشغيل بضغطة واحدة** من Quick Settings Tile
- 🎨 **4 أنماط للخصوصية**: ستارة كاملة، شبكة خطية، شبكة نقطية، منطقة تركيز
- 🌈 **تخصيص كامل للألوان** والشفافية والكثافة
- 🎭 **6 ثيمات جاهزة** + تصدير/استيراد ثيمات `.bfbtheme`
- 🌙 **دعم الوضع الليلي والنهاري + AMOLED**
- 🌐 **دعم العربية (RTL) والإنجليزية (LTR)**
- 📱 **يعمل على Android 7.0+ و HarmonyOS**
- 🚫 **بدون Google Play Services** — مستقل تماماً
- 🔒 **توقيع BFB.AI** في كل مكان

## 📲 التثبيت
حمّل APK من **Actions → Artifacts** بعد نجاح الـ workflow.

## 🛠️ البناء من المصدر
```bash
git clone [https://github.com/Mohammedazizhedia/Shield.git](https://github.com/Mohammedazizhedia/Shield.git)
cd Shield
./gradlew assembleDebug
