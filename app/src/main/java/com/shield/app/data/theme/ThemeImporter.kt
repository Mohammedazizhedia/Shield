// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.data.theme

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
