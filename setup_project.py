#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shield Project Auto-Generator
ينشئ كل ملفات المشروع تلقائياً عند تشغيله من GitHub Actions
"""

import os
import sys

# ==================== محتوى كل الملفات ====================

FILES = {
    # ---------- Gradle (جذر المشروع) ----------
    "build.gradle.kts": """plugins {
    id("com.android.application") version "8.2.0" apply false
    id("org.jetbrains.kotlin.android") version "1.9.22" apply false
}
""",

    "settings.gradle.kts": """pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
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
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.2-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""",

    # ---------- app module ----------
    "app/build.gradle.kts": """plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.shield.app"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.shield.app"
        minSdk = 24
        targetSdk = 34
        versionCode = 1
        versionName = "1.0.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.appcompat:appcompat:1.6.1")
    implementation("com.google.android.material:material:1.11.0")
    implementation("androidx.constraintlayout:constraintlayout:2.1.4")
}
""",

    "app/proguard-rules.pro": """-keepclassmembers class * extends android.service.quicksettings.TileService {
    public <methods>;
}
""",

    # ---------- AndroidManifest ----------
    "app/src/main/AndroidManifest.xml": """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.SYSTEM_ALERT_WINDOW" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_SPECIAL_USE" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <application
        android:allowBackup="false"
        android:icon="@mipmap/ic_launcher"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.Shield"
        tools:targetApi="34">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:label="@string/app_name"
            android:theme="@style/Theme.Shield">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".PrivacyTileService"
            android:exported="true"
            android:icon="@drawable/ic_shield_tile"
            android:label="@string/tile_label"
            android:permission="android.permission.BIND_QUICK_SETTINGS_TILE">
            <intent-filter>
                <action android:name="android.service.quicksettings.action.QS_TILE" />
            </intent-filter>
            <meta-data
                android:name="android.service.quicksettings.ACTIVE_TILE"
                android:value="true" />
        </service>

        <service
            android:name=".PrivacyOverlayService"
            android:exported="false"
            android:foregroundServiceType="specialUse" />

    </application>
</manifest>
""",

    # ---------- Kotlin sources ----------
    "app/src/main/java/com/shield/app/SettingsManager.kt": """package com.shield.app

import android.content.Context
import android.content.SharedPreferences
import android.graphics.Color

class SettingsManager(context: Context) {

    companion object {
        const val PREFS_NAME = "shield_prefs"

        const val KEY_ENABLED = "enabled"
        const val KEY_PATTERN = "pattern"
        const val KEY_OPACITY = "opacity"
        const val KEY_DENSITY = "density"
        const val KEY_PRIMARY_COLOR = "primary_color"
        const val KEY_OVERLAY_COLOR = "overlay_color"

        const val DEFAULT_PATTERN = "solid"
        const val DEFAULT_OPACITY = 30
        const val DEFAULT_DENSITY = 40
        val DEFAULT_PRIMARY_COLOR = Color.parseColor("#1A1A1A")
        val DEFAULT_OVERLAY_COLOR = Color.parseColor("#000000")

        const val PATTERN_SOLID = "solid"
        const val PATTERN_GRID_LINES = "grid_lines"
        const val PATTERN_DOTS = "dots"
        const val PATTERN_FOCUS = "focus"
    }

    private val prefs: SharedPreferences =
        context.applicationContext.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE)

    fun isEnabled(): Boolean = prefs.getBoolean(KEY_ENABLED, false)
    fun setEnabled(value: Boolean) = prefs.edit().putBoolean(KEY_ENABLED, value).apply()

    fun getPattern(): String = prefs.getString(KEY_PATTERN, DEFAULT_PATTERN) ?: DEFAULT_PATTERN
    fun setPattern(value: String) = prefs.edit().putString(KEY_PATTERN, value).apply()

    fun getOpacity(): Int = prefs.getInt(KEY_OPACITY, DEFAULT_OPACITY)
    fun setOpacity(value: Int) = prefs.edit().putInt(KEY_OPACITY, value).apply()

    fun getDensity(): Int = prefs.getInt(KEY_DENSITY, DEFAULT_DENSITY)
    fun setDensity(value: Int) = prefs.edit().putInt(KEY_DENSITY, value).apply()

    fun getPrimaryColor(): Int = prefs.getInt(KEY_PRIMARY_COLOR, DEFAULT_PRIMARY_COLOR)
    fun setPrimaryColor(value: Int) = prefs.edit().putInt(KEY_PRIMARY_COLOR, value).apply()

    fun getOverlayColor(): Int = prefs.getInt(KEY_OVERLAY_COLOR, DEFAULT_OVERLAY_COLOR)
    fun setOverlayColor(value: Int) = prefs.edit().putInt(KEY_OVERLAY_COLOR, value).apply()
}
""",

    "app/src/main/java/com/shield/app/PrivacyOverlayView.kt": """package com.shield.app

import android.content.Context
import android.graphics.Canvas
import android.graphics.Color
import android.graphics.Paint
import android.graphics.PorterDuff
import android.graphics.PorterDuffXfermode
import android.view.View

