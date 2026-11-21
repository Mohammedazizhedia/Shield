// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.service

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
