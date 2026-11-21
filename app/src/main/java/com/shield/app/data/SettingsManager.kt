// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.data

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