class PrivacyOverlayView(context: Context) : View(context) {

    private val settings = SettingsManager(context)
    private val paint = Paint(Paint.ANTI_ALIAS_FLAG)
    private val clearPaint = Paint(Paint.ANTI_ALIAS_FLAG).apply {
        xfermode = PorterDuffXfermode(PorterDuff.Mode.CLEAR)
    }

    init {
        setLayerType(LAYER_TYPE_SOFTWARE, null)
    }

    override fun onDraw(canvas: Canvas) {
        super.onDraw(canvas)

        val pattern = settings.getPattern()
        val opacity = settings.getOpacity().coerceIn(0, 100) / 100f
        val density = settings.getDensity().coerceIn(5, 100)
        val overlayColor = settings.getOverlayColor()
        val alpha = (opacity * 255).toInt()

        canvas.drawColor(Color.TRANSPARENT, PorterDuff.Mode.CLEAR)

        when (pattern) {
            SettingsManager.PATTERN_SOLID -> drawSolid(canvas, overlayColor, alpha)
            SettingsManager.PATTERN_GRID_LINES -> drawGridLines(canvas, overlayColor, alpha, density)
            SettingsManager.PATTERN_DOTS -> drawDots(canvas, overlayColor, alpha, density)
            SettingsManager.PATTERN_FOCUS -> drawFocus(canvas, overlayColor, alpha, density)
        }
    }

    private fun drawSolid(canvas: Canvas, color: Int, alpha: Int) {
        paint.style = Paint.Style.FILL
        paint.color = color
        paint.alpha = alpha
        canvas.drawRect(0f, 0f, width.toFloat(), height.toFloat(), paint)
    }

    private fun drawGridLines(canvas: Canvas, color: Int, alpha: Int, density: Int) {
        paint.color = color
        paint.alpha = alpha
        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 2f

        val spacing = (120 - density).coerceAtLeast(8).toFloat()

        var x = 0f
        while (x < width) {
            canvas.drawLine(x, 0f, x, height.toFloat(), paint)
            x += spacing
        }
        var y = 0f
        while (y < height) {
            canvas.drawLine(0f, y, width.toFloat(), y, paint)
            y += spacing
        }
    }

    private fun drawDots(canvas: Canvas, color: Int, alpha: Int, density: Int) {
        paint.color = color
        paint.alpha = alpha
        paint.style = Paint.Style.FILL

        val spacing = (120 - density).coerceAtLeast(8).toFloat()
        val radius = spacing / 4f

        var y = spacing / 2
        while (y < height) {
            var x = spacing / 2
            while (x < width) {
                canvas.drawCircle(x.toFloat(), y.toFloat(), radius, paint)
                x += spacing
            }
            y += spacing
        }
    }

    private fun drawFocus(canvas: Canvas, color: Int, alpha: Int, density: Int) {
        paint.style = Paint.Style.FILL
        paint.color = color
        paint.alpha = alpha
        canvas.drawRect(0f, 0f, width.toFloat(), height.toFloat(), paint)

        val focusRatio = 1f - (density / 150f)
        val focusW = width * focusRatio
        val focusH = height * focusRatio
        val left = (width - focusW) / 2f
        val top = (height - focusH) / 2f

        canvas.drawRect(left, top, left + focusW, top + focusH, clearPaint)

        paint.style = Paint.Style.STROKE
        paint.strokeWidth = 3f
        paint.alpha = (alpha * 0.5f).toInt()
        canvas.drawRect(left, top, left + focusW, top + focusH, paint)
    }
}
""",

    "app/src/main/java/com/shield/app/PrivacyOverlayService.kt": """package com.shield.app

import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.Service
import android.content.Intent
import android.graphics.PixelFormat
import android.os.Build
import android.os.IBinder
import android.view.Gravity
import android.view.WindowManager
import androidx.core.app.NotificationCompat

class PrivacyOverlayService : Service() {

    companion object {
        const val CHANNEL_ID = "shield_overlay_channel"
        const val NOTIFICATION_ID = 1001
    }

