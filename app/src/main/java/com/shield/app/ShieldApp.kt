// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.shield.app.core.CrashReporter
import com.shield.app.data.theme.ThemeRepository

class ShieldApp : Application() {
    lateinit var themeRepo: ThemeRepository
        private set

    override fun onCreate() {
        super.onCreate()
        instance = this
        CrashReporter.install(this)
        themeRepo = ThemeRepository(this)
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val manager = getSystemService(NotificationManager::class.java)
            manager.createNotificationChannel(
                NotificationChannel(
                    "shield_overlay",
                    getString(R.string.notif_channel_overlay),
                    NotificationManager.IMPORTANCE_LOW
                ).apply { description = getString(R.string.notif_channel_overlay_desc); setShowBadge(false) }
            )
            manager.createNotificationChannel(
                NotificationChannel(
                    "shield_crash",
                    getString(R.string.notif_channel_crash),
                    NotificationManager.IMPORTANCE_DEFAULT
                )
            )
        }
    }

    companion object {
        lateinit var instance: ShieldApp
            private set
    }
}
