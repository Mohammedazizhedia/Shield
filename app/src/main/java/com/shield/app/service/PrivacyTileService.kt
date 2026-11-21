// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.service

import android.content.Intent
import android.graphics.drawable.Icon
import android.os.Build
import android.service.quicksettings.Tile
import android.service.quicksettings.TileService
import androidx.annotation.RequiresApi
import com.shield.app.R
import com.shield.app.data.SettingsManager
import com.shield.app.ui.MainActivity

@RequiresApi(Build.VERSION_CODES.N)
class PrivacyTileService : TileService() {
    private lateinit var settings: SettingsManager
    override fun onCreate() { super.onCreate(); settings = SettingsManager(this) }
    override fun onStartListening() { super.onStartListening(); updateTile() }
    override fun onClick() {
        super.onClick()
        val newState = !settings.isEnabled()
        settings.setEnabled(newState)
        if (newState) {
            if (!android.provider.Settings.canDrawOverlays(this)) {
                settings.setEnabled(false)
                startActivityAndCollapse(Intent(this, MainActivity::class.java).addFlags(Intent.FLAG_ACTIVITY_NEW_TASK))
                return
            }
            val i = Intent(this, PrivacyOverlayService::class.java)
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) startForegroundService(i) else startService(i)
        } else {
            stopService(Intent(this, PrivacyOverlayService::class.java))
        }
        updateTile()
    }
    private fun updateTile() {
        val tile = qsTile ?: return
        val on = settings.isEnabled()
        tile.state = if (on) Tile.STATE_ACTIVE else Tile.STATE_INACTIVE
        tile.label = getString(if (on) R.string.tile_on else R.string.tile_off)
        tile.icon = Icon.createWithResource(this, R.drawable.ic_shield_tile)
        tile.updateTile()
    }
}