    private lateinit var windowManager: WindowManager
    private var overlayView: PrivacyOverlayView? = null

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        windowManager = getSystemService(WINDOW_SERVICE) as WindowManager
        startForegroundNotification()
        addOverlay()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        overlayView?.invalidate()
        return START_STICKY
    }

    override fun onDestroy() {
        removeOverlay()
        super.onDestroy()
    }

    private fun startForegroundNotification() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val channel = NotificationChannel(
                CHANNEL_ID,
                getString(R.string.notification_channel_name),
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = getString(R.string.notification_channel_desc)
                setShowBadge(false)
            }
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(channel)
        }

        val notification: Notification = NotificationCompat.Builder(this, CHANNEL_ID)
            .setContentTitle(getString(R.string.app_name))
            .setContentText(getString(R.string.notification_active))
            .setSmallIcon(R.drawable.ic_shield)
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()

        startForeground(NOTIFICATION_ID, notification)
    }

    private fun addOverlay() {
        if (overlayView != null) return

        overlayView = PrivacyOverlayView(this)

        val layoutParams = WindowManager.LayoutParams(
            WindowManager.LayoutParams.MATCH_PARENT,
            WindowManager.LayoutParams.MATCH_PARENT,
            getWindowType(),
            WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_NOT_TOUCHABLE or
                    WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
            PixelFormat.TRANSLUCENT
        ).apply {
            gravity = Gravity.CENTER
            flags = flags or WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS
        }

        try {
            windowManager.addView(overlayView, layoutParams)
        } catch (e: Exception) {
            e.printStackTrace()
            stopSelf()
        }
    }

    private fun removeOverlay() {
        overlayView?.let {
            try {
                windowManager.removeView(it)
            } catch (_: Exception) { }
        }
        overlayView = null
    }

    private fun getWindowType(): Int {
        return if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
        } else {
            @Suppress("DEPRECATION")
            WindowManager.LayoutParams.TYPE_SYSTEM_OVERLAY
        }
    }
}
""",

    "app/src/main/java/com/shield/app/PrivacyTileService.kt": """package com.shield.app

import android.content.Intent
import android.graphics.drawable.Icon
import android.os.Build
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService
import androidx.annotation.RequiresApi

@RequiresApi(Build.VERSION_CODES.N)
class PrivacyTileService : TileService() {

    private lateinit var settings: SettingsManager

    override fun onCreate() {
        super.onCreate()
        settings = SettingsManager(this)
    }

    override fun onStartListening() {
        super.onStartListening()
        updateTile()
    }

    override fun onClick() {
        super.onClick()

        val currentlyEnabled = settings.isEnabled()
        val newState = !currentlyEnabled
        settings.setEnabled(newState)

        if (newState) {
            if (!android.provider.Settings.canDrawOverlays(this)) {
                settings.setEnabled(false)
                val intent = Intent(this, MainActivity::class.java).apply {
                    addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                }
                startActivityAndCollapse(intent)
                return
            }
            startOverlay()
        } else {
            stopOverlay()
        }

        updateTile()
    }

    private fun startOverlay() {
        val intent = Intent(this, PrivacyOverlayService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun stopOverlay() {
        val intent = Intent(this, PrivacyOverlayService::class.java)
        stopService(intent)
    }

    private fun updateTile() {
        val tile = qsTile ?: return
        val enabled = settings.isEnabled()

        tile.state = if (enabled) Tile.STATE_ACTIVE else Tile.STATE_INACTIVE
        tile.label = getString(if (enabled) R.string.tile_active else R.string.tile_inactive)
        tile.icon = Icon.createWithResource(this, R.drawable.ic_shield_tile)
        tile.updateTile()
    }
}
""",

    "app/src/main/java/com/shield/app/ColorPickerDialog.kt": """package com.shield.app

import android.app.Dialog
import android.content.Context
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
import android.os.Bundle
import android.text.Editable
import android.text.TextWatcher
import android.view.Window
import android.view.WindowManager
import android.widget.SeekBar
import androidx.appcompat.widget.AppCompatButton
import androidx.appcompat.widget.AppCompatEditText

class ColorPickerDialog(
    context: Context,
    private val initialColor: Int,
    private val onColorSelected: (Int) -> Unit
) : Dialog(context) {

    private var currentRed = Color.red(initialColor)
    private var currentGreen = Color.green(initialColor)
    private var currentBlue = Color.blue(initialColor)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        requestWindowFeature(Window.FEATURE_NO_TITLE)
        setContentView(R.layout.dialog_color_picker)

        window?.setLayout(
            (context.resources.displayMetrics.widthPixels * 0.92).toInt(),
            WindowManager.LayoutParams.WRAP_CONTENT
        )

        val preview = findViewById<android.view.View>(R.id.colorPreview)
        val hexInput = findViewById<AppCompatEditText>(R.id.hexInput)
        val seekR = findViewById<SeekBar>(R.id.seekRed)
        val seekG = findViewById<SeekBar>(R.id.seekGreen)
        val seekB = findViewById<SeekBar>(R.id.seekBlue)
        val btnOk = findViewById<AppCompatButton>(R.id.btnOk)
        val btnCancel = findViewById<AppCompatButton>(R.id.btnCancel)

        seekR.max = 255; seekG.max = 255; seekB.max = 255
        seekR.progress = currentRed
        seekG.progress = currentGreen
        seekB.progress = currentBlue

        val listener = object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seek: SeekBar?, progress: Int, fromUser: Boolean) {
                currentRed = seekR.progress
                currentGreen = seekG.progress
                currentBlue = seekB.progress
                updatePreview(preview, hexInput)
            }
            override fun onStartTrackingTouch(seek: SeekBar?) {}
            override fun onStopTrackingTouch(seek: SeekBar?) {}
        }
        seekR.setOnSeekBarChangeListener(listener)
        seekG.setOnSeekBarChangeListener(listener)
        seekB.setOnSeekBarChangeListener(listener)

