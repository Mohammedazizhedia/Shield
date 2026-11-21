// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.ui

import android.os.Bundle
import android.widget.RadioButton
import android.widget.RadioGroup
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import androidx.appcompat.widget.AppCompatButton
import androidx.lifecycle.lifecycleScope
import com.shield.app.R
import com.shield.app.data.theme.BuiltInThemes
import com.shield.app.data.theme.ThemeConfig
import com.shield.app.data.theme.ThemeImporter
import com.shield.app.data.theme.ThemeMode
import com.shield.app.data.theme.ThemeRepository
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
        themeRepo = (application as com.shield.app.ShieldApp).themeRepo
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
                val current = getCurrentConfig()
                themeRepo.saveConfig(current.copy(mode = mode))
            }
        }

        btnReset.setOnClickListener { lifecycleScope.launch { themeRepo.saveConfig(BuiltInThemes.DEFAULT) } }

        btnExport.setOnClickListener {
            lifecycleScope.launch {
                val config = getCurrentConfig()
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

    private suspend fun getCurrentConfig(): ThemeConfig {
        var result = BuiltInThemes.DEFAULT
        themeRepo.configFlow.collect { result = it }
        return result
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
