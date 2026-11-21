// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.data.theme

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
