// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.data.theme

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
