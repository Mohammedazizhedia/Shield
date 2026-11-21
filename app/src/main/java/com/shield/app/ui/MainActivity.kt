// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.ui

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