        hexInput.setText(colorToHex(currentRed, currentGreen, currentBlue))
        hexInput.addTextChangedListener(object : TextWatcher {
            override fun beforeTextChanged(s: CharSequence?, start: Int, count: Int, after: Int) {}
            override fun onTextChanged(s: CharSequence?, start: Int, before: Int, count: Int) {}
            override fun afterTextChanged(s: Editable?) {
                val hex = s?.toString()?.trim() ?: return
                if (hex.matches(Regex("^#[0-9A-Fa-f]{6}$"))) {
                    try {
                        val c = Color.parseColor(hex)
                        currentRed = Color.red(c)
                        currentGreen = Color.green(c)
                        currentBlue = Color.blue(c)
                        seekR.progress = currentRed
                        seekG.progress = currentGreen
                        seekB.progress = currentBlue
                        updatePreview(preview, null)
                    } catch (_: Exception) { }
                }
            }
        })

        updatePreview(preview, hexInput)

        btnOk.setOnClickListener {
            onColorSelected(Color.rgb(currentRed, currentGreen, currentBlue))
            dismiss()
        }
        btnCancel.setOnClickListener { dismiss() }
    }

    private fun updatePreview(preview: android.view.View, hexInput: AppCompatEditText?) {
        val color = Color.rgb(currentRed, currentGreen, currentBlue)
        val drawable = GradientDrawable().apply {
            shape = GradientDrawable.RECTANGLE
            setColor(color)
            setStroke(2, Color.GRAY)
            cornerRadius = 12f
        }
        preview.background = drawable
        hexInput?.let {
            if (!it.hasFocus()) {
                it.setText(colorToHex(currentRed, currentGreen, currentBlue))
            }
        }
    }

    private fun colorToHex(r: Int, g: Int, b: Int): String {
        return String.format("#%02X%02X%02X", r, g, b)
    }
}
""",

    "app/src/main/java/com/shield/app/MainActivity.kt": """package com.shield.app

import android.content.Intent
import android.graphics.Color
import android.graphics.drawable.GradientDrawable
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
import com.google.android.material.appbar.MaterialToolbar

class MainActivity : AppCompatActivity() {

    private lateinit var settings: SettingsManager

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

    private lateinit var viewPrimaryColor: View
    private lateinit var viewOverlayColor: View
    private lateinit var btnPickPrimary: AppCompatButton
    private lateinit var btnPickOverlay: AppCompatButton

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        settings = SettingsManager(this)
        bindViews()
        setupToolbar()
        setupPermissionButton()
        setupTileButton()
        setupPatternRadio()
        setupSliders()
        setupColorButtons()
        setupEnableSwitch()

