// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.data.theme

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
