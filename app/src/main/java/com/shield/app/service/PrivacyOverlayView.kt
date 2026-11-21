// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.service

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