        refreshUI()
    }

    override fun onResume() {
        super.onResume()
        refreshUI()
    }

    private fun bindViews() {
        switchEnable = findViewById(R.id.switchEnable)
        statusText = findViewById(R.id.statusText)
        btnPermission = findViewById(R.id.btnPermission)
        btnAddTile = findViewById(R.id.btnAddTile)

        radioSolid = findViewById(R.id.radioSolid)
        radioGrid = findViewById(R.id.radioGrid)
        radioDots = findViewById(R.id.radioDots)
        radioFocus = findViewById(R.id.radioFocus)

        seekOpacity = findViewById(R.id.seekOpacity)
        txtOpacity = findViewById(R.id.txtOpacity)
        seekDensity = findViewById(R.id.seekDensity)
        txtDensity = findViewById(R.id.txtDensity)

        viewPrimaryColor = findViewById(R.id.viewPrimaryColor)
        viewOverlayColor = findViewById(R.id.viewOverlayColor)
        btnPickPrimary = findViewById(R.id.btnPickPrimary)
        btnPickOverlay = findViewById(R.id.btnPickOverlay)
    }

    private fun setupToolbar() {
        val toolbar = findViewById<MaterialToolbar>(R.id.toolbar)
        setSupportActionBar(toolbar)
    }

    private fun setupPermissionButton() {
        btnPermission.setOnClickListener {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:$packageName")
            )
            startActivity(intent)
        }
    }

    private fun setupTileButton() {
        btnAddTile.setOnClickListener {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                try {
                    val intent = Intent(Settings.ACTION_EDIT_TILE)
                    startActivity(intent)
                    return@setOnClickListener
                } catch (_: Exception) { }
            }
            try {
                val intent = Intent(Settings.ACTION_QUICK_SETTINGS_SETTINGS)
                startActivity(intent)
            } catch (_: Exception) { }
        }
    }

    private fun setupPatternRadio() {
        val listener = android.widget.RadioGroup.OnCheckedChangeListener { _, checkedId ->
            val pattern = when (checkedId) {
                R.id.radioSolid -> SettingsManager.PATTERN_SOLID
                R.id.radioGrid -> SettingsManager.PATTERN_GRID_LINES
                R.id.radioDots -> SettingsManager.PATTERN_DOTS
                R.id.radioFocus -> SettingsManager.PATTERN_FOCUS
                else -> SettingsManager.DEFAULT_PATTERN
            }
            settings.setPattern(pattern)
            refreshOverlay()
        }
        val group = findViewById<android.widget.RadioGroup>(R.id.radioGroupPattern)
        group.setOnCheckedChangeListener(listener)
    }

    private fun setupSliders() {
        seekOpacity.max = 100
        seekDensity.max = 100

        seekOpacity.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seek: SeekBar?, progress: Int, fromUser: Boolean) {
                txtOpacity.text = getString(R.string.opacity_value, progress)
                if (fromUser) {
                    settings.setOpacity(progress)
                    refreshOverlay()
                }
            }
            override fun onStartTrackingTouch(seek: SeekBar?) {}
            override fun onStopTrackingTouch(seek: SeekBar?) {}
        })

        seekDensity.setOnSeekBarChangeListener(object : SeekBar.OnSeekBarChangeListener {
            override fun onProgressChanged(seek: SeekBar?, progress: Int, fromUser: Boolean) {
                txtDensity.text = getString(R.string.density_value, progress)
                if (fromUser) {
                    settings.setDensity(progress)
                    refreshOverlay()
                }
            }
            override fun onStartTrackingTouch(seek: SeekBar?) {}
            override fun onStopTrackingTouch(seek: SeekBar?) {}
        })
    }

    private fun setupColorButtons() {
        btnPickPrimary.setOnClickListener {
            ColorPickerDialog(this, settings.getPrimaryColor()) { color ->
                settings.setPrimaryColor(color)
                refreshUI()
            }.show()
        }
        btnPickOverlay.setOnClickListener {
            ColorPickerDialog(this, settings.getOverlayColor()) { color ->
                settings.setOverlayColor(color)
                refreshUI()
                refreshOverlay()
            }.show()
        }
    }

    private fun setupEnableSwitch() {
        switchEnable.setOnCheckedChangeListener { _, isChecked ->
            if (isChecked && !Settings.canDrawOverlays(this)) {
                switchEnable.isChecked = false
                startActivity(
                    Intent(
                        Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                        Uri.parse("package:$packageName")
                    )
                )
                return@setOnCheckedChangeListener
            }

            settings.setEnabled(isChecked)
            if (isChecked) {
                startOverlay()
            } else {
                stopOverlay()
            }
            updateStatusText()
        }
    }

    private fun refreshUI() {
        when (settings.getPattern()) {
            SettingsManager.PATTERN_SOLID -> radioSolid.isChecked = true
            SettingsManager.PATTERN_GRID_LINES -> radioGrid.isChecked = true
            SettingsManager.PATTERN_DOTS -> radioDots.isChecked = true
            SettingsManager.PATTERN_FOCUS -> radioFocus.isChecked = true
        }

        seekOpacity.progress = settings.getOpacity()
        txtOpacity.text = getString(R.string.opacity_value, settings.getOpacity())
        seekDensity.progress = settings.getDensity()
        txtDensity.text = getString(R.string.density_value, settings.getDensity())

        applyColorPreview(viewPrimaryColor, settings.getPrimaryColor())
        applyColorPreview(viewOverlayColor, settings.getOverlayColor())

        val hasPermission = Settings.canDrawOverlays(this)
        btnPermission.isEnabled = !hasPermission
        btnPermission.text = getString(
            if (hasPermission) R.string.permission_granted else R.string.permission_grant
        )

        switchEnable.isChecked = settings.isEnabled()
        updateStatusText()
    }

    private fun updateStatusText() {
        statusText.text = getString(
            if (settings.isEnabled()) R.string.status_on else R.string.status_off
        )
        statusText.setTextColor(
            if (settings.isEnabled()) Color.parseColor("#4CAF50") else Color.parseColor("#F44336")
        )
    }

    private fun applyColorPreview(view: View, color: Int) {
        val drawable = GradientDrawable().apply {
            shape = GradientDrawable.RECTANGLE
            setColor(color)
            setStroke(2, Color.GRAY)
            cornerRadius = 16f
        }
        view.background = drawable
    }

    private fun startOverlay() {
        val intent = Intent(this, PrivacyOverlayService::class.java)
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            startForegroundService(intent)
        } else {
            startService(intent)
        }
    }

    private fun stopOverlay() {
        stopService(Intent(this, PrivacyOverlayService::class.java))
    }

    private fun refreshOverlay() {
        if (settings.isEnabled()) {
            try {
                startService(Intent(this, PrivacyOverlayService::class.java))
            } catch (_: Exception) { }
        }
    }
}
""",

    # ---------- Layouts ----------
    "app/src/main/res/layout/activity_main.xml": """<?xml version="1.0" encoding="utf-8"?>
