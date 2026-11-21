// Built with BFB.AI — Built For Benefits, by AI
package com.shield.app.ui

import android.os.Bundle
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.shield.app.R

class AboutActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_about)
        setSupportActionBar(findViewById(R.id.toolbar))
        supportActionBar?.setDisplayHomeAsUpEnabled(true)
        supportActionBar?.title = getString(R.string.about)

        findViewById<TextView>(R.id.txtVersion).text = getString(R.string.version_fmt, "1.0.0", "001")
        findViewById<TextView>(R.id.txtBfbSignature).text = getString(R.string.built_with_bfb)
        findViewById<TextView>(R.id.txtBfbMeaning).text = getString(R.string.bfb_meaning)
    }
    override fun onSupportNavigateUp(): Boolean { finish(); return true }
}