<androidx.coordinatorlayout.widget.CoordinatorLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:fitsSystemWindows="true">

    <com.google.android.material.appbar.AppBarLayout
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:fitsSystemWindows="true">

        <com.google.android.material.appbar.MaterialToolbar
            android:id="@+id/toolbar"
            android:layout_width="match_parent"
            android:layout_height="?attr/actionBarSize"
            android:title="@string/app_name"
            app:titleCentered="true" />
    </com.google.android.material.appbar.AppBarLayout>

    <androidx.core.widget.NestedScrollView
        android:layout_width="match_parent"
        android:layout_height="match_parent"
        app:layout_behavior="@string/appbar_scrolling_view_behavior">

        <LinearLayout
            android:layout_width="match_parent"
            android:layout_height="wrap_content"
            android:orientation="vertical"
            android:padding="16dp">

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="12dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="@string/section_control"
                        android:textStyle="bold"
                        android:textSize="16sp" />

                    <LinearLayout
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="12dp"
                        android:gravity="center_vertical"
                        android:orientation="horizontal">

                        <TextView
                            android:layout_width="0dp"
                            android:layout_height="wrap_content"
                            android:layout_weight="1"
                            android:text="@string/enable_shield"
                            android:textSize="15sp" />

                        <androidx.appcompat.widget.SwitchCompat
                            android:id="@+id/switchEnable"
                            android:layout_width="wrap_content"
                            android:layout_height="wrap_content" />
                    </LinearLayout>

                    <TextView
                        android:id="@+id/statusText"
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="4dp"
                        android:textSize="13sp"
                        tools:text="@string/status_off" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="12dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="@string/section_permissions"
                        android:textStyle="bold"
                        android:textSize="16sp" />

                    <androidx.appcompat.widget.AppCompatButton
                        android:id="@+id/btnPermission"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="8dp"
                        android:text="@string/permission_grant" />

                    <androidx.appcompat.widget.AppCompatButton
                        android:id="@+id/btnAddTile"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:text="@string/add_quick_tile"
                        style="@style/Widget.Material3.Button.TonalButton" />

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="4dp"
                        android:text="@string/tile_hint"
                        android:textSize="12sp"
                        android:alpha="0.7" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="12dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="@string/section_pattern"
                        android:textStyle="bold"
                        android:textSize="16sp" />

                    <RadioGroup
                        android:id="@+id/radioGroupPattern"
                        android:layout_width="match_parent"
                        android:layout_height="wrap_content"
                        android:layout_marginTop="8dp">

                        <RadioButton android:id="@+id/radioSolid" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_solid" />
                        <RadioButton android:id="@+id/radioGrid" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_grid" />
                        <RadioButton android:id="@+id/radioDots" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_dots" />
                        <RadioButton android:id="@+id/radioFocus" android:layout_width="match_parent" android:layout_height="wrap_content" android:text="@string/pattern_focus" />
                    </RadioGroup>
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="12dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="@string/section_adjustments"
                        android:textStyle="bold"
                        android:textSize="16sp" />

                    <TextView android:id="@+id/txtOpacity" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:textSize="14sp" tools:text="Opacity: 30%" />
                    <SeekBar android:id="@+id/seekOpacity" android:layout_width="match_parent" android:layout_height="wrap_content" />

                    <TextView android:id="@+id/txtDensity" android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:textSize="14sp" tools:text="Density: 40" />
                    <SeekBar android:id="@+id/seekDensity" android:layout_width="match_parent" android:layout_height="wrap_content" />
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <com.google.android.material.card.MaterialCardView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginBottom="12dp"
                app:cardCornerRadius="16dp"
                app:cardElevation="2dp">

                <LinearLayout
                    android:layout_width="match_parent"
                    android:layout_height="wrap_content"
                    android:orientation="vertical"
                    android:padding="16dp">

                    <TextView
                        android:layout_width="wrap_content"
                        android:layout_height="wrap_content"
                        android:text="@string/section_colors"
                        android:textStyle="bold"
                        android:textSize="16sp" />

                    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="12dp" android:gravity="center_vertical" android:orientation="horizontal">
                        <View android:id="@+id/viewPrimaryColor" android:layout_width="40dp" android:layout_height="40dp" />
                        <TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="12dp" android:layout_weight="1" android:text="@string/primary_color" android:textSize="14sp" />
                        <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnPickPrimary" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/pick" style="@style/Widget.Material3.Button.TextButton" />
                    </LinearLayout>

                    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:gravity="center_vertical" android:orientation="horizontal">
                        <View android:id="@+id/viewOverlayColor" android:layout_width="40dp" android:layout_height="40dp" />
                        <TextView android:layout_width="0dp" android:layout_height="wrap_content" android:layout_marginStart="12dp" android:layout_weight="1" android:text="@string/overlay_color" android:textSize="14sp" />
                        <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnPickOverlay" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/pick" style="@style/Widget.Material3.Button.TextButton" />
                    </LinearLayout>
                </LinearLayout>
            </com.google.android.material.card.MaterialCardView>

            <TextView
                android:layout_width="match_parent"
                android:layout_height="wrap_content"
                android:layout_marginTop="8dp"
                android:layout_marginBottom="24dp"
                android:gravity="center"
                android:text="@string/footer"
                android:textSize="12sp"
                android:alpha="0.6" />

        </LinearLayout>
    </androidx.core.widget.NestedScrollView>

</androidx.coordinatorlayout.widget.CoordinatorLayout>
""",

    "app/src/main/res/layout/dialog_color_picker.xml": """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    android:orientation="vertical"
    android:padding="20dp">

    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/pick_color" android:textSize="18sp" android:textStyle="bold" />

    <View android:id="@+id/colorPreview" android:layout_width="match_parent" android:layout_height="80dp" android:layout_marginTop="16dp" />

    <androidx.appcompat.widget.AppCompatEditText
        android:id="@+id/hexInput"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="12dp"
        android:hint="@string/hex_hint"
        android:inputType="text"
        android:maxLength="7"
        android:singleLine="true" />

    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="16dp" android:text="@string/red" />
    <SeekBar android:id="@+id/seekRed" android:layout_width="match_parent" android:layout_height="wrap_content" android:max="255" />

    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="@string/green" />
    <SeekBar android:id="@+id/seekGreen" android:layout_width="match_parent" android:layout_height="wrap_content" android:max="255" />

    <TextView android:layout_width="wrap_content" android:layout_height="wrap_content" android:layout_marginTop="8dp" android:text="@string/blue" />
    <SeekBar android:id="@+id/seekBlue" android:layout_width="match_parent" android:layout_height="wrap_content" android:max="255" />

    <LinearLayout android:layout_width="match_parent" android:layout_height="wrap_content" android:layout_marginTop="16dp" android:gravity="end" android:orientation="horizontal">
        <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnCancel" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/cancel" style="@style/Widget.Material3.Button.TextButton" />
        <androidx.appcompat.widget.AppCompatButton android:id="@+id/btnOk" android:layout_width="wrap_content" android:layout_height="wrap_content" android:text="@string/ok" />
    </LinearLayout>
</LinearLayout>
""",

    # ---------- Resources ----------
    "app/src/main/res/values/strings.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Shield</string>
    <string name="tile_label">Privacy Shield</string>
    <string name="tile_active">Shield ON</string>
    <string name="tile_inactive">Shield OFF</string>
    <string name="notification_channel_name">Shield Service</string>
    <string name="notification_channel_desc">Keeps the privacy overlay active</string>
    <string name="notification_active">Privacy shield is active</string>
    <string name="section_control">Control</string>
    <string name="enable_shield">Enable Privacy Shield</string>
    <string name="status_on">Shield is active</string>
    <string name="status_off">Shield is inactive</string>
    <string name="section_permissions">Permissions</string>
    <string name="permission_grant">Grant Display Over Apps</string>
    <string name="permission_granted">Permission granted ✓</string>
    <string name="add_quick_tile">Open Quick Settings</string>
    <string name="tile_hint">Add "Privacy Shield" tile from the edit menu of your Quick Settings panel.</string>
    <string name="section_pattern">Pattern</string>
    <string name="pattern_solid">Solid veil (full tint)</string>
    <string name="pattern_grid">Linear grid</string>
    <string name="pattern_dots">Dot grid</string>
    <string name="pattern_focus">Focus area (clear center)</string>
    <string name="section_adjustments">Adjustments</string>
    <string name="opacity_value">Opacity: %1$d%%</string>
    <string name="density_value">Density: %1$d</string>
    <string name="section_colors">Colors</string>
    <string name="primary_color">Primary color</string>
    <string name="overlay_color">Overlay color</string>
    <string name="pick">Pick</string>
    <string name="pick_color">Pick a color</string>
    <string name="hex_hint">#RRGGBB</string>
    <string name="red">Red</string>
    <string name="green">Green</string>
    <string name="blue">Blue</string>
    <string name="ok">OK</string>
    <string name="cancel">Cancel</string>
    <string name="footer">Shield v1.0.0 — No Google Play Services required</string>
</resources>
""",

    "app/src/main/res/values-ar/strings.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Shield</string>
    <string name="tile_label">درع الخصوصية</string>
    <string name="tile_active">الدرع مُفعّل</string>
    <string name="tile_inactive">الدرع مُعطّل</string>
    <string name="notification_channel_name">خدمة Shield</string>
    <string name="notification_channel_desc">تبقي طبقة الخصوصية نشطة</string>
    <string name="notification_active">درع الخصوصية نشط</string>
    <string name="section_control">التحكم</string>
    <string name="enable_shield">تفعيل درع الخصوصية</string>
    <string name="status_on">الدرع مُفعّل</string>
    <string name="status_off">الدرع مُعطّل</string>
    <string name="section_permissions">الصلاحيات</string>
    <string name="permission_grant">منح صلاحية الظهور فوق التطبيقات</string>
    <string name="permission_granted">تم منح الصلاحية ✓</string>
    <string name="add_quick_tile">فتح الإعدادات السريعة</string>
    <string name="tile_hint">أضف بلاطة "درع الخصوصية" من قائمة التعديل في شريط الإعدادات السريعة.</string>
    <string name="section_pattern">النمط</string>
    <string name="pattern_solid">ستارة كاملة (تعتيم موحد)</string>
    <string name="pattern_grid">شبكة خطية</string>
    <string name="pattern_dots">شبكة نقطية</string>
    <string name="pattern_focus">منطقة تركيز (وسط واضح)</string>
    <string name="section_adjustments">الضبط</string>
    <string name="opacity_value">الشفافية: %1$d%%</string>
    <string name="density_value">الكثافة: %1$d</string>
    <string name="section_colors">الألوان</string>
    <string name="primary_color">اللون الأساسي</string>
    <string name="overlay_color">لون الطبقة</string>
    <string name="pick">اختيار</string>
    <string name="pick_color">اختر لوناً</string>
    <string name="hex_hint">#RRGGBB</string>
    <string name="red">أحمر</string>
    <string name="green">أخضر</string>
    <string name="blue">أزرق</string>
    <string name="ok">موافق</string>
    <string name="cancel">إلغاء</string>
    <string name="footer">Shield v1.0.0 — لا يحتاج إلى خدمات Google Play</string>
</resources>
""",

    "app/src/main/res/values/colors.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="shield_primary">#1A73E8</color>
    <color name="shield_primary_dark">#0D47A1</color>
    <color name="shield_on_primary">#FFFFFF</color>
    <color name="shield_surface">#FFFFFF</color>
    <color name="shield_surface_dark">#1C1B1F</color>
    <color name="shield_on_surface">#1C1B1F</color>
    <color name="shield_on_surface_dark">#E6E1E5</color>
</resources>
""",

    "app/src/main/res/values/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.Shield" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">@color/shield_primary</item>
        <item name="colorPrimaryDark">@color/shield_primary_dark</item>
        <item name="colorOnPrimary">@color/shield_on_primary</item>
        <item name="android:colorBackground">@color/shield_surface</item>
        <item name="colorOnBackground">@color/shield_on_surface</item>
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryDark</item>
        <item name="android:windowLightStatusBar" tools:targetApi="m">false</item>
    </style>
</resources>
""",

    "app/src/main/res/values-night/themes.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources xmlns:tools="http://schemas.android.com/tools">
    <style name="Theme.Shield" parent="Theme.Material3.DayNight.NoActionBar">
        <item name="colorPrimary">@color/shield_primary</item>
        <item name="colorPrimaryDark">@color/shield_primary_dark</item>
        <item name="colorOnPrimary">@color/shield_on_primary</item>
        <item name="android:colorBackground">@color/shield_surface_dark</item>
        <item name="colorOnBackground">@color/shield_on_surface_dark</item>
        <item name="android:statusBarColor" tools:targetApi="l">?attr/colorPrimaryDark</item>
        <item name="android:windowLightStatusBar" tools:targetApi="m">false</item>
    </style>
</resources>
""",

    "app/src/main/res/values/arrays.xml": """<?xml version="1.0" encoding="utf-8"?>
<resources>
</resources>
""",

    "app/src/main/res/drawable/ic_shield.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24"
    android:tint="?attr/colorControlNormal">
    <path
        android:fillColor="@android:color/white"
        android:pathData="M12,1L3,5v6c0,5.55 3.84,10.74 9,12 5.16,-1.26 9,-6.45 9,-12V5l-9,-4zM12,11.99h7c-0.53,4.12 -3.28,7.79 -7,8.94V12H5V6.3l7,-3.11v8.8z"/>
</vector>
""",

    "app/src/main/res/drawable/ic_shield_tile.xml": """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="24dp"
    android:height="24dp"
    android:viewportWidth="24"
    android:viewportHeight="24">
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M12,1L3,5v6c0,5.55 3.84,10.74 9,12 5.16,-1.26 9,-6.45 9,-12V5l-9,-4zM12,11.99h7c-0.53,4.12 -3.28,7.79 -7,8.94V12H5V6.3l7,-3.11v8.8z"/>
</vector>
""",

    "app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/shield_primary"/>
    <foreground android:drawable="@drawable/ic_shield"/>
</adaptive-icon>
""",

    "app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml": """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/shield_primary"/>
    <foreground android:drawable="@drawable/ic_shield"/>
</adaptive-icon>
""",

    # ---------- .gitignore ----------
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
"""
}


# ==================== دوال الإنشاء ====================

def create_files():
    """ينشئ كل الملفات في جذر المستودع"""
    print("=" * 60)
    print("🛡️  Shield Project Generator")
    print("=" * 60)

    count = 0
    for rel_path, content in FILES.items():
        full_path = rel_path
        os.makedirs(os.path.dirname(full_path) if os.path.dirname(full_path) else ".", exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content.lstrip("\n"))

        count += 1
        print(f"  ✅ [{count:02d}] {rel_path}")

    print(f"\n✅ تم إنشاء {count} ملف بنجاح!")
    return count


def main():
    count = create_files()
    print("\n" + "=" * 60)
    print(f"🎉 جاهز! تم إنشاء {count} ملف")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
